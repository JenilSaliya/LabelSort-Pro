from datetime import datetime
import shutil

from fastapi import UploadFile
from pypdf import PdfReader

from app.services.export.excel_export_service import ExcelExportService

from app.services.cleanup.cleanup_service import (
    CleanupService,
)

from app.services.job.job_service import JobService
from app.utils.json_utils import load_json, save_json
from app.utils.validation import (
    validate_pdf,
    validate_not_empty,
    validate_file_size,
    validate_pdf_integrity,
)
from app.services.extraction.extraction_service import (
    ExtractionService,
)

from app.services.analysis.analysis_service import (
    AnalysisService,
)



class UploadService:
    def __init__(self):
        self.job_service = JobService()
        self.extraction_service = ExtractionService()
        self.analysis_service = AnalysisService()
        self.excel_exporter = ExcelExportService()
        self.cleanup_service = CleanupService()

    async def upload_pdf(self, file: UploadFile) -> dict:

        validate_pdf(file)

        await validate_not_empty(file)

        validate_file_size(file)

        validate_pdf_integrity(file)

        job = self.job_service.create_job()
        self.cleanup_service.cleanup_old_jobs()

        job_dir = job["job_dir"]

        try:

            destination = job_dir / "original" / "original.pdf"

            #Make sure we start reading from the beginning.
            file.file.seek(0)

            # Save uploaded PDF.
            with open(destination, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Get file size.
            file_size = destination.stat().st_size

            # Get page count.
            reader = PdfReader(destination)
            page_count = len(reader.pages)

            marketplace, labels =(
                self.extraction_service.extract_labels(
                    destination
                )
            )

            analysis =(
                self.analysis_service.analyze(
                    labels=labels,
                    marketplace=marketplace,
                )
            )

            analysis_path = (
                job_dir
                / "reports"
                / "analysis.json"
            )

            save_json(
                analysis_path,
                analysis.model_dump(),
            )

            excel_path = (
                job_dir
                / "reports"
                / "statistics.xlsx"
            )

            self.excel_exporter.export_statistics(
                analysis=analysis,
                output_path=excel_path,
            )

            metadata_path = job_dir / "metadata.json"

            metadata = load_json(metadata_path)

            metadata["original_filename"] = file.filename
            metadata["stored_filename"] = "original.pdf"
            metadata["file_size"] = file_size
            metadata["page_count"] = page_count
            metadata["marketplace"] = marketplace
            metadata["label_groups"] = len(labels)
            metadata["mime_type"] = file.content_type
            metadata["updated_at"] = datetime.now().isoformat()


            save_json(metadata_path, metadata)

            return {
                "job_id": job["job_id"],
                "status": metadata["status"],
            }

        except Exception:
            self.job_service.delete_job(job["job_id"])
            raise