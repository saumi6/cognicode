"""
Auto-generated test cases for function: get_total_price
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:32
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
from unittest.mock import Mock

# The class under test is assumed to live in a module named ``cart_item``.
# Import it directly from that module.
from cart_item import CartItem


@pytest.mark.parametrize(
    "price, quantity, expected",
    [
        (10.0, 1, 10.0),          # simple case
        (5.55, 2, 11.10),         # multiplication with cents
        (0.99, 3, 2.97),          # three items, no rounding needed
        (123.456, 4, 493.824),    # larger numbers
    ],
)
def test_get_total_price_normal_cases(monkeypatch, price, quantity, expected):
    """
    Normal cases  verify that ``get_total_price`` returns the product of
    ``price`` and ``quantity`` when ``round_currency`` is a noop.
    """
    # Patch ``round_currency`` so it returns the raw value (no rounding).
    monkeypatch.setattr("cart_item.round_currency", lambda x: x)

    # Mock a ``Product`` with the required ``price`` attribute.
    product = Mock()
    product.price = price

    item = CartItem(product=product, quantity=quantity)
    result = item.get_total_price()

    assert result == expected


def test_get_total_price_edge_cases(monkeypatch):
    """
    Edge cases  test zero quantity, very large numbers and the real rounding
    behaviour of ``round_currency`` (rounded to two decimal places).
    """
    # Use a realistic rounding implementation (2decimal currency rounding).
    def round_currency(value):
        return round(value, 2)

    monkeypatch.setattr("cart_item.round_currency", round_currency)

    # 1 Zero quantity should yield 0.0 regardless of price.
    product_zero = Mock()
    product_zero.price = 99.99
    item_zero = CartItem(product=product_zero, quantity=0)
    assert item_zero.get_total_price() == 0.0

    # 2 Very large numbers  ensure no overflow and proper rounding.
    product_big = Mock()
    product_big.price = 1_000_000.1234
    item_big = CartItem(product=product_big, quantity=3)
    expected_big = round(1_000_000.1234 * 3, 2)
    assert item_big.get_total_price() == pytest.approx(expected_big)

    # 3 Price that requires rounding (e.g., 2.555 * 2 = 5.11 after rounding).
    product_round = Mock()
    product_round.price = 2.555
    item_round = CartItem(product=product_round, quantity=2)
    expected_round = round(2.555 * 2, 2)  # 5.11
    assert item_round.get_total_price() == pytest.approx(expected_round)


def test_get_total_price_error_cases():
    """
    Error cases  verify that ``get_total_price`` raises appropriate exceptions
    when the ``Product`` or ``quantity`` are of an invalid type.
    """
    # 1 ``product.price`` is ``None``  multiplication should raise TypeError.
    product_none = Mock()
    product_none.price = None
    item_none = CartItem(product=product_none, quantity=1)
    with pytest.raises(TypeError):
        item_none.get_total_price()

    # 2 ``product.price`` is a nonnumeric string.
    product_str = Mock()
    product_str.price = "not-a-number"
    item_str = CartItem(product=product_str, quantity=2)
    with pytest.raises(TypeError):
        item_str.get_total_price()

    # 3 ``quantity`` is not an integer (e.g., a string). The constructor accepts it,
    #    but the multiplication will fail.
    product_ok = Mock()
    product_ok.price = 10.0
    item_bad_qty = CartItem(product=product_ok, quantity="three")
    with pytest.raises(TypeError):
        item_bad_qty.get_total_price()