from fastapi import FastAPI
import logging

from app.api.v1.api import api_router
from app.exceptions.custom_exceptions import (
    LabelSortException
)

from fastapi.middleware.cors import CORSMiddleware

from app.core.exception_handlers import (
    labelsort_exception_handler
)

from app.core.config import settings

# ── Logging ──────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# ── Startup ──────────────────────────────────────────
settings.JOBS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

logger.info(
    "Starting %s v%s [%s]",
    settings.APP_NAME,
    settings.VERSION,
    settings.ENVIRONMENT,
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