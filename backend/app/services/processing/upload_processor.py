import logging
from pathlib import Path

from app.core.config import settings
from app.core.constants import (
    STATUS_PROCESSING,
    STATUS_PARSING,
)
from app.services.job.job_service import JobService
from app.services.extraction.extraction_service import ExtractionService
from app.services.extraction.label_cache import LabelCache
from app.services.analysis.analysis_service import AnalysisService
from app.services.export.excel_export_service import ExcelExportService
from app.utils.json_utils import save_json

logger = logging.getLogger(__name__)


class UploadProcessor:
    """
    Background worker orchestrating the extraction, label caching,
    analysis, and Excel generation pipeline for an uploaded PDF job.

    Completely decoupled from FastAPI HTTP request lifecycle.
    Can be run synchronously, under FastAPI BackgroundTasks, or inside
    a dedicated queue worker (arq/Celery/Redis).
    """

    def __init__(self) -> None:
        self.job_service = JobService()
        self.extraction_service = ExtractionService()
        self.analysis_service = AnalysisService()
        self.excel_exporter = ExcelExportService()
        self.label_cache = LabelCache()

    def process_upload_job(self, job_id: str) -> None:
        """
        Executes the extraction and analysis pipeline for a job.
        """
        job_dir = (settings.JOBS_DIR / job_id).resolve()
        input_pdf = job_dir / "original" / "original.pdf"

        if not input_pdf.exists():
            error_msg = f"Original PDF not found for job: {job_id}"
            logger.error(error_msg)
            self.job_service.fail_job(job_id, error_msg)
            return

        logger.info("Starting background processing for job %s", job_id)

        try:
            # 1. Update status to parsing / extracting
            self.job_service.update_progress(
                job_id=job_id,
                progress=10,
                current_step="extracting",
                status=STATUS_PROCESSING,
            )

            # Define progress callback for page extraction
            def on_page_progress(current_page: int, total_pages: int) -> None:
                # Map page progress from 10% to 80%
                percent = 10 + int(70 * (current_page / max(1, total_pages)))
                self.job_service.update_progress(
                    job_id=job_id,
                    progress=percent,
                    current_step="extracting",
                    pages_processed=current_page,
                    total_pages=total_pages,
                )

            # 2. Extract labels and page count
            marketplace, page_count, labels = self.extraction_service.extract_labels(
                input_pdf=input_pdf,
                on_progress=on_page_progress,
            )

            # 3. Cache labels to disk for sorting phase
            self.job_service.update_progress(
                job_id=job_id,
                progress=82,
                current_step="caching",
                pages_processed=page_count,
                total_pages=page_count,
            )
            self.label_cache.save(
                labels=labels,
                marketplace=marketplace,
                page_count=page_count,
                job_dir=job_dir,
            )

            # 4. Run dataset analysis
            self.job_service.update_progress(
                job_id=job_id,
                progress=88,
                current_step="analyzing",
            )
            analysis = self.analysis_service.analyze(
                labels=labels,
                marketplace=marketplace,
            )

            analysis_path = job_dir / "reports" / "analysis.json"
            save_json(
                analysis_path,
                analysis.model_dump(),
            )

            # 5. Export statistics Excel
            self.job_service.update_progress(
                job_id=job_id,
                progress=94,
                current_step="generating_report",
            )
            excel_path = job_dir / "reports" / "statistics.xlsx"
            self.excel_exporter.export_statistics(
                analysis=analysis,
                output_path=excel_path,
            )

            # 6. Mark completed
            self.job_service.complete_upload_job(
                job_id=job_id,
                marketplace=marketplace,
                page_count=page_count,
                label_count=len(labels),
            )
            logger.info("Successfully completed processing for job %s (%d labels, %d pages)", job_id, len(labels), page_count)

        except Exception as exc:
            logger.exception("Background processing failed for job %s: %s", job_id, exc)
            self.job_service.fail_job(job_id, str(exc))
