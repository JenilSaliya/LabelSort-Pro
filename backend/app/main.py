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
    allow_origins=[
        settings.FRONTEND_NETWORK_URL,
        settings.FRONTEND_URL,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    LabelSortException,
    labelsort_exception_handler,
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message" : "Welcome to LabelSort API"
    }