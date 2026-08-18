from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "LabelSort API"
    VERSION: str = "1.0.0"

    # "development" or "production"
    ENVIRONMENT: str = "development"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    TEMP_DIR: Path = BASE_DIR / "temp"
    JOBS_DIR: Path = TEMP_DIR / "jobs"

    MAX_FILE_SIZE_MB: int = 100

    FRONTEND_URL: str = "http://localhost:5173"

    ALLOWED_EXTENSIONS: tuple[str, ...] = ("pdf",)

    JOB_RETENTION_HOURS: int = 6

    @property
    def cors_origins(self) -> list[str]:
        """
        Build CORS allowed origins based on environment.

        Development: allow localhost and LAN variants.
        Production:  allow only the configured FRONTEND_URL.
        """
        if self.ENVIRONMENT == "production":
            origins = [self.FRONTEND_URL]
            # Filter out empty strings
            return [o for o in origins if o]

        # Development: allow common local origins
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            self.FRONTEND_URL,
        ]


settings = Settings()