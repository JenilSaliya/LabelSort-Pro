from pathlib import Path

# import fitz

from app.core.config import settings
# from app.models.label import Label
from app.models.sort_options import SortOptions

# from app.services.meesho.parser import MeeshoParser
# from app.services.meesho.label_builder import build_label
from app.services.pipeline.label_sort_pipeline import LabelSortPipeline
from datetime import datetime

from app.utils.json_utils import (
    load_json,
    save_json,
)

# from app.services.marketplace.detector import (
#     # Marketplace,
#     MarketplaceDetector,
# )

from app.services.analysis.analysis_service import (
    AnalysisService,
)

from app.services.extraction.extraction_service import (
    ExtractionService,
)




class ProcessingService:
    """
    Coordinates the complete PDF processing workflow.

    Flow:

        Original PDF
            ↓
        MeeshoParser
            ↓
        Label Builder
            ↓
        Label objects
            ↓
        LabelSortPipeline
            ↓
        Sorted PDF

    This service only orchestrates the existing components.
    It does not contain sorting logic.
    """

    def __init__(self) -> None:
        self.extraction_service = ExtractionService()
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

        metadata["status"] = "sotring"
        metadata["updated_at"] = datetime.now().isoformat()

        save_json(
            metadata_path,
            metadata,
        )
        # --------------------------------------------------
        # STEP 3 - Parse PDF
        # --------------------------------------------------

        marketplace, labels = (
            self.extraction_service.extract_labels(
                input_pdf
            )
        )

       

        # --------------------------------------------------
        # STEP 5 - Sort labels and create PDF
        # --------------------------------------------------

        output_path = self.pipeline.sort_labels(
            labels=labels,
            options=options,
            input_pdf=input_pdf,
            output_pdf=output_pdf,
        )

        metadata_path = job_dir / "metadata.json"

        metadata = load_json(metadata_path)

        metadata["status"] = "completed"
        metadata["marketplace"] = (marketplace)
        metadata["label_groups"] = len(labels)
        metadata["updated_at"] = datetime.now().isoformat()

        save_json(
            metadata_path,
            metadata,
        )
        # --------------------------------------------------
        # STEP 6 - Return processing result
        # --------------------------------------------------

        return {
            "job_id": job_id,
            "status": "processed",
            "marketplace": marketplace,
            "input_pdf": str(input_pdf),
            "output_pdf": str(output_path),
            "page_count": sum(
                len(label.pages) 
                for label in labels
            ),
            "label_count": len(labels),
        }