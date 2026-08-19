from datetime import datetime
from pathlib import Path
import shutil
import uuid
import logging

from app.utils.json_utils import load_json, save_json
from app.core.config import settings
from app.core.constants import (
    STATUS_UPLOADED,
    STATUS_PROCESSING,
    STATUS_COMPLETED,
    STATUS_FAILED,
)

logger = logging.getLogger(__name__)


class JobService:
    """
    Handles lifecycle, metadata, progress, and directory management of processing jobs.
    """

    def create_job(self) -> dict:
        """
        Creates a new processing job workspace and initializes metadata.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_id = uuid.uuid4().hex[:6]
        job_id = f"{timestamp}_{random_id}"

        job_dir = settings.JOBS_DIR / job_id

        # Initialize job folder hierarchy
        (job_dir / "original").mkdir(parents=True, exist_ok=True)
        (job_dir / "uploads").mkdir(parents=True, exist_ok=True)
        (job_dir / "output").mkdir(parents=True, exist_ok=True)
        (job_dir / "preview").mkdir(parents=True, exist_ok=True)
        (job_dir / "extracted").mkdir(parents=True, exist_ok=True)
        (job_dir / "reports").mkdir(parents=True, exist_ok=True)
        (job_dir / "logs").mkdir(parents=True, exist_ok=True)

        metadata = {
            "job_id": job_id,
            "status": STATUS_UPLOADED,
            "progress": 0,
            "current_step": "uploading",
            "pages_processed": 0,
            "total_pages": 0,
            "error": None,
            "marketplace": None,
            "original_filename": None,
            "stored_filename": None,
            "mime_type": "application/pdf",
            "file_size": None,
            "page_count": None,
            "label_groups": None,
            "uploaded_filenames": [],
            "uploaded_file_count": 0,
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

    def get_job(self, job_id: str) -> dict:
        """
        Loads metadata dictionary for a job.
        """
        job_dir = (settings.JOBS_DIR / job_id).resolve()
        jobs_root = settings.JOBS_DIR.resolve()

        if jobs_root not in job_dir.parents:
            raise ValueError(f"Invalid job ID: {job_id}")

        metadata_path = job_dir / "metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Job {job_id} not found.")

        return load_json(metadata_path)

    def save_metadata(self, job_id: str, metadata: dict) -> None:
        """
        Saves updated metadata dictionary for a job.
        """
        job_dir = (settings.JOBS_DIR / job_id).resolve()
        metadata["updated_at"] = datetime.now().isoformat()
        metadata_path = job_dir / "metadata.json"
        save_json(metadata_path, metadata)

    def update_progress(
        self,
        job_id: str,
        progress: int,
        current_step: str,
        pages_processed: int | None = None,
        total_pages: int | None = None,
        status: str | None = None,
    ) -> None:
        """
        Updates live progress for background processing.
        """
        try:
            metadata = self.get_job(job_id)
            metadata["progress"] = min(100, max(0, progress))
            metadata["current_step"] = current_step
            if pages_processed is not None:
                metadata["pages_processed"] = pages_processed
            if total_pages is not None:
                metadata["total_pages"] = total_pages
            if status is not None:
                metadata["status"] = status
            self.save_metadata(job_id, metadata)
        except Exception as exc:
            logger.warning("Failed to update progress for job %s: %s", job_id, exc)

    def fail_job(self, job_id: str, error_message: str) -> None:
        """
        Marks a job as failed with a human-readable error message.
        """
        try:
            metadata = self.get_job(job_id)
            metadata["status"] = STATUS_FAILED
            metadata["error"] = error_message
            metadata["current_step"] = "failed"
            self.save_metadata(job_id, metadata)
            logger.error("Job %s marked as failed: %s", job_id, error_message)
        except Exception as exc:
            logger.exception("Failed to record failure for job %s: %s", job_id, exc)

    def complete_upload_job(
        self,
        job_id: str,
        marketplace: str,
        page_count: int,
        label_count: int,
    ) -> None:
        """
        Marks upload background extraction/analysis as completed.
        """
        metadata = self.get_job(job_id)
        metadata["status"] = STATUS_COMPLETED
        metadata["progress"] = 100
        metadata["current_step"] = "completed"
        metadata["marketplace"] = marketplace
        metadata["page_count"] = page_count
        metadata["pages_processed"] = page_count
        metadata["total_pages"] = page_count
        metadata["label_groups"] = label_count
        self.save_metadata(job_id, metadata)

    def delete_job(self, job_id: str) -> None:
        """
        Safely deletes the complete workspace for a job.
        """
        job_dir = (settings.JOBS_DIR / job_id).resolve()
        jobs_root = settings.JOBS_DIR.resolve()

        if jobs_root not in job_dir.parents:
            raise ValueError(f"Invalid job ID: {job_id}")

        if job_dir.exists():
            shutil.rmtree(job_dir)
            logger.info("Deleted workspace for job %s", job_id)