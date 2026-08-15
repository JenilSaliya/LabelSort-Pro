from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.utils.json_utils import load_json

router = APIRouter()


@router.get("/{job_id}")
def get_job(job_id: str):
    """
    Return job metadata.
    """

    metadata_path = (
        settings.JOBS_DIR
        / job_id
        / "metadata.json"
    )

    if not metadata_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return load_json(metadata_path)


@router.get("/{job_id}/download")
def download_sorted_pdf(job_id: str):
    """
    Download the sorted PDF.
    """

    pdf_path = (
        settings.JOBS_DIR
        / job_id
        / "output"
        / "sorted.pdf"
    )

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Sorted PDF not found."
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

    pdf_path = (
        settings.JOBS_DIR
        / job_id
        / "output"
        / "sorted.pdf"
    )

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Sorted PDF not found."
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
    )



@router.get("/{job_id}/analysis")
def get_analysis(
    job_id: str,
):

    analysis_path = (
        settings.JOBS_DIR
        / job_id
        / "reports"
        / "analysis.json"
    )

    if not analysis_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    return load_json(
        analysis_path
    )


@router.get("/{job_id}/statistics")
async def download_statistics(
    job_id: str,
):
    excel_path = (
        settings.JOBS_DIR
        / job_id
        / "reports"
        / "statistics.xlsx"
    )

    if not excel_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Statistics file not found."
        )

    return FileResponse(
        path=excel_path,
        filename="statistics.xlsx",
        media_type=(
            "application/"
            "vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )