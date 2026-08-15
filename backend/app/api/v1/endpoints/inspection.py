from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.pdf.inspection_service import PDFInspectionService


router = APIRouter()

inspection_service = PDFInspectionService()


@router.get("/inspect/{job_id}")
async def inspect_pdf(job_id: str):
    """
    Inspect the original PDF belonging to a job.
    """

    pdf_path = (
        settings.JOBS_DIR
        / job_id
        / "original"
        / "original.pdf"
    )

    try:
        result = inspection_service.inspect_pdf(pdf_path)

        return {
            "job_id": job_id,
            "inspection": result,
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Original PDF not found for this job.",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PDF inspection failed: {str(exc)}",
        )


@router.get("/coordinates/{job_id}/{page_number}")
async def inspect_page_coordinates(
    job_id: str,
    page_number: int,
):
    """
    Inspect text coordinates for one PDF page.
    """

    pdf_path = (
        settings.JOBS_DIR
        / job_id
        / "original"
        / "original.pdf"
    )

    try:
        result = inspection_service.inspect_page_coordinates(
            pdf_path,
            page_number,
        )

        return {
            "job_id": job_id,
            "inspection": result,
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Original PDF not found for this job.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Coordinate inspection failed: {str(exc)}",
        )