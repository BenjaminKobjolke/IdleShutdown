"""Load the bundled release notes and show them newest first in a Tk window."""

import json
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path

NOTES_FILE_NAME = "en.json"


@dataclass(frozen=True)
class ReleaseNote:
    version: str
    date: str
    title: str
    notes: list[str]


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def load_release_notes(notes_dir: Path) -> list[ReleaseNote]:
    releases = []
    for path in notes_dir.glob(f"*/{NOTES_FILE_NAME}"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            release = ReleaseNote(
                version=str(data["version"]),
                date=str(data["date"]),
                title=str(data["title"]),
                notes=[str(note) for note in data["notes"]],
            )
            _version_key(release.version)  # reject a non-numeric version here
            releases.append(release)
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ):
            continue  # one broken release must not hide the others
    return sorted(
        releases, key=lambda release: _version_key(release.version), reverse=True
    )


def format_release_note(release: ReleaseNote) -> str:
    bullets = "\n".join(f"- {note}" for note in release.notes)
    return f"{release.version} - {release.date}\n{release.title}\n\n{bullets}"


def show_release_notes(parent: tk.Misc, notes_dir: Path) -> None:
    releases = load_release_notes(notes_dir)
    window = tk.Toplevel(parent)
    window.title("Release notes")

    text = tk.Label(
        window, justify="left", anchor="w", wraplength=400, padx=20, pady=20
    )
    text.pack(fill="both", expand=True)
    navigation = tk.Frame(window)
    navigation.pack(pady=(0, 10))
    position = {"index": 0}

    def render() -> None:
        if not releases:
            text.config(text="No release notes available.")
            older.config(state="disabled")
            newer.config(state="disabled")
            return
        index = position["index"]
        text.config(text=format_release_note(releases[index]))
        older.config(state="normal" if index < len(releases) - 1 else "disabled")
        newer.config(state="normal" if index > 0 else "disabled")

    def move(step: int) -> None:
        position["index"] += step
        render()

    older = tk.Button(navigation, text="Older", command=lambda: move(1))
    older.pack(side="left", padx=5)
    newer = tk.Button(navigation, text="Newer", command=lambda: move(-1))
    newer.pack(side="left", padx=5)
    render()
