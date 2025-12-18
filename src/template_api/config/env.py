"""Environment variables management for TESEO API Process."""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file if it exists
if Path(".env").exists():
    load_dotenv(Path(".env"))


class Environment:
    """Environment variables configuration."""

    APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "local")
    if APP_ENVIRONMENT not in ["local", "development", "production"]:
        raise ValueError(
            f"Invalid APP_ENVIRONMENT: {APP_ENVIRONMENT}. Must be one of 'local', 'development', 'production'."
        )

    # API specific
    API_ROOT_PATH = os.getenv("API_ROOT_PATH", "")
    API_PREFIX = os.getenv("API_PREFIX", "")

    # Directories
    _dir = os.getenv("TMP_DIR", "./tmp")
    TMP_DIR = Path(_dir)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Telemetry
    _traces = os.getenv("EXPORT_TRACES", "true").lower()
    EXPORT_TRACES = _traces not in ["0", "false", "no"]

    _excluded_urls = os.getenv("OTEL_PYTHON_EXCLUDED_URLS", "")
    OTEL_PYTHON_EXCLUDED_URLS = _excluded_urls.split(",") if _excluded_urls else []

    # Environment detection
    ENV = os.getenv("ENV", "development")

    @classmethod
    def validate(cls) -> None:
        """Check that required environment variables are set."""
        required_vars = []
        missing = [var for var in required_vars if getattr(cls, var) is None]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        # Environment validation completed (logged in main.py)


# Global environment instance
env = Environment()
