import logging
from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.core.constants import (
    STATUS_SORTING,
    STATUS_COMPLETED,
    STATUS_FAILED,
)
from app.models.sort_options import SortOptions
from app.services.pipeline.label_sort_pipeline import LabelSortPipeline
from app.services.extraction.label_cache import LabelCache
from app.services.job.job_service import JobService

logger = logging.getLogger(__name__)


class ProcessingService:
    """
    Coordinates the complete PDF processing workflow.

    Flow:
        Cached Labels (from upload step)
            ↓
        LabelSortPipeline (Validation & Sorting)
            ↓
        Sorted PDF (C-level PyMuPDF select)

    Orchestrates sorting without re-parsing PDF from scratch.
    """

    def __init__(self) -> None:
        self.label_cache = LabelCache()
        self.pipeline = LabelSortPipeline()
        self.job_service = JobService()

    def process_job(
        self,
        job_id: str,
        options: SortOptions,
    ) -> dict:
        """
        Process an uploaded job and generate the sorted PDF.
        """
        job_dir = (settings.JOBS_DIR / job_id).resolve()
        jobs_root = settings.JOBS_DIR.resolve()

        # Security check: job directory must remain inside JOBS_DIR
        if jobs_root not in job_dir.parents:
            raise ValueError("Invalid job path.")

        input_pdf = job_dir / "original" / "original.pdf"
        output_pdf = job_dir / "output" / "sorted.pdf"

        if not input_pdf.exists():
            raise FileNotFoundError("Original PDF not found for this job.")

        output_pdf.parent.mkdir(parents=True, exist_ok=True)

        metadata = self.job_service.get_job(job_id)
        metadata["status"] = STATUS_SORTING
        metadata["current_step"] = "sorting"
        self.job_service.save_metadata(job_id, metadata)

        try:
            # 1. Load cached labels (no PDF re-parsing)
            marketplace, page_count, labels = self.label_cache.load(job_dir)

            # 2. Sort labels and create output PDF
            output_path = self.pipeline.sort_labels(
                labels=labels,
                options=options,
                input_pdf=input_pdf,
                output_pdf=output_pdf,
            )

            # 3. Update job metadata
            metadata["status"] = STATUS_COMPLETED
            metadata["current_step"] = "completed"
            metadata["status_message"] = "Sorted PDF ready for download."
            metadata["marketplace"] = marketplace
            metadata["label_groups"] = len(labels)
            metadata["page_count"] = page_count
            self.job_service.save_metadata(job_id, metadata)

            return {
                "job_id": job_id,
                "status": "processed",
                "marketplace": marketplace,
                "input_pdf": str(input_pdf),
                "output_pdf": str(output_path),
                "page_count": page_count,
                "label_count": len(labels),
            }

        except Exception as exc:
            logger.exception("Sorting failed for job %s: %s", job_id, exc)
            self.job_service.fail_job(job_id, f"Sorting failed: {exc}")
            raise