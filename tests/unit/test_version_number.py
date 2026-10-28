"""Unit tests for the semver release helper in tools/release/version_number.py."""

import pytest

from tools.release.version_number import read_version, shift_patch

PYPROJECT = (
    '[project]\nname = "app"\nversion = "0.1.9"\n\n[tool.ruff]\nversion = "0.1.9"\n'
)


def test_read_version(tmp_path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text(PYPROJECT, encoding="utf-8")

    assert read_version(path) == "0.1.9"


def test_shift_patch_increments_only_the_project_version(tmp_path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_bytes(PYPROJECT.encode("utf-8"))

    assert shift_patch(1, path) == "0.1.10"
    assert path.read_bytes().decode("utf-8") == PYPROJECT.replace(
        'name = "app"\nversion = "0.1.9"', 'name = "app"\nversion = "0.1.10"'
    )


def test_shift_patch_rolls_back(tmp_path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text(PYPROJECT, encoding="utf-8")

    shift_patch(1, path)

    assert shift_patch(-1, path) == "0.1.9"


def test_shift_patch_refuses_negative_patch(tmp_path) -> None:
    path = tmp_path / "pyproject.toml"
    path.write_text('[project]\nversion = "0.2.0"\n', encoding="utf-8")

    with pytest.raises(ValueError):
        shift_patch(-1, path)
