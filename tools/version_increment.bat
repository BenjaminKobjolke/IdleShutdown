@echo off
REM Bump the last version segment in pyproject.toml (0.1.0 -> 0.1.1) and print it.
setlocal
uv run python "%~dp0release\version_number.py" increment
set "VERSION_EXIT_CODE=%ERRORLEVEL%"
endlocal & exit /b %VERSION_EXIT_CODE%
