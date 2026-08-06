# PyInstaller spec per generare il sidecar del backend PromptArchive.
#
# Uso (dalla RADICE del repo, con venv attivo e pyinstaller installato):
#
#   pip install -r backend/requirements.txt pyinstaller
#   pyinstaller promptarchive_backend.spec
#
# Genera dist/promptarchive-backend(.exe), da rinominare/spostare in
# src-tauri/binaries/promptarchive-backend-<target-triple><ext>
# (vedi .github/workflows/build-windows.yml per il nome esatto su Windows).

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['sidecar_entry.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'backend',
        'backend.main',
        'backend.models',
        'backend.database',
        'backend.deps',
        'backend.migrations',
        'backend.seed',
        'backend.crud',
        'backend.schemas',
        'backend.routers',
        'backend.routers.prompts',
        'backend.routers.folders',
        'backend.routers.categories',
        'backend.routers.settings',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'sqlalchemy.sql.default_comparator',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='promptarchive-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
