"""
Auto-generated test cases for function: __init__
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:10:06
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

# The Logger class lives in the ``test_repo.logger`` module (the file name is
# ``logger.py`` without the ``.py`` extension).  Import it using the full import
# path so that the test runner can locate it correctly.
from test_repo.logger import Logger


@pytest.mark.parametrize(
    "name_input, expected_name",
    [
        ("app", "app"),
        ("MyLogger", "MyLogger"),
        ("", ""),                         # empty string  still a valid name
        ("   spaced   ", "   spaced   "), # leading/trailing spaces are kept
        ("", ""),               # unicode / emoji characters
        ("a" * 1024, "a" * 1024),         # long string (1KB)
    ],
)
def test___init___normal_cases(name_input, expected_name):
    """
    Normal usage of ``Logger.__init__``  the provided ``name`` should be stored
    unchanged on the instance.
    """
    logger = Logger(name_input)
    assert hasattr(logger, "name"), "Logger instance should have a ``name`` attribute"
    assert logger.name == expected_name


def test___init___edge_cases():
    """
    Edgecase values for the ``name`` argument.
    """
    # 0length string (already covered in normal cases, but we repeat for clarity)
    logger_empty = Logger("")
    assert logger_empty.name == ""

    # Very long string (10KB)  ensure the attribute can hold large data
    long_name = "x" * 10_240
    logger_long = Logger(long_name)
    assert logger_long.name == long_name
    assert len(logger_long.name) == 10_240

    # String subclass  ``isinstance`` should still be ``str`` and the value stored
    class MyStr(str):
        pass

    subclass_name = MyStr("subclass")
    logger_sub = Logger(subclass_name)
    assert isinstance(logger_sub.name, str)
    assert logger_sub.name == "subclass"


def test___init___error_cases():
    """
    Error cases for ``Logger.__init__``  calling the method with an incorrect
    signature should raise ``TypeError``.
    """
    # Missing the required ``name`` argument
    with pytest.raises(TypeError):
        Logger.__init__(Logger)  # ``self`` is supplied implicitly, but ``name`` is missing

    # Providing too many positional arguments
    with pytest.raises(TypeError):
        Logger("first", "second")  # ``__init__`` expects only one positional argument after ``self``

    # Supplying ``None`` as the name is technically allowed (it will be stored as ``None``),
    # but if the implementation later expects a string, this is a logical error.
    # Here we only verify that the constructor itself does **not** raise.
    logger_none = Logger(None)  # should succeed
    assert logger_none.name is None