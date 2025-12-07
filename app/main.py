"""
OptionPrisma FastAPI application.

This demonstrates:
1. Async request handling for I/O operations
2. Proper error handling with HTTP status codes
3. Dependency injection patterns
4. CRUD operations on JSON storage
"""

import asyncio
import secrets
import time
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.models import (
    OptionPricingRequest,
    OptionPricingResponse,
    SimulationResult,
    HealthCheckResponse,
)
from app.monte_carlo import price_european_option, validate_pricing_inputs
from app.black_scholes import black_scholes_price, calculate_greeks
from app.persistence import (
    save_simulation_result,
    get_simulation_result,
    get_all_simulation_results,
    delete_simulation_result,
)
from app.config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    RISK_FREE_RATE_FETCH_DELAY,
)

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
)


# =======================
# ASYNC HELPER FUNCTIONS
# =======================


async def fetch_risk_free_rate_async() -> float:
    """
    Simulate fetching the risk-free rate from an external API.

    In a real application, this might call:
    - Federal Reserve Economic Data (FRED) API
    - Treasury yield curve endpoint
    - Bloomberg/Reuters data feed

    This demonstrates async I/O without blocking the event loop.
    """
    # Simulate network delay
    await asyncio.sleep(RISK_FREE_RATE_FETCH_DELAY)

    # In reality, you'd parse the API response here
    # For demo, we'll just return a placeholder
    return 0.0  # We'll use the user-provided rate


async def validate_inputs_async(request: OptionPricingRequest) -> None:
    """
    Async wrapper for input validation.

    Why async? In production, you might:
    - Check if the stock ticker exists in a database
    - Verify user's API quota from Redis
    - Log validation attempts to an external service

    All of these are I/O operations that benefit from async.
    """
    # Simulate async validation (e.g., database lookup)
    await asyncio.sleep(0.01)

    # Perform synchronous validation
    is_valid, error_msg = validate_pricing_inputs(
        spot_price=request.spot_price,
        strike_price=request.strike_price,
        time_to_maturity=request.time_to_maturity,
        volatility=request.volatility,
        risk_free_rate=request.risk_free_rate,
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_msg,
        )


# ==============
# API ENDPOINTS
# ==============


@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint.

    Why async? Even though this is simple, keeping all endpoints async
    maintains consistency and allows adding I/O operations later.
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=APP_VERSION,
    )


@app.post(
    "/simulations",
    response_model=OptionPricingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_simulation(request: OptionPricingRequest):
    """
    Run a Monte Carlo simulation and store the result.

    This endpoint demonstrates:
    1. Async validation (simulates DB/API checks)
    2. Mixing async and sync code (CPU-bound pricing is sync)
    3. Async file I/O for persistence
    4. Proper error handling with appropriate HTTP codes
    """
    try:
        # Step 1: Validate inputs (async - might involve DB/API calls)
        await validate_inputs_async(request)

        # Step 2: Simulate fetching market data (async I/O)
        # In production, this might fetch current spot prices, volatility surface, etc.
        await fetch_risk_free_rate_async()

        # Step 3: Run the pricing calculation (CPU-bound, so NOT async)
        # We run this in the default thread pool to avoid blocking
        # For truly CPU-intensive work, consider running in a process pool
        pricing_result = price_european_option(
            spot_price=request.spot_price,
            strike_price=request.strike_price,
            time_to_maturity=request.time_to_maturity,
            volatility=request.volatility,
            risk_free_rate=request.risk_free_rate,
            option_type=request.option_type,
            num_simulations=request.num_simulations,
        )

        # Step 4: Calculate Black-Scholes price and Greeks for comparison
        bs_price = black_scholes_price(
            spot_price=request.spot_price,
            strike_price=request.strike_price,
            time_to_maturity=request.time_to_maturity,
            volatility=request.volatility,
            risk_free_rate=request.risk_free_rate,
            option_type=request.option_type,
        )

        greeks = calculate_greeks(
            spot_price=request.spot_price,
            strike_price=request.strike_price,
            time_to_maturity=request.time_to_maturity,
            volatility=request.volatility,
            risk_free_rate=request.risk_free_rate,
            option_type=request.option_type,
        )

        # Step 5: Generate unique ID and timestamp
        simulation_id = f"sim_{int(time.time())}_{secrets.token_hex(4)}"
        timestamp = datetime.utcnow()

        # Step 6: Save to JSON (async file I/O)
        result = SimulationResult(
            simulation_id=simulation_id,
            option_price=pricing_result["price"],
            std_error=pricing_result["std_error"],
            confidence_interval_95=pricing_result["confidence_interval_95"],
            black_scholes_price=bs_price,
            greeks=greeks,
            inputs=request.model_dump(),
            timestamp=timestamp,
        )

        await save_simulation_result(result)

        # Step 7: Return response
        return OptionPricingResponse(
            simulation_id=simulation_id,
            option_price=pricing_result["price"],
            std_error=pricing_result["std_error"],
            confidence_interval_95=pricing_result["confidence_interval_95"],
            black_scholes_price=bs_price,
            greeks=greeks,
            inputs=request,
            timestamp=timestamp,
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        # Catch unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(e)}",
        )


@app.get("/simulations/{simulation_id}", response_model=SimulationResult)
async def get_simulation(simulation_id: str):
    """
    Retrieve a specific simulation result by ID.

    Why async? File I/O operations (reading JSON) are I/O-bound.
    """
    result = await get_simulation_result(simulation_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation {simulation_id} not found",
        )

    return result


@app.get("/simulations", response_model=List[SimulationResult])
async def list_simulations():
    """
    List all stored simulation results.

    In production, you'd add pagination:
    - Query params: ?skip=0&limit=10
    - Return metadata: total_count, next_page, etc.
    """
    results = await get_all_simulation_results()
    return results


@app.delete("/simulations/{simulation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_simulation(simulation_id: str):
    """
    Delete a simulation result.

    Returns 204 No Content on success.
    """
    success = await delete_simulation_result(simulation_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Simulation {simulation_id} not found",
        )

    # 204 responses should not have a body
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)