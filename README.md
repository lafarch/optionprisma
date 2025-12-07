# OptionPrisma 📊

A high-performance asynchronous API for European option pricing using Monte Carlo simulation.

##  Features

- ⚡ **Async FastAPI** for concurrent request handling
- 📈 **Monte Carlo Simulation** for European option pricing
- 🎲 **Black-Scholes Model** for analytical comparison
- 📊 **Greeks Calculation** (Delta, Gamma, Vega, Theta, Rho)
- ✅ **Full CRUD Operations** with JSON persistence
- 🧪 **Comprehensive Testing** (unit, integration, property-based)
# OptionPrisma 

A high-performance asynchronous API for European option pricing using Monte Carlo simulation.

##  Features

-  **Async FastAPI** for concurrent request handling
-  **Monte Carlo** for European option pricing
- **Black-Scholes Model** for analytical comparison
- **Greeks Calculation** (Delta, Gamma, Vega, Theta, Rho)
- **Full CRUD Operations** with JSON persistence
- **Comprehensive Testing** (unit, integration, property-based)
- **Docker Ready** for easy deployment

# Quick Start

## Prerequisites

- Python 3.11+
- WSL2 (Ubuntu) or Linux/macOS
- Git

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/optionprisma.git
cd optionprisma

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the API

**Development mode (recommended):**

```bash
fastapi dev app/main.py
```

**Alternative (explicit control):**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

> **Note**: `fastapi dev` is a development-only command. For production, always use `uvicorn` directly.

Visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Usage Examples

### Python

```python
import requests

# Create a simulation
response = requests.post(
    "http://localhost:8000/simulations",
    json={
        "spot_price": 100,
        "strike_price": 105,
        "time_to_maturity": 1.0,
        "volatility": 0.25,
        "risk_free_rate": 0.05,
        "option_type": "call",
        "num_simulations": 100000
    }
)

result = response.json()
print(f"Option Price: ${result['option_price']:.2f}")
print(f"Black-Scholes: {result['black_scholes_price']:.2f}")
print(f"Delta: {result['greeks']['delta']:.4f}")
```

### cURL

```bash
curl -X POST http://localhost:8000/simulations \
  -H "Content-Type: application/json" \
  -d '{
    "spot_price": 100,
    "strike_price": 105,
    "time_to_maturity": 1.0,
    "volatility": 0.25,
    "risk_free_rate": 0.05,
    "option_type": "call"
  }'
```

# More

This project is licensed under the MIT License.

## Authors

- Black-Scholes-Merton model for option pricing
- FastAPI documentation and community
- Quantitative finance resources

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_monte_carlo.py -v

# Run tests matching a pattern
pytest -k "test_call" -v
```

## 🐳 Docker

```bash
# Build image
docker build -t optionprisma:latest .

# Run container
docker run -d -p 8000:8000 --name optionprisma optionprisma:latest

# View logs
docker logs optionprisma

# Stop and remove
docker stop optionprisma
docker rm optionprisma
```

## 📁 Project Structure

```
optionprisma/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & routes
│   ├── models.py            # Pydantic schemas
│   ├── monte_carlo.py       # Monte Carlo simulation engine
│   ├── black_scholes.py     # Black-Scholes analytical pricing
│   ├── persistence.py       # JSON CRUD operations
│   └── config.py            # Configuration
├── tests/
│   ├── __init__.py
│   ├── test_monte_carlo.py  # Unit tests for pricing logic
│   ├── test_api.py          # Integration tests for endpoints
│   └── test_persistence.py  # Tests for JSON operations
├── data/
│   └── results.json         # Simulation results storage
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔧 Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Validation**: Pydantic
- **Computation**: NumPy, SciPy
- **Testing**: Pytest, Hypothesis
- **Containerization**: Docker

## 🎓 Key Concepts Demonstrated

### Async Programming
- Non-blocking I/O operations
- Concurrent request handling
- Async file operations with `aiofiles`

### Quantitative Finance
- Monte Carlo simulation using Geometric Brownian Motion
- Black-Scholes closed-form solution
- Options Greeks (sensitivity analysis)

### Software Engineering
- Clean architecture (separation of concerns)
- Type hints and validation with Pydantic
- Comprehensive testing (unit, integration)
- Error handling and HTTP status codes
- Docker containerization

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/simulations` | Create new simulation |
| GET | `/simulations` | List all simulations |
| GET | `/simulations/{id}` | Get specific simulation |
| DELETE | `/simulations/{id}` | Delete simulation |

## 🎯 Development vs Production

### Development
Use `fastapi dev` for the best development experience:
- Auto-reload on code changes
- Better error messages
- Automatic configuration

### Production
Use `uvicorn` directly for production deployments:
- Multiple workers for concurrency
- Full configuration control
- Better performance tuning

```bash
# Production with 4 workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Your Name - [Your Portfolio/LinkedIn]

## 🙏 Acknowledgments

- Black-Scholes-Merton model for option pricing
- FastAPI documentation and community
- Quantitative finance resources