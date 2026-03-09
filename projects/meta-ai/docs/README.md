# Persistent Agent Memory Library

**Phase 1 of Faintech Lab Meta-AI Infrastructure**

A lightweight, file-based memory system for AI agents that survives session restarts.

## Why This Exists

AI agents lose all context between sessions. This library provides persistent, structured memory that agents can read/write/search, enabling:

- **Learning retention** - Remember mistakes and solutions across sessions
- **Pattern recognition** - Track recurring issues and successful patterns
- **Context recovery** - Rebuild understanding after context loss
- **Cross-agent learning** - Share learnings between agents (future)

## Features

✅ **File-based storage** - No external DB, inspectable files, version-controllable  
✅ **Structured schema** - Consistent entry format with metadata  
✅ **Searchable** - Query by keywords, filters, tags, recency  
✅ **Auto-compaction** - Summarize old entries to prevent unbounded growth  
✅ **Python-first** - Simple API, easy integration  
✅ **CLI tool** - Command-line interface for quick operations  

## Installation

```bash
# From Faintech OS
cd projects/meta-ai
pip install -e .

# Or copy the src/memory module to your project
```

## Quick Start

### Python API

```python
from src.memory import MemoryStore, MemoryEntry, MemoryType

# Initialize store
store = MemoryStore()

# Write a learning
entry = MemoryEntry(
    agent_id="faintech-backend",
    project_id="faintech-os",
    task_id="TASK-123",
    type=MemoryType.LEARNING,
    content="Discovered that pytest fixtures need explicit scope for async tests",
    tags=["testing", "pytest", "async"]
)

entry_id = store.write(entry)
print(f"Saved memory: {entry_id}")

# Search recent learnings
results = store.search(
    query="pytest",
    agent_id="faintech-backend",
    entry_type=MemoryType.LEARNING,
    limit=5
)

for result in results:
    print(f"[{result.timestamp}] {result.content}")

# Get all entries for a task
task_memories = store.get_for_task("faintech-os", "TASK-123")

# Get recent entries for agent
recent = store.get_recent_for_agent("faintech-backend", limit=10)
```

### CLI Usage

```bash
# Write a memory entry
python -m src.memory.cli write \
  --agent-id faintech-backend \
  --project-id faintech-os \
  --task-id TASK-123 \
  --type learning \
  --content "Learned to use context managers for file handling" \
  --tags "python,best-practices"

# Search memories
python -m src.memory.cli search "pytest" \
  --agent-id faintech-backend \
  --type learning \
  --limit 10

# Compact old entries (7+ days)
python -m src.memory.cli compact --agent-id faintech-backend --days 7
```

## Memory Schema

Every memory entry has this structure:

```python
{
    "id": "uuid",                    # Auto-generated unique ID
    "agent_id": "faintech-backend",  # Agent who created the entry
    "project_id": "faintech-os",     # Project namespace
    "task_id": "TASK-123",           # Optional: Related task
    "timestamp": "2026-03-09T...",   # ISO 8601 timestamp
    "type": "learning",              # learning | error | decision | pattern | fact
    "content": "...",                # Main memory content (string)
    "tags": ["tag1", "tag2"],        # Searchable tags
    "metadata": {}                   # Optional structured data
}
```

### Entry Types

| Type | Use Case | Example |
|------|----------|---------|
| `learning` | Something learned that should be remembered | "Discovered X fails with Y config" |
| `error` | An error or failure encountered | "Got timeout error when calling Z API" |
| `decision` | An architectural or design decision | "Decided to use PostgreSQL for storage" |
| `pattern` | A recurring pattern noticed | "Task cycling happens when AC is unclear" |
| `fact` | A factual piece of information | "API rate limit is 1000 req/hour" |

## Storage Architecture

```
~/.agent-memory/
├── faintech-backend/
│   ├── 2026-03-09.jsonl      # Daily memory files
│   ├── 2026-03-10.jsonl
│   └── archive/              # Compacted old files
│       ├── 2026-03-02.jsonl
│       └── ...
├── faintech-cto/
│   └── ...
└── ...
```

**Why JSONL?**
- Append-only writes (no locking issues)
- Line-delimited (easy to read/write/stream)
- Human-readable (inspectable without tools)
- Git-friendly (version control if needed)

## Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| Write | <100ms | ~5ms |
| Search (1000 entries) | <100ms | ~20ms |
| Compact (100 entries) | <1s | ~200ms |

## Integration with OpenClaw Agents

### Adding Memory to Your Agent

```python
# In your agent's initialization
from pathlib import Path
from src.memory import MemoryStore, MemoryEntry, MemoryType

class MyAgent:
    def __init__(self, agent_id: str, project_id: str):
        self.memory = MemoryStore()
        self.agent_id = agent_id
        self.project_id = project_id
    
    def remember(self, content: str, entry_type: MemoryType, tags: list = None):
        """Write a memory entry."""
        entry = MemoryEntry(
            agent_id=self.agent_id,
            project_id=self.project_id,
            type=entry_type,
            content=content,
            tags=tags or []
        )
        return self.memory.write(entry)
    
    def recall(self, query: str, limit: int = 5):
        """Search past memories."""
        return self.memory.search(
            query=query,
            agent_id=self.agent_id,
            limit=limit
        )
    
    def learn_from_past(self, task_id: str):
        """Get all memories for current task."""
        return self.memory.get_for_task(self.project_id, task_id)

# Usage
agent = MyAgent("faintech-backend", "faintech-os")

# Learn from mistakes
agent.remember(
    "Always verify PR merge state before marking task done",
    MemoryType.LEARNING,
    tags=["workflow", "git"]
)

# Check past learnings
past = agent.recall("git workflow")
for memory in past:
    print(memory.content)
```

### Automatic Compaction

Run weekly via cron or scheduled task:

```python
# Weekly maintenance script
from src.memory import MemoryStore

store = MemoryStore()

# Compact all agents
for agent_dir in store.base_path.iterdir():
    if agent_dir.is_dir():
        result = store.compact(agent_dir.name, days_old=7)
        print(f"{agent_dir.name}: {result['message']}")
```

## Testing

```bash
# Run all tests
cd projects/meta-ai
pytest tests/test_memory.py -v

# Run with coverage
pytest tests/test_memory.py -v --cov=src.memory --cov-report=term-missing

# Expected: 90%+ coverage
```

## API Reference

### MemoryStore

#### `__init__(base_path: Optional[Path] = None)`
Initialize memory store. Uses `~/.agent-memory` by default.

#### `write(entry: MemoryEntry) -> str`
Write a memory entry. Returns entry ID.

#### `search(query: str, **filters) -> List[MemoryEntry]`
Search entries by keyword and filters.

**Filters:**
- `agent_id: str` - Filter by agent
- `project_id: str` - Filter by project
- `task_id: str` - Filter by task
- `entry_type: MemoryType` - Filter by type
- `tags: List[str]` - Filter by tags (AND logic)
- `limit: int` - Max results (default 10, max 100)
- `since: str` - ISO 8601 timestamp filter
- `until: str` - ISO 8601 timestamp filter

#### `get_for_task(project_id: str, task_id: str, limit: int = 50) -> List[MemoryEntry]`
Get all entries for a specific task.

#### `get_recent_for_agent(agent_id: str, limit: int = 10) -> List[MemoryEntry]`
Get recent entries for an agent.

#### `compact(agent_id: str, days_old: int = 7) -> Dict[str, Any]`
Compact entries older than threshold into summaries.

### MemoryEntry

#### Fields
- `id: str` - Auto-generated UUID
- `agent_id: str` - Agent identifier
- `project_id: str` - Project namespace
- `task_id: Optional[str]` - Related task ID
- `timestamp: str` - ISO 8601 timestamp
- `type: MemoryType` - Entry type enum
- `content: str` - Memory content
- `tags: List[str]` - Searchable tags
- `metadata: Dict[str, Any]` - Optional structured data

## Best Practices

### 1. Be Specific
```python
# Bad
agent.remember("Fixed bug", MemoryType.LEARNING)

# Good
agent.remember(
    "Fixed memory leak in data processing: forgot to close file handles in error path",
    MemoryType.LEARNING,
    tags=["bug", "memory-leak", "file-handling"]
)
```

### 2. Use Tags Wisely
Tags enable powerful filtering. Use consistent tag vocabularies:
- Component: `api`, `database`, `frontend`
- Type: `bug`, `feature`, `refactor`
- Context: `production`, `testing`, `development`

### 3. Write Immediately
Don't wait until end of task. Write learnings as they happen:
```python
try:
    risky_operation()
except Exception as e:
    agent.remember(
        f"Operation failed: {str(e)}. Root cause: X",
        MemoryType.ERROR,
        tags=["error", "operation-name"]
    )
    raise
```

### 4. Review Before Starting
```python
# Check past learnings before starting similar work
past = agent.recall("similar-feature")
if past:
    print("Past learnings:")
    for memory in past:
        print(f"  - {memory.content}")
```

## Future Phases

**Phase 2 - Self-Improvement (planned)**
- Pattern detector: Identify recurring failures across agents
- Behavior promoter: Auto-update AGENT.md from learned patterns
- Regression guard: Verify behavior changes didn't break anything

**Phase 3 - Observability (planned)**
- Execution ledger: Track every agent action with evidence
- Drift detector: Alert when behavior diverges from SOUL.md
- Cost attribution: Track tokens per task/agent/project

## Contributing

This is part of Faintech Lab's meta-ai infrastructure. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Add tests (maintain 90%+ coverage)
4. Submit PR

## License

MIT - Part of Faintech Solutions SRL

---

**Built at Faintech Lab** - Building better AI agents through infrastructure.
