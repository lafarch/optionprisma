"""
Pydantic models for request/response validation.

This demonstrates:
1. Strong typing prevents runtime errors
2. Custom validators for domain-specific constraints
3. Automatic OpenAPI documentation generation
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime


class OptionPricingRequest(BaseModel):
    """Request schema for option pricing endpoint."""

    spot_price: float = Field(
        ..., gt=0, description="Current stock price", examples=[100.0]
    )
    strike_price: float = Field(
        ..., gt=0, description="Option strike price", examples=[105.0]
    )
    time_to_maturity: float = Field(
        ...,
        gt=0,
        le=10,
        description="Time to expiration in years",
        examples=[1.0],
    )
    volatility: float = Field(
        ...,
        ge=0,
        le=5,
        description="Annual volatility (e.g., 0.2 = 20%)",
        examples=[0.25],
    )
    risk_free_rate: float = Field(
        ...,
        ge=-0.1,
        le=0.3,
        description="Risk-free interest rate",
        examples=[0.05],
    )
    option_type: Literal["call", "put"] = Field(
        ..., description="Type of option", examples=["call"]
    )
    num_simulations: int = Field(
        default=100_000,
        ge=1000,
        le=1_000_000,
        description="Number of Monte Carlo paths",
    )

    @field_validator("volatility")
    @classmethod
    def volatility_must_be_reasonable(cls, v: float) -> float:
        """Additional validation beyond range checks."""
        if v > 2.0:  # 200% volatility
            # In production, you might want to just warn, not reject
            pass  # We'll rely on the le=5 constraint from Field
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "spot_price": 100,
                    "strike_price": 105,
                    "time_to_maturity": 1.0,
                    "volatility": 0.2,
                    "risk_free_rate": 0.05,
                    "option_type": "call",
                    "num_simulations": 100000,
                }
            ]
        }
    }


class OptionPricingResponse(BaseModel):
    """Response schema for option pricing."""

    simulation_id: str
    option_price: float
    std_error: float
    confidence_interval_95: float
    black_scholes_price: float | None = None
    greeks: dict[str, float] | None = None
    inputs: OptionPricingRequest
    timestamp: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "simulation_id": "sim_1701234567_abc123",
                    "option_price": 8.92,
                    "std_error": 0.03,
                    "confidence_interval_95": 0.06,
                    "black_scholes_price": 8.95,
                    "greeks": {
                        "delta": 0.5432,
                        "gamma": 0.0234,
                        "vega": 0.3456,
                        "theta": -0.0123,
                        "rho": 0.2345,
                    },
                    "inputs": {
                        "spot_price": 100,
                        "strike_price": 105,
                        "time_to_maturity": 1.0,
                        "volatility": 0.2,
                        "risk_free_rate": 0.05,
                        "option_type": "call",
                        "num_simulations": 100000,
                    },
                    "timestamp": "2024-01-15T10:30:00Z",
                }
            ]
        }
    }


class SimulationResult(BaseModel):
    """Full simulation result stored in JSON."""

    simulation_id: str
    option_price: float
    std_error: float
    confidence_interval_95: float
    black_scholes_price: float | None = None
    greeks: dict[str, float] | None = None
    inputs: dict  # Store the original request as dict
    timestamp: datetime


class HealthCheckResponse(BaseModel):
    """Health check endpoint response."""

    status: str
    timestamp: datetime
    version: str = "1.0.0"