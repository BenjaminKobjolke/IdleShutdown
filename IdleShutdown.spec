# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec: builds dist/IdleShutdown/IdleShutdown.exe (onedir, windowed).
# Onedir over onefile: no per-launch temp extraction, and the NSIS installer
# packs the folder anyway. UPX off: slows load, trips antivirus.
# Build via tools/build_exe.bat.

# release_notes/ travels inside the build so the in-app Release notes view works.
datas = [('release_notes', 'release_notes')]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='IdleShutdown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # no console window (matches pythonw behavior)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='IdleShutdown',
)
