"""
Auto-generated test cases for function: calculate_total
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:26:48
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

# Assume the module containing PriceCalculator is named `price_calculator`.
# The following imports are only for type checking and will be resolved
# by the test runner when the module is available.
try:
    from price_calculator import PriceCalculator
except Exception:
    # If the module cannot be imported, define a minimal stub for the
    # purpose of type checking. The real implementation will be
    # provided by the user during test execution.
    class PriceCalculator:
        def calculate_total(self, cart, discount_percent=0):
            pass


@pytest.mark.parametrize(
    "subtotal, discount_percent, qualifies_free_shipping, expected_total",
    [
        # No discount, no free shipping
        (100.0, 0, False, 100.0 * 1.1 + 5),
        # 10% discount, no free shipping
        (200.0, 10, False, (200.0 * 0.9) * 1.1 + 5),
        # 20% discount, free shipping
        (150.0, 20, True, (150.0 * 0.8) * 1.1),
        # 0% discount, free shipping
        (50.0, 0, True, 50.0 * 1.1),
        # 100% discount, no free shipping
        (80.0, 100, False, 0.0 * 1.1 + 5),
    ],
)
def test_calculate_total_normal_cases(
    subtotal, discount_percent, qualifies_free_shipping, expected_total, monkeypatch
):
    """
    Test normal operation of `calculate_total` with a variety of
    subtotal amounts, discount percentages, and shipping eligibility.
    """
    # Patch the external dependencies used by PriceCalculator
    monkeypatch.setattr("price_calculator.calculate_discount", lambda s, d: s * (1 - d / 100))
    monkeypatch.setattr("price_calculator.apply_tax", lambda s: s * 1.1)
    monkeypatch.setattr("price_calculator.SHRIPPING_FEE", 5)

    # Create a mock CartManager
    cart = MagicMock()
    cart.get_subtotal.return_value = subtotal
    cart.qualifies_for_free_shipping.return_value = qualifies_free_shipping

    # Instantiate the calculator and compute the total
    calculator = PriceCalculator()
    result = calculator.calculate_total(cart, discount_percent)

    # Assert that the result matches the expected value within floatingpoint tolerance
    assert result == pytest.approx(expected_total)


def test_calculate_total_edge_cases(monkeypatch):
    """
    Test boundary and edge cases such as zero subtotal, 100% discount,
    negative discount values, and free shipping eligibility.
    """
    # Patch dependencies
    monkeypatch.setattr("price_calculator.calculate_discount", lambda s, d: s * (1 - d / 100))
    monkeypatch.setattr("price_calculator.apply_tax", lambda s: s * 1.1)
    monkeypatch.setattr("price_calculator.SHRIPPING_FEE", 5)

    calculator = PriceCalculator()

    # 1. Zero subtotal, no discount, no free shipping
    cart_zero = MagicMock()
    cart_zero.get_subtotal.return_value = 0.0
    cart_zero.qualifies_for_free_shipping.return_value = False
    total_zero = calculator.calculate_total(cart_zero, 0)
    assert total_zero == pytest.approx(0.0 * 1.1 + 5)

    # 2. 100% discount, free shipping
    cart_free = MagicMock()
    cart_free.get_subtotal.return_value = 120.0
    cart_free.qualifies_for_free_shipping.return_value = True
    total_free = calculator.calculate_total(cart_free, 100)
    assert total_free == pytest.approx(0.0 * 1.1)

    # 3. Negative discount (treated as no discount)
    cart_negative = MagicMock()
    cart_negative.get_subtotal.return_value = 50.0
    cart_negative.qualifies_for_free_shipping.return_value = False
    total_negative = calculator.calculate_total(cart_negative, -5)
    assert total_negative == pytest.approx(50.0 * 1.1 + 5)

    # 4. Discount exactly 0 (no discount applied)
    cart_no_discount = MagicMock()
    cart_no_discount.get_subtotal.return_value = 75.0
    cart_no_discount.qualifies_for_free_shipping.return_value = True
    total_no_discount = calculator.calculate_total(cart_no_discount, 0)
    assert total_no_discount == pytest.approx(75.0 * 1.1)


def test_calculate_total_error_cases(monkeypatch):
    """
    Test that `calculate_total` raises appropriate exceptions when
    given invalid inputs such as a nonCartManager object or
    nonnumeric discount values.
    """
    # Patch dependencies to avoid side effects
    monkeypatch.setattr("price_calculator.calculate_discount", lambda s, d: s * (1 - d / 100))
    monkeypatch.setattr("price_calculator.apply_tax", lambda s: s * 1.1)
    monkeypatch.setattr("price_calculator.SHRIPPING_FEE", 5)

    calculator = PriceCalculator()

    # 1. cart is None -> AttributeError when calling get_subtotal
    with pytest.raises(AttributeError):
        calculator.calculate_total(None, 10)

    # 2. discount_percent is a string -> TypeError when comparing > 0
    cart = MagicMock()
    cart.get_subtotal.return_value = 100.0
    cart.qualifies_for_free_shipping.return_value = False
    with pytest.raises(TypeError):
        calculator.calculate_total(cart, "ten")

    # 3. discount_percent is None -> TypeError when comparing > 0
    with pytest.raises(TypeError):
        calculator.calculate_total(cart, None)