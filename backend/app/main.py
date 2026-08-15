from fastapi import FastAPI
from app.api.v1.api import api_router
from app.exceptions.custom_exceptions import (
    LabelSortException
)

from app.core.exception_handlers import (
    labelsort_exception_handler
)

app = FastAPI(
    title = "LabelSort API",
    description = "Backend API for LabelSort Platform",
    version = "1.0.0"
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