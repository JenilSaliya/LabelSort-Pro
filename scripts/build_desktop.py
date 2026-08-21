#!/usr/bin/env python3
"""
LabelSort Pro — Automated Desktop Build Pipeline
Executes full build sequence:
  1. Compiles FastAPI + PyMuPDF sidecar with PyInstaller (--onedir)
  2. Stages sidecar into frontend/src-tauri/binaries/
  3. Builds React/TypeScript frontend (Vite)
  4. Prepares updater signing keys and builds Tauri v2 Windows Installer (NSIS / MSI)
"""

import os
import sys
import base64
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
TAURI_DIR = FRONTEND_DIR / "src-tauri"
BINARIES_DIR = TAURI_DIR / "binaries" / "labelsort-engine"

# Permanent release signing private key matching public key in tauri.conf.json
DEFAULT_PRIVATE_KEY = "dW50cnVzdGVkIGNvbW1lbnQ6IHJzaWduIGVuY3J5cHRlZCBzZWNyZXQga2V5ClJXUlRZMEl5T2ZhZnhNTVNuOXpvSGw0SVZobXNRMkh6RXpDODNSeHVSV0NHQ1pDOStIWUFBQkFBQUFBQUFBQUFBQUlBQUFBQWNOdHgwcG8wK3pYRVQwenNwWGpuZWFvQkdDa2FFeWNUWkkycFdoMHAwaFg5MUwrTVhMWEova2h6Ry9iM0dhdkVaT2NFTG5TTS90U3lFNWdZN2xPNEQrRFhtT2o4emI2Y3Ewdlk0d2VRQlpqN3h3YnRSWUJuWTBtMXRGbjBpQUs0cy9HYVhmeGpMRUU9Cg=="


def run_command(cmd, cwd=ROOT_DIR):
    """Runs a shell command and streams output using current os.environ."""
    print(f"\n[EXEC] {cmd} (cwd: {cwd})")
    res = subprocess.run(cmd, cwd=cwd, shell=True, env=os.environ)
    if res.returncode != 0:
        print(f"[ERROR] Command failed with exit code {res.returncode}: {cmd}")
        sys.exit(res.returncode)


def prepare_signing_key():
    """
    Configures TAURI_SIGNING_PRIVATE_KEY as a clean Base64 string for Tauri v2 CLI.
    Ensures TAURI_SIGNING_PRIVATE_KEY_PASSWORD is set to empty string for passwordless keys.
    """
    key_str = os.environ.get("TAURI_SIGNING_PRIVATE_KEY", "").strip()
    if not key_str:
        print("[SIGNER] Using embedded release signing key...")
        key_str = DEFAULT_PRIVATE_KEY

    # If raw multi-line string was passed, convert to Base64
    if key_str.startswith("untrusted comment:"):
        key_str = base64.b64encode(key_str.encode("utf-8")).decode("utf-8")

    # Strip any accidental newlines or whitespace
    key_str = "".join(key_str.split())

    os.environ["TAURI_SIGNING_PRIVATE_KEY"] = key_str
    os.environ["TAURI_SIGNING_PRIVATE_KEY_PASSWORD"] = ""
    print(f"[OK] Initialized TAURI_SIGNING_PRIVATE_KEY (Base64 length: {len(key_str)})")


def main():
    print("=" * 70)
    print("      LabelSort Pro — Desktop Edition Build Pipeline")
    print("=" * 70)

    # 1. Compile Backend Sidecar with PyInstaller
    print("\n>>> Step 1/4: Compiling Python Backend Sidecar...")
    run_command("pyinstaller pyinstaller.spec --noconfirm", cwd=BACKEND_DIR)

    sidecar_dist = BACKEND_DIR / "dist" / "labelsort-engine"
    if not sidecar_dist.exists() or not (sidecar_dist / "labelsort-engine.exe").exists():
        print("[ERROR] PyInstaller build did not produce labelsort-engine.exe")
        sys.exit(1)

    # 2. Stage Sidecar into Tauri Binaries Directory
    print("\n>>> Step 2/4: Staging sidecar assets to Tauri binaries folder...")
    if BINARIES_DIR.exists():
        shutil.rmtree(BINARIES_DIR, ignore_errors=True)
    BINARIES_DIR.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(sidecar_dist, BINARIES_DIR)
    print(f"[OK] Staged sidecar to {BINARIES_DIR}")

    # 3. Build React Frontend
    print("\n>>> Step 3/4: Compiling React Frontend (Vite)...")
    run_command("npm.cmd run build", cwd=FRONTEND_DIR)

    # 4. Prepare Signing Keys & Build Tauri Desktop Application
    print("\n>>> Step 4/4: Building Tauri v2 Windows Installer...")
    prepare_signing_key()

    if shutil.which("cargo") is not None:
        run_command("npm.cmd run tauri:build", cwd=FRONTEND_DIR)
        print("\n" + "=" * 70)
        print("  BUILD COMPLETE!")
        print("  Installers are available at:")
        print(f"  {TAURI_DIR / 'target' / 'release' / 'bundle' / 'nsis'}")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("[NOTICE] Cargo/Rust is not detected in your current local environment.")
        print("Backend sidecar and frontend web assets have been compiled and staged.")
        print("When Rust is installed or in GitHub Actions CI, run:")
        print("  cd frontend && npm run tauri:build")
        print("=" * 70)


if __name__ == "__main__":
    main()
