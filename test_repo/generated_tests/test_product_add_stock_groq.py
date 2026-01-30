"""
Auto-generated test cases for function: add_stock
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 23:27:14
Source file: product.py
Function signature: def add_stock(self, qty: int)
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
import product  # the module that contains the Product class


@pytest.mark.parametrize(
    "qty, expected_stock",
    [
        (1, 1),
        (5, 5),
        (10, 10),
    ],
)
def test_add_stock_normal_cases(qty, expected_stock, monkeypatch):
    """
    Test that add_stock correctly increments the stock for typical positive
    integer quantities.
    """
    # Patch the helper functions so that Product can be instantiated
    monkeypatch.setattr("product.round_currency", lambda x: x)
    monkeypatch.setattr(
        "product.generate_sku",
        lambda category, name: f"{category[:3].upper()}-{name[:3].upper()}",
    )

    prod = product.Product(name="Widget", price=9.99, category="Tools")
    prod.add_stock(qty)
    assert prod.stock == expected_stock


@pytest.mark.parametrize(
    "qty, expected_stock",
    [
        (0, 0),                # adding zero should leave stock unchanged
        (1_000_000, 1_000_000),  # large positive number
        (-5, -5),              # negative quantity reduces stock
        (-1_000_000, -1_000_000),  # large negative number
    ],
)
def test_add_stock_edge_cases(qty, expected_stock, monkeypatch):
    """
    Test boundary and edge cases for add_stock, including zero, large numbers,
    and negative quantities.
    """
    monkeypatch.setattr("product.round_currency", lambda x: x)
    monkeypatch.setattr(
        "product.generate_sku",
        lambda category, name: f"{category[:3].upper()}-{name[:3].upper()}",
    )

    prod = product.Product(name="Widget", price=9.99, category="Tools")
    prod.add_stock(qty)
    assert prod.stock == expected_stock


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        "10",
        [5],
        {"qty": 5},
    ],
)
def test_add_stock_error_cases(invalid_input, monkeypatch):
    """
    Test that add_stock raises a TypeError when called with nonnumeric
    arguments that cannot be added to an integer.
    """
    monkeypatch.setattr("product.round_currency", lambda x: x)
    monkeypatch.setattr(
        "product.generate_sku",
        lambda category, name: f"{category[:3].upper()}-{name[:3].upper()}",
    )

    prod = product.Product(name="Widget", price=9.99, category="Tools")
    with pytest.raises(TypeError):
        prod.add_stock(invalid_input)