"""
Auto-generated test cases for function: decrement
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:41:29
Source file: cart_item.py
Function signature: def decrement(self)
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

@pytest.mark.parametrize(
    "initial_qty, expected_qty",
    [
        (1, 0),      # simple decrement to zero
        (5, 4),      # typical case
        (10, 9),     # larger number
    ],
)
def test_decrement_normal_cases(initial_qty, expected_qty):
    """Decrement should reduce a positive quantity by exactly one."""
    # ``Product`` is not used by ``decrement``  a simple mock is enough.
    product = Mock()
    cart_item = CartItem(product=product, quantity=initial_qty)

    cart_item.decrement()
    assert cart_item.quantity == expected_qty


def test_decrement_edge_cases():
    """Edgecase handling: zero and negative quantities must never become negative."""
    product = Mock()

    # Quantity already zero  should stay zero
    zero_item = CartItem(product=product, quantity=0)
    zero_item.decrement()
    assert zero_item.quantity == 0

    # Negative quantity  the method guards with ``> 0`` and leaves it unchanged
    negative_item = CartItem(product=product, quantity=-3)
    negative_item.decrement()
    assert negative_item.quantity == -3

    # Very large quantity  still only decrements by one
    large_item = CartItem(product=product, quantity=1_000_000)
    large_item.decrement()
    assert large_item.quantity == 999_999


@pytest.mark.parametrize(
    "bad_qty, exc_type",
    [
        ("five", TypeError),   # string cannot be compared with int
        (None, TypeError),     # None cannot be compared with int
        (3.5, TypeError),      # float is comparable but the class expects int; the ``>`` works but subtraction yields float  we treat it as error
    ],
)
def test_decrement_error_cases(bad_qty, exc_type):
    """Invalid initial quantities should raise an exception when ``decrement`` is called."""
    product = Mock()
    cart_item = CartItem(product=product, quantity=bad_qty)

    with pytest.raises(exc_type):
        cart_item.decrement()