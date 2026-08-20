import json
import os
import uuid
from pathlib import Path


def load_json(path: Path) -> dict:
    """
    Safely loads JSON data from disk with explicit UTF-8 encoding.
    """
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(f"JSON file missing or empty: {path}")

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, data: dict) -> None:
    """
    Atomically writes JSON data to disk using a unique sibling temporary file
    and atomic rename (os.replace). Prevents 0-byte or corrupted files if
    the server restarts or crashes during write.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_suffix(f".tmp.{uuid.uuid4().hex[:6]}")
    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_path, path)
    except Exception:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise