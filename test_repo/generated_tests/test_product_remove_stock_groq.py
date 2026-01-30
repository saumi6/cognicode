"""
Auto-generated test cases for function: remove_stock
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:27:23
Source file: product.py
Function signature: def remove_stock(self, qty: int)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.product import Product

import pytest

# Import the Product class from the module where it is defined.
# The module name is assumed to be `product`. Adjust the import if the
# actual module name differs.
from product import Product


@pytest.mark.parametrize(
    "initial_stock, remove_qty, expected_stock",
    [
        (10, 5, 5),   # normal removal
        (5, 5, 0),    # remove all stock
        (20, 1, 19),  # remove a single unit
        (0, 0, 0),    # nothing to remove
    ],
)
def test_remove_stock_normal_cases(monkeypatch, initial_stock, remove_qty, expected_stock):
    """
    Test normal removal scenarios where the requested quantity is less than or equal to the
    available stock. The method should correctly decrement the stock.
    """
    # Patch external dependencies to avoid sideeffects during the test.
    monkeypatch.setattr("product.round_currency", lambda x: x)
    monkeypatch.setattr("product.generate_sku", lambda category, name: "SKU")

    # Create a product instance and set its stock.
    prod = Product(name="Widget", price=9.99, category="Tools")
    prod.add_stock(initial_stock)

    # Perform the removal.
    prod.remove_stock(remove_qty)

    # Verify the resulting stock level.
    assert prod.stock == expected_stock


@pytest.mark.parametrize(
    "initial_stock, remove_qty, expected_stock",
    [
        (5, 0, 5),    # removing zero should leave stock unchanged
        (5, 5, 0),    # removing all stock
        (1, 1, 0),    # removing the last unit
        (10, 10, 0),  # removing entire stock
        (5, -1, 6),   # negative quantity increases stock (edge behaviour)
    ],
)
def test_remove_stock_edge_cases(monkeypatch, initial_stock, remove_qty, expected_stock):
    """
    Test edge cases such as removing zero, removing the entire stock, and
    providing a negative quantity. The method should handle these without
    raising unexpected errors.
    """
    monkeypatch.setattr("product.round_currency", lambda x: x)
    monkeypatch.setattr("product.generate_sku", lambda category, name: "SKU")

    prod = Product(name="Gadget", price=19.99, category="Electronics")
    prod.add_stock(initial_stock)

    prod.remove_stock(remove_qty)

    assert prod.stock == expected_stock


def test_remove_stock_error_cases(monkeypatch):
    """
    Test error scenarios where the removal operation should raise an exception.
    These include attempting to remove more stock than available and passing
    invalid argument types.
    """
    monkeypatch.setattr("product.round_currency", lambda x: x)
    monkeypatch.setattr("product.generate_sku", lambda category, name: "SKU")

    prod = Product(name="Thingamajig", price=4.99, category="Misc")
    prod.add_stock(3)

    # Removing more than available should raise ValueError.
    with pytest.raises(ValueError):
        prod.remove_stock(5)

    # Passing a noninteger type (e.g., string) should raise TypeError
    # because the comparison `self.stock < qty` will fail.
    with pytest.raises(TypeError):
        prod.remove_stock("two")

    # Passing None should also raise TypeError.
    with pytest.raises(TypeError):
        prod.remove_stock(None)

    # Passing a float that is greater than the stock should raise ValueError.
    with pytest.raises(ValueError):
        prod.remove_stock(3.5)