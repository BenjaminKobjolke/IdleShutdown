; IdleShutdown - Windows installer.
;
; Built by tools\build_release.bat, which passes VERSION, SRCDIR and OUTFILE
; as /D defines. The bat is the single place that knows the release version.

!ifndef VERSION
  !error "VERSION not defined - build via tools\build_release.bat, not makensis directly"
!endif

!define APPNAME   "IdleShutdown"
!define EXENAME   "IdleShutdown.exe"
!define COMPANY   "XIDA GmbH"
!define REGKEY    "Software\Microsoft\Windows\CurrentVersion\Uninstall\IdleShutdown"

Name "${APPNAME}"
OutFile "${OUTFILE}"
Unicode true
SetCompressor /SOLID lzma

; Per-user install, no admin, no UAC prompt. Settings live in %APPDATA%\IdleShutdown.
RequestExecutionLevel user
InstallDir "$LOCALAPPDATA\IdleShutdown"
InstallDirRegKey HKCU "${REGKEY}" "InstallLocation"

; VIProductVersion needs four numeric parts; the semver version has three.
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName"     "${APPNAME}"
VIAddVersionKey "CompanyName"     "${COMPANY}"
VIAddVersionKey "FileDescription" "${APPNAME} Setup"
VIAddVersionKey "FileVersion"     "${VERSION}"
VIAddVersionKey "LegalCopyright"  "${COMPANY}"

!include "MUI2.nsh"
!insertmacro MUI_PAGE_LICENSE "..\LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

; Overwriting a running exe fails with a locked-file error, and a countdown may
; be running during an upgrade. A non-zero taskkill exit just means it was not running.
!macro KillRunning
  DetailPrint "Closing any running ${EXENAME}..."
  nsExec::Exec 'taskkill /F /IM "${EXENAME}"'
  Pop $0
!macroend

Section "${APPNAME}" SEC_APP
  SectionIn RO
  !insertmacro KillRunning

  SetOutPath "$INSTDIR"
  File /r "${SRCDIR}\*.*"

  CreateShortCut "$SMPROGRAMS\${APPNAME}.lnk" "$INSTDIR\${EXENAME}"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  WriteRegStr HKCU "${REGKEY}" "DisplayName"     "${APPNAME}"
  WriteRegStr HKCU "${REGKEY}" "DisplayVersion"  "${VERSION}"
  WriteRegStr HKCU "${REGKEY}" "Publisher"       "${COMPANY}"
  WriteRegStr HKCU "${REGKEY}" "DisplayIcon"     "$INSTDIR\${EXENAME}"
  WriteRegStr HKCU "${REGKEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${REGKEY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegDWORD HKCU "${REGKEY}" "NoModify" 1
  WriteRegDWORD HKCU "${REGKEY}" "NoRepair" 1
SectionEnd

Section /o "Desktop shortcut" SEC_DESKTOP
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXENAME}"
SectionEnd

Section "Uninstall"
  !insertmacro KillRunning

  Delete "$SMPROGRAMS\${APPNAME}.lnk"
  Delete "$DESKTOP\${APPNAME}.lnk"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$INSTDIR\${EXENAME}"
  RMDir /r "$INSTDIR\_internal"
  RMDir "$INSTDIR"

  DeleteRegKey HKCU "${REGKEY}"
SectionEnd
