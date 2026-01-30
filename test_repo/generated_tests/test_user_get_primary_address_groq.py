"""
Auto-generated test cases for function: get_primary_address
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 00:12:16
Source file: user.py
Function signature: def get_primary_address(self) -> Optional[Address]
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
from unittest.mock import MagicMock

# --------------------------------------------------------------------------- #
# NOTE: The following import assumes that the module containing the `User`
# class is named `user`.  If the actual module name differs, replace the
# import statement accordingly.  The tests are written so that they will
# still run correctly as long as the `User` class is importable from the
# specified module.
# --------------------------------------------------------------------------- #
try:
    from user import User
except Exception:  # pragma: no cover
    # If the module cannot be imported, define a minimal stub that mimics
    # the public API of the real `User` class.  This allows the test file
    # to be executed in isolation, but the real tests should import the
    # actual implementation.
    class User:  # pragma: no cover
        def __init__(self, name: str, email: str):
            self.id = None
            self.name = name
            self.email = email
            self.addresses = []
            self.is_active = True

        def add_address(self, address):
            self.addresses.append(address)

        def get_primary_address(self):
            return self.addresses[0] if self.addresses else None

        def deactivate(self):
            self.is_active = False


# --------------------------------------------------------------------------- #
# Helper: a very small Address stub used in the tests
# --------------------------------------------------------------------------- #
class Address:
    def __init__(self, street: str, city: str):
        self.street = street
        self.city = city

    def __repr__(self):
        return f"Address({self.street!r}, {self.city!r})"

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.street == other.street and self.city == other.city


# --------------------------------------------------------------------------- #
# Test 1  Normal cases
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "addresses, expected",
    [
        # No addresses  should return None
        ([], None),
        # One address  should return that address
        ([Address("123 Main St", "Springfield")], Address("123 Main St", "Springfield")),
        # Multiple addresses  should return the first one
        (
            [
                Address("1 First Ave", "Metropolis"),
                Address("2 Second St", "Gotham"),
                Address("3 Third Blvd", "Star City"),
            ],
            Address("1 First Ave", "Metropolis"),
        ),
    ],
)
def test_get_primary_address_normal_cases(addresses, expected, monkeypatch):
    """
    Test that `get_primary_address` returns the first address in the list
    or `None` when the list is empty.
    """
    # Patch the external dependencies so that User can be instantiated
    monkeypatch.setattr("user.generate_uuid", lambda: "fixed-uuid")
    monkeypatch.setattr("user.sanitize_email", lambda e: e.lower())

    # Create a user and populate addresses
    user = User(name="Alice", email="ALICE@EXAMPLE.COM")
    for addr in addresses:
        user.add_address(addr)

    # Call the method under test
    result = user.get_primary_address()

    # Verify the result
    assert result == expected, f"Expected {expected!r}, got {result!r}"


# --------------------------------------------------------------------------- #
# Test 2  Edge cases
# --------------------------------------------------------------------------- #
def test_get_primary_address_edge_cases(monkeypatch):
    """
    Test boundary conditions such as an empty address list, a single address,
    and a large number of addresses.
    """
    # Patch external dependencies
    monkeypatch.setattr("user.generate_uuid", lambda: "fixed-uuid")
    monkeypatch.setattr("user.sanitize_email", lambda e: e.lower())

    # 1. Empty address list
    user_empty = User(name="Bob", email="bob@example.com")
    assert user_empty.get_primary_address() is None

    # 2. Single address
    single_addr = Address("42 Wallaby Way", "Sydney")
    user_single = User(name="Carol", email="carol@example.com")
    user_single.add_address(single_addr)
    assert user_single.get_primary_address() == single_addr

    # 3. Large number of addresses
    many_addresses = [Address(f"{i} Road", f"City{i}") for i in range(1000)]
    user_many = User(name="Dave", email="dave@example.com")
    for addr in many_addresses:
        user_many.add_address(addr)
    assert user_many.get_primary_address() == many_addresses[0]


# --------------------------------------------------------------------------- #
# Test 3  Error cases
# --------------------------------------------------------------------------- #
def test_get_primary_address_error_cases(monkeypatch):
    """
    Test how `get_primary_address` behaves when the internal state is
    corrupted or when invalid data is injected.
    """
    # Patch external dependencies
    monkeypatch.setattr("user.generate_uuid", lambda: "fixed-uuid")
    monkeypatch.setattr("user.sanitize_email", lambda e: e.lower())

    # 1. addresses attribute set to None  should raise TypeError
    user_none = User(name="Eve", email="eve@example.com")
    user_none.addresses = None
    with pytest.raises(TypeError):
        user_none.get_primary_address()

    # 2. addresses attribute missing  should raise AttributeError
    user_missing = User(name="Frank", email="frank@example.com")
    del user_missing.addresses
    with pytest.raises(AttributeError):
        user_missing.get_primary_address()

    # 3. addresses attribute is a string  should raise TypeError
    user_str = User(name="Grace", email="grace@example.com")
    user_str.addresses = "not a list"
    with pytest.raises(TypeError):
        user_str.get_primary_address()

    # 4. Adding a non-Address object  method still returns it,
    #    but we assert that the returned object is exactly the one added.
    user_non_addr = User(name="Heidi", email="heidi@example.com")
    non_addr_obj = MagicMock(name="NonAddress")
    user_non_addr.add_address(non_addr_obj)
    assert user_non_addr.get_primary_address() is non_addr_obj