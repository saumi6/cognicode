"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:11:01
Source file: logger.py
Function signature: def __init__(self, name: str)
"""

import pytest
import sys
import os
from typing import Any, Dict, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, r"C:\Users\gurav\prog\college\BE Proj\cognicode")

# Import the function to be tested
from test_repo.logger import Logger

import pytest

# Adjust the import path to match the location of the Logger class.
# For example, if the class is defined in `logger.py` in the same directory,
# the following import works.  Change it if the module name is different.
from logger import Logger


@pytest.mark.parametrize(
    "name_input, expected_name",
    [
        ("app", "app"),
        ("MyLogger", "MyLogger"),
        ("", ""),                         # empty string  still a valid name
        ("", ""),                  # unicode characters
        ("a" * 1024, "a" * 1024),        # long string (1KB)
    ],
)
def test___init___normal_cases(name_input, expected_name):
    """Verify that the Logger stores the provided name unchanged for typical inputs."""
    logger = Logger(name_input)
    assert hasattr(logger, "name"), "Logger instance should have a `name` attribute"
    assert logger.name == expected_name, "The stored name should match the input value"


def test___init___edge_cases():
    """Test boundary and edgecase values for the `name` argument."""
    # 1. Whitespaceonly name
    whitespace_name = "   \t\n"
    logger_ws = Logger(whitespace_name)
    assert logger_ws.name == whitespace_name

    # 2. Name that looks like a number but is a string
    numeric_string = "12345"
    logger_num = Logger(numeric_string)
    assert logger_num.name == numeric_string

    # 3. Very long name (10KB)
    long_name = "x" * 10_240
    logger_long = Logger(long_name)
    assert logger_long.name == long_name
    assert len(logger_long.name) == 10_240

    # 4. Name containing control characters
    control_name = "log\x00name\x1F"
    logger_ctrl = Logger(control_name)
    assert logger_ctrl.name == control_name


def test___init___error_cases():
    """Check that incorrect usage of the constructor raises the appropriate Python errors."""
    # 1. Missing required positional argument
    with pytest.raises(TypeError):
        Logger()                     # type: ignore[arg-type]

    # 2. Too many positional arguments
    with pytest.raises(TypeError):
        Logger("valid_name", "extra_arg")   # type: ignore[arg-type]

    # 3. Passing a nonstring that cannot be represented (e.g., a bytes object)
    #    The implementation does not enforce type checking, so this should *not* raise.
    #    We include it here to demonstrate that the error case is limited to signature misuse.
    #    (If future validation is added, this test will start failing, signalling a change.)
    with pytest.raises(TypeError):
        # Force a TypeError by calling the unbound __init__ directly with a wrong `self`.
        Logger.__init__(None, "name")  # type: ignore[arg-type]