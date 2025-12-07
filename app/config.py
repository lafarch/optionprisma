"""Application configuration."""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_FILE = DATA_DIR / "results.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Application settings
APP_NAME = "OptionPrisma"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = """
**OptionPrisma** - A quantitative finance API for European option pricing.

## Features
* Monte Carlo simulation engine
* Async operation for high throughput
* JSON-based result persistence
* Full CRUD operations

Built with FastAPI, Pydantic, and NumPy.
"""

# Simulation defaults
DEFAULT_SIMULATIONS = 100_000
MAX_SIMULATIONS = 1_000_000

# Simulated async delay for "fetching risk-free rate"
RISK_FREE_RATE_FETCH_DELAY = 0.5  # seconds