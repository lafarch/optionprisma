"""Tests for JSON persistence layer."""

import pytest
from datetime import datetime
from pathlib import Path

from app.models import SimulationResult
from app.persistence import (
    save_simulation_result,
    get_simulation_result,
    get_all_simulation_results,
    delete_simulation_result,
)
import app.config as config


@pytest.fixture
def temp_results_file(tmp_path):
    """Create a temporary results file for testing."""
    temp_file = tmp_path / "test_results.json"
    original_file = config.RESULTS_FILE

    # Override the config
    config.RESULTS_FILE = temp_file

    yield temp_file

    # Restore original
    config.RESULTS_FILE = original_file


@pytest.mark.asyncio
async def test_save_and_retrieve_result(temp_results_file):
    """Test saving and retrieving a simulation result."""
    result = SimulationResult(
        simulation_id="test_123",
        option_price=10.5,
        std_error=0.05,
        confidence_interval_95=0.1,
        inputs={"spot_price": 100, "strike_price": 105},
        timestamp=datetime.utcnow(),
    )

    # Save
    await save_simulation_result(result)

    # Retrieve
    retrieved = await get_simulation_result("test_123")

    assert retrieved is not None
    assert retrieved.simulation_id == "test_123"
    assert retrieved.option_price == 10.5


@pytest.mark.asyncio
async def test_get_nonexistent_result(temp_results_file):
    """Test retrieving a result that doesn't exist."""
    result = await get_simulation_result("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_delete_result(temp_results_file):
    """Test deleting a simulation result."""
    result = SimulationResult(
        simulation_id="test_delete",
        option_price=10.5,
        std_error=0.05,
        confidence_interval_95=0.1,
        inputs={},
        timestamp=datetime.utcnow(),
    )

    await save_simulation_result(result)

    # Delete
    success = await delete_simulation_result("test_delete")
    assert success

    # Verify it's gone
    retrieved = await get_simulation_result("test_delete")
    assert retrieved is None


@pytest.mark.asyncio
async def test_get_all_results(temp_results_file):
    """Test retrieving all results."""
    # Save multiple results
    for i in range(3):
        result = SimulationResult(
            simulation_id=f"test_{i}",
            option_price=10.0 + i,
            std_error=0.05,
            confidence_interval_95=0.1,
            inputs={},
            timestamp=datetime.utcnow(),
        )
        await save_simulation_result(result)

    # Retrieve all
    all_results = await get_all_simulation_results()
    assert len(all_results) == 3