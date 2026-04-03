"""
Auto-generated test cases for function: restock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 10:25:40
Source file: inventory_manager.py
Function signature: def restock(self, sku: str, qty: int)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.inventory_manager import InventoryManager

import pytest
from unittest.mock import MagicMock

# The class under test  adjust the import path to match your project layout.
# For example, if the class lives in `myapp/inventory.py` you would write:
# from myapp.inventory import InventoryManager
from inventory_manager import InventoryManager  # <-- replace with the correct module name


def _make_mock_product(sku: str, initial_stock: int = 0):
    """
    Helper that creates a simple mock ``Product`` object with the attributes
    required by ``InventoryManager`` (``sku``, ``stock`` and ``add_stock``).
    """
    product = MagicMock()
    product.sku = sku
    product.stock = initial_stock

    def _add_stock(qty):
        # emulate the real behaviour  increase the internal ``stock`` counter
        product.stock += qty

    product.add_stock.side_effect = _add_stock
    return product


@pytest.mark.parametrize(
    "initial_stock, restock_qty, expected_stock",
    [
        (0, 5, 5),          # simple addition
        (10, 15, 25),       # adding to existing stock
        (3, 0, 3),          # restocking zero does not change stock
        (100, 1, 101),      # minimal positive increment
    ],
)
def test_restock_normal_cases(initial_stock, restock_qty, expected_stock):
    """
    Normal usage: the product exists and ``qty`` is a nonnegative integer.
    After calling ``restock`` the product's ``stock`` attribute should reflect
    the added quantity.
    """
    manager = InventoryManager()
    sku = "TESTSKU"

    # Insert a mock product into the manager's internal dict
    manager.products[sku] = _make_mock_product(sku, initial_stock)

    # Perform the operation under test
    manager.restock(sku, restock_qty)

    # Verify that the stock was updated correctly
    assert manager.products[sku].stock == expected_stock
    # Ensure that ``add_stock`` was called exactly once with the right argument
    manager.products[sku].add_stock.assert_called_once_with(restock_qty)


def test_restock_edge_cases():
    """
    Edgecase scenarios:
    * Restocking a SKU that does **not** exist  the method should silently do nothing.
    * Restocking with a negative quantity  the mock ``add_stock`` will raise
      ``ValueError`` (simulating a real implementation that forbids negative stock).
    """
    manager = InventoryManager()

    # 1 Nonexistent SKU  nothing should happen and no exception is raised
    missing_sku = "MISSING"
    # No product is added to ``manager.products`` for this SKU
    manager.restock(missing_sku, 10)  # should be a noop
    assert missing_sku not in manager.products

    # 2 Negative quantity  we configure the mock to raise on negative input
    sku = "NEGSKU"
    product = MagicMock()
    product.sku = sku
    product.stock = 20

    def _add_stock(qty):
        if qty < 0:
            raise ValueError("Quantity cannot be negative")
        product.stock += qty

    product.add_stock.side_effect = _add_stock
    manager.products[sku] = product

    with pytest.raises(ValueError):
        manager.restock(sku, -5)

    # Stock must remain unchanged after the failed restock attempt
    assert product.stock == 20
    # ``add_stock`` should have been called once (the call that raised)
    product.add_stock.assert_called_once_with(-5)


def test_restock_error_cases():
    """
    so we rely on the underlying ``Product.add_stock`` to raise when it receives
    inappropriate data. Here we simulate that behaviour with a mock.
    """
    manager = InventoryManager()
    sku = "ERRSKU"
    product = MagicMock()
    product.sku = sku
    product.stock = 0

    # Simulate a typechecking error inside ``add_stock``
    def _add_stock(qty):
        if not isinstance(qty, int):
            raise TypeError("Quantity must be an integer")
        product.stock += qty

    product.add_stock.side_effect = _add_stock
    manager.products[sku] = product

    # Passing a string instead of an int should propagate a TypeError
    with pytest.raises(TypeError):
        manager.restock(sku, "ten")

    # Ensure that the stock has not been modified
    assert product.stock == 0
    product.add_stock.assert_called_once_with("ten")