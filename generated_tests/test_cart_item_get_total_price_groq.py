"""
Auto-generated test cases for function: get_total_price
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:41:09
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
from unittest.mock import Mock, MagicMock

# The class under test is assumed to live in a module named ``cart_item``.
# Adjust the import path if the actual module name differs.
from cart_item import CartItem


@pytest.mark.parametrize(
    "price, quantity, expected_total",
    [
        (10.0, 1, 10.0),          # simple integer quantity
        (5.55, 2, 11.10),         # price with cents, quantity > 1
        (0.99, 3, 2.97),          # multiple items, rounding not needed
        (1234.56, 0, 0.0),        # zero quantity edgecase
        (1.2345, 4, 4.938),       # price with more than two decimals
    ],
)
def test_get_total_price_normal_cases(monkeypatch, price, quantity, expected_total):
    """
    Normal cases for ``CartItem.get_total_price``.
    function so that the expected total is simply ``price * quantity``.
    """
    # Patch ``round_currency`` to return the raw value (identity)
    monkeypatch.setattr("cart_item.round_currency", lambda x: x)

    # Mock a ``Product`` instance with the required ``price`` attribute
    product_mock = Mock()
    product_mock.price = price

    # Instantiate the CartItem with the mocked product
    item = CartItem(product=product_mock, quantity=quantity)

    # Call the method under test
    total = item.get_total_price()

    # Assert the total matches the expected value (floating point safe)
    assert total == pytest.approx(expected_total)


def test_get_total_price_edge_cases(monkeypatch):
    """
    Edgecase tests for ``CartItem.get_total_price``:
    * quantity = 0 (should return 0)
    * very large numbers (ensure no overflow)
    * ``round_currency`` is verified to be called with the correct raw value.
    """
    # Keep a record of the argument passed to ``round_currency``
    called_args = {}

    def fake_round_currency(value):
        called_args["value"] = value
        # Simulate a realistic rounding to two decimal places
        return round(value, 2)

    monkeypatch.setattr("cart_item.round_currency", fake_round_currency)

    # ---- Edge case 1: quantity = 0 ----
    product_zero_qty = Mock()
    product_zero_qty.price = 99.99
    item_zero_qty = CartItem(product=product_zero_qty, quantity=0)

    total_zero_qty = item_zero_qty.get_total_price()
    assert total_zero_qty == pytest.approx(0.0)
    assert called_args["value"] == pytest.approx(0.0)

    # ---- Edge case 2: very large numbers ----
    large_price = 1_000_000.1234
    large_quantity = 10_000
    product_large = Mock()
    product_large.price = large_price
    item_large = CartItem(product=product_large, quantity=large_quantity)

    total_large = item_large.get_total_price()
    expected_raw = large_price * large_quantity
    # ``fake_round_currency`` rounds to two decimals
    expected_rounded = round(expected_raw, 2)

    assert total_large == pytest.approx(expected_rounded)
    assert called_args["value"] == pytest.approx(expected_raw)


def test_get_total_price_error_cases():
    """
    Error cases for ``CartItem.get_total_price``:
    * ``product`` is ``None``  should raise ``AttributeError`` when accessing ``price``.
    * ``product.price`` is not a number  should raise ``TypeError`` during multiplication.
    * ``quantity`` is a nonint (e.g., string)  should raise ``TypeError`` when used in multiplication.
    """
    # ---- Case 1: product is None ----
    with pytest.raises(AttributeError):
        item = CartItem(product=None, quantity=1)
        item.get_total_price()

    # ---- Case 2: product.price is nonnumeric ----
    product_bad_price = Mock()
    product_bad_price.price = "not-a-number"
    item_bad_price = CartItem(product=product_bad_price, quantity=2)
    with pytest.raises(TypeError):
        item_bad_price.get_total_price()

    # ---- Case 3: quantity is nonint (string) ----
    product_ok = Mock()
    product_ok.price = 10.0
    item_bad_qty = CartItem(product=product_ok, quantity="3")
    with pytest.raises(TypeError):
        item_bad_qty.get_total_price()