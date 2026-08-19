from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from app.schemas.response import ApiResponse
from app.services.upload.upload_service import UploadService

router = APIRouter()

upload_service = UploadService()


@router.post("/", response_model=ApiResponse)
async def upload_pdf(
    background_tasks: BackgroundTasks,
    files: list[UploadFile] = File(...),
):
    """
    Uploads PDF files, creates a processing job, starts background extraction,
    and returns immediately with the job_id.
    """
    result = await upload_service.upload_pdf(files, background_tasks)

    return ApiResponse(
        success=True,
        message="PDF uploaded successfully. Processing started in background.",
        data=result,
    )