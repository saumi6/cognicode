"""
Auto-generated test cases for function: get_total_price
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 01:03:11
Source file: cart_item.py
Function signature: def get_total_price(self) -> float
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.cart_item import CartItem

import pytest
from unittest.mock import MagicMock

# Import the class and the helper function from the module that contains them.
# Adjust the import path if the module name differs.
from cart_item import CartItem, round_currency


@pytest.mark.parametrize(
    "price, quantity, expected",
    [
        (10.0, 1, 10.0),
        (9.99, 3, 29.97),
        (0.0, 5, 0.0),
        (123.456, 2, 246.912),
        (1.2345, 10, 12.345),
    ],
)
def test_get_total_price_normal_cases(monkeypatch, price, quantity, expected):
    """
    Test normal cases for CartItem.get_total_price.

    The round_currency function is monkeypatched to the identity function
    so that the test focuses on the multiplication logic.
    """
    # Patch round_currency to avoid any rounding sideeffects.
    monkeypatch.setattr("cart_item.round_currency", lambda x: x)

    # Create a mock product with the desired price.
    product = MagicMock()
    product.price = price

    # Instantiate CartItem and compute the total price.
    item = CartItem(product=product, quantity=quantity)
    result = item.get_total_price()

    # Assert that the result matches the expected value.
    assert result == pytest.approx(expected)


def test_get_total_price_edge_cases(monkeypatch):
    """
    Test edge cases for CartItem.get_total_price.

    Edge cases include zero quantity, very large numbers, and zero price.
    """
    # Patch round_currency to the identity function.
    monkeypatch.setattr("cart_item.round_currency", lambda x: x)

    # 1. Zero quantity
    product_zero_qty = MagicMock()
    product_zero_qty.price = 99.99
    item_zero_qty = CartItem(product=product_zero_qty, quantity=0)
    assert item_zero_qty.get_total_price() == 0.0

    # 2. Zero price
    product_zero_price = MagicMock()
    product_zero_price.price = 0.0
    item_zero_price = CartItem(product=product_zero_price, quantity=5)
    assert item_zero_price.get_total_price() == 0.0

    # 3. Very large numbers
    large_price = 1e12
    large_qty = 1e6
    product_large = MagicMock()
    product_large.price = large_price
    item_large = CartItem(product=product_large, quantity=int(large_qty))
    expected_large = large_price * large_qty
    assert item_large.get_total_price() == pytest.approx(expected_large)


def test_get_total_price_error_cases(monkeypatch):
    """
    Test error cases for CartItem.get_total_price.

    These include invalid product types, nonnumeric prices, and
    exceptions raised by round_currency.
    """
    # 1. Product is None -> AttributeError when accessing .price
    with pytest.raises(AttributeError):
        item_none = CartItem(product=None, quantity=1)
        item_none.get_total_price()

    # 2. Product.price is a string -> TypeError during multiplication
    product_str_price = MagicMock()
    product_str_price.price = "not_a_number"
    with pytest.raises(TypeError):
        item_str_price = CartItem(product=product_str_price, quantity=2)
        item_str_price.get_total_price()

    # 3. round_currency raises an exception
    def faulty_round(x):
        raise ValueError("rounding failed")

    monkeypatch.setattr("cart_item.round_currency", faulty_round)

    product_valid = MagicMock()
    product_valid.price = 10.0
    item_faulty = CartItem(product=product_valid, quantity=3)
    with pytest.raises(ValueError, match="rounding failed"):
        item_faulty.get_total_price()