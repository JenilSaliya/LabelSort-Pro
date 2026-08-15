from pathlib import Path

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader

from app.core.config import settings


def validate_pdf(file: UploadFile) -> None:
    """
    Validate uploaded file name and extension.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    extension = Path(file.filename).suffix.lower().replace(".", "")

    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )


async def validate_not_empty(file: UploadFile) -> None:
    """
    Validate that the uploaded file contains data.
    """

    file.file.seek(0)

    content = await file.read(1)

    file.file.seek(0)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

def validate_pdf_integrity(file: UploadFile) -> None:
    """
    Validate that the uploaded file is a readable PDF
    with at least one page.
    """

    file.file.seek(0)

    try:
        reader = PdfReader(file.file)

        if len(reader.pages) == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF contains no pages."
            )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF."
        )

    finally:
        file.file.seek(0)

def validate_file_size(file: UploadFile) -> None:
    """
    Validate that the uploaded file does not exceed
    the configured maximum file size.
    """

    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=(
                f"File size exceeds the maximum allowed size "
                f"of {settings.MAX_FILE_SIZE_MB} MB."
            )
        )