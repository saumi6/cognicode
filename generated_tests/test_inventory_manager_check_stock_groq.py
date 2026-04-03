"""
Auto-generated test cases for function: check_stock
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 10:25:32
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
from unittest.mock import MagicMock

# Import the class under test  adjust the import path to match your project layout.
# For example, if the class lives in `inventory_manager.py`:
# from inventory_manager import InventoryManager
# Here we assume it is already importable as shown in the prompt.
from inventory_manager import InventoryManager


def _make_product(sku: str, stock: int) -> MagicMock:
    """
    Helper that creates a minimal ``Product`` mock with the attributes
    accessed by :meth:`InventoryManager.check_stock`.
    """
    product = MagicMock()
    product.sku = sku
    product.stock = stock
    # ``name`` is used only by ``add_product``  not needed here, but we set it
    # to keep the mock realistic.
    product.name = f"Product-{sku}"
    return product


@pytest.mark.parametrize(
    "sku, stock, qty, expected",
    [
        ("A001", 10, 5, True),   # sufficient stock
        ("B002", 3, 3, True),    # exact match
        ("C003", 0, 1, False),   # no stock
        ("D004", 5, 10, False),  # insufficient stock
    ],
)
def test_check_stock_normal_cases(sku, stock, qty, expected):
    """
    Normal operation: the SKU exists and the comparison ``stock >= qty`` is
    evaluated correctly.
    """
    manager = InventoryManager()
    manager.products[sku] = _make_product(sku, stock)

    result = manager.check_stock(sku, qty)
    assert result is expected


def test_check_stock_edge_cases():
    """
    Edgecase scenarios such as zero/negative quantities, missing SKUs and
    very large numbers.
    """
    manager = InventoryManager()

    # 1. Zero quantity  should always be True if the product exists.
    sku_zero = "Z001"
    manager.products[sku_zero] = _make_product(sku_zero, stock=0)
    assert manager.check_stock(sku_zero, 0) is True

    # 2. Negative quantity  ``stock >= qty`` is True for any nonnegative stock.
    sku_negative = "N001"
    manager.products[sku_negative] = _make_product(sku_negative, stock=0)
    assert manager.check_stock(sku_negative, -5) is True

    # 3. SKU not present  should return False regardless of qty.
    assert manager.check_stock("NON_EXISTENT", 1) is False

    # 4. Very large quantity compared to stock.
    sku_large = "L001"
    manager.products[sku_large] = _make_product(sku_large, stock=1_000_000)
    assert manager.check_stock(sku_large, 2_000_000) is False

    # 5. Stock exactly equals the requested quantity.
    sku_exact = "E001"
    manager.products[sku_exact] = _make_product(sku_exact, stock=42)
    assert manager.check_stock(sku_exact, 42) is True


def test_check_stock_error_cases():
    """
    ``check_stock`` performs a numeric comparison, so a nonnumeric ``qty``
    triggers a ``TypeError``.
    """
    manager = InventoryManager()
    sku = "ERR001"
    manager.products[sku] = _make_product(sku, stock=5)

    # ``qty`` as a string  comparison with int raises TypeError.
    with pytest.raises(TypeError):
        manager.check_stock(sku, "5")

    # ``qty`` as ``None``  also raises TypeError.
    with pytest.raises(TypeError):
        manager.check_stock(sku, None)

    # ``qty`` as a list  raises TypeError as well.
    with pytest.raises(TypeError):
        manager.check_stock(sku, [1, 2, 3])