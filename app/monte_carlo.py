"""
Monte Carlo pricing engine for European options.

This module demonstrates:
1. Correct financial mathematics (GBM simulation)
2. Type hints for maintainability
3. Separation of concerns (pure functions, no I/O)
"""

import numpy as np
from typing import Literal


def price_european_option(
    spot_price: float,
    strike_price: float,
    time_to_maturity: float,  # In years
    volatility: float,  # Annual volatility (e.g., 0.2 = 20%)
    risk_free_rate: float,  # Annual rate (e.g., 0.05 = 5%)
    option_type: Literal["call", "put"],
    num_simulations: int = 100_000,
    random_seed: int | None = None,
) -> dict[str, float]:
    """
    Price a European option using Monte Carlo simulation.

    Args:
        spot_price: Current stock price (S_0)
        strike_price: Option strike price (K)
        time_to_maturity: Time to expiration in years (T)
        volatility: Annual volatility (σ)
        risk_free_rate: Risk-free interest rate (r)
        option_type: "call" or "put"
        num_simulations: Number of Monte Carlo paths
        random_seed: For reproducible results in testing

    Returns:
        Dictionary containing:
            - price: The option price
            - std_error: Standard error of the estimate
            - confidence_interval: 95% CI for the price
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Generate random draws from standard normal distribution
    Z = np.random.standard_normal(num_simulations)

    # Simulate terminal stock prices using Geometric Brownian Motion
    # S_T = S_0 * exp((r - 0.5*σ²)*T + σ*√T*Z)
    drift = (risk_free_rate - 0.5 * volatility**2) * time_to_maturity
    diffusion = volatility * np.sqrt(time_to_maturity) * Z
    terminal_prices = spot_price * np.exp(drift + diffusion)

    # Calculate payoffs
    if option_type == "call":
        payoffs = np.maximum(terminal_prices - strike_price, 0)
    else:  # put
        payoffs = np.maximum(strike_price - terminal_prices, 0)

    # Discount payoffs to present value
    discount_factor = np.exp(-risk_free_rate * time_to_maturity)
    discounted_payoffs = payoffs * discount_factor

    # Calculate statistics
    option_price = np.mean(discounted_payoffs)
    std_error = np.std(discounted_payoffs) / np.sqrt(num_simulations)
    confidence_interval = 1.96 * std_error  # 95% CI

    return {
        "price": float(option_price),
        "std_error": float(std_error),
        "confidence_interval_95": float(confidence_interval),
    }


def validate_pricing_inputs(
    spot_price: float,
    strike_price: float,
    time_to_maturity: float,
    volatility: float,
    risk_free_rate: float,
) -> tuple[bool, str]:
    """
    Validate option pricing inputs.

    Returns:
        (is_valid, error_message) tuple
    """
    if spot_price <= 0:
        return False, "Spot price must be positive"

    if strike_price <= 0:
        return False, "Strike price must be positive"

    if time_to_maturity <= 0:
        return False, "Time to maturity must be positive"

    if volatility < 0:
        return False, "Volatility cannot be negative"

    if volatility > 5:  # 500% is unrealistic
        return False, "Volatility seems unrealistically high (>500%)"

    # Risk-free rate can be negative in some markets, but let's be reasonable
    if risk_free_rate < -0.1 or risk_free_rate > 0.3:
        return False, "Risk-free rate should be between -10% and 30%"

    return True, ""