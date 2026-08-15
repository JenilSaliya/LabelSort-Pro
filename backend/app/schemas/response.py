from typing import Any, Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """
    Standard API response model.

    Every endpoint in LabelSort Pro should return this structure.
    """

    success: bool
    message: str
    data: Optional[Any] = None