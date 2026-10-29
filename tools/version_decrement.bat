@echo off
REM Roll the last version segment in pyproject.toml back by one and print it.
setlocal
uv run python "%~dp0release\version_number.py" decrement
set "VERSION_EXIT_CODE=%ERRORLEVEL%"
endlocal & exit /b %VERSION_EXIT_CODE%
