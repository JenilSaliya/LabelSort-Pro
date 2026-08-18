"""
Label cache — persists extracted labels to disk as JSON.

Eliminates the need to re-parse the PDF during the
processing step, cutting memory usage and latency.
"""

import json
import logging
from pathlib import Path

from app.models.label import Label

logger = logging.getLogger(__name__)

# Schema version to detect stale caches if Label model changes.
_CACHE_VERSION = 1


class LabelCache:
    """
    Saves and loads extracted labels from a JSON file
    inside the job directory.

    Cache file: {job_dir}/extracted/labels.json
    """

    @staticmethod
    def save(
        labels: list[Label],
        marketplace: str,
        page_count: int,
        job_dir: Path,
    ) -> Path:
        """
        Serialize labels to JSON and write to disk.

        Returns the path to the cache file.
        """
        cache_dir = job_dir / "extracted"
        cache_dir.mkdir(parents=True, exist_ok=True)

        cache_path = cache_dir / "labels.json"

        payload = {
            "version": _CACHE_VERSION,
            "marketplace": marketplace,
            "page_count": page_count,
            "label_count": len(labels),
            "labels": [
                label.model_dump() for label in labels
            ],
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)

        logger.info(
            "Cached %d labels to %s",
            len(labels),
            cache_path,
        )

        return cache_path

    @staticmethod
    def load(
        job_dir: Path,
    ) -> tuple[str, int, list[Label]]:
        """
        Deserialize labels from the cache file.

        Returns (marketplace, page_count, labels).

        Raises FileNotFoundError if the cache doesn't exist.
        """
        cache_path = job_dir / "extracted" / "labels.json"

        if not cache_path.exists():
            raise FileNotFoundError(
                f"Label cache not found: {cache_path}"
            )

        with open(cache_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        labels = [
            Label.model_validate(item)
            for item in payload["labels"]
        ]

        marketplace = payload["marketplace"]
        page_count = payload.get("page_count", 0)

        logger.info(
            "Loaded %d cached labels from %s",
            len(labels),
            cache_path,
        )

        return marketplace, page_count, labels
