from fastapi import APIRouter

from app.schemas.process import ProcessRequest
from app.schemas.response import ApiResponse

from app.models.sort_options import SortOptions

from app.services.processing.processing_service import (
    ProcessingService,
)

router = APIRouter()

processing_service = ProcessingService()


@router.post("/{job_id}")
async def process_job(
    job_id: str,
    request: ProcessRequest,
):

    options = SortOptions(
        fields=request.fields,
        reverse=request.reverse,
        courier_priority=(
            request.courier_priority
        ),
    )
    result = processing_service.process_job(
        job_id=job_id,
        options=options,
    )

    return ApiResponse(
        success=True,
        message="PDF processed successfully.",
        data=result,
    )