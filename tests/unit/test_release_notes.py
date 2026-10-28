"""Unit tests for loading and formatting bundled release notes."""

import json
from pathlib import Path

from release_notes import ReleaseNote, format_release_note, load_release_notes


def _write_note(notes_dir: Path, label: str, data: object) -> None:
    folder = notes_dir / label
    folder.mkdir(parents=True)
    (folder / "en.json").write_text(json.dumps(data), encoding="utf-8")


def _note_data(version: str, build: int) -> dict[str, object]:
    return {
        "version": version,
        "build": build,
        "date": "2026-10-28",
        "title": f"Build {build}",
        "notes": ["First change", "Second change"],
    }


def test_load_release_notes_sorts_newest_first(tmp_path) -> None:
    _write_note(tmp_path, "0.1.0_1", _note_data("0.1.0", 1))
    _write_note(tmp_path, "0.2.0_3", _note_data("0.2.0", 3))
    _write_note(tmp_path, "0.1.0_2", _note_data("0.1.0", 2))

    notes = load_release_notes(tmp_path)

    assert [note.build for note in notes] == [3, 2, 1]


def test_load_release_notes_skips_malformed_files(tmp_path) -> None:
    _write_note(tmp_path, "0.1.0_1", _note_data("0.1.0", 1))
    _write_note(tmp_path, "0.1.0_2", {"version": "0.1.0"})
    (tmp_path / "broken").mkdir()
    (tmp_path / "broken" / "en.json").write_text("not json", encoding="utf-8")

    notes = load_release_notes(tmp_path)

    assert [note.build for note in notes] == [1]


def test_load_release_notes_returns_empty_for_missing_dir(tmp_path) -> None:
    assert load_release_notes(tmp_path / "missing") == []


def test_format_release_note() -> None:
    note = ReleaseNote("0.1.0", 1, "2026-10-28", "First release", ["One", "Two"])

    assert format_release_note(note) == (
        "0.1.0 (build 1) - 2026-10-28\nFirst release\n\n- One\n- Two"
    )
