from fastapi import APIRouter
from fastapi import HTTPException

from app.core.config import settings
from app.services.sorting_config.sorting_config_service import (
    SortingConfigService,
)

router = APIRouter()

service = SortingConfigService()


@router.get(
    "/{job_id}/sorting-options"
)
async def get_sorting_options(
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
            detail="Analysis not found."
        )

    return service.get_config(
        analysis_path
    )