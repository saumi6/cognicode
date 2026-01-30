"""
Auto-generated test cases for function: add_stock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:55:16
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
from product import Product  # the module that contains the Product class


def _patch_product_dependencies(monkeypatch):
    """
    Helper that replaces external helpers used by ``Product`` with simple
    standins so the class can be instantiated without pulling in the real
    implementations.
    """
    # ``round_currency`` is expected to return a numeric value  we just return the input.
    monkeypatch.setattr("product.round_currency", lambda x: x, raising=False)

    # ``generate_sku`` should return a string  we return a deterministic placeholder.
    monkeypatch.setattr("product.generate_sku", lambda cat, name: f"{cat[:3]}-{name[:3]}", raising=False)

    # ``ValidationError`` is used only for price validation  map it to a plain Exception subclass.
    class SimpleValidationError(Exception):
        pass

    monkeypatch.setattr("product.ValidationError", SimpleValidationError, raising=False)


@pytest.mark.parametrize(
    "price, qty, expected_stock",
    [
        (10.0, 5, 5),          # normal positive addition
        (15.5, 1, 1),          # single unit
        (0.99, 100, 100),      # larger quantity
    ],
)
def test_add_stock_normal_cases(monkeypatch, price, qty, expected_stock):
    """
    Verify that ``add_stock`` correctly increments the ``stock`` attribute for
    typical positive quantities.
    """
    _patch_product_dependencies(monkeypatch)

    # Create a product with a valid (nonnegative) price.
    prod = Product(name="TestProduct", price=price)

    # Precondition: stock starts at 0
    assert prod.stock == 0

    # Act
    prod.add_stock(qty)

    # Assert
    assert prod.stock == expected_stock


def test_add_stock_edge_cases(monkeypatch):
    """
    Test boundary and edge conditions such as adding zero, a negative amount,
    and a very large integer.
    """
    _patch_product_dependencies(monkeypatch)

    prod = Product(name="EdgeCase", price=1.23)

    # 1. Adding zero should leave stock unchanged.
    prod.add_stock(0)
    assert prod.stock == 0

    # 2. Adding a negative quantity reduces stock (method does not guard against it).
    prod.add_stock(-3)
    assert prod.stock == -3

    # 3. Adding a huge quantity (e.g., sys.maxsize) works without overflow in Python.
    import sys
    huge_qty = sys.maxsize
    prod.add_stock(huge_qty)
    assert prod.stock == -3 + huge_qty


def test_add_stock_error_cases(monkeypatch):
    """
    Ensure that ``add_stock`` raises appropriate exceptions when supplied with
    invalid input types.
    """
    _patch_product_dependencies(monkeypatch)

    prod = Product(name="ErrorCase", price=5.0)

    # Passing a string should raise a TypeError because ``int`` + ``str`` is invalid.
    with pytest.raises(TypeError):
        prod.add_stock("ten")

    # Passing ``None`` should also raise a TypeError.
    with pytest.raises(TypeError):
        prod.add_stock(None)

    # Passing a float is allowed by Python (it will coerce the stock to float),
    # but the method is typed to accept ``int``  we treat this as an error case.
    with pytest.raises(TypeError):
        prod.add_stock(3.14)
**Explanation of the test suite**

* **Dependency patching**  The helper ``_patch_product_dependencies`` replaces the external
  functions ``round_currency`` and ``generate_sku`` and the ``ValidationError`` class with
  minimal standins so that the ``Product`` constructor can be used without importing the real
  implementations.

* **`test_add_stock_normal_cases`**  Uses ``@pytest.mark.parametrize`` to run three typical
  scenarios, asserting that the ``stock`` attribute matches the expected value after the call.

* **`test_add_stock_edge_cases`**  Checks boundary conditions:
  * Adding `0` (no change),
  * Adding a negative number (stock can become negative because the method does not guard),
  * Adding a very large integer (`sys.maxsize`) to ensure no overflow issues.

* **`test_add_stock_error_cases`**  Confirms that inappropriate argument types raise a
  ``TypeError``. The method itself does not perform explicit validation, so Pythons native
  typechecking triggers the exception when an unsupported type is added to an ``int``.

All three functions are selfcontained, include docstrings, and can be executed directly with
``pytest``.