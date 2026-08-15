from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "LabelSort API"
    VERSION: str = "1.0.0"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    TEMP_DIR: Path = BASE_DIR / "temp"
    JOBS_DIR: Path = TEMP_DIR / "jobs"

    MAX_FILE_SIZE_MB: int = 100

    ALLOWED_EXTENSIONS: tuple[str, ...] = ("pdf",)

    JOB_RETENTION_HOURS: int = 6


settings = Settings()