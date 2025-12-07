"""
Black-Scholes closed-form solution for European options.

This provides:
- Analytical benchmark for Monte Carlo validation
- Greeks calculation (delta, gamma, vega, theta, rho)
- Much faster computation for simple cases
"""

import numpy as np
from scipy.stats import norm
from typing import Literal


def black_scholes_price(
    spot_price: float,
    strike_price: float,
    time_to_maturity: float,
    volatility: float,
    risk_free_rate: float,
    option_type: Literal["call", "put"],
) -> float:
    """
    Calculate European option price using Black-Scholes formula.
    
    Formula:
    - Call: S*N(d1) - K*e^(-rT)*N(d2)
    - Put: K*e^(-rT)*N(-d2) - S*N(-d1)
    
    Where:
    - d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
    - d2 = d1 - σ√T
    """
    # Calculate d1 and d2
    d1 = (
        np.log(spot_price / strike_price)
        + (risk_free_rate + 0.5 * volatility**2) * time_to_maturity
    ) / (volatility * np.sqrt(time_to_maturity))
    
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    
    # Calculate price based on option type
    if option_type == "call":
        price = spot_price * norm.cdf(d1) - strike_price * np.exp(
            -risk_free_rate * time_to_maturity
        ) * norm.cdf(d2)
    else:  # put
        price = strike_price * np.exp(
            -risk_free_rate * time_to_maturity
        ) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)
    
    return float(price)


def calculate_greeks(
    spot_price: float,
    strike_price: float,
    time_to_maturity: float,
    volatility: float,
    risk_free_rate: float,
    option_type: Literal["call", "put"],
) -> dict[str, float]:
    """
    Calculate option Greeks using Black-Scholes.
    
    Greeks measure sensitivity to various parameters:
    - Delta: sensitivity to spot price
    - Gamma: rate of change of delta
    - Vega: sensitivity to volatility
    - Theta: time decay
    - Rho: sensitivity to interest rate
    """
    # Calculate d1 and d2
    d1 = (
        np.log(spot_price / strike_price)
        + (risk_free_rate + 0.5 * volatility**2) * time_to_maturity
    ) / (volatility * np.sqrt(time_to_maturity))
    
    d2 = d1 - volatility * np.sqrt(time_to_maturity)
    
    # Delta
    if option_type == "call":
        delta = norm.cdf(d1)
    else:
        delta = -norm.cdf(-d1)
    
    # Gamma (same for call and put)
    gamma = norm.pdf(d1) / (spot_price * volatility * np.sqrt(time_to_maturity))
    
    # Vega (same for call and put, divided by 100 for 1% change)
    vega = spot_price * norm.pdf(d1) * np.sqrt(time_to_maturity) / 100
    
    # Theta (time decay per day)
    if option_type == "call":
        theta = (
            -(spot_price * norm.pdf(d1) * volatility) / (2 * np.sqrt(time_to_maturity))
            - risk_free_rate * strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
        ) / 365
    else:
        theta = (
            -(spot_price * norm.pdf(d1) * volatility) / (2 * np.sqrt(time_to_maturity))
            + risk_free_rate * strike_price * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2)
        ) / 365
    
    # Rho (sensitivity to 1% change in interest rate)
    if option_type == "call":
        rho = strike_price * time_to_maturity * np.exp(
            -risk_free_rate * time_to_maturity
        ) * norm.cdf(d2) / 100
    else:
        rho = -strike_price * time_to_maturity * np.exp(
            -risk_free_rate * time_to_maturity
        ) * norm.cdf(-d2) / 100
    
    return {
        "delta": float(delta),
        "gamma": float(gamma),
        "vega": float(vega),
        "theta": float(theta),
        "rho": float(rho),
    }