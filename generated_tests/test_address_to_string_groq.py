"""
Auto-generated test cases for function: to_string
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:33:58
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

# The test file assumes that the class `Address` and the exception `ValidationError`
# are available in the import path (e.g. `from address import Address, ValidationError`).
# They will be provided by the test runner, so we do not import them explicitly here.


@pytest.mark.parametrize(
    "street, city, zip_code, expected",
    [
        ("123 Main St", "Springfield", "12345", "123 Main St, Springfield 12345"),
        ("456 Oak Ave", "Metropolis", "98765", "456 Oak Ave, Metropolis 98765"),
        ("789 Pine Blvd", "Gotham", "00100", "789 Pine Blvd, Gotham 00100"),
        ("10 Downing St", "London", "SW1A 2AA", "10 Downing St, London SW1A 2AA"),
        ("1600 Pennsylvania Ave NW", "Washington", "20500", "1600 Pennsylvania Ave NW, Washington 20500"),
    ],
)
def test_to_string_normal_cases(street, city, zip_code, expected):
    """Verify that `Address.to_string` returns the correctly formatted string for typical inputs."""
    addr = Address(street=street, city=city, zip_code=zip_code)
    result = addr.to_string()
    assert result == expected


def test_to_string_edge_cases():
    """Test edgecase inputs such as empty street/city, Unicode characters and very long strings."""
    # Empty street
    addr1 = Address(street="", city="Nowhere", zip_code="00000")
    assert addr1.to_string() == ", Nowhere 00000"

    # Empty city
    addr2 = Address(street="42 Wallaby Way", city="", zip_code="12345")
    assert addr2.to_string() == "42 Wallaby Way,  12345"

    # Unicode characters
    addr3 = Address(street="So Paulo", city="Mnchen", zip_code="80331")
    assert addr3.to_string() == "So Paulo, Mnchen 80331"

    # Very long strings
    long_street = "A" * 500
    long_city = "B" * 300
    long_zip = "9" * 20
    addr4 = Address(street=long_street, city=long_city, zip_code=long_zip)
    expected = f"{long_street}, {long_city} {long_zip}"
    assert addr4.to_string() == expected


def test_to_string_error_cases():
    """Ensure that invalid initialization (missing zip code) raises the expected ValidationError."""
    # Empty zip code string
    with pytest.raises(ValidationError):
        Address(street="123 Fake St", city="Faketown", zip_code="")

    # None as zip code
    with pytest.raises(ValidationError):
        Address(street="123 Fake St", city="Faketown", zip_code=None)

    # Zip code that evaluates to False (e.g., 0)  still should raise because it is not a nonempty string
    with pytest.raises(ValidationError):
        Address(street="123 Fake St", city="Faketown", zip_code=0)