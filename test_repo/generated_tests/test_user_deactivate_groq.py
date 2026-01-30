"""
Auto-generated test cases for function: deactivate
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 00:12:29
Source file: user.py
Function signature: def deactivate(self)
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

# Import the User class from the module where it is defined.
# Adjust the import path if the module name differs.
# For the purpose of these tests we assume the module is named `user`.
from user import User


# --------------------------------------------------------------------------- #
# 1. Normal cases
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "name, email",
    [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "CHARLIE@EXAMPLE.COM"),
    ],
)
def test_deactivate_normal_cases(name, email, monkeypatch):
    """
    Test that `deactivate` correctly sets `is_active` to False for normal
    user instances.  The test also verifies that the user is initially
    active and that other attributes remain unchanged.
    """
    # Patch external dependencies to deterministic values
    monkeypatch.setattr("user.generate_uuid", lambda: "fixed-uuid")
    monkeypatch.setattr("user.sanitize_email", lambda e: e.lower())

    # Instantiate the user
    user = User(name=name, email=email)

    # Verify initial state
    assert user.is_active is True
    assert user.name == name
    assert user.email == email.lower()

    # Call deactivate
    user.deactivate()

    # Verify final state
    assert user.is_active is False


# --------------------------------------------------------------------------- #
# 2. Edge cases
# --------------------------------------------------------------------------- #
def test_deactivate_edge_cases(monkeypatch):
    """
    Test edge cases for `deactivate`:
    * User with no addresses
    * User with multiple addresses
    * Calling deactivate twice
    """
    # Patch external dependencies
    monkeypatch.setattr("user.generate_uuid", lambda: "edge-uuid")
    monkeypatch.setattr("user.sanitize_email", lambda e: e)

    # Case 1: No addresses
    user_no_addr = User(name="NoAddr", email="noaddr@example.com")
    assert user_no_addr.addresses == []
    user_no_addr.deactivate()
    assert user_no_addr.is_active is False

    # Case 2: Multiple addresses
    user_many_addr = User(name="ManyAddr", email="many@example.com")
    addr1 = MagicMock(name="Address1")
    addr2 = MagicMock(name="Address2")
    user_many_addr.add_address(addr1)
    user_many_addr.add_address(addr2)
    assert user_many_addr.addresses == [addr1, addr2]
    user_many_addr.deactivate()
    assert user_many_addr.is_active is False
    # Addresses should remain unchanged
    assert user_many_addr.addresses == [addr1, addr2]

    # Case 3: Deactivate twice
    user_twice = User(name="Twice", email="twice@example.com")
    user_twice.deactivate()
    assert user_twice.is_active is False
    # Second call should not raise and keep the state
    user_twice.deactivate()
    assert user_twice.is_active is False


# --------------------------------------------------------------------------- #
# 3. Error cases
# --------------------------------------------------------------------------- #
def test_deactivate_error_cases(monkeypatch):
    """
    Test error scenarios during user creation that indirectly affect
    the ability to call `deactivate`.  Since `deactivate` itself does not
    raise errors, we test that invalid inputs to the constructor raise
    appropriate exceptions.
    """
    # Case 1: sanitize_email raises ValueError
    def fake_sanitize(email):
        raise ValueError("Invalid email format")

    monkeypatch.setattr("user.sanitize_email", fake_sanitize)
    monkeypatch.setattr("user.generate_uuid", lambda: "uuid-error")

    with pytest.raises(ValueError):
        User(name="InvalidEmail", email="bad-email")

    # Case 2: generate_uuid raises RuntimeError
    monkeypatch.setattr("user.sanitize_email", lambda e: e)  # restore normal
    monkeypatch.setattr("user.generate_uuid", lambda: (_ for _ in ()).throw(RuntimeError("UUID generation failed")))

    with pytest.raises(RuntimeError):
        User(name="UUIDError", email="valid@example.com")