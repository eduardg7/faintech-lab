"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    # Application
    app_name: str = "Agent Memory Cloud API"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./amc.db"
    database_echo: bool = False
    test_database_url: Optional[str] = None
    # Database type for dual-mode support (TD-015: pgvector migration)
    # "sqlite" → JSON embedding column (dev default)
    # "postgres" → Vector(1536) embedding column (production, requires pgvector)
    database_type: str = "sqlite"

    # Connection pool settings (TD-017: fix pool exhaustion for beta)
    # These are critical for handling concurrent load without connection exhaustion
    db_pool_size: int = 20  # Number of connections to keep in pool
    db_max_overflow: int = 10  # Additional connections beyond pool_size
    db_pool_timeout: int = 30  # Seconds to wait for a connection before error
    db_pool_recycle: int = 1800  # Recycle connections after 30 minutes (prevents stale connections)
    db_pool_pre_ping: bool = True  # Test connection health before use

    # API
    api_v1_prefix: str = "/v1"

    # Security
    api_key_header: str = "X-API-Key"
    jwt_secret_key: str  # JWT signing key - MUST be set in production
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # CORS (TD-009: fix wildcard origin conflict with credentials)
    # Comma-separated list of allowed origins. Set via env var CORS_ORIGINS.
    # Production must NOT use "*" when allow_credentials=True (CORS spec violation).
    # Example: CORS_ORIGINS="http://localhost:3000,https://amc.faintech.com"
    cors_origins_str: str = "http://localhost:3000"  # Env var: CORS_ORIGINS

    # Content limits
    max_content_size_bytes: int = 10 * 1024  # 10KB

    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS_ORIGINS env var as list (comma-separated)."""
        if self.cors_origins_str.strip() == "*":
            # Wildcard mode - but allow_credentials must be False in main.py
            # This is kept for dev convenience but production should use explicit origins
            return ["*"]
        return [origin.strip() for origin in self.cors_origins_str.split(",") if origin.strip()]


settings = Settings()
