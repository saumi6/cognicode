"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:16:43
Source file: checkout_controller.py
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
from test_repo.checkout_controller import CheckoutController

import pytest
from unittest.mock import Mock, MagicMock

# NOTE:
# The CheckoutController class is assumed to live in a module named `checkout_controller`.
# All monkeypatches therefore use the absolute import path `checkout_controller.PriceCalculator`.


def _make_controller_without_init():
    """
    Helper that creates a CheckoutController instance **without** invoking its __init__.
    """
    # Import inside the function so the test file does not need the real module at import time.
    from checkout_controller import CheckoutController

    # Bypass __init__ by using __new__
    return CheckoutController.__new__(CheckoutController)


@pytest.mark.parametrize(
    "price_calc_class, expected_attr, expected_value",
    [
        # Simple mock class with a custom attribute
        (type("DummyCalc1", (object,), {"name": "calc_one"}), "name", "calc_one"),
        # Mock class that also implements a dummy method
        (
            type(
                "DummyCalc2",
                (object,),
                {"description": "second calculator", "dummy_method": lambda self: 42},
            ),
            "description",
            "second calculator",
        ),
        # MagicMock subclass to ensure it behaves like a typical mock
        (type("DummyCalc3", (MagicMock,), {}), "_mock_name", None),
    ],
)
def test___init___normal_cases(monkeypatch, price_calc_class, expected_attr, expected_value):
    """
    Normal cases for CheckoutController.__init__.

    dummy classes and verifies that the ``calc`` attribute of the controller
    is an instance of the patched class and that any custom attributes are
    preserved.
    """
    # Patch the PriceCalculator used inside CheckoutController
    monkeypatch.setattr("checkout_controller.PriceCalculator", price_calc_class)

    # Create an instance without running __init__
    controller = _make_controller_without_init()

    # Manually invoke __init__
    controller.__init__()

    # The calc attribute should be an instance of the patched class
    assert isinstance(controller.calc, price_calc_class)

    # If the dummy class defines a custom attribute, check its value
    if expected_attr:
        assert getattr(controller.calc, expected_attr) == expected_value


def test___init___edge_cases(monkeypatch):
    """
    Edge case: ``PriceCalculator`` raises an exception during instantiation.

    """
    class ExplodingCalculator:
        def __init__(self):
            raise RuntimeError("boom")

    # Patch the PriceCalculator to the exploding version
    monkeypatch.setattr("checkout_controller.PriceCalculator", ExplodingCalculator)

    controller = _make_controller_without_init()

    # The exception from the calculator should bubble up when __init__ is called
    with pytest.raises(RuntimeError) as excinfo:
        controller.__init__()
    assert "boom" in str(excinfo.value)


def test___init___error_cases(monkeypatch):
    """
    Error cases for CheckoutController.__init__.

    1. ``PriceCalculator`` is not callable (e.g., set to an int).
    2. Calling ``__init__`` with unexpected positional arguments.
    """
    # 1. Noncallable PriceCalculator
    monkeypatch.setattr("checkout_controller.PriceCalculator", 12345)  # not a class / callable

    controller = _make_controller_without_init()
    with pytest.raises(TypeError):
        controller.__init__()

    # 2. Passing extra arguments to __init__
    # Repatch with a normal dummy class so the first error does not interfere
    class DummyCalc:
        pass

    monkeypatch.setattr("checkout_controller.PriceCalculator", DummyCalc)

    controller = _make_controller_without_init()
    # __init__ expects only the implicit ``self``; providing extra args should raise TypeError
    with pytest.raises(TypeError):
        controller.__init__(object())