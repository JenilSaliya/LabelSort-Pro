from fastapi import APIRouter, File, UploadFile
from app.schemas.response import ApiResponse
from app.services.upload.upload_service import UploadService

router = APIRouter()

upload_service = UploadService()

@router.post("/", response_model=ApiResponse)
async def upload_pdf(
    file: UploadFile = File(...)
):
    result = await upload_service.upload_pdf(file)

    return ApiResponse(
        success = True,
        message = "PDF uploaded successfully.",
        data = result
    )