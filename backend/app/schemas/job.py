from datetime import datetime
from pydantic import BaseModel

class JobMetadata(BaseModel):
    job_id:str
    status:str

    marketplace: str | None = None

    filename: str | None = None

    file_size: int | None = None

    page_count: int | None = None

    label_groups: int | None = None

    created_at: datetime

    updated_at: datetime
    