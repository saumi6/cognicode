"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 10:26:17
Source file: product_controller.py
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
from test_repo.product_controller import ProductController

import pytest
from unittest.mock import MagicMock, Mock

# NOTE: The absolute import path for the module that contains `ProductController`
# is assumed to be ``test_repo.product_controller``. Adjust the path if the
# actual location differs.
MODULE_PATH = "test_repo.product_controller"


def _make_mock_class(return_value):
    """
    Helper that creates a mock class which, when called, returns *return_value*.
    The mock class itself records how it was called (useful for assertions).
    """
    mock_cls = MagicMock(name=f"MockClass_{id(return_value)}")
    mock_cls.return_value = return_value
    return mock_cls


@pytest.mark.parametrize(
    "inventory_return, recommender_return",
    [
        (MagicMock(name="InvInstanceA"), MagicMock(name="RecInstanceA")),
        (MagicMock(name="InvInstanceB"), MagicMock(name="RecInstanceB")),
        (MagicMock(name="InvInstanceC"), MagicMock(name="RecInstanceC")),
    ],
)
def test___init___normal_cases(monkeypatch, inventory_return, recommender_return):
    """
    Normal cases  verify that ``ProductController.__init__`` creates an
    ``InventoryManager`` instance and passes it to ``RecommendationEngine``.
    Different mock return objects are supplied via parametrisation.
    """
    # Patch the two dependency classes with mocks that return the supplied objects
    mock_inventory_cls = _make_mock_class(inventory_return)
    mock_recommender_cls = _make_mock_class(recommender_return)

    monkeypatch.setattr(f"{MODULE_PATH}.InventoryManager", mock_inventory_cls)
    monkeypatch.setattr(f"{MODULE_PATH}.RecommendationEngine", mock_recommender_cls)

    # Create an uninitialised instance and call __init__ manually (as required)
    from test_repo.product_controller import ProductController  # import inside test
    pc = ProductController.__new__(ProductController)
    pc.__init__()  # <-- the method under test

    # Assertions --------------------------------------------------------------
    # ``InventoryManager`` should have been instantiated exactly once
    mock_inventory_cls.assert_called_once_with()
    # The created inventory object must be the one we supplied
    assert pc.inventory is inventory_return

    # ``RecommendationEngine`` must have been instantiated with the inventory
    mock_recommender_cls.assert_called_once_with(inventory_return)
    # The created recommender object must be the one we supplied
    assert pc.recommender is recommender_return


def test___init___edge_cases(monkeypatch):
    """
    Edgecase tests  cover unusual but possible situations:
    * ``InventoryManager`` returns ``None``.
    * ``RecommendationEngine`` raises an exception after receiving the inventory.
    attached to the controller before the failure.
    """
    # 1 InventoryManager returns ``None`` (still a valid object for the controller)
    mock_inventory_cls = _make_mock_class(None)
    mock_recommender_cls = _make_mock_class(MagicMock(name="RecInstance"))

    monkeypatch.setattr(f"{MODULE_PATH}.InventoryManager", mock_inventory_cls)
    monkeypatch.setattr(f"{MODULE_PATH}.RecommendationEngine", mock_recommender_cls)

    from test_repo.product_controller import ProductController
    pc = ProductController.__new__(ProductController)
    pc.__init__()

    assert pc.inventory is None
    mock_inventory_cls.assert_called_once_with()
    mock_recommender_cls.assert_called_once_with(None)
    assert isinstance(pc.recommender, MagicMock)

    # 2 RecommendationEngine raises an exception  the exception should bubble up
    mock_inventory_cls = _make_mock_class(MagicMock(name="InvInstance"))
    failing_recommender = MagicMock(side_effect=RuntimeError("boom"))
    monkeypatch.setattr(f"{MODULE_PATH}.InventoryManager", mock_inventory_cls)
    monkeypatch.setattr(f"{MODULE_PATH}.RecommendationEngine", failing_recommender)

    pc2 = ProductController.__new__(ProductController)
    with pytest.raises(RuntimeError) as excinfo:
        pc2.__init__()
    assert "boom" in str(excinfo.value)

    # Even though the recommender failed, the inventory should still be set
    assert isinstance(pc2.inventory, MagicMock)
    mock_inventory_cls.assert_called_once_with()


def test___init___error_cases(monkeypatch):
    """
    Error cases  verify that misuse of ``__init__`` raises the appropriate
    Python errors.
    * Calling ``__init__`` with unexpected positional arguments.
    * Patching ``InventoryManager`` with a noncallable object (e.g., an int)
      which should cause a ``TypeError`` when ``__init__`` tries to instantiate it.
    """
    from test_repo.product_controller import ProductController

    # 1 Passing extra arguments to __init__ should raise TypeError
    pc = ProductController.__new__(ProductController)
    with pytest.raises(TypeError):
        pc.__init__("unexpected_arg")

    # 2 ``InventoryManager`` is not callable  should raise TypeError during init
    monkeypatch.setattr(f"{MODULE_PATH}.InventoryManager", 123)  # not a class / callable
    # Keep RecommendationEngine as a harmless mock to isolate the failure point
    mock_recommender_cls = _make_mock_class(MagicMock(name="RecInstance"))
    monkeypatch.setattr(f"{MODULE_PATH}.RecommendationEngine", mock_recommender_cls)

    pc2 = ProductController.__new__(ProductController)
    with pytest.raises(TypeError):
        pc2.__init__()