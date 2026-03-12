# @agentmemory/sdk

TypeScript SDK for [Agent Memory Cloud](https://faintech.dev) - Persistent memory infrastructure for AI agent fleets.

## Installation

```bash
npm install @agentmemory/sdk
# or
yarn add @agentmemory/sdk
# or
pnpm add @agentmemory/sdk
```

## Quick Start

### 1. Get Your API Key

Sign up at [faintech.dev](https://faintech.dev) and generate an API key from your dashboard.

### 2. Initialize the Client

```typescript
import { MemoryClient } from '@agentmemory/sdk';

// Initialize with API key
const client = new MemoryClient({ apiKey: 'your-api-key-here' });

// Or use environment variable
// export AGENT_MEMORY_API_KEY="your-api-key-here"
const client = new MemoryClient();
```

### 3. Store Your First Memory

```typescript
// Create a memory
const memory = await client.memories.create({
  agentId: 'my-agent-001',
  memoryType: 'outcome',
  content: 'Successfully deployed Redis caching layer for search optimization. Response times improved by 60%.',
  tags: ['deployment', 'redis', 'performance'],
  metadata: {
    confidence: 0.95,
    environment: 'production'
  }
});

console.log(`Created memory: ${memory.id}`);
```

### 4. Search Memories

```typescript
// Keyword search
const results = await client.search.keyword({
  query: 'redis caching',
  limit: 10
});

for (const result of results) {
  console.log(`Score: ${result.score}`);
  console.log(`Content: ${result.memory.content}`);
  console.log(`Tags: ${result.memory.tags}\n`);
}
```

### 5. Semantic Search

```typescript
// Natural language search
const results = await client.search.semantic({
  query: 'How did we improve the search performance?',
  limit: 5
});

for (const result of results) {
  console.log(`Relevance: ${result.score.toFixed(2)}`);
  console.log(`Memory: ${result.memory.content}\n`);
}
```

## Core Concepts

### Memory Types

The SDK supports four types of memories:

- **outcome**: Results of actions or tasks
- **learning**: Insights and lessons learned
- **preference**: User or agent preferences
- **decision**: Important decisions made

```typescript
// Outcome memory
await client.memories.create({
  agentId: 'agent-001',
  memoryType: 'outcome',
  content: 'Task completed successfully with optimizations'
});

// Learning memory
await client.memories.create({
  agentId: 'agent-001',
  memoryType: 'learning',
  content: 'Redis caching works best for frequently accessed data'
});

// Preference memory
await client.memories.create({
  agentId: 'agent-001',
  memoryType: 'preference',
  content: 'User prefers concise summaries over detailed reports'
});

// Decision memory
await client.memories.create({
  agentId: 'agent-001',
  memoryType: 'decision',
  content: 'Chose PostgreSQL over MongoDB for better relational queries'
});
```

### Agents

Agents represent AI assistants or bots that create and own memories.

```typescript
// Create an agent
const agent = await client.agents.create({
  name: 'Customer Support Bot',
  description: 'Handles customer inquiries and support tickets'
});

// List all agents
const agents = await client.agents.list();
for (const agent of agents.items) {
  console.log(`${agent.id}: ${agent.name}`);
}
```

### Projects

Projects help organize memories by context or initiative.

```typescript
// Create a project
const project = await client.projects.create({
  name: 'E-commerce Platform',
  description: 'Main e-commerce system'
});

// Create memory with project association
await client.memories.create({
  agentId: 'agent-001',
  projectId: project.id,
  memoryType: 'outcome',
  content: 'Implemented payment processing module'
});
```

## API Reference

### Memories

#### Create Memory

```typescript
const memory = await client.memories.create({
  agentId: string,              // Required: Agent ID
  memoryType: MemoryType,       // Required: "outcome" | "learning" | "preference" | "decision"
  content: string,              // Required: Memory content (max 10KB)
  projectId?: string,           // Optional: Project association
  tags?: string[],              // Optional: Tags (max 10)
  metadata?: Record<string, unknown> // Optional: Additional metadata
});
```

#### Get Memory

```typescript
const memory = await client.memories.get('memory-uuid');
```

#### List Memories

```typescript
// List all memories
const memories = await client.memories.list();

// With filters
const memories = await client.memories.list({
  agentId: 'agent-001',
  projectId: 'project-001',
  memoryType: 'outcome',
  tags: ['redis'],
  limit: 20,
  offset: 0
});
```

#### Update Memory

```typescript
const memory = await client.memories.update({
  memoryId: 'memory-uuid',
  content: 'Updated content',
  tags: ['new-tag'],
  confidence: 0.9
});
```

#### Delete Memory

```typescript
await client.memories.delete('memory-uuid');
```

#### Compact Memories

```typescript
const result = await client.memories.compact({
  agentId: 'agent-001',
  maxAgeDays: 30,
});
console.log(`Processed ${result.memoriesProcessed} memories`);
```

### Search

#### Keyword Search

```typescript
const results = await client.search.keyword({
  query: string,                     // Required: Search query
  agentId?: string,                  // Optional: Filter by agent
  projectId?: string,                // Optional: Filter by project
  tags?: string[],                   // Optional: Filter by tags
  limit?: number                     // Optional: Max results (default: 10)
});
```

#### Semantic Search

```typescript
const results = await client.search.semantic({
  query: string,                     // Required: Natural language query
  agentId?: string,                  // Optional: Filter by agent
  projectId?: string,                // Optional: Filter by project
  tags?: string[],                   // Optional: Filter by tags
  limit?: number                     // Optional: Max results (default: 5)
});
```

### Agents

```typescript
// Create agent
const agent = await client.agents.create({
  name: string,
  description?: string
});

// List agents
const agents = await client.agents.list();

// Get agent
const agent = await client.agents.get('agent-id');
```

### Projects

```typescript
// Create project
const project = await client.projects.create({
  name: string,
  description?: string
});

// List projects
const projects = await client.projects.list();

// Get project
const project = await client.projects.get('project-id');
```

## Advanced Usage

### Pagination

For large result sets, use pagination:

```typescript
let offset = 0;
const limit = 50;
const allMemories = [];

while (true) {
  const response = await client.memories.list({ limit, offset });
  allMemories.push(...response.items);
  
  if (!hasMore(response)) {
    break;
  }
  
  offset += limit;
}

console.log(`Total memories: ${allMemories.length}`);
```

### Error Handling

```typescript
import { 
  MemoryClient, 
  NotFoundError, 
  ValidationError,
  AuthenticationError,
  RateLimitError 
} from '@agentmemory/sdk';

const client = new MemoryClient();

try {
  const memory = await client.memories.get('invalid-id');
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log('Memory not found');
  } else if (error instanceof ValidationError) {
    console.log(`Validation error: ${error.message}`);
  } else if (error instanceof AuthenticationError) {
    console.log('Invalid API key');
  } else if (error instanceof RateLimitError) {
    console.log(`Rate limited. Retry after: ${error.retryAfter}s`);
  } else {
    console.log(`Error: ${error}`);
  }
}
```

### Custom Base URL

For development or self-hosted instances:

```typescript
const client = new MemoryClient({
  apiKey: 'your-key',
  baseUrl: 'http://localhost:8000/v1'
});
```

## Type Safety

This SDK is written in TypeScript and provides full type definitions with `strict` mode enabled. All methods and models are fully typed:

```typescript
import {
  MemoryClient,
  Memory,
  MemoryType,
  Agent,
  Project,
  SearchResult,
  MemoryCreateParams,
  PaginatedResponse
} from '@agentmemory/sdk';

// Full autocomplete and type checking
const client = new MemoryClient();

const memory: Memory = await client.memories.create({
  agentId: 'agent-001',
  memoryType: 'outcome', // Autocomplete shows valid types
  content: 'Task completed'
});
```

## Requirements

- Node.js 16.x or higher
- TypeScript 4.7 or higher (for type checking)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📧 Email: support@faintech.dev
- 📖 Documentation: https://docs.faintech.dev
- 🐛 Issues: https://github.com/faintech/agentmemory-sdk-typescript/issues

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.
