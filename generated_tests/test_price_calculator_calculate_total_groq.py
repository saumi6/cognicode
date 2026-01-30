"""
Auto-generated test cases for function: calculate_total
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:47
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
        # no discount, no tax, free shipping
        (100.0, 0, 0.0, True, 100.0),
        # 10% discount, 5% tax, shipping fee applied
        (200.0, 10, 0.05, False,  (200.0 * 0.90) * 1.05 + 5.0),
        # 0% discount, 20% tax, free shipping
        (50.0, 0, 0.20, True,  50.0 * 1.20),
        # 25% discount, 0% tax, shipping fee applied
        (80.0, 25, 0.0, False, (80.0 * 0.75) + 5.0),
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

    # Mock ``apply_tax`` to apply a simple tax rate (passed via closure).
    def make_fake_apply_tax(rate):
        return lambda amount: amount * (1 + rate)

    # Mock ``SHIPPING_FEE`` constant.
    fake_shipping_fee = 5.0

    monkeypatch.setattr("price_calculator.calculate_discount", fake_calculate_discount)
    monkeypatch.setattr("price_calculator.apply_tax", make_fake_apply_tax(tax_rate))
    monkeypatch.setattr("price_calculator.SHIPPING_FEE", fake_shipping_fee)

    # Mock CartManager instance.
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
    """Edgecase handling such as 0%/100% discount and zero subtotal."""
    # ----------------------------------------------------------------------
    # Arrange  helpers that behave deterministically for edge values
    # ----------------------------------------------------------------------
    def fake_calculate_discount(amount, percent):
        # 100% discount should yield 0, otherwise simple reduction.
        return amount * (1 - percent / 100)

    def fake_apply_tax(amount):
        # Tax is a fixed 10% for this edgecase suite.
        return amount * 1.10

    monkeypatch.setattr("price_calculator.calculate_discount", fake_calculate_discount)
    monkeypatch.setattr("price_calculator.apply_tax", fake_apply_tax)
    monkeypatch.setattr("price_calculator.SHIPPING_FEE", 7.5)

    # Helper to run a single scenario.
    def run_scenario(subtotal, discount, free_shipping, expected):
        cart = MagicMock()
        cart.get_subtotal.return_value = subtotal
        cart.qualifies_for_free_shipping.return_value = free_shipping
        calc = PriceCalculator()
        total = calc.calculate_total(cart, discount_percent=discount)
        assert total == pytest.approx(expected)

    # 0% discount, free shipping, zero subtotal
    run_scenario(subtotal=0.0, discount=0, free_shipping=True, expected=0.0)

    # 100% discount, tax still applied to 0, shipping fee added
    run_scenario(subtotal=123.45, discount=100, free_shipping=False,
                 expected=0.0 + 7.5)

    # Subtotal positive, discount 0, tax applied, free shipping
    run_scenario(subtotal=80.0, discount=0, free_shipping=True,
                 expected=80.0 * 1.10)

    # Subtotal positive, discount 100, free shipping (total should be 0)
    run_scenario(subtotal=80.0, discount=100, free_shipping=True,
                 expected=0.0)


def test_calculate_total_error_cases(monkeypatch):
    """Invalid inputs should raise appropriate exceptions."""
    # ----------------------------------------------------------------------
    # Arrange  make ``calculate_discount`` raise on negative discount
    # ----------------------------------------------------------------------
    def fake_calculate_discount(amount, percent):
        if percent < 0:
            raise ValueError("Discount percent cannot be negative")
        return amount * (1 - percent / 100)

    def fake_apply_tax(amount):
        return amount  # tax is irrelevant for these error tests

    monkeypatch.setattr("price_calculator.calculate_discount", fake_calculate_discount)
    monkeypatch.setattr("price_calculator.apply_tax", fake_apply_tax)
    monkeypatch.setattr("price_calculator.SHIPPING_FEE", 5.0)

    # ----------------------------------------------------------------------
    # 1. Negative discount percent should raise ValueError from calculate_discount
    # ----------------------------------------------------------------------
    cart = MagicMock()
    cart.get_subtotal.return_value = 50.0
    cart.qualifies_for_free_shipping.return_value = True
    calc = PriceCalculator()
    with pytest.raises(ValueError):
        calc.calculate_total(cart, discount_percent=-10)

    # ----------------------------------------------------------------------
    # 2. Nonnumeric discount percent should raise TypeError when compared
    # ----------------------------------------------------------------------
    cart = MagicMock()
    cart.get_subtotal.return_value = 30.0
    cart.qualifies_for_free_shipping.return_value = True
    calc = PriceCalculator()
    with pytest.raises(TypeError):
        # Passing a string forces the ``> 0`` comparison to fail
        calc.calculate_total(cart, discount_percent="twenty")

    # ----------------------------------------------------------------------
    # 3. Cart returning a nonnumeric subtotal should propagate a TypeError
    # ----------------------------------------------------------------------
    cart = MagicMock()
    cart.get_subtotal.return_value = "not-a-number"
    cart.qualifies_for_free_shipping.return_value = True
    calc = PriceCalculator()
    with pytest.raises(TypeError):
        calc.calculate_total(cart, discount_percent=0)