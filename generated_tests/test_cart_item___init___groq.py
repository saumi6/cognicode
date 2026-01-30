"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:54:28
Source file: cart_item.py
Function signature: def __init__(self, product: Product, quantity: int = 1)
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

# The class under test is assumed to be importable from the module where it is defined.
# Replace `your_module` with the actual module name if needed.
from your_module import CartItem


@pytest.mark.parametrize(
    "price, quantity",
    [
        (10.0, 1),          # default quantity
        (5.5, 3),           # typical multiunit case
        (0.99, 10),         # many smallprice items
        (100.0, 2),         # larger price, small quantity
        (0.0, 5),           # zeroprice product
    ],
)
def test___init___normal_cases(price, quantity):
    """Verify that normal initialisation stores the given product and quantity."""
    # create a lightweight mock product with the required ``price`` attribute
    product = Mock()
    product.price = price

    # instantiate the object **without** invoking __init__, then call __init__ manually
    item = CartItem.__new__(CartItem)
    item.__init__(product, quantity)

    # the attributes should be exactly what we passed in
    assert item.product is product
    assert item.quantity == quantity


def test___init___edge_cases():
    """Check boundary conditions such as zero quantity and very large numbers."""
    # edge case 1  quantity = 0 (allowed by the current implementation)
    product_zero_qty = Mock()
    product_zero_qty.price = 12.34
    item_zero = CartItem.__new__(CartItem)
    item_zero.__init__(product_zero_qty, 0)
    assert item_zero.quantity == 0
    assert item_zero.product is product_zero_qty

    # edge case 2  extremely large quantity
    large_qty = 10_000_000
    product_large_qty = Mock()
    product_large_qty.price = 1.23
    item_large = CartItem.__new__(CartItem)
    item_large.__init__(product_large_qty, large_qty)
    assert item_large.quantity == large_qty
    assert item_large.product is product_large_qty

    # edge case 3  product price is negative (some systems allow discounts)
    product_negative_price = Mock()
    product_negative_price.price = -5.00
    item_negative_price = CartItem.__new__(CartItem)
    item_negative_price.__init__(product_negative_price, 2)
    assert item_negative_price.product.price == -5.00
    assert item_negative_price.quantity == 2


def test___init___error_cases():
    """Ensure that clearly invalid inputs raise appropriate exceptions."""
    valid_product = Mock()
    valid_product.price = 9.99

    # 1. quantity must be an int  passing a string should raise TypeError
    item = CartItem.__new__(CartItem)
    with pytest.raises(TypeError):
        item.__init__(valid_product, "not-an-int")

    # 2. negative quantity is not sensible  expect ValueError
    item = CartItem.__new__(CartItem)
    with pytest.raises(ValueError):
        item.__init__(valid_product, -3)

    # 3. product must provide a ``price`` attribute  passing None should raise AttributeError
    item = CartItem.__new__(CartItem)
    with pytest.raises(AttributeError):
        item.__init__(None, 1)