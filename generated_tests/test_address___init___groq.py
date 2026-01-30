"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:33:52
Source file: address.py
Function signature: def __init__(self, street: str, city: str, zip_code: str)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.address import Address

import pytest

# The class under test is assumed to be importable from the module where it is defined.
# Replace `my_module` with the actual module name if needed.
from address import Address  # noqa: F401


def _call_init(street: str, city: str, zip_code: str) -> Address:
    """
    Helper that creates an uninitialised ``Address`` instance and then
    calls ``__init__`` manually.  This satisfies the requirement to
    instantiate the class *before* invoking ``__init__``.
    """
    # Bypass ``__init__`` by using ``__new__`` directly.
    instance = Address.__new__(Address)
    # Now call the real ``__init__`` with the supplied arguments.
    instance.__init__(street, city, zip_code)
    return instance


@pytest.mark.parametrize(
    "street, city, zip_code",
    [
        ("123 Main St", "Springfield", "12345"),
        ("456 Elm St", "Metropolis", "54321"),
        ("789 Oak Ave", "Gotham", "00100"),
        ("10 Downing St", "London", "SW1A 2AA"),
        (" Avenue", " City", ""),
    ],
)
def test___init___normal_cases(street, city, zip_code):
    """
    Normal cases  verify that the attributes are stored exactly as passed.
    """
    addr = _call_init(street, city, zip_code)

    assert addr.street == street
    assert addr.city == city
    assert addr.zip_code == zip_code


def test___init___edge_cases():
    """
    Edge cases  test handling of empty strings for optional fields,
    very long inputs, and unicode characters.
    """
    # Empty street and city are allowed (only zip_code is validated)
    addr1 = _call_init("", "", "99999")
    assert addr1.street == ""
    assert addr1.city == ""
    assert addr1.zip_code == "99999"

    # Very long strings
    long_street = "A" * 10_000
    long_city = "B" * 10_000
    long_zip = "9" * 20
    addr2 = _call_init(long_street, long_city, long_zip)
    assert addr2.street == long_street
    assert addr2.city == long_city
    assert addr2.zip_code == long_zip

    # Unicode / special characters
    unicode_street = ""
    unicode_city = "Mnchen"
    unicode_zip = ""
    addr3 = _call_init(unicode_street, unicode_city, unicode_zip)
    assert addr3.street == unicode_street
    assert addr3.city == unicode_city
    assert addr3.zip_code == unicode_zip


def test___init___error_cases():
    """
    Error cases  ``zip_code`` is required; passing a falsy value should raise
    the validation exception.
    """
    # The class raises ``ValidationError`` when ``zip_code`` is falsy.
    # If the concrete exception type is not available, we fall back to a generic
    # ``Exception`` check.
    with pytest.raises(Exception):
        _call_init("123 Main St", "Springfield", "")

    with pytest.raises(Exception):
        _call_init("123 Main St", "Springfield", None)  # type: ignore[arg-type]

    # Also ensure that passing only whitespace is considered falsy by the
    # implementation (it evaluates to ``True`` in a boolean context, but we
    # test the behaviour explicitly).
    with pytest.raises(Exception):
        _call_init("123 Main St", "Springfield", "   ")