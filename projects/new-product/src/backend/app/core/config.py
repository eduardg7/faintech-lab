"""Configuration management using environment variables."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Agent Memory Cloud"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./amc.db"  # Default to SQLite for dev
    database_pool_size: int = 50
    database_max_overflow: int = 100

    # API
    api_v1_prefix: str = "/api/v1"

    # Security
    api_key_header: str = "X-API-Key"

    # Rate limiting
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
