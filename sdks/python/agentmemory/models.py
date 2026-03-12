"""Data models for Agent Memory Cloud SDK."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MemoryType(str, Enum):
    """Type of memory entry."""

    OUTCOME = "outcome"
    LEARNING = "learning"
    PREFERENCE = "preference"
    DECISION = "decision"


@dataclass
class Memory:
    """Represents a memory entry."""

    id: str
    agent_id: str
    memory_type: MemoryType
    content: str
    created_at: datetime
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    updated_at: Optional[datetime] = None
    confidence: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Memory":
        """Create Memory instance from API response dict."""
        return cls(
            id=data["id"],
            agent_id=data["agent_id"],
            memory_type=MemoryType(data["memory_type"]),
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            workspace_id=data.get("workspace_id"),
            project_id=data.get("project_id"),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding"),
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
            if data.get("updated_at")
            else None,
            confidence=data.get("confidence"),
        )


@dataclass
class Agent:
    """Represents an AI agent that owns memories."""

    id: str
    name: str
    created_at: datetime
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Agent":
        """Create Agent instance from API response dict."""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            metadata=data.get("metadata", {}),
        )


@dataclass
class Project:
    """Represents a project for organizing memories."""

    id: str
    name: str
    created_at: datetime
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create Project instance from API response dict."""
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            metadata=data.get("metadata", {}),
        )


@dataclass
class SearchResult:
    """Represents a search result with relevance score."""

    memory: Memory
    score: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        """Create SearchResult instance from API response dict."""
        return cls(
            memory=Memory.from_dict(data["memory"]),
            score=data["score"],
        )


@dataclass
class PaginatedResponse:
    """Generic paginated response."""

    items: List[Any]
    total: int
    limit: int
    offset: int

    @property
    def has_more(self) -> bool:
        """Check if there are more results."""
        return self.offset + len(self.items) < self.total

    @classmethod
    def from_dict(cls, data: Dict[str, Any], item_class: type) -> "PaginatedResponse":
        """Create PaginatedResponse from API response dict."""
        return cls(
            items=[item_class.from_dict(item) for item in data["items"]],
            total=data["total"],
            limit=data["limit"],
            offset=data["offset"],
        )
