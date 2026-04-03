"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:41:56
Source file: product.py
Function signature: def __init__(self, name: str, price: float, category: str = 'General')
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
from unittest.mock import MagicMock

# ----------------------------------------------------------------------
# NOTE:
# The production code lives in a file called ``product.py`` (module name ``product``).
# The tests import the ``Product`` class from that module and monkeypatch the
# helper functions ``round_currency`` and ``generate_sku`` as well as the
# ``ValidationError`` exception that the class uses.
# ----------------------------------------------------------------------


@pytest.fixture(autouse=True)
def patch_helpers(monkeypatch):
    """
    Patch external helpers used by ``Product.__init__`` so the tests are
    deterministic and do not depend on the real implementations.
    """
    # a very simple rounding implementation  just return the value rounded to 2 decimals
    monkeypatch.setattr(
        "product.round_currency", lambda x: round(x, 2), raising=True
    )
    # deterministic SKU generation  concatenate category and name with a dash
    monkeypatch.setattr(
        "product.generate_sku", lambda cat, name: f"{cat[:3].upper()}-{name[:3].upper()}", raising=True
    )
    # a simple ValidationError that behaves like a normal Exception
    class _ValidationError(Exception):
        pass

    monkeypatch.setattr("product.ValidationError", _ValidationError, raising=True)
    return _ValidationError


@pytest.mark.parametrize(
    "name, price, category, expected_price, expected_sku",
    [
        ("Apple", 1.234, "Fruit", 1.23, "FRU-APP"),
        ("Banana", 0.99, "Fruit", 0.99, "FRU-BAN"),
        ("Notebook", 12.5, "Stationery", 12.5, "STA-NOT"),
        ("Pen", 2.0, None, 2.0, "GEN-PEN"),  # ``category`` defaults to "General"
    ],
)
def test___init___normal_cases(name, price, category, expected_price, expected_sku):
    """
    Normal initialisation scenarios:
    * typical name / price / category combinations
    * default category handling when ``category`` is omitted / ``None``
    """
    # Import inside the test so the monkeypatch fixture is already active
    from product import Product

    # ``category`` may be ``None`` to trigger the default argument inside the class
    if category is None:
        prod = Product(name, price)          # default category = "General"
    else:
        prod = Product(name, price, category)

    assert prod.name == name
    assert prod.price == pytest.approx(expected_price)
    # The class stores the *actual* category value (defaulted to "General" when omitted)
    expected_category = category if category is not None else "General"
    assert prod.category == expected_category
    assert prod.sku == expected_sku
    # Stock should always start at zero
    assert prod.stock == 0


def test___init___edge_cases():
    """
    Edgecase initialisation:
    * price exactly zero
    * empty strings for ``name`` and ``category``
    * very large price value
    * price with many decimal places (rounding check)
    """
    from product import Product

    # 1. Zero price  should be accepted and rounded to 0.0
    p_zero = Product(name="Freebie", price=0.0)
    assert p_zero.price == pytest.approx(0.0)
    assert p_zero.category == "General"
    assert p_zero.sku == "GEN-FRE"

    # 2. Empty name and empty category  still valid, just stored asis
    p_empty = Product(name="", price=10.0, category="")
    assert p_empty.name == ""
    assert p_empty.category == ""
    # SKU generation uses the first three characters (which may be empty)
    assert p_empty.sku == "-"

    # 3. Very large price  ensure it is rounded correctly
    huge_price = 9_999_999.98765
    p_huge = Product(name="Luxury", price=huge_price, category="Expensive")
    assert p_huge.price == pytest.approx(round(huge_price, 2))
    assert p_huge.sku == "EXP-LUX"

    # 4. Price with many decimal places  rounding to two decimals
    p_precise = Product(name="Precise", price=1.9999, category="Math")
    assert p_precise.price == pytest.approx(2.00)
    assert p_precise.sku == "MAT-PRE"


def test___init___error_cases():
    """
    Error handling:
    * negative price should raise the patched ``ValidationError``.
    """
    from product import Product, ValidationError

    # Negative price  expect ValidationError
    with pytest.raises(ValidationError):
        Product(name="BadProduct", price=-5.0)

    # Also test that a negative price with an explicit category still raises
    with pytest.raises(ValidationError):
        Product(name="BadProduct", price=-0.01, category="Invalid")