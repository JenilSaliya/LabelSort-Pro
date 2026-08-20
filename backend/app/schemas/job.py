from pydantic import BaseModel


class JobMetadata(BaseModel):
    job_id: str
    status: str
    progress: int = 0
    current_step: str | None = None
    status_message: str | None = None
    pages_processed: int | None = None
    total_pages: int | None = None
    elapsed_seconds: float | None = None
    eta_seconds: int | None = None
    eta_formatted: str | None = None
    processing_speed_pps: float | None = None
    error: str | None = None
    marketplace: str | None = None
    original_filename: str | None = None
    stored_filename: str | None = None
    file_size: int | None = None
    page_count: int | None = None
    label_groups: int | None = None
    uploaded_filenames: list[str] | None = None
    uploaded_file_count: int | None = None
    mime_type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None