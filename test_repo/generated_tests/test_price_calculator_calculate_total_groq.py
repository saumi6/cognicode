"""
Auto-generated test cases for function: calculate_total
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:08:12
Source file: price_calculator.py
Function signature: def calculate_total(self, cart: CartManager, discount_percent: float = 0)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.price_calculator import PriceCalculator

import pytest
from unittest.mock import MagicMock

# The module that contains PriceCalculator is assumed to be named ``price_calculator``.
# Adjust the import path if the actual file name differs.
from price_calculator import PriceCalculator


@pytest.mark.parametrize(
    "subtotal, discount_percent, tax_rate, free_shipping, expected_total",
    [
        # No discount, tax 10%, free shipping
        (100.0, 0, 0.10, True, 110.0),
        # 10% discount, tax 5%, shipping fee applied
        (200.0, 10, 0.05, False,  (200.0 * 0.90) * 1.05 + 5.0),
        # 25% discount, tax 0%, free shipping
        (80.0, 25, 0.0, True, 80.0 * 0.75),
        # No discount, tax 0%, shipping fee applied
        (50.0, 0, 0.0, False, 50.0 + 5.0),
    ],
)
def test_calculate_total_normal_cases(
    monkeypatch,
    subtotal,
    discount_percent,
    tax_rate,
    free_shipping,
    expected_total,
):
    """Normal operation with various combinations of discount, tax and shipping."""
    # ----------------------------------------------------------------------
    # Arrange  mock the external helpers and the CartManager dependency
    # ----------------------------------------------------------------------
    # Mock ``calculate_discount`` to apply a simple percentage reduction.
    def fake_calculate_discount(amount, percent):
        return amount * (1 - percent / 100)

    # Mock ``apply_tax`` to apply a configurable tax rate.
    def fake_apply_tax(amount):
        return amount * (1 + tax_rate)

    # Patch the helpers using the **full absolute import path**.
    monkeypatch.setattr("price_calculator.calculate_discount", fake_calculate_discount)
    monkeypatch.setattr("price_calculator.apply_tax", fake_apply_tax)

    # Mock the CartManager instance.
    cart = MagicMock()
    cart.get_subtotal.return_value = subtotal
    cart.qualifies_for_free_shipping.return_value = free_shipping

    # ----------------------------------------------------------------------
    # Act
    # ----------------------------------------------------------------------
    calculator = PriceCalculator()
    result = calculator.calculate_total(cart, discount_percent=discount_percent)

    # ----------------------------------------------------------------------
    # Assert
    # ----------------------------------------------------------------------
    assert result == pytest.approx(expected_total)


def test_calculate_total_edge_cases(monkeypatch):
    """Edgecase scenarios such as 0%/100% discount and zero subtotal."""
    # ----------------------------------------------------------------------
    # Helper functions for this test suite
    # ----------------------------------------------------------------------
    def identity_discount(amount, percent):
        # 0% or 100% discount handling  the function itself is trivial.
        return amount * (1 - percent / 100)

    def tax_plus_10pct(amount):
        return amount * 1.10

    # Patch the helpers.
    monkeypatch.setattr("price_calculator.calculate_discount", identity_discount)
    monkeypatch.setattr("price_calculator.apply_tax", tax_plus_10pct)

    # ----------------------------------------------------------------------
    # Case 1  zero subtotal, no discount, free shipping
    # ----------------------------------------------------------------------
    cart1 = MagicMock()
    cart1.get_subtotal.return_value = 0.0
    cart1.qualifies_for_free_shipping.return_value = True

    calc = PriceCalculator()
    total1 = calc.calculate_total(cart1)
    assert total1 == pytest.approx(0.0)  # tax on zero is still zero, no shipping

    # ----------------------------------------------------------------------
    # Case 2  100% discount, tax applied, shipping fee charged
    # ----------------------------------------------------------------------
    cart2 = MagicMock()
    cart2.get_subtotal.return_value = 150.0
    cart2.qualifies_for_free_shipping.return_value = False

    total2 = calc.calculate_total(cart2, discount_percent=100)
    # After 100% discount subtotal becomes 0, tax leaves it 0, then shipping fee added.
    assert total2 == pytest.approx(5.0)  # SHIPPING_FEE is assumed to be 5.0 in the module

    # ----------------------------------------------------------------------
    # Case 3  discount just below 0% (invalid)  we let the helper raise.
    # ----------------------------------------------------------------------
    def raise_on_negative(amount, percent):
        if percent < 0:
            raise ValueError("Discount percent cannot be negative")
        return amount * (1 - percent / 100)

    monkeypatch.setattr("price_calculator.calculate_discount", raise_on_negative)

    cart3 = MagicMock()
    cart3.get_subtotal.return_value = 100.0
    cart3.qualifies_for_free_shipping.return_value = True

    with pytest.raises(ValueError):
        calc.calculate_total(cart3, discount_percent=-5)


def test_calculate_total_error_cases(monkeypatch):
    """Invalid inputs that should raise exceptions."""
    # ----------------------------------------------------------------------
    # Arrange  make the helper functions raise on bad input
    # ----------------------------------------------------------------------
    def safe_calculate_discount(amount, percent):
        if not isinstance(percent, (int, float)):
            raise TypeError("discount_percent must be numeric")
        if percent < 0 or percent > 100:
            raise ValueError("discount_percent out of range")
        return amount * (1 - percent / 100)

    def safe_apply_tax(amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("subtotal must be numeric")
        return amount * 1.08  # assume 8% tax for the test

    monkeypatch.setattr("price_calculator.calculate_discount", safe_calculate_discount)
    monkeypatch.setattr("price_calculator.apply_tax", safe_apply_tax)

    calc = PriceCalculator()

    # ----------------------------------------------------------------------
    # 1. Nonnumeric discount_percent should raise TypeError
    # ----------------------------------------------------------------------
    cart = MagicMock()
    cart.get_subtotal.return_value = 50.0
    cart.qualifies_for_free_shipping.return_value = True

    with pytest.raises(TypeError):
        calc.calculate_total(cart, discount_percent="ten")

    # ----------------------------------------------------------------------
    # 2. Discount percent > 100 should raise ValueError
    # ----------------------------------------------------------------------
    with pytest.raises(ValueError):
        calc.calculate_total(cart, discount_percent=150)

    # ----------------------------------------------------------------------
    # 3. Cart returning a nonnumeric subtotal should propagate TypeError from apply_tax
    # ----------------------------------------------------------------------
    bad_cart = MagicMock()
    bad_cart.get_subtotal.return_value = "not-a-number"
    bad_cart.qualifies_for_free_shipping.return_value = True

    with pytest.raises(TypeError):
        calc.calculate_total(bad_cart, discount_percent=0)