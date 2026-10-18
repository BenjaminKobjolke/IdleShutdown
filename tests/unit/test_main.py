"""Unit tests for the idle shutdown helpers."""

import pytest

from main import format_time, parse_time


def test_parse_time_minutes() -> None:
    assert parse_time("30m") == 1800


def test_parse_time_hours() -> None:
    assert parse_time("2h") == 7200


@pytest.mark.parametrize("value", ["30s", "xm"])
def test_parse_time_rejects_invalid_input(value: str) -> None:
    with pytest.raises(SystemExit):
        parse_time(value)


def test_format_time() -> None:
    assert format_time(125) == "2 minutes, 5 seconds"
