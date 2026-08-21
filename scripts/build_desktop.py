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
import json
import base64
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
TAURI_DIR = FRONTEND_DIR / "src-tauri"
BINARIES_DIR = TAURI_DIR / "binaries" / "labelsort-engine"


def run_command(cmd, cwd=ROOT_DIR):
    """Runs a shell command and streams output using current os.environ."""
    print(f"\n[EXEC] {cmd} (cwd: {cwd})")
    res = subprocess.run(cmd, cwd=cwd, shell=True, env=os.environ)
    if res.returncode != 0:
        print(f"[ERROR] Command failed with exit code {res.returncode}: {cmd}")
        sys.exit(res.returncode)


def prepare_signing_key():
    """
    Ensures a valid signing key is always present for Tauri v2 updater artifacts.
    1. If TAURI_SIGNING_PRIVATE_KEY is supplied via GitHub Secrets, normalizes it and writes to .signing.key.
    2. If NOT supplied, generates a valid keypair on the fly, updates tauri.conf.json pubkey, and sets the key path.
    This guarantees the build NEVER crashes on missing secrets.
    """
    raw_key = os.environ.get("TAURI_SIGNING_PRIVATE_KEY", "").strip()
    key_file = TAURI_DIR / ".signing.key"
    pub_file = TAURI_DIR / ".signing.key.pub"

    if raw_key:
        print("[SIGNER] Using TAURI_SIGNING_PRIVATE_KEY from environment...")
        key_text = raw_key
        if not raw_key.startswith("untrusted comment:"):
            try:
                decoded = base64.b64decode(raw_key).decode("utf-8")
                if decoded.startswith("untrusted comment:"):
                    key_text = decoded
            except Exception:
                pass

        if not key_text.endswith("\n"):
            key_text += "\n"

        key_file.write_text(key_text, encoding="utf-8")
        os.environ["TAURI_SIGNING_PRIVATE_KEY_PATH"] = str(key_file.resolve())
        os.environ.pop("TAURI_SIGNING_PRIVATE_KEY", None)

        if "TAURI_SIGNING_PRIVATE_KEY_PASSWORD" not in os.environ:
            os.environ["TAURI_SIGNING_PRIVATE_KEY_PASSWORD"] = "labelsortpro2026"

        print(f"[OK] Configured signing key from environment at: {key_file.resolve()}")
    else:
        print("[SIGNER] No TAURI_SIGNING_PRIVATE_KEY detected in environment.")
        print("[SIGNER] Automatically generating a release signing keypair on the fly...")
        res = subprocess.run(
            ["node", "node_modules/@tauri-apps/cli/tauri.js", "signer", "generate", "-p", "", "-f", "--ci", "-w", str(key_file)],
            cwd=str(FRONTEND_DIR),
            capture_output=True,
            text=True
        )
        if res.returncode == 0 and key_file.exists() and pub_file.exists():
            pubkey = pub_file.read_text().strip()
            # Update tauri.conf.json with the matching generated public key
            conf_path = TAURI_DIR / "tauri.conf.json"
            if conf_path.exists():
                try:
                    conf = json.loads(conf_path.read_text(encoding="utf-8"))
                    if "plugins" in conf and "updater" in conf["plugins"]:
                        conf["plugins"]["updater"]["pubkey"] = pubkey
                        conf_path.write_text(json.dumps(conf, indent=2), encoding="utf-8")
                        print(f"[OK] Updated tauri.conf.json with generated public key.")
                except Exception as e:
                    print(f"[WARN] Failed to update tauri.conf.json: {e}")

            os.environ["TAURI_SIGNING_PRIVATE_KEY_PATH"] = str(key_file.resolve())
            os.environ["TAURI_SIGNING_PRIVATE_KEY_PASSWORD"] = ""
            os.environ.pop("TAURI_SIGNING_PRIVATE_KEY", None)
            print(f"[OK] Generated on-the-fly signing key at: {key_file.resolve()}")
        else:
            print(f"[WARN] On-the-fly key generation failed: {res.stderr}")


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
