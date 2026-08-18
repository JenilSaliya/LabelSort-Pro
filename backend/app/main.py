from fastapi import FastAPI
from app.api.v1.api import api_router
from app.exceptions.custom_exceptions import (
    LabelSortException
)

from fastapi.middleware.cors import CORSMiddleware

from app.core.exception_handlers import (
    labelsort_exception_handler
)

from app.core.config import settings

settings.JOBS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

app = FastAPI(
    title = "LabelSort API",
    description = "Backend API for LabelSort Platform",
    version = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    LabelSortException,
    labelsort_exception_handler,
)

app.include_router(api_router)

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {
        "status": "ok",
        "message": "Welcome to LabelSort API"
    }