"""
Auto-generated test cases for function: remove_stock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:55:26
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
from unittest.mock import Mock

# The module that contains the Product class is assumed to be named ``product``.
# Adjust the import path if the actual module name differs.
from product import Product, ValidationError


@pytest.fixture(autouse=True)
def _mock_dependencies(monkeypatch):
    """
    Mock the external helpers used by ``Product.__init__`` so that the class can be
    instantiated without pulling in the real implementations.
    """
    # ``round_currency`` is expected to return a numeric value  we simply return the
    # value that was passed in.
    monkeypatch.setattr(
        "product.round_currency", lambda x: x, raising=False
    )
    # ``generate_sku`` should return a string  we return a deterministic placeholder.
    monkeypatch.setattr(
        "product.generate_sku", lambda cat, name: f"SKU-{cat[:3]}-{name[:3]}", raising=False
    )
    # ``ValidationError`` is already imported from the module, no need to mock it.


def _make_product(initial_stock: int = 0) -> Product:
    """
    Helper that creates a ``Product`` instance with a given initial stock level.
    """
    p = Product(name="TestProduct", price=10.0, category="TestCat")
    p.add_stock(initial_stock)
    return p


@pytest.mark.parametrize(
    "initial_stock, remove_qty, expected_stock",
    [
        (10, 1, 9),          # simple decrement
        (5, 5, 0),           # remove exactly the whole stock
        (100, 20, 80),       # larger numbers
        (3, 0, 3),           # removing zero does not change stock
    ],
)
def test_remove_stock_normal_cases(initial_stock, remove_qty, expected_stock):
    """
    Normal usage: removing a quantity that is less than or equal to the current stock.
    """
    product = _make_product(initial_stock)
    product.remove_stock(remove_qty)
    assert product.stock == expected_stock


def test_remove_stock_edge_cases():
    """
    Edgecase scenarios such as removing the entire stock or handling very large numbers.
    """
    # Edge case 1  remove all stock in one go
    product_all = _make_product(initial_stock=1_000_000)
    product_all.remove_stock(1_000_000)
    assert product_all.stock == 0

    # Edge case 2  remove zero items (should be a noop)
    product_zero = _make_product(initial_stock=42)
    product_zero.remove_stock(0)
    assert product_zero.stock == 42

    # Edge case 3  remove a quantity that leaves exactly one item left
    product_one_left = _make_product(initial_stock=2)
    product_one_left.remove_stock(1)
    assert product_one_left.stock == 1


def test_remove_stock_error_cases():
    """
    Verify that the method raises the appropriate exceptions for invalid operations.
    """
    # Case 1  trying to remove more than is available raises ``ValueError``
    product = _make_product(initial_stock=3)
    with pytest.raises(ValueError) as excinfo:
        product.remove_stock(5)
    assert "Not enough stock" in str(excinfo.value)

    # Case 2  passing a noninteger (e.g., a string) triggers a ``TypeError``
    product = _make_product(initial_stock=5)
    with pytest.raises(TypeError):
        product.remove_stock("two")

    # Case 3  passing a negative quantity does not raise, but it *adds* stock.
    # This behaviour is documented by the implementation (no guard against negatives).
    product = _make_product(initial_stock=10)
    product.remove_stock(-3)  # stock should increase by 3
    assert product.stock == 13