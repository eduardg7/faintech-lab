"""Workspace model for multi-tenant isolation."""
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List

from app.core.database import Base, generate_uuid


class Workspace(Base):
    """Multi-tenant workspace. Each customer = one workspace."""
    
    __tablename__ = "workspaces"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    tier = Column(String(50), nullable=False, default="pro")
    rate_limit = Column(Integer, nullable=False, default=100)
    storage_limit_mb = Column(Integer, nullable=False, default=100)
    
    # Stripe integration
    stripe_customer_id = Column(String(255), nullable=True, index=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    api_keys = relationship("ApiKey", back_populates="workspace", cascade="all, delete-orphan")
    memories = relationship("Memory", back_populates="workspace", cascade="all, delete-orphan")
    patterns = relationship("Pattern", back_populates="workspace", cascade="all, delete-orphan")
    users = relationship("User", back_populates="workspace", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Workspace(id={self.id}, slug={self.slug}, tier={self.tier})>"
    
    @property
    def is_active(self) -> bool:
        """Check if workspace is active (not deleted)."""
        return self.deleted_at is None
