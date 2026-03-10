"""Pattern model for detected patterns from cross-agent learning."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
import json

from app.core.database import Base, generate_uuid


class Pattern(Base):
    """Detected patterns from cross-agent learning."""
    
    __tablename__ = "patterns"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Pattern content
    type = Column(String(50), nullable=False, index=True)  # preference, behavior, error_pattern
    summary = Column(Text, nullable=False)
    frequency = Column(Integer, nullable=False, default=1)
    
    # Source agents (stored as JSON array for SQLite compatibility)
    agent_ids = Column(Text, nullable=False, default="[]")
    
    # Timestamps
    first_seen_at = Column(DateTime, nullable=False)
    last_seen_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True)
    confidence = Column(Float, nullable=False, default=0.5)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="patterns")
    examples = relationship("PatternExample", back_populates="pattern", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Pattern(id={self.id}, type={self.type}, frequency={self.frequency})>"
    
    def get_agent_ids(self) -> list[str]:
        """Get agent IDs as a list."""
        if not self.agent_ids:
            return []
        try:
            return json.loads(self.agent_ids)
        except json.JSONDecodeError:
            return []
    
    def set_agent_ids(self, agent_ids: list[str]) -> None:
        """Set agent IDs from a list."""
        self.agent_ids = json.dumps(agent_ids)
    
    def add_agent_id(self, agent_id: str) -> None:
        """Add an agent ID to the list."""
        agents = self.get_agent_ids()
        if agent_id not in agents:
            agents.append(agent_id)
            self.set_agent_ids(agents)


class PatternExample(Base):
    """Link patterns to source memories."""
    
    __tablename__ = "pattern_examples"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    pattern_id = Column(String(36), ForeignKey("patterns.id", ondelete="CASCADE"), nullable=False, index=True)
    memory_id = Column(String(36), ForeignKey("memories.id", ondelete="CASCADE"), nullable=False, index=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    pattern = relationship("Pattern", back_populates="examples")
    memory = relationship("Memory", back_populates="pattern_examples")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("pattern_id", "memory_id", name="uq_pattern_memory"),
    )
    
    def __repr__(self) -> str:
        return f"<PatternExample(pattern_id={self.pattern_id}, memory_id={self.memory_id})>"
