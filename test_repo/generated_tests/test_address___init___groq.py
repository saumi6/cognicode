"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 00:11:17
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
from address import Address, ValidationError


@pytest.mark.parametrize(
    "street, city, zip_code",
    [
        ("123 Main St", "Springfield", "12345"),
        ("456 Elm St", "Metropolis", "54321"),
        ("789 Oak Ave", "Gotham", "00001"),
    ],
)
def test___init___normal_cases(street, city, zip_code):
    """Test normal initialization with valid inputs."""
    addr = Address(street, city, zip_code)

    # Basic attribute checks
    assert addr.street == street
    assert addr.city == city
    assert addr.zip_code == zip_code

    # to_string() should format the address correctly
    expected_string = f"{street}, {city} {zip_code}"
    assert addr.to_string() == expected_string

    # to_dict() should contain all expected keys
    d = addr.to_dict()
    assert d["street"] == street
    assert d["city"] == city
    assert d["zip"] == zip_code
    assert isinstance(d["slug"], str)  # slug should be a string


@pytest.mark.parametrize(
    "street, city, zip_code",
    [
        ("", "SomeCity", "12345"),          # empty street
        ("Some Street", "", "12345"),       # empty city
        ("   ", "   ", "12345"),            # whitespace only
        ("A" * 1000, "B" * 1000, "12345"),  # very long strings
        ("123 Main St", "Springfield", "00000"),  # zip with leading zeros
        ("123 Main St", "Springfield", "12345-6789"),  # hyphenated zip
    ],
)
def test___init___edge_cases(street, city, zip_code):
    """Test edge cases for initialization."""
    addr = Address(street, city, zip_code)

    # Ensure attributes are set exactly as passed
    assert addr.street == street
    assert addr.city == city
    assert addr.zip_code == zip_code

    # to_string() should still format correctly even with edge values
    expected_string = f"{street}, {city} {zip_code}"
    assert addr.to_string() == expected_string


def test___init___error_cases():
    """Test that initializing with missing zip code raises ValidationError."""
    # Empty string zip code
    with pytest.raises(ValidationError):
        Address("123 Main St", "Springfield", "")

    # None zip code
    with pytest.raises(ValidationError):
        Address("123 Main St", "Springfield", None)