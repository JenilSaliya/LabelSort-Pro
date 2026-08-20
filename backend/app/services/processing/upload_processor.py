import logging
import time
from pathlib import Path

from app.core.config import settings
from app.core.constants import (
    STATUS_PROCESSING,
    STATUS_COMPLETED,
    STATUS_FAILED,
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

    Maintains job metadata in memory during execution to eliminate
    redundant disk read round-trips.
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
            # Load metadata once into memory for the entire processing run
            metadata = self.job_service.get_job(job_id)

            def _sync_metadata(
                progress: int,
                current_step: str,
                status_message: str | None = None,
                pages_processed: int | None = None,
                total_pages: int | None = None,
                elapsed_seconds: float | None = None,
                eta_seconds: int | None = None,
                eta_formatted: str | None = None,
                processing_speed_pps: float | None = None,
                status: str | None = None,
            ) -> None:
                metadata["progress"] = min(100, max(0, progress))
                metadata["current_step"] = current_step
                if status_message is not None:
                    metadata["status_message"] = status_message
                if pages_processed is not None:
                    metadata["pages_processed"] = pages_processed
                if total_pages is not None:
                    metadata["total_pages"] = total_pages
                if elapsed_seconds is not None:
                    metadata["elapsed_seconds"] = round(elapsed_seconds, 1)
                if eta_seconds is not None:
                    metadata["eta_seconds"] = eta_seconds
                if eta_formatted is not None:
                    metadata["eta_formatted"] = eta_formatted
                if processing_speed_pps is not None:
                    metadata["processing_speed_pps"] = round(processing_speed_pps, 1)
                if status is not None:
                    metadata["status"] = status
                # Save mutated in-memory metadata directly (0 disk reads)
                self.job_service.save_metadata(job_id, metadata)

            # 1. Initialize extraction status
            _sync_metadata(
                progress=10,
                current_step="extracting",
                status_message="Analyzing document structure...",
                status=STATUS_PROCESSING,
            )

            start_time = time.time()

            # Progress callback for page extraction
            def on_page_progress(current_page: int, total_pages: int) -> None:
                elapsed = max(0.1, time.time() - start_time)
                speed = current_page / elapsed

                # Calculate ETA only after at least 20 pages have been processed
                if current_page >= 20 and speed > 0:
                    remaining_pages = max(0, total_pages - current_page)
                    eta_sec = int(remaining_pages / speed)
                    if eta_sec < 60:
                        eta_str = f"~{eta_sec}s remaining"
                    else:
                        mins = eta_sec // 60
                        secs = eta_sec % 60
                        eta_str = f"~{mins}m {secs}s remaining"
                else:
                    eta_sec = None
                    eta_str = "Calculating..."

                # Map page extraction to 10% - 80%
                percent = 10 + int(70 * (current_page / max(1, total_pages)))
                status_msg = f"Extracting page {current_page} of {total_pages}..."

                _sync_metadata(
                    progress=percent,
                    current_step="extracting",
                    status_message=status_msg,
                    pages_processed=current_page,
                    total_pages=total_pages,
                    elapsed_seconds=elapsed,
                    eta_seconds=eta_sec,
                    eta_formatted=eta_str,
                    processing_speed_pps=speed,
                )

            # 2. Extract labels and page count
            marketplace, page_count, labels = self.extraction_service.extract_labels(
                input_pdf=input_pdf,
                on_progress=on_page_progress,
            )

            total_elapsed = max(0.1, time.time() - start_time)
            avg_speed = page_count / total_elapsed

            # 3. Cache labels to disk for sorting phase
            _sync_metadata(
                progress=82,
                current_step="caching",
                status_message="Caching extracted labels...",
                pages_processed=page_count,
                total_pages=page_count,
                elapsed_seconds=total_elapsed,
                eta_seconds=0,
                eta_formatted="Almost done...",
                processing_speed_pps=avg_speed,
            )
            self.label_cache.save(
                labels=labels,
                marketplace=marketplace,
                page_count=page_count,
                job_dir=job_dir,
            )

            # 4. Run dataset analysis
            _sync_metadata(
                progress=88,
                current_step="analyzing",
                status_message="Analyzing SKU distribution and couriers...",
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
            _sync_metadata(
                progress=94,
                current_step="generating_report",
                status_message="Generating summary spreadsheet...",
            )
            excel_path = job_dir / "reports" / "statistics.xlsx"
            self.excel_exporter.export_statistics(
                analysis=analysis,
                output_path=excel_path,
            )

            # 6. Mark completed
            metadata["status"] = STATUS_COMPLETED
            metadata["progress"] = 100
            metadata["current_step"] = "completed"
            metadata["status_message"] = "Processing complete! Ready to sort."
            metadata["marketplace"] = marketplace
            metadata["page_count"] = page_count
            metadata["pages_processed"] = page_count
            metadata["total_pages"] = page_count
            metadata["label_groups"] = len(labels)
            metadata["elapsed_seconds"] = round(total_elapsed, 1)
            metadata["eta_seconds"] = 0
            metadata["eta_formatted"] = "Ready"
            metadata["processing_speed_pps"] = round(avg_speed, 1)
            self.job_service.save_metadata(job_id, metadata)

            logger.info(
                "Successfully completed processing for job %s (%d labels, %d pages in %.1fs)",
                job_id,
                len(labels),
                page_count,
                total_elapsed,
            )

        except Exception as exc:
            logger.exception("Background processing failed for job %s: %s", job_id, exc)
            self.job_service.fail_job(job_id, str(exc))
