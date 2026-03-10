"""SQLAlchemy database models for Agent Memory Cloud."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


def generate_uuid():
    """Generate a UUID string."""
    return str(uuid.uuid4())


class Workspace(Base):
    """Workspace model - represents a tenant/organization."""
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agents = relationship("Agent", back_populates="workspace", cascade="all, delete-orphan")
    api_keys = relationship("ApiKey", back_populates="workspace", cascade="all, delete-orphan")


class Agent(Base):
    """Agent model - represents an AI agent in a workspace."""
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    agent_type = Column(String(100), nullable=False)  # e.g., "claude", "gpt", "custom"
    metadata_json = Column(Text, nullable=True)  # JSON blob for agent-specific metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="agents")
    memories = relationship("Memory", back_populates="agent", cascade="all, delete-orphan")


class Memory(Base):
    """Memory model - represents a memory entry for an agent."""
    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    memory_type = Column(String(50), nullable=False)  # e.g., "episodic", "semantic", "procedural"
    importance_score = Column(Integer, default=0)  # 0-100 importance rating
    metadata_json = Column(Text, nullable=True)  # JSON blob for memory metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="memories")


class ApiKey(Base):
    """API Key model - represents authentication credentials for a workspace."""
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=generate_uuid)
    workspace_id = Column(String, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)  # Human-readable name
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="api_keys")
