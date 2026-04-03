"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 10:25:10
Source file: inventory_manager.py
Function signature: def __init__(self)
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

# The class under test is assumed to be importable in the test environment.
# If it lives in a module called `inventory`, you would normally do:
# from inventory import InventoryManager
# For the purpose of these snippets we refer to it directly.


@pytest.mark.parametrize(
    "instance_label",
    [
        "first_instance",
        "second_instance",
        "third_instance",
    ],
)
def test___init___normal_cases(instance_label):
    """
    Normal cases for ``InventoryManager.__init__``.
    deterministic behaviour across repeated instantiations.
    """
    manager = InventoryManager()          # instantiate the class
    # ``products`` must be a dict and start empty
    assert isinstance(manager.products, dict), "products attribute should be a dict"
    assert len(manager.products) == 0, "products dict should be empty on construction"


def test___init___edge_cases():
    """
    Edgecase tests for ``InventoryManager.__init__``.
    Verify that each instance gets its *own* ``products`` dictionary
    (i.e. the dict is not shared between instances) and that the attribute
    can be safely replaced without affecting other instances.
    """
    manager_a = InventoryManager()
    manager_b = InventoryManager()

    # The two instances must have distinct dict objects
    assert manager_a.products is not manager_b.products, "Each instance should own its own dict"

    # Mutate one instance and ensure the other stays unchanged
    dummy_product = Mock()
    dummy_product.sku = "SKU123"
    manager_a.products[dummy_product.sku] = dummy_product

    assert dummy_product.sku in manager_a.products
    assert dummy_product.sku not in manager_b.products, "Mutation of one instance must not affect another"


def test___init___error_cases():
    """
    Errorcase tests for ``InventoryManager.__init__``.
    or keyword arguments should raise ``TypeError``.
    """
    # Passing a positional argument
    with pytest.raises(TypeError):
        InventoryManager("unexpected positional arg")

    # Passing a keyword argument
    with pytest.raises(TypeError):
        InventoryManager(sku="unexpected keyword arg")