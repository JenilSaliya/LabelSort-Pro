import os
import sys
from pathlib import Path
from pydantic_settings import BaseSettings


def get_default_jobs_dir() -> Path:
    """
    Determines the jobs directory dynamically:
    - If running as a frozen executable (PyInstaller Desktop Sidecar):
      Uses %LOCALAPPDATA%/LabelSortPro/jobs on Windows or ~/.labelsort/jobs on POSIX.
      This ensures write permissions regardless of where the app is installed (e.g. Program Files).
    - If running in standard web/dev mode:
      Uses <project_root>/backend/temp/jobs.
    """
    if getattr(sys, "frozen", False):
        local_app_data = os.getenv("LOCALAPPDATA")
        if local_app_data:
            base_dir = Path(local_app_data) / "LabelSortPro"
        else:
            base_dir = Path.home() / ".labelsort"
        jobs_dir = base_dir / "jobs"
    else:
        base_dir = Path(__file__).resolve().parent.parent.parent
        jobs_dir = base_dir / "temp" / "jobs"

    jobs_dir.mkdir(parents=True, exist_ok=True)
    return jobs_dir


class Settings(BaseSettings):
    APP_NAME: str = "LabelSort API"
    VERSION: str = "1.0.0"

    # "development" or "production"
    ENVIRONMENT: str = "development"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    TEMP_DIR: Path = BASE_DIR / "temp"
    JOBS_DIR: Path = get_default_jobs_dir()

    MAX_FILE_SIZE_MB: int = 100

    FRONTEND_URL: str = "http://localhost:5173"

    ALLOWED_EXTENSIONS: tuple[str, ...] = ("pdf",)

    JOB_RETENTION_HOURS: int = 1

    LOG_LEVEL: str = "INFO"

    IS_DESKTOP: bool = getattr(sys, "frozen", False)

    @property
    def cors_origins(self) -> list[str]:
        """
        Build CORS allowed origins based on environment.
        Supports web production, local development, and desktop webviews (Tauri/Electron).
        """
        if self.ENVIRONMENT == "production" and not getattr(sys, "frozen", False):
            origins = [self.FRONTEND_URL]
            return [o for o in origins if o]

        # Development & Desktop: allow local origins, LAN variants, and Tauri schemes
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://labelsort-pro.vercel.app",
            "https://labelsort-pro.vercel.app/",
            "tauri://localhost",
            "http://tauri.localhost",
            "https://tauri.localhost",
            self.FRONTEND_URL,
        ]


settings = Settings()
