@echo off
REM Freeze main.py into dist\IdleShutdown\IdleShutdown.exe (onedir, no console).
pushd "%~dp0.."
uv run pyinstaller IdleShutdown.spec --noconfirm --clean
set "BUILD_EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %BUILD_EXIT_CODE%
