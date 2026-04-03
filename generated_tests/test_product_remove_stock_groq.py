"""
Auto-generated test cases for function: remove_stock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:42:40
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
from product import Product


def _patch_dependencies(monkeypatch):
    """
    Helper that installs harmless standins for the external helpers used by
    ``Product`` (``round_currency``, ``generate_sku`` and ``ValidationError``).
    instructions.
    """
    # ``round_currency`` is expected to return a monetary value  for the tests a
    # simple identity function is sufficient.
    monkeypatch.setattr(
        "product.round_currency",
        lambda x: x,
        raising=False,
    )
    # ``generate_sku`` only needs to return *something* that can be stored on the
    # instance; a deterministic string keeps the behaviour predictable.
    monkeypatch.setattr(
        "product.generate_sku",
        lambda category, name: f"{category[:2].upper()}-{name[:2].upper()}",
        raising=False,
    )
    # ``ValidationError`` is only used for a negativeprice guard; mapping it to
    # the builtin ``Exception`` type is enough for the test suite.
    monkeypatch.setattr(
        "product.ValidationError",
        Exception,
        raising=False,
    )


@pytest.mark.parametrize(
    "initial_stock, remove_qty, expected_stock",
    [
        (10, 3, 7),      # typical case
        (5, 5, 0),       # remove exactly the whole stock
        (100, 1, 99),    # large stock, small removal
        (1, 0, 1),       # removing zero does not change stock
        (50, 25, 25),    # half the stock removed
    ],
)
def test_remove_stock_normal_cases(monkeypatch, initial_stock, remove_qty, expected_stock):
    """
    Normal operation: after adding a known amount of stock, removing a valid
    quantity should decrease ``product.stock`` to the expected value.
    """
    _patch_dependencies(monkeypatch)

    # Arrange  create a product with a positive price (price is irrelevant for
    # stock handling) and give it the required initial stock.
    prod = Product(name="Widget", price=9.99, category="Tools")
    prod.add_stock(initial_stock)

    # Act  remove the requested quantity.
    prod.remove_stock(remove_qty)

    # Assert  the remaining stock matches the expectation.
    assert prod.stock == expected_stock


def test_remove_stock_edge_cases(monkeypatch):
    """
    Edgecase scenarios such as removing zero items, removing the entire stock,
    and handling very large integer values.
    """
    _patch_dependencies(monkeypatch)

    # 1. Removing zero from a nonzero stock should leave the stock unchanged.
    prod_zero = Product(name="Gadget", price=1.23)
    prod_zero.add_stock(42)
    prod_zero.remove_stock(0)
    assert prod_zero.stock == 42

    # 2. Removing the exact amount of stock should bring the stock down to zero.
    prod_exact = Product(name="Gizmo", price=2.34)
    prod_exact.add_stock(7)
    prod_exact.remove_stock(7)
    assert prod_exact.stock == 0

    # 3. Very large stock values should be handled without overflow or loss.
    huge_number = 10**12  # one trillion
    prod_huge = Product(name="MegaWidget", price=99.99)
    prod_huge.add_stock(huge_number)
    prod_huge.remove_stock(1)
    assert prod_huge.stock == huge_number - 1
    # Removing the rest should end at zero.
    prod_huge.remove_stock(huge_number - 1)
    assert prod_huge.stock == 0


def test_remove_stock_error_cases(monkeypatch):
    """
    Verify that the method raises the appropriate exceptions when asked to
    remove more stock than is available or when supplied with an invalid type.
    """
    _patch_dependencies(monkeypatch)

    # Setup a product with a known stock level.
    prod = Product(name="Faulty", price=5.00)
    prod.add_stock(3)

    # 1. Attempting to remove more than the available stock must raise ``ValueError``.
    with pytest.raises(ValueError) as excinfo:
        prod.remove_stock(5)
    assert "Not enough stock" in str(excinfo.value)

    # 2. Supplying a noninteger (e.g., a string) should raise ``TypeError`` because
    # the comparison ``self.stock < qty`` cannot be performed.
    with pytest.raises(TypeError):
        prod.remove_stock("two")