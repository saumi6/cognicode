"""
Auto-generated test cases for function: add_address
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 00:12:07
Source file: user.py
Function signature: def add_address(self, address: Address)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.user import User

import pytest
from dataclasses import dataclass
from typing import List, Optional

# Assume the User class is defined in a module named `user`.
# Adjust the import path if the module has a different name.
from user import User


# --------------------------------------------------------------------------- #
# Helper data structures
# --------------------------------------------------------------------------- #
@dataclass
class Address:
    """Simple address representation used only for testing."""
    street: str
    city: str
    zip_code: str = ""


# --------------------------------------------------------------------------- #
# 1. Normal cases
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "addresses_to_add, expected_primary",
    [
        # Single address
        (
            [Address("123 Main St", "Springfield")],
            Address("123 Main St", "Springfield"),
        ),
        # Multiple addresses  first one should be primary
        (
            [
                Address("1 First Ave", "Metropolis"),
                Address("2 Second St", "Gotham"),
                Address("3 Third Blvd", "Star City"),
            ],
            Address("1 First Ave", "Metropolis"),
        ),
        # Addresses with empty fields  still accepted
        (
            [
                Address("", ""),
                Address("456 Elm St", "Smallville"),
            ],
            Address("", ""),
        ),
    ],
)
def test_add_address_normal_cases(addresses_to_add, expected_primary):
    """
    Test that `add_address` correctly appends addresses and that
    `get_primary_address` returns the first added address.
    """
    user = User(name="Alice", email="alice@example.com")

    # Add each address and verify the list grows as expected
    for idx, addr in enumerate(addresses_to_add):
        user.add_address(addr)
        assert len(user.addresses) == idx + 1
        assert user.addresses[-1] is addr

    # Primary address should be the first one added
    primary = user.get_primary_address()
    assert primary is not None
    assert primary is expected_primary
    assert primary.street == expected_primary.street
    assert primary.city == expected_primary.city
    assert primary.zip_code == expected_primary.zip_code


# --------------------------------------------------------------------------- #
# 2. Edge cases
# --------------------------------------------------------------------------- #
def test_add_address_edge_cases():
    """
    Test boundary and edge conditions such as:
    - Adding the same address object multiple times.
    - Adding a large number of addresses.
    - Adding after deactivating the user.
    """
    user = User(name="Bob", email="bob@example.com")

    # Edge case 1: Add the same address object twice
    shared_address = Address("789 Oak St", "Riverdale")
    user.add_address(shared_address)
    user.add_address(shared_address)
    assert user.addresses.count(shared_address) == 2

    # Edge case 2: Add a large number of addresses (e.g., 100)
    for i in range(100):
        addr = Address(f"{i} Test Ln", f"City{i}")
        user.add_address(addr)
    assert len(user.addresses) == 102  # 2 from before + 100 new

    # Edge case 3: Deactivate the user and still add addresses
    user.deactivate()
    assert not user.is_active
    new_addr = Address("999 Last St", "Endtown")
    user.add_address(new_addr)
    assert user.addresses[-1] is new_addr
    assert user.is_active is False  # deactivation flag remains unchanged


# --------------------------------------------------------------------------- #
# 3. Error cases
# --------------------------------------------------------------------------- #
def test_add_address_error_cases(monkeypatch):
    """
    Test scenarios where `add_address` should raise an exception.
    These are intentional misuse cases, such as corrupting the internal
    `addresses` attribute or passing an unsupported type.
    """
    user = User(name="Charlie", email="charlie@example.com")

    # Case 1: Corrupt the internal list to a tuple (immutable)
    monkeypatch.setattr(user, "addresses", tuple())
    with pytest.raises(AttributeError):
        user.add_address(Address("1 Fake St", "Nowhere"))

    # Case 2: Set the addresses attribute to None
    monkeypatch.setattr(user, "addresses", None)
    with pytest.raises(AttributeError):
        user.add_address(Address("2 Fake St", "Nowhere"))

    # Case 3: Pass an object that is not an Address instance.
    # The method itself does not enforce type, so it will succeed,
    # but we can still assert that the object is stored as-is.
    # This is not an error case for `add_address`, but we include it
    # to demonstrate that the method accepts any object.
    non_address = "I am not an address"
    user.add_address(non_address)
    assert user.addresses[-1] == non_address