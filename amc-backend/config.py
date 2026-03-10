"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Application
    app_name: str = "Agent Memory Cloud API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./amc.db"
    database_echo: bool = False
    test_database_url: Optional[str] = None
    
    # API
    api_v1_prefix: str = "/v1"
    
    # Security
    api_key_header: str = "X-API-Key"
    
    # Content limits
    max_content_size_bytes: int = 10 * 1024  # 10KB


settings = Settings()
