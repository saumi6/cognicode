"""
Auto-generated test cases for function: to_dict
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:34:07
Source file: address.py
Function signature: def to_dict(self) -> Dict[str, str]
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
from unittest.mock import Mock

# The class under test is assumed to live in a module named ``address``.
# Adjust the import path if the actual file name differs.
from address import Address, ValidationError


@pytest.mark.parametrize(
    "street, city, zip_code, slug_return, expected",
    [
        # simple latin characters
        (
            "123 Main St",
            "Springfield",
            "12345",
            "springfield",
            {
                "street": "123 Main St",
                "city": "Springfield",
                "zip": "12345",
                "slug": "springfield",
            },
        ),
        # city with spaces  slugify should collapse them (mocked)
        (
            "456 Oak Ave",
            "New York",
            "10001",
            "new-york",
            {
                "street": "456 Oak Ave",
                "city": "New York",
                "zip": "10001",
                "slug": "new-york",
            },
        ),
        # city with mixed case and punctuation
        (
            "789 Pine Rd",
            "St. Louis",
            "63101",
            "st-louis",
            {
                "street": "789 Pine Rd",
                "city": "St. Louis",
                "zip": "63101",
                "slug": "st-louis",
            },
        ),
    ],
)
def test_to_dict_normal_cases(monkeypatch, street, city, zip_code, slug_return, expected):
    """Normal usage  verify that ``to_dict`` returns the expected mapping."""
    # Patch the ``slugify`` function used inside ``Address.to_dict``.
    monkeypatch.setattr("address.slugify", lambda c: slug_return)

    addr = Address(street=street, city=city, zip_code=zip_code)
    result = addr.to_dict()

    assert result == expected


def test_to_dict_edge_cases(monkeypatch):
    """Edgecase handling  empty street, leading zeros in zip, Unicode city names."""
    # 1. Empty street (allowed)  city with Unicode characters.
    monkeypatch.setattr("address.slugify", lambda c: "mnchen")
    addr1 = Address(street="", city="Mnchen", zip_code="00123")
    expected1 = {
        "street": "",
        "city": "Mnchen",
        "zip": "00123",
        "slug": "mnchen",
    }
    assert addr1.to_dict() == expected1

    # 2. City containing only whitespace  slugify should still be called.
    monkeypatch.setattr("address.slugify", lambda c: "whitespace-city")
    addr2 = Address(street="10 Downing St", city="   ", zip_code="SW1A2AA")
    expected2 = {
        "street": "10 Downing St",
        "city": "   ",
        "zip": "SW1A2AA",
        "slug": "whitespace-city",
    }
    assert addr2.to_dict() == expected2

    # 3. Zip code with leading zeros  ensure they are preserved as strings.
    monkeypatch.setattr("address.slugify", lambda c: "zero-city")
    addr3 = Address(street="1 Infinite Loop", city="ZeroCity", zip_code="00001")
    expected3 = {
        "street": "1 Infinite Loop",
        "city": "ZeroCity",
        "zip": "00001",
        "slug": "zero-city",
    }
    assert addr3.to_dict() == expected3


def test_to_dict_error_cases():
    """Invalid inputs  ``zip_code`` missing should raise ``ValidationError``."""
    # Empty string zip code
    with pytest.raises(ValidationError):
        Address(street="123 Any St", city="AnyTown", zip_code="")

    # ``None`` as zip code
    with pytest.raises(ValidationError):
        Address(street="123 Any St", city="AnyTown", zip_code=None)

    # Omitted zip_code argument (TypeError from missing positional argument)
    with pytest.raises(TypeError):
        Address(street="123 Any St", city="AnyTown")  # type: ignore[arg-type]