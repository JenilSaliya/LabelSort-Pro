import shutil
import logging
from datetime import datetime
from fastapi import UploadFile, BackgroundTasks, HTTPException

from app.services.cleanup.cleanup_service import CleanupService
from app.services.pdf.pdf_merge_service import PdfMergeService
from app.services.job.job_service import JobService
from app.services.processing.upload_processor import UploadProcessor
from app.core.constants import STATUS_QUEUED
from app.utils.validation import (
    validate_pdf,
    validate_not_empty,
    validate_file_size,
    validate_pdf_file_on_disk,
)

logger = logging.getLogger(__name__)


class UploadService:
    """
    Handles PDF upload validation, persistence, job creation, and background scheduling.
    """

    def __init__(self):
        self.job_service = JobService()
        self.cleanup_service = CleanupService()
        self.pdf_merge_service = PdfMergeService()
        self.upload_processor = UploadProcessor()

    async def upload_pdf(
        self,
        files: list[UploadFile],
        background_tasks: BackgroundTasks,
    ) -> dict:
        """
        Validates uploaded PDF files, saves them to disk, creates a job,
        enqueues the background processing task, and returns immediately.
        """
        # Clean up expired jobs safely
        self.cleanup_service.cleanup_old_jobs()

        if not files:
            raise HTTPException(status_code=400, detail="No PDF files uploaded.")

        if len(files) > 20:
            raise HTTPException(status_code=400, detail="Maximum 20 files allowed per batch.")

        # 1. Validate initial metadata and magic bytes
        for file in files:
            validate_pdf(file)
            await validate_not_empty(file)
            validate_file_size(file)

        # 2. Create job directory
        job = self.job_service.create_job()
        job_id = job["job_id"]
        job_dir = job["job_dir"]
        uploads_dir = job_dir / "uploads"
        uploads_dir.mkdir(parents=True, exist_ok=True)

        try:
            # 3. Stream and persist uploaded files to disk
            saved_files = []
            for index, file in enumerate(files):
                pdf_path = uploads_dir / f"upload_{index + 1}.pdf"
                file.file.seek(0)
                with open(pdf_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Validate PDF structure directly on disk with zero Python byte allocations
                validate_pdf_file_on_disk(pdf_path)
                saved_files.append(pdf_path)

            destination = job_dir / "original" / "original.pdf"

            # 4. Copy single file or merge multi-file upload into original.pdf
            if len(saved_files) == 1:
                shutil.copy2(saved_files[0], destination)
            else:
                self.pdf_merge_service.merge(
                    pdf_files=saved_files,
                    output_pdf=destination,
                )

            # Validate final merged document
            validate_pdf_file_on_disk(destination)
            file_size = destination.stat().st_size

            # 5. Update initial metadata with file information
            metadata = self.job_service.get_job(job_id)
            metadata["uploaded_filenames"] = [f.filename for f in files if f.filename]
            metadata["stored_filename"] = "original.pdf"
            metadata["file_size"] = file_size
            metadata["uploaded_file_count"] = len(saved_files)
            metadata["status"] = STATUS_QUEUED
            metadata["current_step"] = "queued"
            metadata["status_message"] = "Queued for processing..."
            metadata["updated_at"] = datetime.now().isoformat()
            self.job_service.save_metadata(job_id, metadata)

            # 6. Schedule asynchronous background processing
            background_tasks.add_task(
                self.upload_processor.process_upload_job,
                job_id,
            )

            logger.info("Enqueued upload processing for job %s (%d files, %d bytes)", job_id, len(saved_files), file_size)

            # 7. Return immediate response
            return {
                "job_id": job_id,
                "status": STATUS_QUEUED,
                "uploaded_file_count": len(saved_files),
                "file_size": file_size,
            }

        except Exception as exc:
            self.job_service.fail_job(job_id, f"Upload setup failed: {str(exc)}")
            raise