# TypeScript SDK Quickstart Guide

**Agent Memory Cloud TypeScript/JavaScript SDK**

Get started with the Agent Memory Cloud TypeScript SDK in 5 minutes.

---

## Installation

### npm

```bash
npm install @faintech/agent-memory-client
```

### yarn

```bash
yarn add @faintech/agent-memory-client
```

### pnpm

```bash
pnpm add @faintech/agent-memory-client
```

---

## Quick Start

### 1. Initialize the Client

```typescript
import { MemoryClient } from '@faintech/agent-memory-client';

// Initialize client (development mode - no auth required)
const client = new MemoryClient({
  baseUrl: 'http://localhost:8000/api/v1'
});

// For production, configure with authentication
// const client = new MemoryClient({
//   baseUrl: 'https://api.example.com/api/v1',
//   apiKey: 'your-api-key'
// });
```

### 2. Create a Workspace

```typescript
// Create a new workspace for your project
const workspace = await client.workspaces.create({
  name: 'My AI Project',
  slug: 'my-ai-project'
});

console.log(`Workspace created: ${workspace.id}`);
```

### 3. Register an Agent

```typescript
// Register your AI agent in the workspace
const agent = await client.agents.create({
  workspaceId: workspace.id,
  name: 'Code Assistant',
  agentType: 'assistant',
  metadata: {
    model: 'gpt-4',
    capabilities: ['code-generation', 'debugging']
  }
});

console.log(`Agent registered: ${agent.id}`);
```

### 4. Store Memories

```typescript
// Store a learning memory
const memory = await client.memories.create({
  agentId: agent.id,
  projectId: 'my-project',
  taskId: 'TASK-001',
  type: 'learning',
  content: 'User prefers TypeScript over JavaScript for new projects',
  tags: ['preference', 'typescript', 'coding-style'],
  metadata: { importance: 'high', source: 'user-feedback' }
});

console.log(`Memory stored: ${memory.id}`);
```

### 5. Search Memories

```typescript
// Semantic search across memories
const results = await client.memories.search({
  query: 'typescript preferences',
  agentId: agent.id,
  tags: ['preference'],
  limit: 10
});

for (const memory of results.memories) {
  console.log(`- ${memory.content}`);
}
```

---

## TypeScript Types

The SDK provides full TypeScript types for all operations:

```typescript
import {
  MemoryClient,
  Workspace,
  WorkspaceCreate,
  Agent,
  AgentCreate,
  Memory,
  MemoryCreate,
  MemoryType,
  MemorySearchRequest,
  MemoryListResponse,
  APIError
} from '@faintech/agent-memory-client';

// All types are fully typed
const workspaceCreate: WorkspaceCreate = {
  name: 'Typed Workspace',
  slug: 'typed-workspace'
};

const memoryCreate: MemoryCreate = {
  agentId: 'agent-id',
  projectId: 'project-id',
  type: 'learning' as MemoryType,
  content: 'TypeScript provides excellent type safety'
};
```

---

## Common Patterns

### Storing Different Memory Types

```typescript
// Learning: Things the agent discovered
await client.memories.create({
  agentId: agent.id,
  projectId: 'my-project',
  type: 'learning',
  content: 'React 18 introduced automatic batching',
  tags: ['react', 'performance']
});

// Decision: Important choices made
await client.memories.create({
  agentId: agent.id,
  projectId: 'my-project',
  type: 'decision',
  content: 'Chose PostgreSQL over MongoDB for ACID compliance requirements',
  tags: ['architecture', 'database', 'decision']
});

// Error: Issues encountered and resolutions
await client.memories.create({
  agentId: agent.id,
  projectId: 'my-project',
  type: 'error',
  content: 'CORS error resolved by adding credentials: true to fetch options',
  tags: ['cors', 'frontend', 'bug-fix']
});

// Context: Important context to remember
await client.memories.create({
  agentId: agent.id,
  projectId: 'my-project',
  type: 'context',
  content: 'Project uses ESLint with Airbnb config and Prettier for formatting',
  tags: ['linting', 'formatting', 'tooling']
});
```

### Batch Memory Operations

```typescript
// Store multiple memories using Promise.all
const memoriesData = [
  {
    agentId: agent.id,
    projectId: 'my-project',
    type: 'learning' as MemoryType,
    content: 'Zod provides runtime type validation',
    tags: ['validation', 'typescript']
  },
  {
    agentId: agent.id,
    projectId: 'my-project',
    type: 'learning' as MemoryType,
    content: 'TanStack Query simplifies server state management',
    tags: ['state-management', 'react']
  }
];

const memories = await Promise.all(
  memoriesData.map(data => client.memories.create(data))
);

console.log(`Created ${memories.length} memories`);
```

### Time-Based Filtering

```typescript
// Get memories from the last 7 days
const since = new Date();
since.setDate(since.getDate() - 7);

const results = await client.memories.search({
  agentId: agent.id,
  since: since.toISOString(),
  until: new Date().toISOString(),
  limit: 50
});
```

### Getting Recent Memories

```typescript
// Get recent memories for an agent
const recent = await client.memories.getByAgent({
  agentId: agent.id,
  limit: 20
});

for (const memory of recent.memories) {
  console.log(`[${memory.type}] ${memory.content}`);
}
```

### Task-Specific Memories

```typescript
// Get all memories related to a specific task
const taskMemories = await client.memories.getByTask({
  projectId: 'my-project',
  taskId: 'TASK-001',
  limit: 100
});

// Useful for context injection before working on a task
const context = taskMemories.memories.map(m => m.content).join('\n');
console.log('Task context:', context);
```

---

## Memory Compaction

For long-running agents, compact old memories to save space:

```typescript
// Compact memories older than 30 days
const result = await client.memories.compact({
  agentId: agent.id,
  daysOld: 30
});

console.log(`Compacted ${result.compacted} memories`);
console.log(`Created ${result.summariesCreated} summary memories`);
```

---

## Error Handling

```typescript
import { MemoryClient, APIError, NotFoundError, ConflictError } from '@faintech/agent-memory-client';

const client = new MemoryClient({ baseUrl: 'http://localhost:8000/api/v1' });

try {
  const workspace = await client.workspaces.create({
    name: 'Test Workspace',
    slug: 'test-workspace'
  });
} catch (error) {
  if (error instanceof ConflictError) {
    console.log(`Workspace already exists: ${error.message}`);
  } else if (error instanceof NotFoundError) {
    console.log(`Resource not found: ${error.resourceId}`);
  } else if (error instanceof APIError) {
    console.log(`API Error: ${error.message}`);
    console.log(`Status Code: ${error.statusCode}`);
    console.log(`Details:`, error.details);
  } else {
    throw error;
  }
}
```

### Common Error Codes

| Code | Error Class | Description | Solution |
|------|-------------|-------------|----------|
| 400 | `ValidationError` | Bad Request | Check request body format |
| 404 | `NotFoundError` | Not Found | Verify resource ID exists |
| 409 | `ConflictError` | Conflict | Resource already exists |
| 429 | `RateLimitError` | Rate Limited | Reduce request frequency |
| 500 | `APIError` | Server Error | Retry or contact support |

### Error Classes

```typescript
import {
  APIError,
  ValidationError,
  NotFoundError,
  ConflictError,
  RateLimitError
} from '@faintech/agent-memory-client';

// Each error class provides specific information
try {
  await client.workspaces.get('non-existent-id');
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log(`Resource type: ${error.resourceType}`);
    console.log(`Resource ID: ${error.resourceId}`);
  }
}

try {
  await client.workspaces.create({ name: 'Test', slug: 'existing-slug' });
} catch (error) {
  if (error instanceof ConflictError) {
    console.log(`Conflict field: ${error.field}`);
    console.log(`Conflict value: ${error.value}`);
  }
}
```

---

## Rate Limiting

The SDK automatically handles rate limiting with exponential backoff:

```typescript
// Configure custom rate limit handling
const client = new MemoryClient({
  baseUrl: 'http://localhost:8000/api/v1',
  maxRetries: 3,
  retryDelay: 1000  // milliseconds
});
```

Default limits:
- General endpoints: 100 requests/minute
- Search endpoints: 30 requests/minute
- Write endpoints: 50 requests/minute

### Manual Rate Limit Handling

```typescript
import { RateLimitError } from '@faintech/agent-memory-client';

try {
  await client.memories.create({ ... });
} catch (error) {
  if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after: ${error.retryAfter}ms`);
    console.log(`Limit: ${error.limit}`);
    console.log(`Remaining: ${error.remaining}`);

    // Wait and retry
    await new Promise(resolve => setTimeout(resolve, error.retryAfter));
    await client.memories.create({ ... });
  }
}
```

---

## Complete Example: AI Assistant with Memory

```typescript
import { MemoryClient, Memory, MemoryType } from '@faintech/agent-memory-client';

interface AssistantConfig {
  baseUrl: string;
  name: string;
}

class MemoryEnabledAssistant {
  private client: MemoryClient;
  private workspaceId?: string;
  private agentId?: string;
  private name: string;

  constructor(config: AssistantConfig) {
    this.client = new MemoryClient({ baseUrl: config.baseUrl });
    this.name = config.name;
  }

  async setup(): Promise<void> {
    // Create or get workspace
    const workspaces = await this.client.workspaces.list();
    let workspace = workspaces.find(w => w.name === this.name);

    if (!workspace) {
      workspace = await this.client.workspaces.create({
        name: this.name,
        slug: this.name.toLowerCase().replace(/\s+/g, '-')
      });
    }

    this.workspaceId = workspace.id;

    // Create agent
    const agent = await this.client.agents.create({
      workspaceId: workspace.id,
      name: `${this.name} Assistant`,
      agentType: 'assistant'
    });

    this.agentId = agent.id;
  }

  async remember(
    content: string,
    type: MemoryType = 'learning',
    tags: string[] = [],
    taskId?: string
  ): Promise<Memory> {
    if (!this.agentId || !this.workspaceId) {
      throw new Error('Assistant not initialized. Call setup() first.');
    }

    return this.client.memories.create({
      agentId: this.agentId,
      projectId: this.name.toLowerCase().replace(/\s+/g, '-'),
      taskId,
      type,
      content,
      tags
    });
  }

  async recall(query: string, limit: number = 10): Promise<Memory[]> {
    if (!this.agentId) {
      throw new Error('Assistant not initialized. Call setup() first.');
    }

    const result = await this.client.memories.search({
      query,
      agentId: this.agentId,
      limit
    });

    return result.memories;
  }

  async getContext(taskId?: string): Promise<Memory[]> {
    if (!this.agentId || !this.workspaceId) {
      throw new Error('Assistant not initialized. Call setup() first.');
    }

    if (taskId) {
      const result = await this.client.memories.getByTask({
        projectId: this.name.toLowerCase().replace(/\s+/g, '-'),
        taskId,
        limit: 50
      });
      return result.memories;
    }

    const result = await this.client.memories.getByAgent({
      agentId: this.agentId,
      limit: 20
    });

    return result.memories;
  }
}

// Usage
async function main() {
  const assistant = new MemoryEnabledAssistant({
    baseUrl: 'http://localhost:8000/api/v1',
    name: 'Code Review Bot'
  });

  await assistant.setup();

  // Remember something
  await assistant.remember(
    'User prefers descriptive variable names over short ones',
    'learning',
    ['coding-style', 'variables']
  );

  // Recall relevant memories
  const memories = await assistant.recall('variable naming preferences');
  for (const memory of memories) {
    console.log(`- ${memory.content}`);
  }
}

main().catch(console.error);
```

---

## Pagination

For large result sets, use pagination:

```typescript
// List all workspaces with pagination
async function getAllWorkspaces(): Promise<Workspace[]> {
  const allWorkspaces: Workspace[] = [];
  let skip = 0;
  const limit = 100;

  while (true) {
    const batch = await client.workspaces.list({ skip, limit });
    allWorkspaces.push(...batch);

    if (batch.length < limit) {
      break;
    }
    skip += limit;
  }

  console.log(`Total workspaces: ${allWorkspaces.length}`);
  return allWorkspaces;
}
```

---

## Using with React

```typescript
import { useEffect, useState } from 'react';
import { MemoryClient, Memory } from '@faintech/agent-memory-client';

const client = new MemoryClient({ baseUrl: 'http://localhost:8000/api/v1' });

export function useMemories(agentId: string, limit: number = 20) {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function fetchMemories() {
      try {
        const result = await client.memories.getByAgent({
          agentId,
          limit
        });
        setMemories(result.memories);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    }

    fetchMemories();
  }, [agentId, limit]);

  const addMemory = async (content: string, type: MemoryType = 'learning') => {
    const memory = await client.memories.create({
      agentId,
      projectId: 'react-app',
      type,
      content
    });
    setMemories(prev => [memory, ...prev]);
    return memory;
  };

  return { memories, loading, error, addMemory };
}

// Usage in component
function MemoryList({ agentId }: { agentId: string }) {
  const { memories, loading, error, addMemory } = useMemories(agentId);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <button onClick={() => addMemory('New memory', 'learning')}>
        Add Memory
      </button>
      <ul>
        {memories.map(memory => (
          <li key={memory.id}>
            <strong>[{memory.type}]</strong> {memory.content}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Using with Next.js API Routes

```typescript
// pages/api/memories.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { MemoryClient } from '@faintech/agent-memory-client';

const client = new MemoryClient({
  baseUrl: process.env.MEMORY_API_URL!
});

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    const { agentId, limit = '20' } = req.query;

    const result = await client.memories.getByAgent({
      agentId: agentId as string,
      limit: parseInt(limit as string, 10)
    });

    return res.status(200).json(result);
  }

  if (req.method === 'POST') {
    const memory = await client.memories.create(req.body);
    return res.status(201).json(memory);
  }

  return res.status(405).json({ message: 'Method not allowed' });
}
```

---

## Configuration Options

```typescript
const client = new MemoryClient({
  baseUrl: 'http://localhost:8000/api/v1',
  apiKey: 'your-api-key',          // Optional: for production auth
  timeout: 30000,                   // Request timeout in milliseconds
  maxRetries: 3,                    // Max retry attempts
  retryDelay: 1000,                 // Initial retry delay in ms
  verifySSL: true,                  // SSL verification
  userAgent: 'MyApp/1.0',           // Custom user agent
  headers: {                        // Custom headers
    'X-Custom-Header': 'value'
  }
});
```

---

## Testing

For testing, you can mock the client:

```typescript
import { MemoryClient } from '@faintech/agent-memory-client';
import { mockDeep, DeepMockProxy } from 'jest-mock-extended';

describe('MemoryService', () => {
  let client: DeepMockProxy<MemoryClient>;

  beforeEach(() => {
    client = mockDeep<MemoryClient>();
  });

  it('should create a memory', async () => {
    client.memories.create.mockResolvedValue({
      id: 'test-memory-id',
      agentId: 'test-agent',
      projectId: 'test-project',
      taskId: null,
      timestamp: new Date().toISOString(),
      type: 'learning',
      content: 'Test content',
      tags: [],
      metadata: {}
    });

    const memory = await client.memories.create({
      agentId: 'test-agent',
      projectId: 'test-project',
      type: 'learning',
      content: 'Test'
    });

    expect(memory.id).toBe('test-memory-id');
    expect(client.memories.create).toHaveBeenCalledWith({
      agentId: 'test-agent',
      projectId: 'test-project',
      type: 'learning',
      content: 'Test'
    });
  });
});
```

---

## Environment Variables

```bash
# .env
MEMORY_API_URL=http://localhost:8000/api/v1
MEMORY_API_KEY=your-api-key
MEMORY_TIMEOUT=30000
MEMORY_MAX_RETRIES=3
```

```typescript
// config.ts
import { MemoryClient } from '@faintech/agent-memory-client';

export const memoryClient = new MemoryClient({
  baseUrl: process.env.MEMORY_API_URL!,
  apiKey: process.env.MEMORY_API_KEY,
  timeout: parseInt(process.env.MEMORY_TIMEOUT || '30000', 10),
  maxRetries: parseInt(process.env.MEMORY_MAX_RETRIES || '3', 10)
});
```

---

## Next Steps

- Read the [Full API Reference](./API_REFERENCE.md)
- Check out [Python SDK Quickstart](./PYTHON_SDK_QUICKSTART.md)
- Review [Error Handling Best Practices](./ERROR_HANDLING.md)
- Learn about [Memory Compaction Strategies](./MEMORY_COMPACTION.md)

---

**Last Updated:** 2026-03-26
**Maintained By:** Faintech Lab Team
