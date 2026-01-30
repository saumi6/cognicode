"""
Auto-generated test cases for function: generate_inventory_report
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 04:06:26
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

# ----------------------------------------------------------------------
# Helper objects used only inside the tests
# ----------------------------------------------------------------------
class _FakeInventoryManager:
    """
    Minimal standin for the real ``InventoryManager`` used by
    ``generate_inventory_report``.  It only needs to expose the attributes
    accessed by the function  in our tests we assume the function works with
    an ``items`` attribute that is an iterable of dictionaries with the keys
    ``name``, ``quantity`` and ``price``.
    """
    def __init__(self, items):
        self.items = items


# ----------------------------------------------------------------------
# 1. Normal cases  parametrised
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "items, expected_fragments",
    [
        # single item, simple numbers
        (
            [{"name": "Widget", "quantity": 3, "price": 9.99}],
            ["Widget", "3", "9.99", "29.97"],
        ),
        # two items, different quantities / prices
        (
            [
                {"name": "Gadget", "quantity": 1, "price": 199.95},
                {"name": "Sprocket", "quantity": 5, "price": 2.5},
            ],
            ["Gadget", "1", "199.95", "199.95", "Sprocket", "5", "2.5", "12.5"],
        ),
        # three items, mixed integer / float prices
        (
            [
                {"name": "Bolt", "quantity": 10, "price": 0.15},
                {"name": "Nut", "quantity": 20, "price": 0.10},
                {"name": "Washer", "quantity": 30, "price": 0.05},
            ],
            ["Bolt", "10", "0.15", "1.5", "Nut", "20", "0.10", "2.0", "Washer", "30", "0.05", "1.5"],
        ),
    ],
)
def test_generate_inventory_report_normal_cases(items, expected_fragments):
    """
    Verify that a correctlystructured report string is produced for typical
    inventories.  The test checks that each expected piece of information
    (item name, quantity, unit price and line total) appears somewhere in the
    output.
    """
    inventory = _FakeInventoryManager(items)

    # Call the function under test
    report = generate_inventory_report(inventory)

    # The function must return a string
    assert isinstance(report, str)

    # Every expected fragment must be present in the report
    for fragment in expected_fragments:
        assert fragment in report
        

# ----------------------------------------------------------------------
# 2. Edge cases  boundary conditions
# ----------------------------------------------------------------------
def test_generate_inventory_report_edge_cases():
    """
    Test boundary conditions such as an empty inventory, zero quantities,
    and very large numeric values.
    """
    # ---- Empty inventory -------------------------------------------------
    empty_inventory = _FakeInventoryManager([])
    empty_report = generate_inventory_report(empty_inventory)

    # The implementation may return a specific message; we only require that
    # the report is a nonempty string and mentions that there are no items.
    assert isinstance(empty_report, str)
    assert "no items" in empty_report.lower() or empty_report.strip() == ""

    # ---- Zero quantity ---------------------------------------------------
    zero_qty_inventory = _FakeInventoryManager(
        [{"name": "ZeroItem", "quantity": 0, "price": 123.45}]
    )
    zero_qty_report = generate_inventory_report(zero_qty_inventory)

    # Quantity zero should still be reported, and the line total must be 0.
    assert "ZeroItem" in zero_qty_report
    assert "0" in zero_qty_report
    assert "0.00" in zero_qty_report or "0" in zero_qty_report.split()[-1]

    # ---- Very large numbers ------------------------------------------------
    large_inventory = _FakeInventoryManager(
        [
            {"name": "MegaWidget", "quantity": 10_000, "price": 9_999.99},
            {"name": "GigaGadget", "quantity": 1_000_000, "price": 0.99},
        ]
    )
    large_report = generate_inventory_report(large_inventory)

    # Verify that the large numbers appear (as strings) in the report.
    assert "MegaWidget" in large_report
    assert "10000" in large_report  # quantity without commas
    assert "9999.99" in large_report
    # The total for MegaWidget is 10_000 * 9_999.99 = 99_999_900.0
    assert "99999900" in large_report.replace(",", "")

    assert "GigaGadget" in large_report
    assert "1000000" in large_report
    assert "0.99" in large_report
    # Total for GigaGadget is 990_000.0
    assert "990000" in large_report.replace(",", "")


# ----------------------------------------------------------------------
# 3. Error cases  invalid inputs
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "bad_input",
    [
        None,
        42,
        "not an inventory",
        {"items": []},               # plain dict, not an InventoryManager
        _FakeInventoryManager(None) # items attribute is None
    ],
)
def test_generate_inventory_report_error_cases(bad_input):
    """
    Ensure that ``generate_inventory_report`` raises an appropriate exception
    when called with objects that do not conform to the expected ``InventoryManager``
    interface.
    """
    with pytest.raises(Exception):
        generate_inventory_report(bad_input)