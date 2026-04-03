"""
Auto-generated test cases for function: is_expired
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:11:36
Source file: date_utils.py
Function signature: def is_expired(expiry_date_str: str) -> bool
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.date_utils import is_expired

import datetime
import pytest

# The function under test is assumed to be imported in the test module, e.g.:
# from my_package.date_utils import is_expired


@pytest.mark.parametrize(
    "expiry_str, expected",
    [
        ("2023-01-10", True),   # clearly before the reference today
        ("2023-01-20", False),  # clearly after the reference today
        ("2023-01-15", False),  # same day  not considered expired
    ],
)
def test_is_expired_normal_cases(monkeypatch, expiry_str, expected):
    """Typical past / future / present dates."""
    # Fix today to 20230115 for deterministic testing
    fixed_today = datetime.date(2023, 1, 15)

    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_today

    # Patch the datetime.date class used inside `is_expired`
    monkeypatch.setattr(datetime, "date", MockDate)

    result = is_expired(expiry_str)
    assert result is expected


@pytest.mark.parametrize(
    "today_iso, expiry_str, expected",
    [
        # Leapyear edge: 20240229 is before 20240301
        ("2024-03-01", "2024-02-29", True),
        # Endofyear rollover
        ("2023-12-31", "2024-01-01", False),
        # Very old date
        ("2000-01-01", "1900-01-01", True),
        # Very far future date
        ("2000-01-01", "2100-12-31", False),
        # Same day but with a different format that should still be parsed (if supported)
        ("2023-05-05", "2023-05-05", False),
    ],
)
def test_is_expired_edge_cases(monkeypatch, today_iso, expiry_str, expected):
    """Boundary conditions such as leap years, yearend, and extreme dates."""
    fixed_today = datetime.date.fromisoformat(today_iso)

    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_today

    monkeypatch.setattr(datetime, "date", MockDate)

    result = is_expired(expiry_str)
    assert result is expected


@pytest.mark.parametrize(
    "bad_input",
    [
        "2023/01/01",   # wrong separator
        "01-01-2023",   # unsupported order
        "not-a-date",   # nonsense string
        "",             # empty string
        None,           # None instead of str
        12345,          # nonstring type
    ],
)
def test_is_expired_error_cases(bad_input):
    """Invalid inputs should raise a ValueError."""
    with pytest.raises(ValueError):
        is_expired(bad_input)
These three test functions cover:

1. **Normal cases**  typical past, future, and present dates with a fixed today.
2. **Edge cases**  leapyear handling, yearend transition, extremely old/future dates, and sameday comparison.
3. **Error cases**  malformed strings, empty input, `None`, and nonstring types, all of which must raise `ValueError`.