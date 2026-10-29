@echo off
REM Print the release version (pyproject.toml [project] version).
setlocal
uv run python "%~dp0release\version_number.py" get
set "VERSION_EXIT_CODE=%ERRORLEVEL%"
endlocal & exit /b %VERSION_EXIT_CODE%
