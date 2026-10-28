@echo off
REM Build a signed release installer for the current label (tools\version_get.bat).
REM tools\release_create.bat bumps the build counter before calling this; run
REM tools\build_increment.bat first when building by hand.
REM On success: releases\windows\IdleShutdown_v<label>.exe, its stable-name copy
REM IdleShutdown.exe (the FTP and GitHub asset) and release_version.txt holding the
REM completed label; publish_release.bat ships that build, not the current source label.
setlocal
for %%I in ("%~dp0..") do set "PROJECT_ROOT=%%~fI"
set "OUTDIR=%PROJECT_ROOT%\releases\windows"
set "APP_EXE=%PROJECT_ROOT%\dist\IdleShutdown\IdleShutdown.exe"

echo [build_release] Running unit tests...
call "%~dp0run_tests.bat"
if errorlevel 1 (
    echo [build_release] Tests failed; aborting.
    exit /b 1
)

for /f "usebackq delims=" %%I in (`call "%~dp0version_get.bat"`) do set "LABEL=%%I"
for /f "tokens=1,2 delims=_" %%A in ("%LABEL%") do (
    set "VERSION=%%A"
    set "BUILD=%%B"
)
if not defined BUILD (
    echo [build_release] Could not read the release label; aborting.
    exit /b 1
)
echo [build_release] Release label: %LABEL%

set "MAKENSIS=%ProgramFiles(x86)%\NSIS\makensis.exe"
if not exist "%MAKENSIS%" set "MAKENSIS=%ProgramFiles%\NSIS\makensis.exe"
if not exist "%MAKENSIS%" for %%I in (makensis.exe) do set "MAKENSIS=%%~$PATH:I"
if not exist "%MAKENSIS%" (
    echo [build_release] makensis.exe not found. Install NSIS: https://nsis.sourceforge.io/
    exit /b 1
)

REM Rebuilding the recorded label overwrites its installer in place, so drop the
REM record first: a failed rebuild must not leave a half-built pair publishable.
set "RECORD=%OUTDIR%\release_version.txt"
set "RECORDED="
if exist "%RECORD%" set /p "RECORDED="<"%RECORD%"
if "%RECORDED%"=="%LABEL%" del "%RECORD%"

call "%~dp0build_exe.bat"
if errorlevel 1 (
    echo [build_release] PyInstaller build failed; aborting.
    exit /b 1
)

REM Sign the app exe BEFORE packaging - the signed binary has to end up inside the installer.
call "%~dp0sign_exe.bat" "%APP_EXE%"
if errorlevel 1 exit /b 1

if not exist "%OUTDIR%" mkdir "%OUTDIR%"
set "INSTALLER=%OUTDIR%\IdleShutdown_v%LABEL%.exe"
"%MAKENSIS%" /DVERSION=%VERSION% /DBUILD=%BUILD% /DSRCDIR="%PROJECT_ROOT%\dist\IdleShutdown" /DOUTFILE="%INSTALLER%" "%PROJECT_ROOT%\installer\setup.nsi"
if errorlevel 1 (
    echo [build_release] Installer build failed; aborting.
    exit /b 1
)

call "%~dp0sign_exe.bat" "%INSTALLER%"
if errorlevel 1 exit /b 1

call "%~dp0stage_installer.bat" "%LABEL%"
if errorlevel 1 exit /b 1

>"%RECORD%" (echo %LABEL%)
echo [build_release] Recorded completed build %LABEL% in %RECORD%
echo [build_release] Done: %INSTALLER%
exit /b 0
