# Agent Memory Cloud SDK

Python SDK for [Agent Memory Cloud](https://faintech.dev) - Persistent memory infrastructure for AI agent fleets.

## Installation

```bash
pip install agentmemory
```

## Quick Start

### 1. Get Your API Key

Sign up at [faintech.dev](https://faintech.dev) and generate an API key from your dashboard.

### 2. Authentication

The SDK uses **Bearer token authentication**. Your API key is automatically sent in the `Authorization` header:

```
Authorization: Bearer amc_live_your_api_key_here
```

**Important:** Never share your API key or commit it to version control. Use environment variables instead.

### 3. Initialize the Client

```python
from agentmemory import MemoryClient

# Initialize with API key
client = MemoryClient(api_key="your-api-key-here")

# Or use environment variable (recommended)
# export AGENT_MEMORY_API_KEY="your-api-key-here"
client = MemoryClient()
```

### 3. Store Your First Memory

```python
# Create a memory
memory = client.memories.create(
    agent_id="my-agent-001",
    memory_type="outcome",
    content="Successfully deployed Redis caching layer for search optimization. Response times improved by 60%.",
    tags=["deployment", "redis", "performance"],
    metadata={
        "confidence": 0.95,
        "environment": "production"
    }
)

print(f"Created memory: {memory.id}")
```

### 4. Search Memories

```python
# Keyword search
results = client.search.keyword(
    query="redis caching",
    limit=10
)

for result in results:
    print(f"Score: {result.score}")
    print(f"Content: {result.memory.content}")
    print(f"Tags: {result.memory.tags}\n")
```

### 5. Semantic Search

```python
# Natural language search
results = client.search.semantic(
    query="How did we improve the search performance?",
    limit=5
)

for result in results:
    print(f"Relevance: {result.score:.2f}")
    print(f"Memory: {result.memory.content}\n")
```

## Core Concepts

### Memory Types

The SDK supports four types of memories:

- **outcome**: Results of actions or tasks
- **learning**: Insights and lessons learned
- **preference**: User or agent preferences
- **decision**: Important decisions made

```python
# Outcome memory
client.memories.create(
    agent_id="agent-001",
    memory_type="outcome",
    content="Task completed successfully with optimizations"
)

# Learning memory
client.memories.create(
    agent_id="agent-001",
    memory_type="learning",
    content="Redis caching works best for frequently accessed data"
)

# Preference memory
client.memories.create(
    agent_id="agent-001",
    memory_type="preference",
    content="User prefers concise summaries over detailed reports"
)

# Decision memory
client.memories.create(
    agent_id="agent-001",
    memory_type="decision",
    content="Chose PostgreSQL over MongoDB for better relational queries"
)
```

### Agents

Agents represent AI assistants or bots that create and own memories.

```python
# Create an agent
agent = client.agents.create(
    name="Customer Support Bot",
    description="Handles customer inquiries and support tickets"
)

# List all agents
agents = client.agents.list()
for agent in agents:
    print(f"{agent.id}: {agent.name}")
```

### Projects

Projects help organize memories by context or initiative.

```python
# Create a project
project = client.projects.create(
    name="E-commerce Platform",
    description="Main e-commerce system"
)

# Create memory with project association
client.memories.create(
    agent_id="agent-001",
    project_id=project.id,
    memory_type="outcome",
    content="Implemented payment processing module"
)
```

## API Reference

### Memories

#### Create Memory

```python
memory = client.memories.create(
    agent_id: str,              # Required: Agent ID
    memory_type: str,           # Required: "outcome" | "learning" | "preference" | "decision"
    content: str,               # Required: Memory content (max 10KB)
    project_id: str = None,     # Optional: Project association
    tags: List[str] = [],       # Optional: Tags (max 10)
    metadata: Dict = {}         # Optional: Additional metadata
)
```

#### Get Memory

```python
memory = client.memories.get(memory_id="memory-uuid")
```

#### List Memories

```python
# List all memories
memories = client.memories.list()

# With filters
memories = client.memories.list(
    agent_id="agent-001",
    project_id="project-001",
    memory_type="outcome",
    tags=["redis"],
    limit=20,
    offset=0
)
```

#### Update Memory

```python
memory = client.memories.update(
    memory_id="memory-uuid",
    content="Updated content",
    tags=["new-tag"],
    importance=0.9
)
```

#### Delete Memory

```python
client.memories.delete(memory_id="memory-uuid")
```

### Search

#### Keyword Search

```python
results = client.search.keyword(
    query: str,                     # Required: Search query
    agent_id: str = None,           # Optional: Filter by agent
    project_id: str = None,         # Optional: Filter by project
    memory_types: List[str] = [],   # Optional: Filter by types
    tags: List[str] = [],           # Optional: Filter by tags
    limit: int = 20                 # Optional: Max results
)
```

#### Semantic Search

```python
results = client.search.semantic(
    query: str,                     # Required: Natural language query
    agent_id: str = None,           # Optional: Filter by agent
    project_id: str = None,         # Optional: Filter by project
    memory_types: List[str] = [],   # Optional: Filter by types
    tags: List[str] = [],           # Optional: Filter by tags
    limit: int = 20                 # Optional: Max results
)
```

### Agents

```python
# Create agent
agent = client.agents.create(
    name: str,
    description: str = None
)

# List agents
agents = client.agents.list()

# Get agent
agent = client.agents.get(agent_id="agent-id")

# Update agent
agent = client.agents.update(
    agent_id="agent-id",
    name="New Name"
)

# Delete agent
client.agents.delete(agent_id="agent-id")
```

### Projects

```python
# Create project
project = client.projects.create(
    name: str,
    description: str = None
)

# List projects
projects = client.projects.list()

# Get project
project = client.projects.get(project_id="project-id")

# Update project
project = client.projects.update(
    project_id="project-id",
    name="New Name"
)

# Delete project
client.projects.delete(project_id="project-id")
```

## Advanced Usage

### Pagination

For large result sets, use pagination:

```python
offset = 0
limit = 50
all_memories = []

while True:
    memories = client.memories.list(limit=limit, offset=offset)
    all_memories.extend(memories)

    if len(memories) < limit:
        break

    offset += limit

print(f"Total memories: {len(all_memories)}")
```

### Error Handling

```python
from agentmemory import MemoryClient, NotFoundError, ValidationError

client = MemoryClient()

try:
    memory = client.memories.get("invalid-id")
except NotFoundError:
    print("Memory not found")
except ValidationError as e:
    print(f"Validation error: {e.message}")
except Exception as e:
    print(f"Error: {e}")
```

### Rate Limiting

The SDK automatically handles rate limiting. You can also configure retry behavior:

```python
client = MemoryClient(
    api_key="your-key",
    max_retries=3,
    retry_delay=1.0  # seconds
)
```

### Custom Base URL

For development or self-hosted instances:

```python
client = MemoryClient(
    api_key="your-key",
    base_url="http://localhost:8000/v1"
)
```

## Examples

### Example 1: Store Task Outcomes

```python
from agentmemory import MemoryClient

client = MemoryClient()

def complete_task(task_name, result, success=True):
    """Store task outcome as memory."""
    memory = client.memories.create(
        agent_id="task-runner",
        memory_type="outcome",
        content=f"Task '{task_name}': {result}",
        tags=["task", "automation"],
        metadata={
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
    )
    return memory

# Use it
memory = complete_task(
    "deploy-production",
    "Deployed v2.1.0 to production. All services healthy.",
    success=True
)
```

### Example 2: Learn from User Feedback

```python
def store_user_feedback(user_id, feedback, category):
    """Store user feedback as a learning memory."""
    memory = client.memories.create(
        agent_id=f"user-{user_id}",
        memory_type="learning",
        content=feedback,
        tags=["feedback", category],
        metadata={
            "user_id": user_id,
            "category": category
        }
    )
    return memory

# Use it
store_user_feedback(
    "12345",
    "Users prefer shorter loading screens with progress indicators",
    "ux"
)
```

### Example 3: Context Retrieval for Conversations

```python
def get_relevant_context(user_query, agent_id, limit=5):
    """Retrieve relevant memories for conversation context."""
    results = client.search.semantic(
        query=user_query,
        agent_id=agent_id,
        limit=limit
    )

    context = []
    for result in results:
        context.append({
            "content": result.memory.content,
            "relevance": result.score,
            "type": result.memory.memory_type
        })

    return context

# Use it
context = get_relevant_context(
    "How do I optimize database queries?",
    agent_id="support-bot"
)

for item in context:
    print(f"[{item['type']}] {item['content']} (relevance: {item['relevance']:.2f})")
```

## Type Safety

This SDK provides full type hints for all methods and models. Use with `mypy` for type checking:

```bash
mypy --strict your_code.py
```

## Requirements

- Python 3.8 or higher
- `httpx` >= 0.24.0
- `pydantic` >= 2.0.0

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📧 Email: support@faintech.dev
- 📖 Documentation: https://docs.faintech.dev
- 🐛 Issues: https://github.com/faintech/agentmemory-sdk-python/issues

## Troubleshooting

### Authentication Errors (401 Unauthorized)

If you receive 401 errors:

1. **Check your API key format**: Keys should start with `amc_live_`
2. **Verify the key is active**: Log into your dashboard and ensure the key isn't revoked
3. **Check the Authorization header**: The SDK sends `Authorization: Bearer {api_key}` - verify this in your network logs
4. **Environment variable**: Ensure `AGENT_MEMORY_API_KEY` is set correctly

Example debugging:
```python
import os
print(f"API Key set: {'AGENT_MEMORY_API_KEY' in os.environ}")
print(f"API Key prefix: {os.environ.get('AGENT_MEMORY_API_KEY', '')[:10]}...")
```

### Connection Errors

If you can't connect to the API:

1. **Check base URL**: Default is `https://api.faintech.dev/v1`
2. **Network access**: Ensure your network allows HTTPS connections
3. **Firewall**: Check if corporate firewall blocks the API

For self-hosted instances:
```python
client = MemoryClient(
    api_key="your-key",
    base_url="http://your-instance.com/v1"
)
```

### Rate Limiting (429 Too Many Requests)

The API has rate limits:
- 60 requests/minute
- 1000 requests/hour

The SDK automatically retries on 429 errors. If you still hit limits:
- Reduce request frequency
- Implement client-side caching
- Contact support for limit increases

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.
