"""
Auto-generated test cases for function: update_price
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:55:06
Source file: product.py
Function signature: def update_price(self, new_price: float)
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

# NOTE:
# The tests assume the implementation lives in a module named ``product`` that is
# importable as ``test_repo.product`` (i.e. the repository root is ``test_repo``).
# Adjust the import path if your project uses a different package name.

from test_repo.product import Product, ValidationError


@pytest.fixture(autouse=True)
def patch_helpers(monkeypatch):
    """
    Patch external helper functions used by ``Product`` so that the tests are
    deterministic and do not depend on their real implementations.
    """
    # ``round_currency``  for the purpose of these tests we simply round to
    # two decimal places (the typical behaviour for a currency helper).
    monkeypatch.setattr(
        "test_repo.product.round_currency",
        lambda x: round(x, 2),
        raising=True,
    )
    # ``generate_sku``  return a constant dummy SKU.
    monkeypatch.setattr(
        "test_repo.product.generate_sku",
        lambda category, name: f"SKU-{category[:3].upper()}-{name[:3].upper()}",
        raising=True,
    )
    # No return value; the fixture only ensures the patches are active for every test.
    yield


@pytest.mark.parametrize(
    "initial_price, new_price, expected_price",
    [
        (10.0, 15.99, 15.99),          # simple increase
        (20.555, 30.123, 30.12),       # rounding down
        (0.99, 0.995, 1.0),            # rounding up
        (1000.1234, 2000.5678, 2000.57)  # large numbers with rounding
    ],
)
def test_update_price_normal_cases(initial_price, new_price, expected_price):
    """
    Verify that ``update_price`` correctly updates the ``price`` attribute for
    typical, wellbehaved inputs.
    """
    # Arrange  create a product with a known initial price.
    prod = Product(name="TestProduct", price=initial_price, category="General")

    # Act  update the price.
    prod.update_price(new_price)

    # Assert  the stored price should be the rounded value.
    assert prod.price == pytest.approx(expected_price)


def test_update_price_edge_cases():
    """
    Test boundary conditions such as zero price, very small fractions,
    and repeated updates.
    """
    # Edge case 1  setting price to zero.
    prod_zero = Product(name="ZeroPrice", price=5.0)
    prod_zero.update_price(0.0)
    assert prod_zero.price == pytest.approx(0.0)

    # Edge case 2  a price that is smaller than the rounding precision.
    prod_small = Product(name="SmallPrice", price=1.0)
    prod_small.update_price(0.0001)          # rounds to 0.00
    assert prod_small.price == pytest.approx(0.0)

    # Edge case 3  extremely large price.
    huge_price = 1e12 + 0.555
    prod_huge = Product(name="HugePrice", price=1e12)
    prod_huge.update_price(huge_price)
    assert prod_huge.price == pytest.approx(round(huge_price, 2))

    # Edge case 4  multiple successive updates.
    prod_multi = Product(name="MultiUpdate", price=10.0)
    updates = [12.345, 12.345, 9.999, 9.999]
    for upd in updates:
        prod_multi.update_price(upd)
    # The final price should be the rounded value of the last update.
    assert prod_multi.price == pytest.approx(round(updates[-1], 2))


def test_update_price_error_cases():
    """
    Ensure that invalid inputs raise the appropriate ``ValidationError``.
    """
    prod = Product(name="ErrorCase", price=10.0)

    # Negative price should raise ValidationError.
    with pytest.raises(ValidationError):
        prod.update_price(-5.0)

    # ``new_price`` that is not a number (e.g., ``None``) should also raise.
    # The implementation will attempt the ``< 0`` comparison and raise a
    # ``TypeError``; we treat any exception as a failure of validation.
    with pytest.raises(Exception):
        prod.update_price(None)

    # Very large negative number  still a ValidationError.
    with pytest.raises(ValidationError):
        prod.update_price(-1e9)