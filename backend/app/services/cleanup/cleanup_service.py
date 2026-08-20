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

# Active states that should be protected during standard retention cleanup
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
    Includes zombie job reclamation for jobs abandoned across crashes/restarts.
    """

    def cleanup_old_jobs(self) -> None:
        jobs_dir = settings.JOBS_DIR
        jobs_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        retention_cutoff = now - timedelta(hours=settings.JOB_RETENTION_HOURS)
        abandoned_cutoff = now - timedelta(hours=2)  # Zombie reclamation threshold

        for job_dir in jobs_dir.iterdir():
            if not job_dir.is_dir():
                continue

            metadata_path = job_dir / "metadata.json"
            if not metadata_path.exists():
                # Cleanup orphaned directory without metadata
                try:
                    shutil.rmtree(job_dir, ignore_errors=True)
                    logger.info("Deleted orphaned workspace: %s", job_dir.name)
                except Exception as exc:
                    logger.warning("Failed to delete orphaned workspace %s: %s", job_dir.name, exc)
                continue

            try:
                metadata = load_json(metadata_path)
                status = metadata.get("status")
                updated_at_str = metadata.get("updated_at") or metadata.get("created_at")
                
                if not updated_at_str:
                    shutil.rmtree(job_dir, ignore_errors=True)
                    continue

                updated_at = datetime.fromisoformat(updated_at_str)

                # 1. Standard cleanup for completed or failed jobs older than retention period (1 hour)
                if status in {STATUS_COMPLETED, STATUS_FAILED} and updated_at < retention_cutoff:
                    shutil.rmtree(job_dir, ignore_errors=True)
                    logger.info("Deleted expired job workspace: %s (status=%s)", job_dir.name, status)
                    continue

                # 2. Zombie cleanup for active jobs abandoned for > 2 hours (e.g. server crashed during job)
                if status in ACTIVE_STATUSES and updated_at < abandoned_cutoff:
                    shutil.rmtree(job_dir, ignore_errors=True)
                    logger.warning("Deleted abandoned zombie job workspace: %s (was stuck in status=%s)", job_dir.name, status)
                    continue

            except Exception as exc:
                logger.warning("Cleanup skipped %s: %s", job_dir.name, exc)