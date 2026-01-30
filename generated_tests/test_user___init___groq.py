"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-01-31 03:34:20
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
from unittest.mock import Mock

# The class under test is assumed to live in a module named ``user``.
# Adjust the import path if the actual module name differs.
from user import User


@pytest.fixture(autouse=True)
def _mock_dependencies(monkeypatch):
    """
    Mock the external helpers used by ``User.__init__`` so that the tests
    are deterministic and do not depend on their real implementations.
    """
    # A deterministic UUID value for every test case
    monkeypatch.setattr(
        "user.generate_uuid",
        lambda: "123e4567-e89b-12d3-a456-426614174000",
    )
    # A simple sanitizer that just strips whitespace and lowercases the address
    monkeypatch.setattr(
        "user.sanitize_email",
        lambda email: email.strip().lower(),
    )
    return


def test___init___normal_cases():
    """Normal usage of ``User.__init__`` with typical name/email values."""
    test_data = [
        ("Alice", "alice@example.com"),
        ("Bob", "BOB@EXAMPLE.COM  "),
        ("Charlie", "  charlie@sub.domain.org"),
    ]

    for name, raw_email in test_data:
        user = User(name=name, email=raw_email)

        # ``id`` should be the mocked UUID
        assert user.id == "123e4567-e89b-12d3-a456-426614174000"
        # ``name`` is stored unchanged
        assert user.name == name
        # ``email`` is passed through the mocked sanitizer
        assert user.email == raw_email.strip().lower()
        # ``addresses`` starts empty and ``is_active`` is True
        assert user.addresses == []
        assert user.is_active is True


@pytest.mark.parametrize(
    "name,email,expected_email",
    [
        # Empty name is allowed  we only check that it is stored asis
        ("", "emptyname@example.com", "emptyname@example.com"),
        # Very long name (100 characters)
        ("A" * 100, "longname@example.com", "longname@example.com"),
        # Email with surrounding whitespace and mixed case
        ("Dana", "  DaNa@Example.COM  ", "dana@example.com"),
        # Email containing plusaddressing
        ("Eve", "eve+test@Example.com", "eve+test@example.com"),
    ],
)
def test___init___edge_cases(name, email, expected_email):
    """
    Edgecase handling for ``User.__init__``:
    * empty or very long names,
    * emails with whitespace, case variations, or plusaddressing.
    """
    user = User(name=name, email=email)

    assert user.name == name
    assert user.email == expected_email
    # The mocked UUID is still used
    assert user.id == "123e4567-e89b-12d3-a456-426614174000"
    # Default state checks
    assert user.addresses == []
    assert user.is_active is True


def test___init___error_cases(monkeypatch):
    """
    ``User.__init__`` should propagate errors from the helper functions
    when supplied with invalid input.
    """
    # Make ``sanitize_email`` raise a ``ValueError`` for clearly invalid emails
    def _bad_sanitize(email):
        raise ValueError(f"Invalid email: {email}")

    monkeypatch.setattr("user.sanitize_email", _bad_sanitize)

    # 1. Invalid email format  expect ``ValueError`` from the sanitizer
    with pytest.raises(ValueError):
        User(name="Frank", email="not-an-email")

    # 2. Nonstring name  the constructor does not typecheck ``name`` itself,
    #    but downstream code may rely on it being a string. Here we simply
    #    ensure that passing a nonstring does not break the mocked helpers.
    #    The test demonstrates that no exception is raised for a nonstring name.
    user = User(name=12345, email="valid@example.com")
    assert isinstance(user.name, int) and user.name == 12345
    assert user.email == "valid@example.com"

    # 3. ``generate_uuid`` raising an unexpected exception should surface.
    def _bad_uuid():
        raise RuntimeError("UUID generation failed")

    monkeypatch.setattr("user.generate_uuid", _bad_uuid)

    with pytest.raises(RuntimeError):
        User(name="Grace", email="grace@example.com")