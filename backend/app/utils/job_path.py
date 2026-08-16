from pathlib import Path

from app.core.config import settings


def get_job_dir(job_id: str) -> Path:
    """
    Safely resolve a job directory.

    Ensures that the resolved job directory
    remains inside the configured JOBS_DIR.
    """

    jobs_root = settings.JOBS_DIR.resolve()

    job_dir = (
        settings.JOBS_DIR / job_id
    ).resolve()

    if jobs_root not in job_dir.parents:
        raise ValueError("Invalid job ID.")

    return job_dir