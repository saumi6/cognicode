"""
Auto-generated test cases for function: check_stock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:11:40
Source file: inventory_manager.py
Function signature: def check_stock(self, sku: str, qty: int) -> bool
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
from unittest.mock import Mock

# The InventoryManager class lives in the ``test_repo.inventory_manager`` module.
# Import it using the full absolute import path as required by the guidelines.
from test_repo.inventory_manager import InventoryManager


@pytest.mark.parametrize(
    "sku, stock, qty, expected",
    [
        ("SKU001", 10, 5, True),   # enough stock
        ("SKU002", 3, 5, False),   # not enough stock
        ("SKU003", 7, 7, True),    # exact match
        ("SKU004", 0, 1, False),   # zero stock, request >0
        ("SKU005", 100, 0, True),  # request zero items  always true if product exists
    ],
)
def test_check_stock_normal_cases(sku: str, stock: int, qty: int, expected: bool):
    """
    Normal behaviour of ``check_stock``:
    - Returns ``True`` when the product exists and its stock is greater than or equal to ``qty``.
    - Returns ``False`` when the product exists but stock is insufficient.
    """
    manager = InventoryManager()

    # Create a mock ``Product`` with the required attributes.
    product = Mock()
    product.sku = sku
    product.stock = stock
    product.name = f"Product {sku}"

    # Register the product in the manager.
    manager.add_product(product)

    # Call the method under test.
    result = manager.check_stock(sku, qty)

    assert result is expected


def test_check_stock_edge_cases():
    """
    Edgecase handling for ``check_stock``:
    - ``qty`` equal to zero should succeed when the product exists.
    - Negative ``qty`` should also succeed because any nonnegative stock is >= negative.
    - Missing SKU should return ``False`` regardless of ``qty``.
    """
    manager = InventoryManager()

    # Product with zero stock.
    zero_stock_product = Mock()
    zero_stock_product.sku = "ZERO"
    zero_stock_product.stock = 0
    zero_stock_product.name = "Zero Stock"
    manager.add_product(zero_stock_product)

    # Existing product, negative quantity request.
    neg_qty_product = Mock()
    neg_qty_product.sku = "NEG"
    neg_qty_product.stock = 5
    neg_qty_product.name = "Negative Qty"
    manager.add_product(neg_qty_product)

    # 1. Zero quantity request  should be True because product exists.
    assert manager.check_stock("ZERO", 0) is True

    # 2. Negative quantity request  should be True (stock >= negative number).
    assert manager.check_stock("NEG", -3) is True

    # 3. SKU not present  should be False for any qty.
    assert manager.check_stock("MISSING", 10) is False
    assert manager.check_stock("MISSING", 0) is False


def test_check_stock_error_cases():
    """
    ``check_stock`` should raise a ``TypeError`` when ``qty`` is not comparable
    with the product's integer stock (e.g., a string). Other malformed inputs
    that do not trigger a comparison simply return ``False``.
    """
    manager = InventoryManager()

    product = Mock()
    product.sku = "ERR"
    product.stock = 5
    product.name = "Error Product"
    manager.add_product(product)

    # ``qty`` as a string  the ``>=`` comparison will raise ``TypeError``.
    with pytest.raises(TypeError):
        manager.check_stock("ERR", "five")

    # ``sku`` as ``None``  ``dict.get`` will simply return ``None`` and the method
    # returns ``False`` (no exception expected).
    assert manager.check_stock(None, 1) is False

    # ``qty`` as ``None``  also raises ``TypeError`` because ``>=`` cannot compare.
    with pytest.raises(TypeError):
        manager.check_stock("ERR", None)
These three tests cover:

1. **Normal cases** with a variety of stock/quantity combinations using `@pytest.mark.parametrize`.
2. **Edge cases** such as zero and negative quantities and missing SKUs.
3. **Error cases** where inappropriate argument types cause a `TypeError`, verified with `pytest.raises`.

All tests instantiate `InventoryManager`, mock the required `Product` objects, and contain clear docstrings for readability.