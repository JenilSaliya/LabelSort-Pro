from fastapi import APIRouter
from fastapi import HTTPException
from app.utils.job_path import get_job_dir
# from app.core.config import settings
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

    try:
        job_dir = get_job_dir(job_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid job ID.",
        )

    analysis_path = job_dir / "reports" / "analysis.json"


    if not analysis_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return service.get_config(
        analysis_path
    )