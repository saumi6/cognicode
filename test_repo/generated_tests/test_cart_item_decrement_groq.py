"""
Auto-generated test cases for function: decrement
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:26:40
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

import pytest
from unittest.mock import Mock

# Import the class under test.  Adjust the import path to match your project layout.
# For example, if the class is defined in a file named `cart_item.py`, use:
# from cart_item import CartItem
# If it lives in a package, adjust accordingly.
from cart_item import CartItem


@pytest.mark.parametrize(
    "initial_qty, expected_qty",
    [
        (5, 4),   # typical decrement
        (1, 0),   # decrement to zero
        (10, 9),  # larger number
    ],
)
def test_decrement_normal_cases(initial_qty, expected_qty):
    """
    Test that decrement reduces the quantity by one for normal, positive values.
    """
    # Arrange: create a mock product with a price attribute (unused by decrement)
    product = Mock(price=10.0)

    # Act
    item = CartItem(product, quantity=initial_qty)
    item.decrement()

    # Assert
    assert item.quantity == expected_qty, (
        f"Expected quantity {expected_qty} after decrement, "
        f"but got {item.quantity}"
    )


@pytest.mark.parametrize(
    "initial_qty, expected_qty",
    [
        (0, 0),   # boundary: already zero
        (1, 0),   # boundary: decrement to zero
        (100, 99),  # large number
    ],
)
def test_decrement_edge_cases(initial_qty, expected_qty):
    """
    Test decrement behaviour at boundary conditions:
    - quantity already zero
    - quantity one (should become zero)
    - large quantity
    """
    product = Mock(price=20.0)

    item = CartItem(product, quantity=initial_qty)
    item.decrement()

    assert item.quantity == expected_qty, (
        f"Expected quantity {expected_qty} after decrement, "
        f"but got {item.quantity}"
    )


def test_decrement_error_cases():
    """
    Test that invalid inputs to the constructor raise appropriate errors.
    The decrement method itself does not raise errors for negative values,
    but constructing a CartItem with nonnumeric quantity should fail.
    """
    product = Mock(price=15.0)

    # Nonnumeric quantity: string
    with pytest.raises(TypeError):
        item = CartItem(product, quantity="5")
        item.decrement()

    # Nonnumeric quantity: None
    with pytest.raises(TypeError):
        item = CartItem(product, quantity=None)
        item.decrement()

    # Nonnumeric quantity: float (this is technically allowed but not an int)
    # The constructor accepts it, but decrement will work; we treat it as a
    # valid case rather than an error.  If you want to enforce int, uncomment:
    # with pytest.raises(TypeError):
    #     item = CartItem(product, quantity=3.5)
    #     item.decrement()