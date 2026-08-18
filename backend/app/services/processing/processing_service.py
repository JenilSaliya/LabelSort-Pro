from pathlib import Path
from datetime import datetime

from app.core.config import settings
from app.core.constants import (
    STATUS_SORTING,
    STATUS_COMPLETED,
)
from app.models.sort_options import SortOptions
from app.services.pipeline.label_sort_pipeline import LabelSortPipeline
from app.services.extraction.label_cache import LabelCache

from app.utils.json_utils import (
    load_json,
    save_json,
)


class ProcessingService:
    """
    Coordinates the complete PDF processing workflow.

    Flow:

        Cached Labels (from upload step)
            ↓
        LabelSortPipeline
            ↓
        Sorted PDF

    This service only orchestrates the existing components.
    It does not contain sorting logic.
    """

    def __init__(self) -> None:
        self.label_cache = LabelCache()
        self.pipeline = LabelSortPipeline()

    def process_job(
        self,
        job_id: str,
        options: SortOptions,
    ) -> dict:
        """
        Process an uploaded job and generate the sorted PDF.
        """

        # --------------------------------------------------
        # STEP 1 - Resolve job directory
        # --------------------------------------------------

        job_dir = (
            settings.JOBS_DIR / job_id
        ).resolve()

        jobs_root = settings.JOBS_DIR.resolve()

        # Security check:
        # job directory must remain inside JOBS_DIR.
        if jobs_root not in job_dir.parents:
            raise ValueError(
                "Invalid job path."
            )

        # --------------------------------------------------
        # STEP 2 - Define PDF paths
        # --------------------------------------------------

        input_pdf = (
            job_dir
            / "original"
            / "original.pdf"
        )

        output_pdf = (
            job_dir
            / "output"
            / "sorted.pdf"
        )

        if not input_pdf.exists():
            raise FileNotFoundError(
                "Original PDF not found for this job."
            )

        output_pdf.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata_path = job_dir / "metadata.json"
        
        metadata = load_json(metadata_path)

        metadata["status"] = STATUS_SORTING
        metadata["updated_at"] = datetime.now().isoformat()

        save_json(
            metadata_path,
            metadata,
        )
        # --------------------------------------------------
        # STEP 3 - Load cached labels (no PDF re-parsing)
        # --------------------------------------------------

        marketplace, page_count, labels = (
            self.label_cache.load(job_dir)
        )

        # --------------------------------------------------
        # STEP 4 - Sort labels and create PDF
        # --------------------------------------------------

        output_path = self.pipeline.sort_labels(
            labels=labels,
            options=options,
            input_pdf=input_pdf,
            output_pdf=output_pdf,
        )

        metadata_path = job_dir / "metadata.json"

        metadata = load_json(metadata_path)

        metadata["status"] = STATUS_COMPLETED
        metadata["marketplace"] = (marketplace)
        metadata["label_groups"] = len(labels)
        metadata["updated_at"] = datetime.now().isoformat()

        save_json(
            metadata_path,
            metadata,
        )
        # --------------------------------------------------
        # STEP 5 - Return processing result
        # --------------------------------------------------

        return {
            "job_id": job_id,
            "status": "processed",
            "marketplace": marketplace,
            "input_pdf": str(input_pdf),
            "output_pdf": str(output_path),
            "page_count": page_count,
            "label_count": len(labels),
        }