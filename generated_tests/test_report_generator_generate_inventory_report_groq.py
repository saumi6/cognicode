"""
Auto-generated test cases for function: generate_inventory_report
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 20:35:00
Source file: report_generator.py
Function signature: def generate_inventory_report(inventory: InventoryManager) -> str
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.report_generator import generate_inventory_report

import pytest
from test_repo.report_generator import generate_inventory_report


class DummyInventoryManager:
    """
    Very small standin for the real ``InventoryManager`` used by
    ``generate_inventory_report``.  The real manager is expected to expose a
    ``get_items`` method that returns an iterable of dictionaries with the keys
    ``name``, ``quantity`` and ``price`` (price per unit).
    """
    def __init__(self, items):
        self._items = items

    def get_items(self):
        return self._items


@pytest.mark.parametrize(
    "items, expected",
    [
        # two normal items
        (
            [
                {"name": "Widget", "quantity": 3, "price": 9.99},
                {"name": "Gadget", "quantity": 5, "price": 4.50},
            ],
            (
                "Item: Widget, Qty: 3, Total: $29.97\n"
                "Item: Gadget, Qty: 5, Total: $22.50\n"
                "Total inventory value: $52.47"
            ),
        ),
        # single item
        (
            [
                {"name": "Sprocket", "quantity": 1, "price": 199.95},
            ],
            (
                "Item: Sprocket, Qty: 1, Total: $199.95\n"
                "Total inventory value: $199.95"
            ),
        ),
        # three items with mixed quantities
        (
            [
                {"name": "Bolt", "quantity": 10, "price": 0.15},
                {"name": "Nut", "quantity": 20, "price": 0.10},
                {"name": "Washer", "quantity": 30, "price": 0.05},
            ],
            (
                "Item: Bolt, Qty: 10, Total: $1.50\n"
                "Item: Nut, Qty: 20, Total: $2.00\n"
                "Item: Washer, Qty: 30, Total: $1.50\n"
                "Total inventory value: $5.00"
            ),
        ),
    ],
)
def test_generate_inventory_report_normal_cases(items, expected):
    """
    Normal operation  the report should list each item with its quantity,
    line total and a final grandtotal.
    """
    inventory = DummyInventoryManager(items)
    result = generate_inventory_report(inventory)
    assert result == expected


def test_generate_inventory_report_edge_cases():
    """
    Edgecase handling:
      * an empty inventory should produce a friendly message,
      * very large quantities/prices should be formatted correctly,
      * quantities of zero should be omitted from the total but still listed.
    """
    # 1 Empty inventory
    empty_inventory = DummyInventoryManager([])
    empty_result = generate_inventory_report(empty_inventory)
    assert empty_result == "No items in inventory."

    # 2 Very large numbers (checking formatting, not overflow)
    large_items = [
        {"name": "SuperComputer", "quantity": 1_000_000, "price": 9999.99},
    ]
    large_inventory = DummyInventoryManager(large_items)
    large_result = generate_inventory_report(large_inventory)
    # Expected total = 1_000_000 * 9_999.99 = 9_999_990_000.00
    assert large_result == (
        "Item: SuperComputer, Qty: 1000000, Total: $9999990000.00\n"
        "Total inventory value: $9999990000.00"
    )

    # 3 Zeroquantity item  should appear with $0.00 line total
    zero_qty_items = [
        {"name": "ObsoletePart", "quantity": 0, "price": 123.45},
        {"name": "ActivePart", "quantity": 2, "price": 50.00},
    ]
    zero_qty_inventory = DummyInventoryManager(zero_qty_items)
    zero_qty_result = generate_inventory_report(zero_qty_inventory)
    assert zero_qty_result == (
        "Item: ObsoletePart, Qty: 0, Total: $0.00\n"
        "Item: ActivePart, Qty: 2, Total: $100.00\n"
        "Total inventory value: $100.00"
    )


def test_generate_inventory_report_error_cases():
    """
    Verify that inappropriate inputs raise the expected exceptions.
    """
    # Passing ``None`` instead of an InventoryManager instance
    with pytest.raises(TypeError):
        generate_inventory_report(None)

    # Passing an object that does not implement ``get_items``
    class BadObj:
        pass

    with pytest.raises(AttributeError):
        generate_inventory_report(BadObj())

    # Supplying malformed item dictionaries (missing keys)
    malformed_items = [
        {"name": "Widget", "quantity": 5},                     # missing price
        {"quantity": 2, "price": 10.0},                       # missing name
    ]
    malformed_inventory = DummyInventoryManager(malformed_items)

    with pytest.raises(KeyError):
        generate_inventory_report(malformed_inventory)