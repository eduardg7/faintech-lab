"""Memory model for core memory storage."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, CheckConstraint, Index, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
import json

from app.core.database import Base, generate_uuid


# Valid memory types
MEMORY_TYPES = ("outcome", "learning", "preference", "decision")


class Memory(Base):
    """Core memory storage with metadata and soft delete."""
    
    __tablename__ = "memories"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_id = Column(String(255), nullable=False, index=True)
    project_id = Column(String(255), nullable=True, index=True)
    
    # Memory content
    type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA-256 for deduplication
    
    # Embedding vector for semantic search (1536 dimensions for text-embedding-3-small)
    embedding = Column(ARRAY(Float), nullable=True, index=True)  # Requires pgvector
    
    # Metadata (stored as JSON string for SQLite compatibility)
    tags = Column(Text, nullable=False, default="[]")  # JSON array as string
    importance = Column(Float, nullable=False, default=0.5)
    meta_data = Column("metadata", Text, nullable=False, default="{}")  # JSON object as string
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=True)
    embedded_at = Column(DateTime, nullable=True, index=True)  # When embedding was generated
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    # Relationships
    workspace = relationship("Workspace", back_populates="memories")
    pattern_examples = relationship("PatternExample", back_populates="memory", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(f"type IN {MEMORY_TYPES}", name="ck_memory_type"),
        CheckConstraint("importance >= 0 AND importance <= 1", name="ck_memory_importance"),
        CheckConstraint("LENGTH(content) <= 10240", name="ck_memory_content_length"),
        Index("idx_memories_workspace_agent", "workspace_id", "agent_id"),
        Index("idx_memories_workspace_project", "workspace_id", "project_id"),
        Index("idx_memories_workspace_type", "workspace_id", "type"),
    )
    
    def __repr__(self) -> str:
        return f"<Memory(id={self.id}, type={self.type}, agent={self.agent_id})>"
    
    @property
    def is_active(self) -> bool:
        """Check if memory is active (not deleted)."""
        return self.deleted_at is None
    
    def get_tags(self) -> list[str]:
        """Get tags as a list."""
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except json.JSONDecodeError:
            return []
    
    def set_tags(self, tags: list[str]) -> None:
        """Set tags from a list."""
        self.tags = json.dumps(tags)
    
    def get_metadata(self) -> dict:
        """Get metadata as a dictionary."""
        if not self.meta_data:
            return {}
        try:
            return json.loads(self.meta_data)
        except json.JSONDecodeError:
            return {}
    
    def set_metadata(self, metadata: dict) -> None:
        """Set metadata from a dictionary."""
        self.meta_data = json.dumps(metadata)
