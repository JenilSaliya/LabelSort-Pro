from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.utils.json_utils import load_json
from app.utils.job_path import get_job_dir
from app.services.job.job_service import JobService

router = APIRouter()
job_service = JobService()


@router.get("/{job_id}")
def get_job(job_id: str):
    """
    Return job metadata with crash recovery detection.
    """
    try:
        return job_service.get_job(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Job not found or has expired.",
        )


@router.get("/{job_id}/download")
def download_sorted_pdf(job_id: str):
    """
    Download the sorted PDF.
    """
    try:
        job_dir = get_job_dir(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )

    pdf_path = job_dir / "output" / "sorted.pdf"

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise HTTPException(
            status_code=404,
            detail="Sorted PDF not found or has expired.",
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{job_id}_sorted.pdf",
    )


@router.get("/{job_id}/preview")
def preview_sorted_pdf(job_id: str):
    """
    Open sorted PDF in browser.
    """
    try:
        job_dir = get_job_dir(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )

    pdf_path = job_dir / "output" / "sorted.pdf"

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise HTTPException(
            status_code=404,
            detail="Sorted PDF not found or has expired.",
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
    )


@router.get("/{job_id}/analysis")
def get_analysis(job_id: str):
    """
    Return dataset analysis report.
    """
    try:
        job_dir = get_job_dir(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )

    analysis_path = job_dir / "reports" / "analysis.json"

    if not analysis_path.exists() or analysis_path.stat().st_size == 0:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found or has expired.",
        )

    return load_json(analysis_path)


@router.get("/{job_id}/statistics")
async def download_statistics(job_id: str):
    """
    Download statistics spreadsheet.
    """
    try:
        job_dir = get_job_dir(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )

    excel_path = job_dir / "reports" / "statistics.xlsx"

    if not excel_path.exists() or excel_path.stat().st_size == 0:
        raise HTTPException(
            status_code=404,
            detail="Statistics file not found or has expired.",
        )

    return FileResponse(
        path=excel_path,
        filename="statistics.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )