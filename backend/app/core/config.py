from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Productivity App"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = "your-secret-key-here"  # In production, use environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # CORS
    ALLOW_ORIGINS: str = "http://localhost:5173"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOW_ORIGINS.split(",")]

    # MinIO configuration
    MINIO_ENDPOINT: str = "localhost:9000"  # Default for tests
    MINIO_ACCESS_KEY: str = "minioadmin"  # Default for tests
    MINIO_SECRET_KEY: str = "minioadmin"  # Default for tests
    MINIO_SECURE: bool = False

    # Logging
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in environment


settings = Settings()  # type: ignore
