"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-31 00:11:58
Source file: user.py
Function signature: def __init__(self, name: str, email: str)
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

# Import the class under test.  The module name is assumed to be `user`.
# Adjust the import path if the actual module name differs.
from user import User


# --------------------------------------------------------------------------- #
# 1. Normal cases
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "name, email, expected_email",
    [
        ("Alice", "alice@example.com", "alice@example.com"),
        ("Bob Smith", "bob.smith@example.com", "bob.smith@example.com"),
        ("Charlie", "CHARLIE@EXAMPLE.COM", "charlie@example.com"),
    ],
)
def test___init___normal_cases(monkeypatch, name, email, expected_email):
    """
    Test that User.__init__ correctly assigns attributes for typical inputs.
    """
    # Patch the external dependencies to deterministic values
    monkeypatch.setattr("user.generate_uuid", lambda: "mock-uuid")
    monkeypatch.setattr(
        "user.sanitize_email",
        lambda e: e.lower() if isinstance(e, str) else e,
    )

    # Instantiate the User
    user = User(name=name, email=email)

    # Assertions
    assert user.id == "mock-uuid", "ID should be set by generate_uuid"
    assert user.name == name, "Name should be stored unchanged"
    assert user.email == expected_email, "Email should be sanitized to lowercase"
    assert user.addresses == [], "Addresses list should be empty on init"
    assert user.is_active is True, "User should be active after initialization"


# --------------------------------------------------------------------------- #
# 2. Edge cases
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "name, email, expected_email",
    [
        ("", "", ""),  # Empty strings
        ("A" * 256, "longname@example.com", "longname@example.com"),  # Very long name
        ("Normal", "user+tag@example.com", "user+tag@example.com"),  # Email with special chars
        ("Normal", "USER@EXAMPLE.COM", "user@example.com"),  # Uppercase email
    ],
)
def test___init___edge_cases(monkeypatch, name, email, expected_email):
    """
    Test User.__init__ with boundary and edge case inputs.
    """
    # Patch the external dependencies
    monkeypatch.setattr("user.generate_uuid", lambda: "edge-uuid")
    monkeypatch.setattr(
        "user.sanitize_email",
        lambda e: e.lower() if isinstance(e, str) else e,
    )

    # Instantiate the User
    user = User(name=name, email=email)

    # Assertions
    assert user.id == "edge-uuid", "ID should be set by generate_uuid"
    assert user.name == name, "Name should be stored unchanged"
    assert user.email == expected_email, "Email should be sanitized correctly"
    assert user.addresses == [], "Addresses list should be empty on init"
    assert user.is_active is True, "User should be active after initialization"
    # Verify that get_primary_address returns None when no addresses are added
    assert user.get_primary_address() is None, "Primary address should be None initially"


# --------------------------------------------------------------------------- #
# 3. Error cases
# --------------------------------------------------------------------------- #
def test___init___error_cases(monkeypatch):
    """
    Test that User.__init__ raises appropriate errors for invalid inputs.
    """
    # Patch generate_uuid to a deterministic value
    monkeypatch.setattr("user.generate_uuid", lambda: "error-uuid")

    # Helper function to patch sanitize_email to raise ValueError for specific inputs
    def sanitize_email_side_effect(email):
        if email is None:
            raise ValueError("Email cannot be None")
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        if "@" not in email:
            raise ValueError("Invalid email format")
        return email.lower()

    monkeypatch.setattr("user.sanitize_email", sanitize_email_side_effect)

    # 1. Email is None
    with pytest.raises(ValueError) as excinfo:
        User(name="Test User", email=None)
    assert "Email cannot be None" in str(excinfo.value)

    # 2. Email is not a string
    with pytest.raises(ValueError) as excinfo:
        User(name="Test User", email=12345)
    assert "Email must be a string" in str(excinfo.value)

    # 3. Email missing '@' symbol
    with pytest.raises(ValueError) as excinfo:
        User(name="Test User", email="invalidemail.com")
    assert "Invalid email format" in str(excinfo.value)

    # 4. Name is None (should not raise because __init__ does not validate name)
    # We still patch sanitize_email to raise only on email issues
    user = User(name=None, email="valid@example.com")
    assert user.name is None, "Name can be None if not validated"
    assert user.email == "valid@example.com", "Email should be sanitized correctly"

    # 5. Name is not a string (should not raise)
    user = User(name=123, email="valid@example.com")
    assert user.name == 123, "Name can be non-string if not validated"
    assert user.email == "valid@example.com", "Email should be sanitized correctly"