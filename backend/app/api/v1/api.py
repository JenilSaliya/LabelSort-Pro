from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.upload import router as upload_router
from app.api.v1.endpoints.inspection import router as inspection_router
from app.api.v1.endpoints.process import router as process_router
from app.api.v1.endpoints.job import router as job_router
from app.api.v1.endpoints.sorting_config import router as sorting_router



api_router = APIRouter()

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)

api_router.include_router(
    upload_router,
    prefix="/upload",
    tags=["Upload"]
)


api_router.include_router(
    inspection_router,
    prefix="/inspection",
    tags=["PDF Inspection"],
)

api_router.include_router(
    process_router,
    prefix="/process",
    tags=["Processing"],
)

api_router.include_router(
    job_router,
    prefix="/job",
    tags=["Job"],
)


api_router.include_router(
    sorting_router,
    prefix="/jobs",
    tags=["Sorting"],
)