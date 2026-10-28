"""Unit tests for the idle shutdown helpers."""

import json

import pytest

from main import format_time, load_duration, parse_time, save_duration


def test_parse_time_minutes() -> None:
    assert parse_time("30m") == 1800


def test_parse_time_hours() -> None:
    assert parse_time("2h") == 7200


def test_parse_time_strips_whitespace() -> None:
    assert parse_time(" 30m ") == 1800


@pytest.mark.parametrize("value", ["30s", "xm"])
def test_parse_time_rejects_invalid_input(value: str) -> None:
    with pytest.raises(ValueError):
        parse_time(value)


def test_save_duration_then_load_duration(tmp_path) -> None:
    path = tmp_path / "settings.json"

    save_duration("30m", path)

    assert load_duration(path) == "30m"


def test_save_duration_creates_missing_folder(tmp_path) -> None:
    path = tmp_path / "IdleShutdown" / "settings.json"

    save_duration("2h", path)

    assert load_duration(path) == "2h"


def test_load_duration_returns_none_for_missing_file(tmp_path) -> None:
    assert load_duration(tmp_path / "missing.json") is None


def test_load_duration_returns_none_for_invalid_json(tmp_path) -> None:
    path = tmp_path / "settings.json"
    path.write_text("not json", encoding="utf-8")

    assert load_duration(path) is None


def test_load_duration_returns_none_for_invalid_duration(tmp_path) -> None:
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"duration": "30s"}), encoding="utf-8")

    assert load_duration(path) is None


def test_format_time() -> None:
    assert format_time(125) == "2 minutes, 5 seconds"
