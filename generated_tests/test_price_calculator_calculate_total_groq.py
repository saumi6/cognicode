"""
Auto-generated test cases for function: calculate_total
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:41:36
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
    "subtotal, discount_percent, tax_rate, free_shipping, shipping_fee, expected_total",
    [
        # No discount, no tax, free shipping
        (100.0, 0, 0.0, True, 10.0, 100.0),
        # No discount, 10% tax, paid shipping
        (200.0, 0, 0.10, False, 15.0, 200.0 * 1.10 + 15.0),
        # 20% discount, 5% tax, free shipping
        (150.0, 20, 0.05, True, 12.0, (150.0 * 0.80) * 1.05),
        # 50% discount, 8% tax, paid shipping
        (80.0, 50, 0.08, False, 7.5, (80.0 * 0.50) * 1.08 + 7.5),
    ],
)
def test_calculate_total_normal_cases(
    monkeypatch,
    subtotal,
    discount_percent,
    tax_rate,
    free_shipping,
    shipping_fee,
    expected_total,
):
    """
    Normal operation tests covering combinations of discounts, taxes and shipping.
    """
    # ---- Arrange -----------------------------------------------------------
    # Mock CartManager
    cart = MagicMock()
    cart.get_subtotal.return_value = subtotal
    cart.qualifies_for_free_shipping.return_value = free_shipping

    # Patch external helpers
    def fake_calculate_discount(amount, percent):
        return amount * (1 - percent / 100)

    def fake_apply_tax(amount):
        return amount * (1 + tax_rate)

    monkeypatch.setattr("price_calculator.calculate_discount", fake_calculate_discount)
    monkeypatch.setattr("price_calculator.apply_tax", fake_apply_tax)
    monkeypatch.setattr("price_calculator.SHIPPING_FEE", shipping_fee)

    calculator = PriceCalculator()

    # ---- Act ---------------------------------------------------------------
    result = calculator.calculate_total(cart, discount_percent=discount_percent)

    # ---- Assert ------------------------------------------------------------
    assert result == pytest.approx(expected_total)


def test_calculate_total_edge_cases(monkeypatch):
    """
    Edgecase tests: zero subtotal, 100% discount, and freeshipping toggle.
    """
    # ---- Arrange -----------------------------------------------------------
    # Helper that simply returns the amount unchanged (no tax)
    monkeypatch.setattr("price_calculator.apply_tax", lambda x: x)
    # Shipping fee constant
    monkeypatch.setattr("price_calculator.SHIPPING_FEE", 9.99)

    # 1 Zero subtotal, no discount, free shipping
    cart_zero = MagicMock()
    cart_zero.get_subtotal.return_value = 0.0
    cart_zero.qualifies_for_free_shipping.return_value = True

    # 2 Full discount (100%), paid shipping
    cart_full_discount = MagicMock()
    cart_full_discount.get_subtotal.return_value = 123.45
    cart_full_discount.qualifies_for_free_shipping.return_value = False

    # Discount function that respects 100% discount
    monkeypatch.setattr(
        "price_calculator.calculate_discount",
        lambda amount, percent: amount * (1 - percent / 100),
    )

    calculator = PriceCalculator()

    # ---- Act & Assert -------------------------------------------------------
    # Zero subtotal case
    total_zero = calculator.calculate_total(cart_zero, discount_percent=0)
    assert total_zero == pytest.approx(0.0)  # no tax, no shipping

    # Full discount case (subtotal becomes 0, then shipping added)
    total_full_discount = calculator.calculate_total(
        cart_full_discount, discount_percent=100
    )
    assert total_full_discount == pytest.approx(9.99)  # only shipping remains


def test_calculate_total_error_cases(monkeypatch):
    """
    Tests that invalid inputs raise appropriate exceptions.
    """
    calculator = PriceCalculator()

    # ---- Arrange -----------------------------------------------------------
    # Mock cart that raises when get_subtotal is called
    cart_raises = MagicMock()
    cart_raises.get_subtotal.side_effect = ValueError("invalid subtotal")
    cart_raises.qualifies_for_free_shipping.return_value = True

    # Patch helpers with simple passthroughs (they won't be reached in the error case)
    monkeypatch.setattr("price_calculator.apply_tax", lambda x: x)
    monkeypatch.setattr("price_calculator.calculate_discount", lambda a, p: a)

    # ---- Act & Assert -------------------------------------------------------
    # get_subtotal raises ValueError
    with pytest.raises(ValueError):
        calculator.calculate_total(cart_raises, discount_percent=0)

    # Negative discount percent  our fake calculate_discount will raise
    def bad_discount(amount, percent):
        if percent < 0:
            raise ValueError("discount percent cannot be negative")
        return amount

    monkeypatch.setattr("price_calculator.calculate_discount", bad_discount)

    cart_ok = MagicMock()
    cart_ok.get_subtotal.return_value = 50.0
    cart_ok.qualifies_for_free_shipping.return_value = True

    with pytest.raises(ValueError):
        calculator.calculate_total(cart_ok, discount_percent=-10)

    # Passing a nonCartManager (e.g., None) should raise AttributeError when
    # the method tries to call ``get_subtotal``.
    with pytest.raises(AttributeError):
        calculator.calculate_total(None, discount_percent=0)