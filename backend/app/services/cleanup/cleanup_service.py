import logging
from datetime import datetime, timedelta
import shutil

from app.core.config import settings
from app.utils.json_utils import load_json

logger = logging.getLogger(__name__)


class CleanupService:

    def cleanup_old_jobs(self) -> None:


        jobs_dir = settings.JOBS_DIR

        jobs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        retention_hours = settings.JOB_RETENTION_HOURS

        cutoff_time = (
            datetime.now()
            - timedelta(hours=retention_hours)
        )

        for job_dir in jobs_dir.iterdir():

            if not job_dir.is_dir():
                continue

            metadata_path = (
                job_dir / "metadata.json"
            )

            if not metadata_path.exists():
                continue

            try:

                metadata = load_json(
                    metadata_path
                )

                updated_at = datetime.fromisoformat(
                    metadata["updated_at"]
                )

                if updated_at < cutoff_time:

                    shutil.rmtree(job_dir)

                    logger.info(
                        "Deleted expired job: %s",
                        job_dir.name,
                    )

            except Exception as exc:

                logger.warning(
                    "Cleanup skipped %s: %s",
                    job_dir.name,
                    exc,
                )