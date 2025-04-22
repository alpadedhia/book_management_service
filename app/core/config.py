import tomllib
from pathlib import Path
from typing import Literal
from urllib.parse import quote_plus

from environs import Env
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings
from structlog.stdlib import BoundLogger

from app.core.logger import Logger

PROJECT_DIR = Path(__file__).parent.parent.parent
with open(f"{PROJECT_DIR}/pyproject.toml", "rb") as f:
    PYPROJECT_CONTENT = tomllib.load(f)["tool"]["poetry"]

env = Env()
env.read_env()

CORS_ALLOWED_HEADERS = list(map(str.strip, env.list("BACKEND_CORS_HEADERS", ["*"])))
CORS_ORIGINS = list(
    map(str.strip, env.list("BACKEND_CORS_ORIGINS", ["http://localhost:3000"]))
)
ALLOWED_HOSTS = list(map(str.strip, env.list("ALLOWED_HOSTS", ["localhost"])))


class Settings(BaseSettings):
    # CORE SETTINGS
    ENVIRONMENT: Literal["DEV", "STG", "PROD"] = env.str("ENVIRONMENT", "DEV").upper()

    # LOG SETTINGS
    LOG_LEVEL: Literal["INFO", "DEBUG", "WARN", "ERROR"] = env.str("LOG_LEVEL", "INFO")
    LOG_JSON_FORMAT: bool = env.bool("LOG_JSON_FORMAT", False)

    # PROJECT NAME, VERSION AND DESCRIPTION
    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    ROOT_PATH: str = env.str("ROOT_PATH", "")

    # DOCS SETTINGS
    DOCS_URL: str = f"{ROOT_PATH}/docs"
    OPENAPI_URL: str = f"{ROOT_PATH}/openapi.json"

    # POSTGRESQL DATABASE SETTINGS
    DATABASE_HOSTNAME: str = env.str("DATABASE_HOSTNAME")
    DATABASE_USER: str = env.str("DATABASE_USER")
    DATABASE_PASSWORD: str = env.str("DATABASE_PASSWORD")
    DATABASE_PORT: str = env.str("DATABASE_PORT", "5432")
    DATABASE_DB: str = env.str("DATABASE_DB")
    SQLALCHEMY_DATABASE_URI: str = ""

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def _assemble_db_connection(cls, v: str, info: ValidationInfo) -> str:
        data = info.data
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            data["DATABASE_USER"],
            quote_plus(data["DATABASE_PASSWORD"]),
            data["DATABASE_HOSTNAME"],
            data["DATABASE_PORT"],
            data["DATABASE_DB"],
        )

    # UVICORN SETTINGS
    UVICORN_HOST: str = env.str("UVICORN_HOST", "0.0.0.0")
    UVICORN_PORT: int = env.int("UVICORN_PORT", 5001)

    CACHE_HOST: str = env.str("CACHE_HOST", "localhost")
    CACHE_PORT: int = env.int("CACHE_PORT", 6379)
    CACHE_TTL: int = env.int("CACHE_TTL", 300)


settings: Settings = Settings()  # type: ignore

log: BoundLogger = Logger(
    json_logs=settings.LOG_JSON_FORMAT, log_level=settings.LOG_LEVEL
).setup_logging()
