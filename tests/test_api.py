"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.config as config


@pytest.fixture
def client(tmp_path):
    """Create a test client with temporary storage."""
    # Use temporary file for tests
    temp_file = tmp_path / "test_results.json"
    original_file = config.RESULTS_FILE
    config.RESULTS_FILE = temp_file

    with TestClient(app) as c:
        yield c

    # Restore
    config.RESULTS_FILE = original_file


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


def test_create_simulation(client):
    """Test creating a new simulation."""
    payload = {
        "spot_price": 100,
        "strike_price": 105,
        "time_to_maturity": 1.0,
        "volatility": 0.2,
        "risk_free_rate": 0.05,
        "option_type": "call",
        "num_simulations": 10000,  # Small for speed
    }

    response = client.post("/simulations", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert "simulation_id" in data
    assert data["option_price"] > 0
    assert data["std_error"] > 0
    assert "black_scholes_price" in data
    assert "greeks" in data


def test_create_simulation_with_invalid_volatility(client):
    """Test that negative volatility is rejected."""
    payload = {
        "spot_price": 100,
        "strike_price": 105,
        "time_to_maturity": 1.0,
        "volatility": -0.2,  # Invalid!
        "risk_free_rate": 0.05,
        "option_type": "call",
    }

    response = client.post("/simulations", json=payload)
    assert response.status_code == 422  # Unprocessable Entity


def test_retrieve_simulation(client):
    """Test retrieving a simulation by ID."""
    # Create a simulation
    payload = {
        "spot_price": 100,
        "strike_price": 105,
        "time_to_maturity": 1.0,
        "volatility": 0.2,
        "risk_free_rate": 0.05,
        "option_type": "call",
        "num_simulations": 10000,
    }

    create_response = client.post("/simulations", json=payload)
    simulation_id = create_response.json()["simulation_id"]

    # Retrieve it
    get_response = client.get(f"/simulations/{simulation_id}")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["simulation_id"] == simulation_id


def test_retrieve_nonexistent_simulation(client):
    """Test retrieving a simulation that doesn't exist."""
    response = client.get("/simulations/nonexistent_id")
    assert response.status_code == 404


def test_list_simulations(client):
    """Test listing all simulations."""
    # Create two simulations
    payload = {
        "spot_price": 100,
        "strike_price": 105,
        "time_to_maturity": 1.0,
        "volatility": 0.2,
        "risk_free_rate": 0.05,
        "option_type": "call",
        "num_simulations": 10000,
    }

    client.post("/simulations", json=payload)
    client.post("/simulations", json=payload)

    # List all
    response = client.get("/simulations")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 2  # At least our two


def test_delete_simulation(client):
    """Test deleting a simulation."""
    # Create
    payload = {
        "spot_price": 100,
        "strike_price": 105,
        "time_to_maturity": 1.0,
        "volatility": 0.2,
        "risk_free_rate": 0.05,
        "option_type": "call",
        "num_simulations": 10000,
    }

    create_response = client.post("/simulations", json=payload)
    simulation_id = create_response.json()["simulation_id"]

    # Delete
    delete_response = client.delete(f"/simulations/{simulation_id}")
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/simulations/{simulation_id}")
    assert get_response.status_code == 404