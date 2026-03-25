"""Pydantic schemas for API request/response models."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class MemoryType(str, Enum):
    """Types of memory entries."""
    LEARNING = "learning"
    ERROR = "error"
    DECISION = "decision"
    PATTERN = "pattern"
    FACT = "fact"


# Workspace schemas
class WorkspaceCreate(BaseModel):
    """Schema for creating a workspace."""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$")


class WorkspaceResponse(BaseModel):
    """Schema for workspace response."""
    id: str
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Agent schemas
class AgentCreate(BaseModel):
    """Schema for creating an agent."""
    name: str = Field(..., min_length=1, max_length=255)
    agent_type: str = Field(..., min_length=1, max_length=100)
    metadata_json: Optional[str] = None


class AgentUpdate(BaseModel):
    """Schema for updating an agent."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    agent_type: Optional[str] = Field(None, min_length=1, max_length=100)
    metadata_json: Optional[str] = None
    is_active: Optional[bool] = None


class AgentResponse(BaseModel):
    """Schema for agent response."""
    id: str
    workspace_id: str
    name: str
    agent_type: str
    metadata_json: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Memory schemas
class MemoryCreate(BaseModel):
    """Schema for creating a memory entry."""
    agent_id: str
    project_id: str = Field(default="")
    task_id: Optional[str] = None
    type: MemoryType = MemoryType.FACT
    content: str = Field(..., min_length=1)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemorySearchRequest(BaseModel):
    """Schema for memory search request."""
    query: str = Field(default="")
    agent_id: Optional[str] = None
    project_id: Optional[str] = None
    task_id: Optional[str] = None
    entry_type: Optional[MemoryType] = None
    tags: Optional[List[str]] = None
    limit: int = Field(default=10, ge=1, le=100)
    since: Optional[str] = None
    until: Optional[str] = None


class MemoryResponse(BaseModel):
    """Schema for memory entry response."""
    id: str
    agent_id: str
    project_id: str
    task_id: Optional[str]
    timestamp: str
    type: str
    content: str
    tags: List[str]
    metadata: Dict[str, Any]


class MemoryListResponse(BaseModel):
    """Schema for list of memories."""
    memories: List[MemoryResponse]
    total: int


class CompactRequest(BaseModel):
    """Schema for memory compaction request."""
    agent_id: str
    days_old: int = Field(default=7, ge=1, le=365)


class CompactResponse(BaseModel):
    """Schema for compaction result."""
    compacted: int
    summaries_created: int
    files_archived: int
    message: str


# API Key schemas
class ApiKeyCreate(BaseModel):
    """Schema for creating an API key."""
    name: str = Field(..., min_length=1, max_length=255)
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)


class ApiKeyResponse(BaseModel):
    """Schema for API key response (list view)."""
    id: str
    name: str
    prefix: str
    created_at: datetime
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    revoked_at: Optional[datetime]

    class Config:
        from_attributes = True


class ApiKeyCreateResponse(BaseModel):
    """Schema for API key creation response (includes secret)."""
    id: str
    name: str
    secret: str  # Full key, only shown once
    prefix: str
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True
