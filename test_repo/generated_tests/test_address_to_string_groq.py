"""
Auto-generated test cases for function: to_string
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 00:11:27
Source file: address.py
Function signature: def to_string(self) -> str
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

# Import the class and exception from the module where they are defined.
# Adjust the import path if the module name differs.
from address import Address, ValidationError


@pytest.mark.parametrize(
    "street, city, zip_code, expected",
    [
        # Simple numeric ZIP
        ("123 Main St", "Springfield", "12345", "123 Main St, Springfield 12345"),
        # ZIP with hyphen
        ("456 Elm St", "Metropolis", "54321-9876", "456 Elm St, Metropolis 54321-9876"),
        # Alphabetic ZIP
        ("789 Oak Ave", "Gotham", "ABCDE", "789 Oak Ave, Gotham ABCDE"),
        # Minimal values
        ("1", "2", "3", "1, 2 3"),
        # Unicode street and city
        ("", "", "00123", ",  00123"),
        # ZIP with leading zeros
        ("123 Main St", "New York", "00001", "123 Main St, New York 00001"),
        # ZIP with surrounding spaces
        ("123 Main St", "Springfield", "   12345   ", "123 Main St, Springfield    12345   "),
    ],
)
def test_to_string_normal_cases(street, city, zip_code, expected):
    """Test normal cases for Address.to_string."""
    address = Address(street, city, zip_code)
    assert address.to_string() == expected


def test_to_string_edge_cases():
    """Test edge cases and boundary conditions for Address.to_string."""
    # Empty street
    address = Address("", "Springfield", "12345")
    assert address.to_string() == ", Springfield 12345"

    # Empty city
    address = Address("123 Main St", "", "12345")
    assert address.to_string() == "123 Main St,  12345"

    # ZIP with leading zeros
    address = Address("123 Main St", "Springfield", "00123")
    assert address.to_string() == "123 Main St, Springfield 00123"

    # ZIP with hyphen
    address = Address("123 Main St", "Springfield", "12345-6789")
    assert address.to_string() == "123 Main St, Springfield 12345-6789"

    # ZIP with alphabetic characters
    address = Address("123 Main St", "Springfield", "ABCDE")
    assert address.to_string() == "123 Main St, Springfield ABCDE"

    # ZIP with surrounding spaces
    address = Address("123 Main St", "Springfield", "   12345   ")
    assert address.to_string() == "123 Main St, Springfield    12345   "

    # Extremely long ZIP
    long_zip = "12345678901234567890"
    address = Address("123 Main St", "Springfield", long_zip)
    assert address.to_string() == f"123 Main St, Springfield {long_zip}"

    # Unicode street and city
    address = Address("", "", "00123")
    assert address.to_string() == ",