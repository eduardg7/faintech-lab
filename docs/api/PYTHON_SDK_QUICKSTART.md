# Python SDK Quickstart Guide

**Agent Memory Cloud Python SDK**

Get started with the Agent Memory Cloud Python SDK in 5 minutes.

---

## Installation

```bash
pip install agent-memory-client
```

Or with Poetry:

```bash
poetry add agent-memory-client
```

---

## Quick Start

### 1. Initialize the Client

```python
from agent_memory import MemoryClient

# Initialize client (development mode - no auth required)
client = MemoryClient(base_url="http://localhost:8000/api/v1")

# For production, configure with authentication
# client = MemoryClient(
#     base_url="https://api.example.com/api/v1",
#     api_key="your-api-key"
# )
```

### 2. Create a Workspace

```python
# Create a new workspace for your project
workspace = client.workspaces.create(
    name="My AI Project",
    slug="my-ai-project"
)

print(f"Workspace created: {workspace.id}")
```

### 3. Register an Agent

```python
# Register your AI agent in the workspace
agent = client.agents.create(
    workspace_id=workspace.id,
    name="Code Assistant",
    agent_type="assistant",
    metadata={
        "model": "gpt-4",
        "capabilities": ["code-generation", "debugging"]
    }
)

print(f"Agent registered: {agent.id}")
```

### 4. Store Memories

```python
# Store a learning memory
memory = client.memories.create(
    agent_id=agent.id,
    project_id="my-project",
    task_id="TASK-001",
    type="learning",
    content="User prefers TypeScript over JavaScript for new projects",
    tags=["preference", "typescript", "coding-style"],
    metadata={"importance": "high", "source": "user-feedback"}
)

print(f"Memory stored: {memory.id}")
```

### 5. Search Memories

```python
# Semantic search across memories
results = client.memories.search(
    query="typescript preferences",
    agent_id=agent.id,
    tags=["preference"],
    limit=10
)

for memory in results.memories:
    print(f"- {memory.content}")
```

---

## Common Patterns

### Storing Different Memory Types

```python
# Learning: Things the agent discovered
client.memories.create(
    agent_id=agent.id,
    project_id="my-project",
    type="learning",
    content="FastAPI dependency injection uses Annotated types",
    tags=["fastapi", "python", "dependency-injection"]
)

# Decision: Important choices made
client.memories.create(
    agent_id=agent.id,
    project_id="my-project",
    type="decision",
    content="Chose PostgreSQL over MongoDB for ACID compliance requirements",
    tags=["architecture", "database", "decision"]
)

# Error: Issues encountered and resolutions
client.memories.create(
    agent_id=agent.id,
    project_id="my-project",
    type="error",
    content="CORS error resolved by adding credentials: true to fetch options",
    tags=["cors", "frontend", "bug-fix"]
)

# Context: Important context to remember
client.memories.create(
    agent_id=agent.id,
    project_id="my-project",
    type="context",
    content="Project uses ESLint with Airbnb config and Prettier for formatting",
    tags=["linting", "formatting", "tooling"]
)
```

### Batch Memory Operations

```python
# Store multiple memories at once
memories_data = [
    {
        "agent_id": agent.id,
        "project_id": "my-project",
        "type": "learning",
        "content": "React 18 introduced automatic batching",
        "tags": ["react", "performance"]
    },
    {
        "agent_id": agent.id,
        "project_id": "my-project",
        "type": "learning",
        "content": "Zustand is simpler than Redux for state management",
        "tags": ["state-management", "react"]
    }
]

for data in memories_data:
    client.memories.create(**data)
```

### Time-Based Filtering

```python
from datetime import datetime, timedelta

# Get memories from the last 7 days
results = client.memories.search(
    agent_id=agent.id,
    since=(datetime.now() - timedelta(days=7)).isoformat(),
    until=datetime.now().isoformat(),
    limit=50
)
```

### Getting Recent Memories

```python
# Get recent memories for an agent
recent = client.memories.get_by_agent(
    agent_id=agent.id,
    limit=20
)

for memory in recent.memories:
    print(f"[{memory.type}] {memory.content}")
```

### Task-Specific Memories

```python
# Get all memories related to a specific task
task_memories = client.memories.get_by_task(
    project_id="my-project",
    task_id="TASK-001",
    limit=100
)

# Useful for context injection before working on a task
context = "\n".join([m.content for m in task_memories.memories])
```

---

## Memory Compaction

For long-running agents, compact old memories to save space:

```python
# Compact memories older than 30 days
result = client.memories.compact(
    agent_id=agent.id,
    days_old=30
)

print(f"Compacted {result.compacted} memories")
print(f"Created {result.summaries_created} summary memories")
```

---

## Error Handling

```python
from agent_memory import MemoryClient, APIError, NotFoundError

client = MemoryClient(base_url="http://localhost:8000/api/v1")

try:
    workspace = client.workspaces.create(
        name="Test Workspace",
        slug="test-workspace"
    )
except APIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Details: {e.details}")
except NotFoundError as e:
    print(f"Resource not found: {e.resource_id}")
```

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 400 | Bad Request | Check request body format |
| 404 | Not Found | Verify resource ID exists |
| 409 | Conflict | Resource already exists (e.g., duplicate slug) |
| 429 | Rate Limited | Reduce request frequency |

---

## Rate Limiting

The SDK automatically handles rate limiting with exponential backoff:

```python
# Configure custom rate limit handling
client = MemoryClient(
    base_url="http://localhost:8000/api/v1",
    max_retries=3,
    retry_delay=1.0  # seconds
)
```

Default limits:
- General endpoints: 100 requests/minute
- Search endpoints: 30 requests/minute
- Write endpoints: 50 requests/minute

---

## Complete Example: AI Assistant with Memory

```python
from agent_memory import MemoryClient
from datetime import datetime

class MemoryEnabledAssistant:
    def __init__(self, base_url: str):
        self.client = MemoryClient(base_url=base_url)
        self.workspace = None
        self.agent = None

    def setup(self, name: str):
        """Initialize workspace and agent."""
        # Create or get workspace
        workspaces = self.client.workspaces.list()
        self.workspace = next(
            (w for w in workspaces if w.name == name),
            self.client.workspaces.create(name=name, slug=name.lower().replace(" ", "-"))
        )

        # Create agent
        self.agent = self.client.agents.create(
            workspace_id=self.workspace.id,
            name=f"{name} Assistant",
            agent_type="assistant"
        )

    def remember(self, content: str, memory_type: str = "learning", tags: list = None, task_id: str = None):
        """Store a memory."""
        return self.client.memories.create(
            agent_id=self.agent.id,
            project_id=self.workspace.slug,
            task_id=task_id,
            type=memory_type,
            content=content,
            tags=tags or []
        )

    def recall(self, query: str, limit: int = 10):
        """Search memories."""
        return self.client.memories.search(
            query=query,
            agent_id=self.agent.id,
            limit=limit
        )

    def get_context(self, task_id: str = None):
        """Get relevant context for a task."""
        if task_id:
            result = self.client.memories.get_by_task(
                project_id=self.workspace.slug,
                task_id=task_id,
                limit=50
            )
        else:
            result = self.client.memories.get_by_agent(
                agent_id=self.agent.id,
                limit=20
            )
        return result.memories

# Usage
assistant = MemoryEnabledAssistant("http://localhost:8000/api/v1")
assistant.setup("Code Review Bot")

# Remember something
assistant.remember(
    content="User prefers descriptive variable names over short ones",
    memory_type="preference",
    tags=["coding-style", "variables"]
)

# Recall relevant memories
memories = assistant.recall("variable naming preferences")
for m in memories.memories:
    print(f"- {m.content}")
```

---

## Pagination

For large result sets, use pagination:

```python
# List all workspaces with pagination
skip = 0
limit = 100
all_workspaces = []

while True:
    batch = client.workspaces.list(skip=skip, limit=limit)
    all_workspaces.extend(batch)

    if len(batch) < limit:
        break
    skip += limit

print(f"Total workspaces: {len(all_workspaces)}")
```

---

## Async Support

The SDK supports async operations:

```python
import asyncio
from agent_memory import AsyncMemoryClient

async def main():
    client = AsyncMemoryClient(base_url="http://localhost:8000/api/v1")

    # Create workspace and agent concurrently
    workspace, _ = await asyncio.gather(
        client.workspaces.create(name="Async Project", slug="async-project"),
        asyncio.sleep(0)  # Placeholder for other operations
    )

    agent = await client.agents.create(
        workspace_id=workspace.id,
        name="Async Agent",
        agent_type="assistant"
    )

    # Store multiple memories concurrently
    await asyncio.gather(
        client.memories.create(
            agent_id=agent.id,
            project_id="async-project",
            type="learning",
            content="Async operations improve throughput",
            tags=["async", "performance"]
        ),
        client.memories.create(
            agent_id=agent.id,
            project_id="async-project",
            type="learning",
            content="Use asyncio.gather for concurrent requests",
            tags=["async", "patterns"]
        )
    )

    await client.close()

asyncio.run(main())
```

---

## TypeScript Types

If you're using Python with type checking, the SDK includes full type hints:

```python
from agent_memory import (
    MemoryClient,
    WorkspaceCreate,
    WorkspaceResponse,
    AgentCreate,
    AgentResponse,
    MemoryCreate,
    MemoryResponse,
    MemorySearchRequest,
    MemoryListResponse
)
from typing import List, Optional

def create_and_remember(
    client: MemoryClient,
    workspace_name: str,
    content: str
) -> MemoryResponse:
    workspace: WorkspaceResponse = client.workspaces.create(
        name=workspace_name,
        slug=workspace_name.lower().replace(" ", "-")
    )

    agent: AgentResponse = client.agents.create(
        workspace_id=workspace.id,
        name="Typed Agent",
        agent_type="assistant"
    )

    memory: MemoryResponse = client.memories.create(
        agent_id=agent.id,
        project_id=workspace.slug,
        type="learning",
        content=content
    )

    return memory
```

---

## Configuration Options

```python
client = MemoryClient(
    base_url="http://localhost:8000/api/v1",
    api_key="your-api-key",           # Optional: for production auth
    timeout=30.0,                      # Request timeout in seconds
    max_retries=3,                     # Max retry attempts
    retry_delay=1.0,                   # Initial retry delay
    verify_ssl=True,                   # SSL verification
    user_agent="MyApp/1.0"             # Custom user agent
)
```

---

## Testing

For testing, you can mock the client:

```python
from unittest.mock import Mock, patch
from agent_memory import MemoryClient

def test_memory_creation():
    mock_client = Mock(spec=MemoryClient)
    mock_client.memories.create.return_value = Mock(
        id="test-memory-id",
        content="Test content"
    )

    # Your test code using mock_client
    memory = mock_client.memories.create(
        agent_id="test-agent",
        project_id="test-project",
        type="learning",
        content="Test"
    )

    assert memory.id == "test-memory-id"
```

---

## Next Steps

- Read the [Full API Reference](./API_REFERENCE.md)
- Check out [TypeScript SDK Quickstart](./TYPESCRIPT_SDK_QUICKSTART.md)
- Review [Error Handling Best Practices](./ERROR_HANDLING.md)
- Learn about [Memory Compaction Strategies](./MEMORY_COMPACTION.md)

---

**Last Updated:** 2026-03-26
**Maintained By:** Faintech Lab Team
