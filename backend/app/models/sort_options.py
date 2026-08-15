from pydantic import BaseModel, Field


class SortOptions(BaseModel):

    fields: list[str] = Field(
        min_length=1
    )

    reverse: bool = False

    courier_priority: list[str] = Field(
        default_factory=list
    )