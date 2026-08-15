from typing import Any, Optional

from pydantic import BaseModel, Field


class LabelFields(BaseModel):
    """
    Structured fields extracted from a shipping label.

    Known fields are explicitly defined.
    Unknown marketplace-specific fields can be stored
    inside `extra`.
    """

    courier_partner: Optional[str] = None
    payment_type: Optional[str] = None
    tracking_number: Optional[str] = None

    sku: Optional[str] = None
    product_name: Optional[str] = None
    size: Optional[str] = None
    quantity: Optional[int] = None
    color: Optional[str] = None

    order_number: Optional[str] = None
    invoice_number: Optional[str] = None
    order_date: Optional[str] = None

    extra: dict[str, Any] = Field(default_factory=dict)


class Label(BaseModel):
    """
    Represents one logical shipping label.

    A label may contain one or more PDF pages.
    Pages must remain together during sorting.
    """

    id: str
    pages: list[int] = Field(min_length=1)
    fields: LabelFields