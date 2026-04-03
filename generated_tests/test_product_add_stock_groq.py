"""
Auto-generated test cases for function: add_stock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:42:23
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
from unittest.mock import Mock

# The Product class is assumed to be importable from the module where it is defined.
# Adjust the import path if the module name differs.
from product import Product, ValidationError  # type: ignore


@pytest.fixture(autouse=True)
def _patch_dependencies(monkeypatch):
    """
    Patch external helpers used by ``Product.__init__`` so that the class can be
    instantiated without needing the real implementations.
    """
    # ``round_currency`` is expected to round a float to two decimal places.
    # For the purpose of these tests we simply return the value unchanged.
    monkeypatch.setattr(
        "product.round_currency",  # full absolute import path
        lambda x: x,
        raising=False,
    )
    # ``generate_sku`` creates a stockkeepingunit string.
    # We replace it with a deterministic stub.
    monkeypatch.setattr(
        "product.generate_sku",
        lambda category, name: f"{category[:2].upper()}-{name[:2].upper()}",
        raising=False,
    )
    # ``ValidationError`` is used only in ``__init__`` and ``update_price``.
    # If the real class is not available we provide a simple subclass of ``Exception``.
    if "product.ValidationError" not in globals():
        monkeypatch.setattr(
            "product.ValidationError",
            type("ValidationError", (Exception,), {}),
            raising=False,
        )


def _make_product(name: str = "TestProduct", price: float = 10.0, category: str = "General") -> Product:
    """
    Helper that creates a ``Product`` instance with the patched dependencies.
    """
    return Product(name=name, price=price, category=category)


@pytest.mark.parametrize(
    "initial_stock, qty_to_add, expected_stock",
    [
        (0, 5, 5),
        (0, 1, 1),
        (10, 15, 25),
        (3, 0, 3),   # adding zero should leave stock unchanged
        (100, 200, 300),
    ],
)
def test_add_stock_normal_cases(initial_stock, qty_to_add, expected_stock):
    """
    Verify that ``add_stock`` correctly increments the ``stock`` attribute for
    typical positive quantities.
    """
    product = _make_product()
    # Set up the initial stock manually to test cumulative behaviour.
    product.stock = initial_stock

    product.add_stock(qty_to_add)

    assert product.stock == expected_stock


def test_add_stock_edge_cases():
    """
    Test boundary and edge conditions such as adding zero, a negative quantity,
    and a very large integer.
    """
    product = _make_product()

    # Edge case 1  adding zero should keep stock at 0.
    product.add_stock(0)
    assert product.stock == 0

    # Edge case 2  adding a negative number decreases stock.
    product.add_stock(-5)
    assert product.stock == -5

    # Edge case 3  adding a very large integer (close to sys.maxsize).
    large_qty = 10**12
    product.add_stock(large_qty)
    assert product.stock == -5 + large_qty


@pytest.mark.parametrize(
    "invalid_qty",
    [
        "10",          # string
        3.14,          # float
        None,          # NoneType
        [1, 2, 3],     # list
        {"qty": 5},    # dict
    ],
)
def test_add_stock_error_cases(invalid_qty):
    """
    ``add_stock`` expects an ``int``. Supplying a value of an incompatible type
    should raise a ``TypeError`` because the ``+=`` operation cannot be performed.
    """
    product = _make_product()

    with pytest.raises(TypeError):
        product.add_stock(invalid_qty)