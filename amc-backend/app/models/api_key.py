"""API Key model for workspace authentication."""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional

from app.core.database import Base, generate_uuid


class ApiKey(Base):
    """Authentication keys for workspace access."""
    
    __tablename__ = "api_keys"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), nullable=False, index=True)  # SHA-256 hash of key
    key_prefix = Column(String(10), nullable=False, index=True)  # First 8 chars for identification
    scopes = Column(Text, nullable=False, default="read,write")  # Comma-separated for SQLite
    
    is_active = Column(Boolean, nullable=False, default=True)
    last_used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="api_keys")
    
    def __repr__(self) -> str:
        return f"<ApiKey(id={self.id}, name={self.name}, prefix={self.key_prefix})>"
    
    @property
    def is_valid(self) -> bool:
        """Check if API key is valid for use."""
        if not self.is_active:
            return False
        if self.revoked_at is not None:
            return False
        if self.expires_at is not None and self.expires_at < datetime.utcnow():
            return False
        return True
    
    def get_scopes_list(self) -> list[str]:
        """Get scopes as a list."""
        if not self.scopes:
            return []
        return [s.strip() for s in self.scopes.split(",") if s.strip()]
    
    def has_scope(self, scope: str) -> bool:
        """Check if key has a specific scope."""
        return scope in self.get_scopes_list()
