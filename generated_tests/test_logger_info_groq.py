"""
Auto-generated test cases for function: info
Generated using: Groq LLM (openai/gpt-oss-120b)
Generated on: 2026-05-01 00:10:46
Source file: logger.py
Function signature: def info(self, message: str)
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

import builtins
import pytest
from test_repo.logger import Logger  # the module that contains the Logger class


@pytest.mark.parametrize(
    "logger_name,message,expected_ts",
    [
        ("app", "started", "2023-01-01 00:00:00"),
        ("service-1", "processing request", "2023-12-31 23:59:59"),
        ("my_logger", "finished successfully", "1970-01-01 00:00:00"),
    ],
)
def test_info_normal_cases(monkeypatch, capsys, logger_name, message, expected_ts):
    """
    Normal behaviour: ``info`` should print a line that contains the
    log level, the timestamp, the logger name and the message.
    """
    # make the timestamp deterministic
    monkeypatch.setattr(
        "test_repo.logger.get_current_timestamp", lambda: expected_ts
    )

    logger = Logger(logger_name)
    logger.info(message)

    captured = capsys.readouterr().out.strip()
    # expected format: [INFO] <timestamp> [<name>]: <message>
    assert captured == f"[INFO] {expected_ts} [{logger_name}]: {message}"


def test_info_edge_cases(monkeypatch, capsys):
    """
    Edge cases such as empty strings, very long messages and special
    characters in the logger name.
    """
    # deterministic timestamp for all edge cases
    monkeypatch.setattr(
        "test_repo.logger.get_current_timestamp", lambda: "2025-05-05 05:05:05"
    )

    # 1. empty logger name and empty message
    logger = Logger("")
    logger.info("")
    out = capsys.readouterr().out.strip()
    assert out == "[INFO] 2025-05-05 05:05:05 []: "

    # 2. logger name with special characters and a multiline message
    special_name = "_logger-"
    multiline_message = "first line\nsecond line\r\nthird line"
    logger = Logger(special_name)
    logger.info(multiline_message)
    out = capsys.readouterr().out.strip()
    assert out == f"[INFO] 2025-05-05 05:05:05 [{special_name}]: {multiline_message}"

    # 3. very long message (over 10000 characters)
    long_message = "x" * 12_000
    logger = Logger("long_msg_logger")
    logger.info(long_message)
    out = capsys.readouterr().out.strip()
    assert out.startswith("[INFO] 2025-05-05 05:05:05 [long_msg_logger]: ")
    assert out.endswith(long_message)
    # ensure the length of the printed part after the prefix matches the message length
    printed_msg = out.split(": ", 1)[1]
    assert len(printed_msg) == len(long_message)


def test_info_error_cases(monkeypatch):
    """
    ``info`` should propagate exceptions raised by its dependencies.
    the exception bubbles up.
    """
    # make the timestamp function raise a RuntimeError
    def broken_timestamp():
        raise RuntimeError("timestamp failure")

    monkeypatch.setattr(
        "test_repo.logger.get_current_timestamp", broken_timestamp
    )

    logger = Logger("faulty_logger")
    with pytest.raises(RuntimeError) as excinfo:
        logger.info("this will not be printed")
    assert "timestamp failure" in str(excinfo.value)