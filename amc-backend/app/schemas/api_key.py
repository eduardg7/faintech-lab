"""Schemas for workspace API key management."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ApiKeyCreateRequest(BaseModel):
    """Request body for creating an API key."""

    name: str = Field(..., min_length=1, max_length=255, description="Human-readable key name")


class ApiKeyCreateResponse(BaseModel):
    """Response body for newly created API keys."""

    id: str
    key: str
    created_at: datetime


class ApiKeySummary(BaseModel):
    """List entry for an API key."""

    id: str
    name: str
    key_preview: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    revoked_at: Optional[datetime]
    expires_at: Optional[datetime]


class ApiKeyListResponse(BaseModel):
    """Workspace API key list response."""

    api_keys: list[ApiKeySummary]
    total: int
