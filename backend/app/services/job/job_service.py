from datetime import datetime
from pathlib import Path
import shutil
import uuid

from app.utils.json_utils import save_json
from app.core.config import settings
from app.core.constants import STATUS_UPLOADED


class JobService:
    """
    Handles creation and management of processing jobs.
    """

    def create_job(self) -> dict:
        """
        Creates a new processing job.

        Returns:
            dict: Job metadata
        """

        # Generate Job ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_id = uuid.uuid4().hex[:6]

        job_id = f"{timestamp}_{random_id}"

        job_dir = settings.JOBS_DIR / job_id

        # Create folders
        (job_dir / "original").mkdir(parents=True, exist_ok=True)
        (job_dir / "output").mkdir(parents=True, exist_ok=True)
        (job_dir / "preview").mkdir(parents=True, exist_ok=True)
        (job_dir / "extracted").mkdir(parents=True, exist_ok=True)
        (job_dir / "reports").mkdir(parents=True, exist_ok=True)
        (job_dir / "logs").mkdir(parents=True, exist_ok=True)

        metadata = {
            "job_id": job_id,
            "status": STATUS_UPLOADED,
            "marketplace": None,
            "original_filename": None,
            "stored_filename": None,
            "mime_type": None,
            "file_size": None,
            "page_count": None,
            "label_groups": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        metadata_path = job_dir / "metadata.json"

        save_json(metadata_path, metadata)

        return {
            "job_id": job_id,
            "job_dir": job_dir,
            "metadata": metadata,
        }

    def delete_job(self, job_id: str) -> None:
        """
        Safely delete the complete workspace for a job.
        """

        job_dir = (settings.JOBS_DIR / job_id).resolve()
        jobs_root = settings.JOBS_DIR.resolve()

        # Security check:
        # Make sure the job directory is actually inside JOBS_DIR.
        if jobs_root not in job_dir.parents:
            raise ValueError("Invalid job path.")

        if job_dir.exists():
            shutil.rmtree(job_dir)