"""
Auto-generated test cases for function: round_currency
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 03:44:22
Source file: math_tools.py
Function signature: def round_currency(amount: float) -> float
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.math_tools import round_currency

import pytest

# The function under test is assumed to be imported in the test module, e.g.:
# from my_package.math_tools import round_currency
# The import itself will be added by the test runner, so we call it directly.


@pytest.mark.parametrize(
    "input_val, expected",
    [
        (0.0, 0.0),                     # zero stays zero
        (1.2, 1.2),                     # already at 1dp stays the same
        (1.234, 1.23),                  # normal rounding down
        (1.235, 1.24),                  # normal rounding up
        (1234.5678, 1234.57),           # larger number
        (-2.345, -2.35),                # negative number rounding up (away from zero)
        (-2.344, -2.34),                # negative number rounding down (toward zero)
        (9.999, 10.0),                  # rounding causes a carry to the integer part
        (0.005, 0.01),                  # smallest positive that rounds up
        (-0.005, -0.01),                # smallest negative that rounds down
    ],
)
def test_round_currency_normal_cases(input_val, expected):
    """
    Test typical, everyday inputs for ``round_currency``.
    """
    result = round_currency(input_val)
    # ``pytest.approx`` handles the tiny floatingpoint representation differences.
    assert result == pytest.approx(expected, rel=1e-12)


def test_round_currency_edge_cases():
    """
    Test boundary and edgecase values such as very large numbers,
    very small numbers, and values that sit exactly on the rounding
    halfway point.
    """
    # Very large magnitude
    large = 9_999_999_999.9999
    assert round_currency(large) == pytest.approx(9_999_999_999.99, rel=1e-12)

    # Very small magnitude (close to zero but not zero)
    tiny = 1e-10
    assert round_currency(tiny) == pytest.approx(0.0, rel=1e-12)

    # Halfway cases  Python's builtin round uses bankers rounding
    # (round to the nearest even digit). The implementation is expected
    # to follow the same rule unless documented otherwise.
    assert round_currency(2.125) == pytest.approx(2.12, rel=1e-12)   # 2.12 is even at the 2dp place
    assert round_currency(2.135) == pytest.approx(2.14, rel=1e-12)   # 2.14 is even at the 2dp place

    # Negative halfway case
    assert round_currency(-2.125) == pytest.approx(-2.12, rel=1e-12)


@pytest.mark.parametrize(
    "bad_input",
    [
        None,
        "123.45",
        [1.23],
        {"amount": 1.23},
        (1.23,),
        complex(1, 2),
    ],
)
def test_round_currency_error_cases(bad_input):
    """
    Verify that ``round_currency`` raises an appropriate exception
    when supplied with values that are not real numbers.
    """
    with pytest.raises((TypeError, ValueError)):
        round_currency(bad_input)