"""
Auto-generated test cases for function: decrement
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:39
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
        (5, 4),   # typical decrement
        (2, 1),   # another typical case
        (1, 0),   # decrement to zero
    ],
)
def test_decrement_normal_cases(initial_qty, expected_qty):
    """Decrement should reduce a positive quantity by exactly one."""
    # Mock a simple Product with a price attribute (price is irrelevant for decrement)
    mock_product = Mock()
    mock_product.price = 10.0

    # Instantiate CartItem with the mocked product and the parametrized quantity
    item = CartItem(product=mock_product, quantity=initial_qty)

    # Call the method under test
    item.decrement()

    # Verify that the quantity was decreased correctly
    assert item.quantity == expected_qty


def test_decrement_edge_cases():
    """Edgecase handling for zero and negative quantities."""
    mock_product = Mock()
    mock_product.price = 5.0

    # Case 1: quantity already zero  should stay zero
    zero_item = CartItem(product=mock_product, quantity=0)
    zero_item.decrement()
    assert zero_item.quantity == 0, "Quantity should remain 0 when decrementing at 0"

    # Case 2: negative quantity  method should leave it unchanged
    negative_item = CartItem(product=mock_product, quantity=-3)
    negative_item.decrement()
    assert negative_item.quantity == -3, "Negative quantity should remain unchanged"


def test_decrement_error_cases():
    """Calling decrement with an invalid initial quantity should raise a TypeError."""
    mock_product = Mock()
    mock_product.price = 1.0

    # Initialise CartItem with a nonnumeric quantity (e.g., None)
    invalid_item = CartItem(product=mock_product, quantity=None)

    # The comparison `self.quantity > 0` inside `decrement` will raise TypeError
    with pytest.raises(TypeError):
        invalid_item.decrement()