from fastapi import APIRouter, BackgroundTasks
from app.services.cleanup.cleanup_service import CleanupService

router = APIRouter()
cleanup_service = CleanupService()


@router.api_route("/", methods=["GET", "HEAD"])
def health_check(background_tasks: BackgroundTasks):
    """
    Health check endpoint.
    Triggers asynchronous cleanup of expired jobs without blocking the response.
    """
    background_tasks.add_task(cleanup_service.cleanup_old_jobs)
    return {
        "status": "ok",
        "message": "LabelSort Backend is running",
    }