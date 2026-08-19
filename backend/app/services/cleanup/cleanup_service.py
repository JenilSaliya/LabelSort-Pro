import logging
from datetime import datetime, timedelta
import shutil

from app.core.config import settings
from app.core.constants import (
    STATUS_UPLOADED,
    STATUS_QUEUED,
    STATUS_PROCESSING,
    STATUS_PARSING,
    STATUS_ANALYZING,
    STATUS_SORTING,
    STATUS_GENERATING,
    STATUS_COMPLETED,
    STATUS_FAILED,
)
from app.utils.json_utils import load_json

logger = logging.getLogger(__name__)

# Active states that should NEVER be deleted during periodic cleanup
ACTIVE_STATUSES = {
    STATUS_UPLOADED,
    STATUS_QUEUED,
    STATUS_PROCESSING,
    STATUS_PARSING,
    STATUS_ANALYZING,
    STATUS_SORTING,
    STATUS_GENERATING,
}


class CleanupService:
    """
    Cleans up expired completed or failed jobs while strictly protecting active ones.
    """

    def cleanup_old_jobs(self) -> None:
        jobs_dir = settings.JOBS_DIR
        jobs_dir.mkdir(parents=True, exist_ok=True)

        retention_hours = settings.JOB_RETENTION_HOURS
        cutoff_time = datetime.now() - timedelta(hours=retention_hours)

        for job_dir in jobs_dir.iterdir():
            if not job_dir.is_dir():
                continue

            metadata_path = job_dir / "metadata.json"
            if not metadata_path.exists():
                continue

            try:
                metadata = load_json(metadata_path)
                status = metadata.get("status")

                # Never delete active/in-flight jobs
                if status in ACTIVE_STATUSES:
                    continue

                updated_at_str = metadata.get("updated_at") or metadata.get("created_at")
                if not updated_at_str:
                    continue

                updated_at = datetime.fromisoformat(updated_at_str)

                # Only delete completed or failed jobs older than retention period
                if updated_at < cutoff_time:
                    shutil.rmtree(job_dir)
                    logger.info("Deleted expired job workspace: %s (status=%s)", job_dir.name, status)

            except Exception as exc:
                logger.warning("Cleanup skipped %s: %s", job_dir.name, exc)