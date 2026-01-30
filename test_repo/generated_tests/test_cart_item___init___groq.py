"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 01:03:08
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
from unittest.mock import MagicMock

# Import the class under test.  Adjust the import path if the module name differs.
# The tests assume the implementation lives in a module called `cart_item.py`.
# If the module has a different name, change the import accordingly.
from cart_item import CartItem


@pytest.mark.parametrize(
    "price, quantity",
    [
        (10.0, 1),   # default quantity
        (15.5, 2),   # multiple items
        (0.99, 5),   # small price, larger quantity
    ],
)
def test___init___normal_cases(price, quantity):
    """
    Test that CartItem correctly stores the product and quantity for normal inputs.
    """
    # Arrange
    product = MagicMock()
    product.price = price

    # Act
    item = CartItem(product, quantity)

    # Assert
    assert item.product is product, "Product reference should be stored unchanged."
    assert item.quantity == quantity, "Quantity should be set to the provided value."


def test___init___default_quantity():
    """
    Test that the default quantity is 1 when omitted.
    """
    product = MagicMock()
    product.price = 20.0

    item = CartItem(product)

    assert item.quantity == 1, "Default quantity should be 1 when not specified."


@pytest.mark.parametrize(
    "price, quantity",
    [
        (0.0, 0),          # zero price and zero quantity
        (0.0, 5),          # zero price, positive quantity
        (5.0, 0),          # positive price, zero quantity
        (-5.0, 3),         # negative price, positive quantity
        (5.0, -3),         # positive price, negative quantity
        (-5.0, -3),        # negative price, negative quantity
        (1.2345, 10**6),   # large quantity
    ],
)
def test___init___edge_cases(price, quantity):
    """
    Test edge cases such as zero, negative, and very large values for price and quantity.
    """
    product = MagicMock()
    product.price = price

    item = CartItem(product, quantity)

    assert item.product is product, "Product reference should be stored unchanged."
    assert item.quantity == quantity, "Quantity should be set to the provided value."

    # Verify that get_total_price works even with edge values.
    # We patch round_currency to a simple identity function to avoid external dependencies.
    # The absolute import path must match the module where CartItem is defined.
    from cart_item import round_currency  # noqa: F401

    # Monkeypatch round_currency to identity for deterministic testing
    def identity(x):
        return x

    # Use monkeypatch fixture to temporarily replace round_currency
    # (the fixture is provided by pytest)
    # Since we cannot use fixtures directly in this function, we perform the patch manually.
    import importlib
    cart_module = importlib.import_module("cart_item")
    original_round = cart_module.round_currency
    cart_module.round_currency = identity
    try:
        expected_total = price * quantity
        assert item.get_total_price() == expected_total, (
            f"Total price should be {expected_total} for price={price} and quantity={quantity}"
        )
    finally:
        cart_module.round_currency = original_round


def test___init___error_cases():
    """
    Test that CartItem raises appropriate errors for invalid constructor usage.
    """
    # Missing required positional argument `product`
    with pytest.raises(TypeError):
        CartItem()

    # Too many positional arguments
    product = MagicMock()
    product.price = 10.0
    with pytest.raises(TypeError):
        CartItem(product, 1, 2)

    # Passing a non-Product object (e.g., a string) should not raise an error during __init__,
    # but will cause an AttributeError when accessing `price` later.
    # This demonstrates that __init__ itself does not validate the type of `product`.
    item = CartItem("not_a_product")
    with pytest.raises(AttributeError):
        _ = item.get_total_price()