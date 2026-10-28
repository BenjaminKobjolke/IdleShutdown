# Creating a New Release

A release is identified by the label **`<version>_<build>`**, e.g. `0.1.0_1`:
- `version` (semver) — `pyproject.toml` `[project] version`, bumped by hand for
  feature or breaking changes.
- `build` (integer) — `build_version.txt` at the project root. It holds the last
  shipped build and never resets across versions (`0` = nothing shipped yet).

## One-command release (normal way)

```bat
tools\release_create.bat
```

Configured by `tools/release_create.ini`, run by `release-tool create`
(`RELEASE_TOOL_DIR` in `tools\config.bat`). It:

1. bumps the build counter (`tools\build_increment.bat`) — the only bump per release,
2. writes `release_notes/<label>/en.json` if it is missing,
3. runs `tools\build_release.bat` (rolls the counter back with
   `tools\build_decrement.bat` if the build fails),
4. asks **Publish to Website?** — runs `tools\publish_release.bat` (FTP upload),
5. asks **Commit, tag and push?** — commit `RELEASE (idle-shutdown): <label>`, tag `<label>`,
6. asks **Create GitHub Release?** — `gh release create <label>` with
   `releases/windows/IdleShutdownSetup.exe` attached (needs `gh auth login`).

Add `--dry-run` to preview everything without running it.

Local, gitignored files a fresh clone needs:
- `tools\config.bat` — copy `tools\config_example.bat` (`RELEASE_TOOL_DIR`,
  `SIGNING_PROFILE`).
- `tools\publish_settings.ini` — copy `tools\publish_settings_example.ini`. FTP
  credentials come from the `workflow-tools.com - apps` profile in
  `release-tool\ftp_profiles.ini`.

## 1. Version & build number

```bat
tools\version_get.bat       :: prints <version>_<build>
tools\build_get.bat         :: prints the build number
tools\build_increment.bat   :: bump build before a release
tools\build_decrement.bat   :: undo
```

All four call `tools/release/build_number.py`.

## 2. Release notes + en.json

Create `release_notes/<version>_<build>/en.json`. The release text is the `notes` array:

```json
{
  "version": "0.1.0",
  "build": 1,
  "date": "YYYY-MM-DD",
  "title": "Short headline",
  "notes": ["First change", "Second change"]
}
```

**Author only `en.json`.** The app ships English only (`english_only = true`);
there is no translation step.

## 3. Build the release

```bat
tools\build_increment.bat
tools\build_release.bat
```

`tools\build_release.bat`:
1. runs the unit tests,
2. freezes the app with PyInstaller (`tools\build_exe.bat`, `IdleShutdown.spec`) into
   `dist\IdleShutdown\` — `release_notes/` is bundled inside,
3. **signs `IdleShutdown.exe` before packaging** (`tools\sign_exe.bat` runs
   `release-tool sign` with the `SIGNING_PROFILE` from `tools\config.bat`, default
   `xida remote` in `release-tool\signing_profiles.ini`),
4. builds the NSIS installer (`installer\setup.nsi`) to
   `releases\windows\IdleShutdown_v<label>.exe` and signs it,
5. copies it to the stable name `releases\windows\IdleShutdownSetup.exe` — the file
   uploaded to the website and attached to the GitHub Release. It must not be
   called `IdleShutdown.exe`: the installer closes running `IdleShutdown.exe`
   processes with `taskkill`, which would then kill the installer itself,
6. records the completed label in `releases\windows\release_version.txt`.

## 4. Publish

`tools\publish_release.bat [previous-online-label] [label-to-ship]` uploads the
build recorded in `release_version.txt` (not the current source label) under the
stable name to `/downloads/idle-shutdown/`; the previous remote file is archived
to `versions/<previous-label>/`. Signing is already done, so `[PreSigning]` is off.

Retry publishing an existing build without rebuilding or bumping:

```bat
tools\publish_release.bat 0.1.0_1 0.1.0_2
```

## 5. In-app Release notes view

The **Release notes** button in the countdown window (`main.py`) opens
`release_notes.py` `show_release_notes`: newest release first (sorted by build),
**Older**/**Newer** buttons to page through, and "No release notes available."
when none are bundled.
