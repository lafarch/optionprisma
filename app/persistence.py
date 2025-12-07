"""
JSON-based persistence layer.

This demonstrates:
1. Async file I/O with aiofiles (non-blocking reads/writes)
2. Simple CRUD operations
3. Error handling for file operations

In production, you'd use:
- PostgreSQL with SQLAlchemy (async mode)
- Redis for caching
- MongoDB for document storage
"""

import json
import aiofiles
from typing import List, Optional

from app.models import SimulationResult
from app.config import RESULTS_FILE


async def _read_results_file() -> List[dict]:
    """Read the results JSON file."""
    if not RESULTS_FILE.exists():
        # Initialize empty file
        async with aiofiles.open(RESULTS_FILE, "w") as f:
            await f.write("[]")
        return []

    async with aiofiles.open(RESULTS_FILE, "r") as f:
        content = await f.read()
        return json.loads(content)


async def _write_results_file(results: List[dict]) -> None:
    """Write results to JSON file."""
    async with aiofiles.open(RESULTS_FILE, "w") as f:
        await f.write(json.dumps(results, indent=2, default=str))


async def save_simulation_result(result: SimulationResult) -> None:
    """
    Save a simulation result to JSON.

    Args:
        result: The simulation result to save

    Note: In production, consider:
    - Using a database transaction
    - Implementing retry logic
    - Adding file locking for concurrent writes
    """
    results = await _read_results_file()

    # Convert Pydantic model to dict
    result_dict = result.model_dump(mode="json")

    # Append new result
    results.append(result_dict)

    # Write back to file
    await _write_results_file(results)


async def get_simulation_result(simulation_id: str) -> Optional[SimulationResult]:
    """
    Retrieve a simulation by ID.

    Returns:
        SimulationResult if found, None otherwise
    """
    results = await _read_results_file()

    for result_dict in results:
        if result_dict["simulation_id"] == simulation_id:
            # Convert dict back to Pydantic model
            return SimulationResult(**result_dict)

    return None


async def get_all_simulation_results() -> List[SimulationResult]:
    """
    Retrieve all simulation results.

    In production, add pagination to avoid loading huge datasets.
    """
    results = await _read_results_file()
    return [SimulationResult(**r) for r in results]


async def delete_simulation_result(simulation_id: str) -> bool:
    """
    Delete a simulation result.

    Returns:
        True if deleted, False if not found
    """
    results = await _read_results_file()

    # Filter out the result to delete
    new_results = [r for r in results if r["simulation_id"] != simulation_id]

    # If nothing was removed, the ID wasn't found
    if len(new_results) == len(results):
        return False

    await _write_results_file(new_results)
    return True