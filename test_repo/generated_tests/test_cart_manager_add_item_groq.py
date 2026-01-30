"""
Auto-generated test cases for function: add_item
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:07:34
Source file: cart_manager.py
Function signature: def add_item(self, product: Product, qty: int = 1)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.cart_manager import CartManager

import pytest
from unittest.mock import Mock, MagicMock

# NOTE:
# The tests assume that the implementation lives in a module named ``cart_manager``.
# If the actual file name is different, replace ``cart_manager`` with the correct
# import path (e.g. ``myapp.shopping.cart_manager``) in the ``monkeypatch.setattr``
# calls below.


def _make_product(sku: str):
    """Helper that creates a minimal ``Product`` mock with a ``sku`` attribute."""
    prod = Mock()
    prod.sku = sku
    return prod


def _make_cart_item_class():
    """Factory that returns a very small ``CartItem`` replacement used for testing."""
    class SimpleCartItem:
        def __init__(self, product, quantity):
            self.product = product
            self.quantity = quantity

        def get_total_price(self):
            # For the purpose of these tests the price is irrelevant;
            # we just return a deterministic value.
            return 10.0 * self.quantity

    return SimpleCartItem


@pytest.mark.parametrize(
    "initial_items, new_product, qty, expected_lengths, expected_quantities",
    [
        # Adding a brandnew product to an empty cart
        ([], "SKU-1", 1, 1, {"SKU-1": 1}),
        # Adding the same product again should increase its quantity
        (["SKU-1"], "SKU-1", 2, 1, {"SKU-1": 3}),
        # Adding a second distinct product should increase the list length
        (["SKU-1"], "SKU-2", 1, 2, {"SKU-1": 1, "SKU-2": 1}),
        # Adding multiple distinct products in one call (qty > 1)
        (["SKU-1"], "SKU-3", 4, 2, {"SKU-1": 1, "SKU-3": 4}),
    ],
)
def test_add_item_normal_cases(
    monkeypatch,
    initial_items,
    new_product,
    qty,
    expected_lengths,
    expected_quantities,
):
    """
    Normal usage of ``CartManager.add_item``:
    * adding a new product creates a new ``CartItem``;
    * adding a product that already exists increments its quantity.
    """
    # ------------------------------------------------------------------ #
    # Patch the ``CartItem`` used by ``CartManager`` with a lightweight stub
    # ------------------------------------------------------------------ #
    SimpleCartItem = _make_cart_item_class()
    monkeypatch.setattr("cart_manager.CartItem", SimpleCartItem, raising=False)

    # ------------------------------------------------------------------ #
    # Build the CartManager instance with a mocked ``User``
    # ------------------------------------------------------------------ #
    mock_user = Mock()
    from cart_manager import CartManager, MAX_ITEMS_PER_CART, ValidationError  # noqa: E402

    cart = CartManager(mock_user)

    # ------------------------------------------------------------------ #
    # Prepopulate the cart according to the parametrised ``initial_items``
    # ------------------------------------------------------------------ #
    for sku in initial_items:
        cart.items.append(SimpleCartItem(_make_product(sku), 1))

    # ------------------------------------------------------------------ #
    # Perform the operation under test
    # ------------------------------------------------------------------ #
    product = _make_product(new_product)
    cart.add_item(product, qty)

    # ------------------------------------------------------------------ #
    # Assertions
    # ------------------------------------------------------------------ #
    assert len(cart.items) == expected_lengths, "Unexpected number of CartItem objects"

    # Build a mapping sku -> quantity from the cart for easy comparison
    actual_quantities = {item.product.sku: item.quantity for item in cart.items}
    assert actual_quantities == expected_quantities, "Quantities do not match expected values"


def test_add_item_edge_cases(monkeypatch):
    """
    Edgecase tests:
    * Adding items that exactly fill the cart up to ``MAX_ITEMS_PER_CART``.
    * Adding a quantity of ``0`` (should be a noop but still respect the limit).
    """
    # ------------------------------------------------------------------ #
    # Patch ``CartItem`` with a simple implementation
    # ------------------------------------------------------------------ #
    SimpleCartItem = _make_cart_item_class()
    monkeypatch.setattr("cart_manager.CartItem", SimpleCartItem, raising=False)

    # ------------------------------------------------------------------ #
    # Import the class and constants
    # ------------------------------------------------------------------ #
    from cart_manager import CartManager, MAX_ITEMS_PER_CART, ValidationError  # noqa: E402

    mock_user = Mock()
    cart = CartManager(mock_user)

    # ------------------------------------------------------------------ #
    # Fill the cart to the exact limit using a single product
    # ------------------------------------------------------------------ #
    product_a = _make_product("A")
    cart.add_item(product_a, MAX_ITEMS_PER_CART)  # should succeed

    assert len(cart.items) == 1
    assert cart.items[0].quantity == MAX_ITEMS_PER_CART

    # ------------------------------------------------------------------ #
    # Adding zero items must not change the count and must not raise
    # ------------------------------------------------------------------ #
    cart.add_item(product_a, 0)
    assert cart.items[0].quantity == MAX_ITEMS_PER_CART, "Zeroquantity add altered quantity"

    # ------------------------------------------------------------------ #
    # Adding any positive quantity now would exceed the limit and raise
    # ------------------------------------------------------------------ #
    with pytest.raises(ValidationError):
        cart.add_item(product_a, 1)


def test_add_item_error_cases(monkeypatch):
    """
    Error handling tests:
    * Adding items that would exceed ``MAX_ITEMS_PER_CART`` raises ``ValidationError``.
    * Supplying a product without a ``sku`` attribute raises ``AttributeError``.
    """
    # ------------------------------------------------------------------ #
    # Patch ``CartItem`` with a simple implementation
    # ------------------------------------------------------------------ #
    SimpleCartItem = _make_cart_item_class()
    monkeypatch.setattr("cart_manager.CartItem", SimpleCartItem, raising=False)

    # ------------------------------------------------------------------ #
    # Import the class and constants
    # ------------------------------------------------------------------ #
    from cart_manager import CartManager, MAX_ITEMS_PER_CART, ValidationError  # noqa: E402

    mock_user = Mock()
    cart = CartManager(mock_user)

    # ------------------------------------------------------------------ #
    # 1. Exceeding the maximum allowed items should raise ValidationError
    # ------------------------------------------------------------------ #
    product = _make_product("OVER")
    # Fill the cart close to the limit
    cart.add_item(product, MAX_ITEMS_PER_CART - 1)

    with pytest.raises(ValidationError) as excinfo:
        cart.add_item(product, 2)  # this would push total to MAX+1
    assert "Cart is full" in str(excinfo.value)

    # ------------------------------------------------------------------ #
    # 2. Product without ``sku`` attribute should raise AttributeError
    # ------------------------------------------------------------------ #
    bad_product = Mock()
    # Ensure the mock does NOT have a ``sku`` attribute
    if hasattr(bad_product, "sku"):
        del bad_product.sku

    with pytest.raises(AttributeError):
        cart.add_item(bad_product, 1)