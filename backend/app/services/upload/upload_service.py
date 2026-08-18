from datetime import datetime
import shutil

from fastapi import UploadFile

from app.services.export.excel_export_service import ExcelExportService

from app.services.cleanup.cleanup_service import (
    CleanupService,
)

from app.services.pdf.pdf_merge_service import (
    PdfMergeService,
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
from app.services.extraction.label_cache import (
    LabelCache,
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
        self.pdf_merge_service = PdfMergeService()
        self.label_cache = LabelCache()

    async def upload_pdf(self, files: list[UploadFile]) -> dict:

        self.cleanup_service.cleanup_old_jobs()

        job = self.job_service.create_job()

        job_dir = job["job_dir"]
        
        uploads_dir = (
            job_dir / "uploads"
        )

        uploads_dir.mkdir(
            parents=True,
            exist_ok=True,
        )



        try:

            if not files:
                raise ValueError(
                    "No PDF files uploaded."
                )

            for file in files:
                validate_pdf(file)
                
                await validate_not_empty(file)
        
                validate_file_size(file)
        
                validate_pdf_integrity(file)


            saved_files = []

            for index, file in enumerate(files):

                pdf_path = (
                    uploads_dir
                    / f"upload_{index + 1}.pdf"
                )

                file.file.seek(0)

                with open(pdf_path, "wb") as buffer:
                    shutil.copyfileobj(
                        file.file,
                        buffer,
                    )

                saved_files.append(
                    pdf_path
                )

            destination = job_dir / "original" / "original.pdf"

            if len(saved_files) == 1:

                shutil.copy2(
                    saved_files[0],
                    destination,
                )
            else:

                self.pdf_merge_service.merge(
                    pdf_files=saved_files,
                    output_pdf=destination,
                )

            

            # Get file size.
            file_size = destination.stat().st_size

            # Extract labels and page count in one pass.
            # pymupdf returns page_count for free during extraction,
            # eliminating the need for a separate PdfReader call.
            marketplace, page_count, labels = (
                self.extraction_service.extract_labels(
                    destination
                )
            )

            # Cache labels to disk so processing step
            # can load them without re-parsing the PDF.
            self.label_cache.save(
                labels=labels,
                marketplace=marketplace,
                page_count=page_count,
                job_dir=job_dir,
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

            metadata["uploaded_filenames"]=[
                file.filename
                for file in files
            ]
            metadata["stored_filename"] = "original.pdf"
            metadata["file_size"] = file_size
            metadata["uploaded_file_count"] = len(saved_files)
            metadata["page_count"] = page_count
            metadata["marketplace"] = marketplace
            metadata["label_groups"] = len(labels)
            metadata["mime_type"] = ("application/pdf")
            metadata["updated_at"] = datetime.now().isoformat()


            save_json(metadata_path, metadata)

            return {
                "job_id": job["job_id"],
                "status": metadata["status"],
                "marketplace": marketplace,
                "page_count": page_count,
                "label_count": len(labels),
                "uploaded_file_count": len(saved_files),
            }

        except Exception:
            self.job_service.delete_job(job["job_id"])
            raise