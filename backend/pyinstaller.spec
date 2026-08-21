# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Specification for LabelSort Pro Desktop Engine Sidecar.
Builds a standalone --onedir distribution for integration with Tauri v2.
"""

import sys
import os
from pathlib import Path
from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
    collect_dynamic_libs,
)

# Project root path
SPECPATH = Path(os.path.abspath(SPEC)).parent

# 1. Collect PyMuPDF data, binaries, and hidden submodules
pymupdf_datas = collect_data_files('pymupdf')
pymupdf_binaries = collect_dynamic_libs('pymupdf')
pymupdf_submodules = collect_submodules('pymupdf')

# 2. Collect other dependency assets
fastapi_datas = collect_data_files('fastapi')
starlette_datas = collect_data_files('starlette')
openpyxl_datas = collect_data_files('openpyxl')

# 3. Aggregate all datas and binaries
all_datas = pymupdf_datas + fastapi_datas + starlette_datas + openpyxl_datas
all_binaries = pymupdf_binaries

# 4. Explicitly list all dynamic/hidden imports
hidden_imports = [
    # Uvicorn internals
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.loops.asyncio',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.http.httptools_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.websockets.wsproto_impl',
    'uvicorn.protocols.websockets.websockets_impl',
    'uvicorn.lifespans',
    'uvicorn.lifespans.on',
    'uvicorn.lifespans.off',
    
    # FastAPI & Starlette
    'fastapi',
    'fastapi.applications',
    'fastapi.routing',
    'starlette',
    'starlette.routing',
    'starlette.middleware',
    'starlette.middleware.cors',
    'starlette.middleware.errors',
    'starlette.middleware.exceptions',
    'starlette.responses',
    'starlette.requests',
    
    # Pydantic v2
    'pydantic',
    'pydantic_core',
    'pydantic_settings',
    
    # PyMuPDF (fitz)
    'pymupdf',
    'pymupdf._mupdf',
    'pymupdf.mupdf',
    'fitz',
    
    # File processing & exports
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.styles',
    'pypdf',
    'multipart',
    'python_multipart',
    'dotenv',
    
    # Standard library dynamics
    'email.mime',
    'email.mime.multipart',
    'email.mime.text',
] + pymupdf_submodules

block_cipher = None

a = Analysis(
    ['desktop_entry.py'],
    pathex=[str(SPECPATH)],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'numpy.testing',
        'pytest',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='labelsort-engine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True for development/testing; Tauri launches it headless in background
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='labelsort-engine',
)
