@echo off
REM Copy releases\windows\IdleShutdown_v<label>.exe to the stable name IdleShutdown.exe
REM (constant download URL and [GitHubRelease] asset) and verify the copy byte for byte.
REM Usage: stage_installer.bat <label>
setlocal
set "OUTDIR=%~dp0..\releases\windows"
set "INSTALLER=%OUTDIR%\IdleShutdown_v%~1.exe"
set "STABLE=%OUTDIR%\IdleShutdown.exe"
if not exist "%INSTALLER%" (
    echo [stage_installer] Installer not found: %INSTALLER%
    exit /b 1
)
copy /y "%INSTALLER%" "%STABLE%" >nul
fc /b "%INSTALLER%" "%STABLE%" >nul
if errorlevel 1 (
    echo [stage_installer] %STABLE% does not match %INSTALLER%.
    exit /b 1
)
exit /b 0
