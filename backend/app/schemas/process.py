from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    fields: list[str]

    reverse: bool = False

    courier_priority: list[str] = Field(
        default_factory=list
    )