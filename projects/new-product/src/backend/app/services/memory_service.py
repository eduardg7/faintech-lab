"""Memory service integrating with META-AI memory library."""
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum
from dataclasses import dataclass, field, asdict
import json

# Add meta-ai to path for memory library
meta_ai_path = Path(__file__).parent.parent.parent.parent.parent / "meta-ai" / "src"
if meta_ai_path.exists():
    sys.path.insert(0, str(meta_ai_path))
    from memory.store import MemoryStore
    from memory.models import MemoryEntry, MemoryType as MetaMemoryType
    MEMORY_LIB_AVAILABLE = True
else:
    MEMORY_LIB_AVAILABLE = False


class MemoryType(str, Enum):
    """Types of memory entries."""
    LEARNING = "learning"
    ERROR = "error"
    DECISION = "decision"
    PATTERN = "pattern"
    FACT = "fact"


@dataclass
class LocalMemoryEntry:
    """Local memory entry when META-AI library not available."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    project_id: str = ""
    task_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    type: MemoryType = MemoryType.FACT
    content: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['type'] = self.type.value
        return data


class MemoryService:
    """
    Service for managing agent memories.
    
    Integrates with META-AI memory library when available,
    falls back to local implementation otherwise.
    """
    
    def __init__(self):
        """Initialize memory service."""
        if MEMORY_LIB_AVAILABLE:
            self._store = MemoryStore()
        else:
            self._store = None
    
    def write(
        self,
        agent_id: str,
        content: str,
        project_id: str = "",
        task_id: Optional[str] = None,
        entry_type: MemoryType = MemoryType.FACT,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Write a memory entry.
        
        Args:
            agent_id: Agent ID
            content: Memory content
            project_id: Project ID
            task_id: Task ID
            entry_type: Type of memory
            tags: Optional tags
            metadata: Optional metadata
            
        Returns:
            Created memory entry as dict
        """
        tags = tags or []
        metadata = metadata or {}
        
        if MEMORY_LIB_AVAILABLE:
            # Use META-AI library
            entry = MemoryEntry(
                agent_id=agent_id,
                project_id=project_id,
                task_id=task_id,
                type=MetaMemoryType(entry_type.value),
                content=content,
                tags=tags,
                metadata=metadata
            )
            self._store.write(entry)
            return entry.to_dict()
        else:
            # Fallback to local
            entry = LocalMemoryEntry(
                agent_id=agent_id,
                project_id=project_id,
                task_id=task_id,
                type=entry_type,
                content=content,
                tags=tags,
                metadata=metadata
            )
            return entry.to_dict()
    
    def search(
        self,
        query: str = "",
        agent_id: Optional[str] = None,
        project_id: Optional[str] = None,
        task_id: Optional[str] = None,
        entry_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
        since: Optional[str] = None,
        until: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memory entries.
        
        Args:
            query: Search query
            agent_id: Filter by agent
            project_id: Filter by project
            task_id: Filter by task
            entry_type: Filter by type
            tags: Filter by tags
            limit: Max results
            since: ISO timestamp filter
            until: ISO timestamp filter
            
        Returns:
            List of matching memory entries
        """
        if MEMORY_LIB_AVAILABLE:
            meta_type = MetaMemoryType(entry_type.value) if entry_type else None
            entries = self._store.search(
                query=query,
                agent_id=agent_id,
                project_id=project_id,
                task_id=task_id,
                entry_type=meta_type,
                tags=tags,
                limit=limit,
                since=since,
                until=until
            )
            return [e.to_dict() for e in entries]
        else:
            # Fallback - return empty for now
            return []
    
    def get_for_agent(self, agent_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent memories for an agent.
        
        Args:
            agent_id: Agent ID
            limit: Max results
            
        Returns:
            List of memory entries
        """
        if MEMORY_LIB_AVAILABLE:
            entries = self._store.get_recent_for_agent(agent_id, limit)
            return [e.to_dict() for e in entries]
        else:
            return []
    
    def get_for_task(self, project_id: str, task_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get memories for a specific task.
        
        Args:
            project_id: Project ID
            task_id: Task ID
            limit: Max results
            
        Returns:
            List of memory entries
        """
        if MEMORY_LIB_AVAILABLE:
            entries = self._store.get_for_task(project_id, task_id, limit)
            return [e.to_dict() for e in entries]
        else:
            return []
    
    def compact(self, agent_id: str, days_old: int = 7) -> Dict[str, Any]:
        """
        Compact old memories into summaries.
        
        Args:
            agent_id: Agent ID
            days_old: Age threshold
            
        Returns:
            Compaction statistics
        """
        if MEMORY_LIB_AVAILABLE:
            return self._store.compact(agent_id, days_old)
        else:
            return {
                "compacted": 0,
                "summaries_created": 0,
                "files_archived": 0,
                "message": "Memory library not available"
            }


# Singleton service instance
_memory_service: Optional[MemoryService] = None


def get_memory_service() -> MemoryService:
    """Get or create memory service instance."""
    global _memory_service
    if _memory_service is None:
        _memory_service = MemoryService()
    return _memory_service
