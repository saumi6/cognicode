"""
Auto-generated test cases for function: add_days
Generated using: Groq LLM (openai/gpt-oss-20b)
Generated on: 2026-01-30 20:31:13
Source file: date_utils.py
Function signature: def add_days(date_str: str, days: int) -> str
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.date_utils import add_days

import pytest

# NOTE: The function under test is assumed to be available in the test
# environment under the name `add_days`.  No explicit import is performed
# because the test runner will provide the function in the namespace.

@pytest.mark.parametrize(
    "date_str, days, expected",
    [
        # Simple forward addition
        ("2023-01-01", 1, "2023-01-02"),
        ("2023-01-31", 1, "2023-02-01"),
        ("2023-12-31", 1, "2024-01-01"),
        # Leap‑year handling
        ("2020-02-28", 1, "2020-02-29"),
        ("2020-02-28", 2, "2020-03-01"),
        # Zero days
        ("2023-03-15", 0, "2023-03-15"),
    ],
)
def test_add_days_normal_cases(date_str, days, expected):
    """
    Test normal, expected behaviour of `add_days` for a variety of
    typical dates and day offsets.
    """
    result = add_days(date_str, days)
    assert result == expected


def test_add_days_edge_cases():
    """
    Test edge cases such as negative offsets, large offsets that span
    multiple years, and month/year boundaries.
    """
    # Negative offset crossing a year boundary
    assert add_days("2023-01-01", -1) == "2022-12-31"

    # Large offset spanning two years
    assert add_days("2023-01-01", 730) == "2025-01-01"

    # Large offset within a single year (non‑leap)
    assert add_days("2023-01-01", 365) == "2023-12-31"

    # End of month transitions
    assert add_days("2023-04-30", 1) == "2023-05-01"
    assert add_days("2023-02-28", 1) == "2023-03-01"

    # End of February in a leap year
    assert add_days("2024-02-28", 1) == "2024-02-29"

    # Negative offset spanning a full year
    assert add_days("2023-01-01", -365) == "2022-01-01"


def test_add_days_error_cases():
    """
    Test that `add_days` raises appropriate exceptions for invalid
    inputs such as malformed dates, non‑integer day offsets, and
    None values.
    """
    # Malformed date string
    with pytest.raises(ValueError):
        add_days("2023/01/01", 5)

    # Non‑existent date
    with pytest.raises(ValueError):
        add_days("2023-02-30", 1)

    # Non‑integer days
    with pytest.raises(TypeError):
        add_days("2023-01-01", "5")

    # None as date string
    with pytest.raises(TypeError):
        add_days(None, 5)

    # None as days
    with pytest.raises(TypeError):
        add_days("2023-01-01", None)

    # Float days
    with pytest.raises(TypeError):
        add_days("2023-01-01", 5.5)

    # Days as a non‑numeric string
    with pytest.raises(TypeError):
        add_days("2023-01-01", "five")