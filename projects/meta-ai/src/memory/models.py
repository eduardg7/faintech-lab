"""Memory entry models for persistent agent memory."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import json
import uuid


class MemoryType(str, Enum):
    """Types of memory entries."""
    LEARNING = "learning"
    ERROR = "error"
    DECISION = "decision"
    PATTERN = "pattern"
    FACT = "fact"


@dataclass
class MemoryEntry:
    """Structured memory entry for agent persistence."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    project_id: str = ""
    task_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    type: MemoryType = MemoryType.FACT
    content: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_json(self) -> str:
        """Serialize to JSON string for JSONL storage."""
        data = asdict(self)
        data['type'] = self.type.value
        return json.dumps(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MemoryEntry':
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        data['type'] = MemoryType(data['type'])
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['type'] = self.type.value
        return data
