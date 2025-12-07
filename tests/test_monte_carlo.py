"""Unit tests for Monte Carlo pricing engine."""

import pytest
import numpy as np
from app.monte_carlo import price_european_option, validate_pricing_inputs


class TestOptionPricing:
    """Test suite for option pricing calculations."""

    def test_call_option_pricing(self):
        """Test that call option pricing produces reasonable results."""
        result = price_european_option(
            spot_price=100,
            strike_price=100,
            time_to_maturity=1.0,
            volatility=0.2,
            risk_free_rate=0.05,
            option_type="call",
            num_simulations=100_000,
            random_seed=42,  # For reproducibility
        )

        # At-the-money call with reasonable parameters should be priced around 10
        # (Using Black-Scholes as a reference, this should be ~10.45)
        assert 9.0 < result["price"] < 12.0
        assert result["std_error"] > 0
        assert result["confidence_interval_95"] > 0

    def test_put_option_pricing(self):
        """Test put option pricing."""
        result = price_european_option(
            spot_price=100,
            strike_price=100,
            time_to_maturity=1.0,
            volatility=0.2,
            risk_free_rate=0.05,
            option_type="put",
            num_simulations=100_000,
            random_seed=42,
        )

        # At-the-money put should be cheaper than call (due to positive drift)
        assert 5.0 < result["price"] < 8.0

    def test_deep_in_the_money_call(self):
        """Deep ITM call should approximately equal intrinsic value."""
        result = price_european_option(
            spot_price=150,
            strike_price=100,
            time_to_maturity=0.1,  # Short time to expiry
            volatility=0.2,
            risk_free_rate=0.05,
            option_type="call",
            num_simulations=50_000,
            random_seed=42,
        )

        # Intrinsic value is 50, so price should be close to that
        assert result["price"] > 49.0

    def test_out_of_the_money_put(self):
        """Deep OTM put should be nearly worthless."""
        result = price_european_option(
            spot_price=150,
            strike_price=100,
            time_to_maturity=0.1,
            volatility=0.2,
            risk_free_rate=0.05,
            option_type="put",
            num_simulations=50_000,
            random_seed=42,
        )

        # Should be very close to zero
        assert result["price"] < 0.1


class TestInputValidation:
    """Test input validation logic."""

    def test_negative_spot_price(self):
        """Negative spot price should be invalid."""
        is_valid, msg = validate_pricing_inputs(
            spot_price=-100,
            strike_price=100,
            time_to_maturity=1.0,
            volatility=0.2,
            risk_free_rate=0.05,
        )
        assert not is_valid
        assert "spot price" in msg.lower()

    def test_negative_volatility(self):
        """Negative volatility should be invalid."""
        is_valid, msg = validate_pricing_inputs(
            spot_price=100,
            strike_price=100,
            time_to_maturity=1.0,
            volatility=-0.2,
            risk_free_rate=0.05,
        )
        assert not is_valid
        assert "volatility" in msg.lower()

    def test_unrealistic_volatility(self):
        """Volatility > 500% should be flagged."""
        is_valid, msg = validate_pricing_inputs(
            spot_price=100,
            strike_price=100,
            time_to_maturity=1.0,
            volatility=6.0,  # 600%
            risk_free_rate=0.05,
        )
        assert not is_valid

    def test_valid_inputs(self):
        """Valid inputs should pass."""
        is_valid, msg = validate_pricing_inputs(
            spot_price=100,
            strike_price=105,
            time_to_maturity=1.0,
            volatility=0.25,
            risk_free_rate=0.05,
        )
        assert is_valid
        assert msg == ""