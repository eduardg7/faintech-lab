"""Pydantic schemas for Memory API endpoints."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum


class MemoryType(str, Enum):
    """Memory entry type."""
    OUTCOME = "outcome"
    LEARNING = "learning"
    PREFERENCE = "preference"
    DECISION = "decision"


class MemoryCreate(BaseModel):
    """Schema for creating a new memory."""
    agent_id: str = Field(..., description="Agent ID that owns this memory")
    project_id: Optional[str] = Field(None, description="Associated project ID")
    task_id: Optional[str] = Field(None, description="Associated task ID (TD-013)")
    memory_type: MemoryType = Field(..., description="Type of memory entry")
    content: str = Field(..., description="Memory content", max_length=10240)  # 10KB limit
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")

    @validator('content')
    def validate_content_size(cls, v):
        """Validate content is not too large."""
        if len(v.encode('utf-8')) > 10240:  # 10KB in bytes
            raise ValueError('Content exceeds 10KB limit')
        return v

    @validator('tags')
    def validate_tags_count(cls, v):
        """Validate number of tags."""
        if len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return v


class MemoryUpdate(BaseModel):
    """Schema for updating an existing memory."""
    content: Optional[str] = Field(None, max_length=10240)
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None

    @validator('content')
    def validate_content_size(cls, v):
        """Validate content is not too large."""
        if v and len(v.encode('utf-8')) > 10240:
            raise ValueError('Content exceeds 10KB limit')
        return v

    @validator('tags')
    def validate_tags_count(cls, v):
        """Validate number of tags."""
        if v and len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return v


class MemoryResponse(BaseModel):
    """Schema for memory response."""
    id: str  # UUID string
    workspace_id: str
    agent_id: str
    task_id: Optional[str] = None
    project_id: Optional[str] = None
    memory_type: str  # Using string to match model's 'type' field
    content: str
    tags: List[str]
    metadata: Optional[dict]
    importance: float = 0.5
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MemoryListResponse(BaseModel):
    """Schema for paginated memory list response."""
    memories: List[MemoryResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


class MemoryFilter(BaseModel):
    """Schema for filtering memories."""
    agent_id: Optional[str] = None
    project_id: Optional[str] = None
    task_id: Optional[str] = None  # TD-013: Filter by task ID
    memory_type: Optional[MemoryType] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
