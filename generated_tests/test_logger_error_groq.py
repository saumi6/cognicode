"""
Auto-generated test cases for function: error
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-04-03 04:00:45
Source file: logger.py
Function signature: def error(self, message: str)
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
from logger import Logger  # <-- adjust the import path to where the Logger class lives


@pytest.mark.parametrize(
    "logger_name,message,expected_timestamp",
    [
        ("app", "something went wrong", "2023-01-01 00:00:00"),
        ("service", "failed to connect", "1999-12-31 23:59:59"),
        ("worker", "unexpected error", "2025-07-15 12:34:56"),
    ],
)
def test_error_normal_cases(monkeypatch, capsys, logger_name, message, expected_timestamp):
    """Verify that ``Logger.error`` prints the correctly formatted string for normal inputs."""
    # Mock the timestamp function used inside Logger.error
    monkeypatch.setattr(
        "logger.get_current_timestamp",  # full absolute import path
        lambda: expected_timestamp,
    )

    logger = Logger(logger_name)
    logger.error(message)

    captured = capsys.readouterr()
    # Expected format: [ERROR] <timestamp> [<logger_name>]: <message>
    expected_output = f"[ERROR] {expected_timestamp} [{logger_name}]: {message}\n"
    assert captured.out == expected_output


def test_error_edge_cases(monkeypatch, capsys):
    """Test edgecase inputs such as empty strings, very long messages and special characters."""
    fixed_ts = "2022-02-22 22:22:22"
    monkeypatch.setattr("logger.get_current_timestamp", lambda: fixed_ts)

    # 1. Empty logger name and empty message
    logger = Logger("")
    logger.error("")
    out = capsys.readouterr().out
    assert out == f"[ERROR] {fixed_ts} []: \n"

    # 2. Very long message
    long_msg = "A" * 10_000  # 10k characters
    logger = Logger("long_msg_logger")
    logger.error(long_msg)
    out = capsys.readouterr().out
    assert out == f"[ERROR] {fixed_ts} [long_msg_logger]: {long_msg}\n"

    # 3. Message with Unicode and control characters
    special_msg = "Error \nNewLine\tTab\bBackspace"
    logger = Logger("unicode")
    logger.error(special_msg)
    out = capsys.readouterr().out
    # The newline inside the message will be printed as a real newline, so we compare the raw string
    expected = f"[ERROR] {fixed_ts} [unicode]: {special_msg}\n"
    assert out == expected


def test_error_error_cases(monkeypatch, capsys):
    """Ensure that unexpected failures inside ``Logger.error`` are propagated."""
    # Mock the timestamp function to a normal value
    monkeypatch.setattr("logger.get_current_timestamp", lambda: "2021-01-01 00:00:00")

    class BadStr:
        """Object whose __str__ raises an exception."""

        def __str__(self):
            raise ValueError("cannot convert to string")

    logger = Logger("bad_logger")

    # Passing an object that raises in __str__ should propagate the exception
    with pytest.raises(ValueError, match="cannot convert to string"):
        logger.error(BadStr())

    # The function should not have printed anything before the exception was raised
    captured = capsys.readouterr()
    assert captured.out == ""