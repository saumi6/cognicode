"""
Auto-generated test cases for function: add_days
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:11:53
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

# The function under test is assumed to be imported in the test module, e.g.:
# from my_package.date_utils import add_days


def test_add_days_normal_cases():
    """Normal usage  adding a positive number of days to a valid ISO date."""
    @pytest.mark.parametrize(
        "date_str, days, expected",
        [
            ("2023-01-01", 1, "2023-01-02"),
            ("2023-01-31", 1, "2023-02-01"),
            ("2023-02-27", 3, "2023-03-02"),
            ("2020-02-28", 1, "2020-02-29"),   # leap year
            ("2020-02-29", 1, "2020-03-01"),
            ("2023-12-31", 1, "2024-01-01"),
            ("2023-04-15", 30, "2023-05-15"),
            ("2023-04-15", 365, "2024-04-14"),
        ],
    )
    def _inner(date_str, days, expected):
        result = add_days(date_str, days)
        assert result == expected

    # Run the parametrized inner test
    _inner()


def test_add_days_edge_cases():
    """Boundary and edgecase scenarios such as zero/negative days and large offsets."""
    # Zero days  should return the original date unchanged
    assert add_days("2023-07-20", 0) == "2023-07-20"

    # Negative days  moving backwards in time
    assert add_days("2023-07-20", -1) == "2023-07-19"
    assert add_days("2020-03-01", -1) == "2020-02-29"   # leapyear backstep
    assert add_days("2021-01-01", -365) == "2020-01-02"

    # Very large positive offset  crossing many years
    assert add_days("2000-01-01", 10_000) == "2027-05-19"

    # Very large negative offset  crossing many years backwards
    assert add_days("2027-05-19", -10_000) == "2000-01-01"


def test_add_days_error_cases():
    """Invalid inputs should raise appropriate exceptions."""
    # Wrong date format
    with pytest.raises(ValueError):
        add_days("2023/01/01", 5)

    # Nonexistent calendar date
    with pytest.raises(ValueError):
        add_days("2023-02-30", 1)

    # Empty string
    with pytest.raises(ValueError):
        add_days("", 3)

    # Nonstring date argument
    with pytest.raises(TypeError):
        add_days(20230101, 2)   # type: ignore[arg-type]

    # Noninteger days argument
    with pytest.raises(TypeError):
        add_days("2023-01-01", "5")   # type: ignore[arg-type]

    # None as input
    with pytest.raises(TypeError):
        add_days(None, 1)   # type: ignore[arg-type]