from pathlib import Path

from fastapi import APIRouter, HTTPException
from app.utils.job_path import get_job_dir
# from app.core.config import settings
from app.services.pdf.inspection_service import PDFInspectionService


router = APIRouter()

inspection_service = PDFInspectionService()


@router.get("/inspect/{job_id}")
async def inspect_pdf(job_id: str):
    """
    Inspect the original PDF belonging to a job.
    """

    try:
        job_dir = get_job_dir(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )

    pdf_path = job_dir / "original" / "original.pdf"
    

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
    try:
        job_dir = get_job_dir(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )

    pdf_path = job_dir / "original" / "original.pdf"
    

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