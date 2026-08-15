from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    LabelSortException,
)


async def labelsort_exception_handler(
    request: Request,
    exc: LabelSortException,
):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
        },
    )