# Agent Memory Cloud API Reference

**Version:** 1.0.0
**Base URL:** `http://localhost:8000/api/v1`
**Content-Type:** `application/json`

---

## Overview

Agent Memory Cloud provides a RESTful API for managing workspaces, agents, and their persistent memories. The API supports CRUD operations, semantic search, and memory compaction.

**Authentication:** Currently no authentication (development mode)
**Rate Limiting:** Applied per endpoint (see individual endpoints)
**CORS:** Enabled for configured origins

---

## Endpoints

### Health

#### GET /health
Check API health status.

**Request:**
```http
GET /api/v1/health
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-03-25T15:00:00Z"
}
```

---

### Workspaces

#### POST /workspaces
Create a new workspace.

**Request:**
```http
POST /api/v1/workspaces
Content-Type: application/json

{
  "name": "Production Workspace",
  "slug": "prod-workspace"
}
```

**Response:** `201 Created`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Production Workspace",
  "slug": "prod-workspace",
  "created_at": "2026-03-25T15:00:00Z",
  "updated_at": "2026-03-25T15:00:00Z"
}
```

**Errors:**
- `409 Conflict` - Workspace with slug already exists

---

#### GET /workspaces
List all workspaces.

**Request:**
```http
GET /api/v1/workspaces?skip=0&limit=100
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100, max: 100)

**Response:** `200 OK`
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Production Workspace",
    "slug": "prod-workspace",
    "created_at": "2026-03-25T15:00:00Z",
    "updated_at": "2026-03-25T15:00:00Z"
  }
]
```

---

#### GET /workspaces/{workspace_id}
Get a workspace by ID.

**Request:**
```http
GET /api/v1/workspaces/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Production Workspace",
  "slug": "prod-workspace",
  "created_at": "2026-03-25T15:00:00Z",
  "updated_at": "2026-03-25T15:00:00Z"
}
```

**Errors:**
- `404 Not Found` - Workspace not found

---

#### DELETE /workspaces/{workspace_id}
Delete a workspace.

**Request:**
```http
DELETE /api/v1/workspaces/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `204 No Content`

**Errors:**
- `404 Not Found` - Workspace not found

---

### Agents

#### POST /agents
Create a new agent in a workspace.

**Request:**
```http
POST /api/v1/agents?workspace_id=550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{
  "name": "Dev Agent",
  "agent_type": "developer",
  "metadata_json": {
    "skills": ["python", "typescript"],
    "priority": "high"
  }
}
```

**Query Parameters:**
- `workspace_id` (required): Workspace ID to create agent in

**Response:** `201 Created`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Dev Agent",
  "agent_type": "developer",
  "is_active": true,
  "metadata_json": {
    "skills": ["python", "typescript"],
    "priority": "high"
  },
  "created_at": "2026-03-25T15:00:00Z",
  "updated_at": "2026-03-25T15:00:00Z"
}
```

**Errors:**
- `404 Not Found` - Workspace not found

---

#### GET /agents
List agents in a workspace.

**Request:**
```http
GET /api/v1/agents?workspace_id=550e8400-e29b-41d4-a716-446655440000&skip=0&limit=100&active_only=false
```

**Query Parameters:**
- `workspace_id` (required): Workspace ID
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100, max: 100)
- `active_only` (optional): Filter to active agents only (default: false)

**Response:** `200 OK`
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Dev Agent",
    "agent_type": "developer",
    "is_active": true,
    "metadata_json": {
      "skills": ["python", "typescript"],
      "priority": "high"
    },
    "created_at": "2026-03-25T15:00:00Z",
    "updated_at": "2026-03-25T15:00:00Z"
  }
]
```

---

#### GET /agents/{agent_id}
Get an agent by ID.

**Request:**
```http
GET /api/v1/agents/660e8400-e29b-41d4-a716-446655440001
```

**Response:** `200 OK`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Dev Agent",
  "agent_type": "developer",
  "is_active": true,
  "metadata_json": {
    "skills": ["python", "typescript"],
    "priority": "high"
  },
  "created_at": "2026-03-25T15:00:00Z",
  "updated_at": "2026-03-25T15:00:00Z"
}
```

**Errors:**
- `404 Not Found` - Agent not found

---

#### PATCH /agents/{agent_id}
Update an agent.

**Request:**
```http
PATCH /api/v1/agents/660e8400-e29b-41d4-a716-446655440001
Content-Type: application/json

{
  "name": "Senior Dev Agent",
  "is_active": false
}
```

**Response:** `200 OK`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Senior Dev Agent",
  "agent_type": "developer",
  "is_active": false,
  "metadata_json": {
    "skills": ["python", "typescript"],
    "priority": "high"
  },
  "created_at": "2026-03-25T15:00:00Z",
  "updated_at": "2026-03-25T15:30:00Z"
}
```

**Errors:**
- `404 Not Found` - Agent not found

---

#### DELETE /agents/{agent_id}
Delete an agent.

**Request:**
```http
DELETE /api/v1/agents/660e8400-e29b-41d4-a716-446655440001
```

**Response:** `204 No Content`

**Errors:**
- `404 Not Found` - Agent not found

---

### Memories

#### POST /memories
Create a new memory entry.

**Request:**
```http
POST /api/v1/memories
Content-Type: application/json

{
  "agent_id": "660e8400-e29b-41d4-a716-446655440001",
  "project_id": "faintech-lab",
  "task_id": "SPRINT3-001",
  "type": "learning",
  "content": "Discovered that FastAPI uses Pydantic models for request/response validation",
  "tags": ["fastapi", "pydantic", "validation"],
  "metadata": {
    "importance": "high",
    "category": "technical"
  }
}
```

**Response:** `201 Created`
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "agent_id": "660e8400-e29b-41d4-a716-446655440001",
  "project_id": "faintech-lab",
  "task_id": "SPRINT3-001",
  "timestamp": "2026-03-25T15:00:00Z",
  "type": "learning",
  "content": "Discovered that FastAPI uses Pydantic models for request/response validation",
  "tags": ["fastapi", "pydantic", "validation"],
  "metadata": {
    "importance": "high",
    "category": "technical"
  }
}
```

---

#### POST /memories/search
Search memory entries with filters.

**Request:**
```http
POST /api/v1/memories/search
Content-Type: application/json

{
  "query": "fastapi validation",
  "agent_id": "660e8400-e29b-41d4-a716-446655440001",
  "project_id": "faintech-lab",
  "entry_type": "learning",
  "tags": ["fastapi"],
  "limit": 10,
  "since": "2026-03-01T00:00:00Z",
  "until": "2026-03-31T23:59:59Z"
}
```

**Response:** `200 OK`
```json
{
  "memories": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "agent_id": "660e8400-e29b-41d4-a716-446655440001",
      "project_id": "faintech-lab",
      "task_id": "SPRINT3-001",
      "timestamp": "2026-03-25T15:00:00Z",
      "type": "learning",
      "content": "Discovered that FastAPI uses Pydantic models for request/response validation",
      "tags": ["fastapi", "pydantic", "validation"],
      "metadata": {
        "importance": "high",
        "category": "technical"
      }
    }
  ],
  "total": 1
}
```

---

#### GET /memories/agent/{agent_id}
Get recent memories for an agent.

**Request:**
```http
GET /api/v1/memories/agent/660e8400-e29b-41d4-a716-446655440001?limit=10
```

**Query Parameters:**
- `limit` (optional): Maximum results (default: 10, min: 1, max: 100)

**Response:** `200 OK`
```json
{
  "memories": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "agent_id": "660e8400-e29b-41d4-a716-446655440001",
      "project_id": "faintech-lab",
      "task_id": "SPRINT3-001",
      "timestamp": "2026-03-25T15:00:00Z",
      "type": "learning",
      "content": "Discovered that FastAPI uses Pydantic models for request/response validation",
      "tags": ["fastapi", "pydantic", "validation"],
      "metadata": {
        "importance": "high",
        "category": "technical"
      }
    }
  ],
  "total": 1
}
```

---

#### GET /memories/task/{project_id}/{task_id}
Get memories for a specific task.

**Request:**
```http
GET /api/v1/memories/task/faintech-lab/SPRINT3-001?limit=50
```

**Query Parameters:**
- `limit` (optional): Maximum results (default: 50, min: 1, max: 100)

**Response:** `200 OK`
```json
{
  "memories": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "agent_id": "660e8400-e29b-41d4-a716-446655440001",
      "project_id": "faintech-lab",
      "task_id": "SPRINT3-001",
      "timestamp": "2026-03-25T15:00:00Z",
      "type": "learning",
      "content": "Discovered that FastAPI uses Pydantic models for request/response validation",
      "tags": ["fastapi", "pydantic", "validation"],
      "metadata": {
        "importance": "high",
        "category": "technical"
      }
    }
  ],
  "total": 1
}
```

---

#### POST /memories/compact
Compact old memories into summaries.

**Request:**
```http
POST /api/v1/memories/compact
Content-Type: application/json

{
  "agent_id": "660e8400-e29b-41d4-a716-446655440001",
  "days_old": 30
}
```

**Response:** `200 OK`
```json
{
  "compacted": 45,
  "summaries_created": 3,
  "files_archived": 42,
  "message": "Successfully compacted 45 memories older than 30 days"
}
```

---

## Error Responses

All endpoints return consistent error responses:

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource 'resource_id' not found"
}
```

### 409 Conflict
```json
{
  "detail": "Resource with field 'value' already exists"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

---

## Data Models

### WorkspaceCreate
```typescript
{
  name: string      // Required
  slug: string      // Required, unique
}
```

### WorkspaceResponse
```typescript
{
  id: string
  name: string
  slug: string
  created_at: string    // ISO 8601 datetime
  updated_at: string    // ISO 8601 datetime
}
```

### AgentCreate
```typescript
{
  name: string              // Required
  agent_type: string        // Required
  metadata_json?: object    // Optional
}
```

### AgentUpdate
```typescript
{
  name?: string
  agent_type?: string
  is_active?: boolean
  metadata_json?: object
}
```

### AgentResponse
```typescript
{
  id: string
  workspace_id: string
  name: string
  agent_type: string
  is_active: boolean
  metadata_json: object | null
  created_at: string    // ISO 8601 datetime
  updated_at: string    // ISO 8601 datetime
}
```

### MemoryCreate
```typescript
{
  agent_id: string           // Required
  project_id: string         // Required
  task_id?: string           // Optional
  type: string               // Required: "learning" | "decision" | "error" | "context"
  content: string            // Required
  tags?: string[]            // Optional
  metadata?: object          // Optional
}
```

### MemoryResponse
```typescript
{
  id: string
  agent_id: string
  project_id: string
  task_id: string | null
  timestamp: string          // ISO 8601 datetime
  type: string
  content: string
  tags: string[]
  metadata: object
}
```

### MemorySearchRequest
```typescript
{
  query?: string
  agent_id?: string
  project_id?: string
  task_id?: string
  entry_type?: string
  tags?: string[]
  limit?: number           // Default: 10, Min: 1, Max: 100
  since?: string           // ISO 8601 datetime
  until?: string           // ISO 8601 datetime
}
```

### MemoryListResponse
```typescript
{
  memories: MemoryResponse[]
  total: number
}
```

### CompactRequest
```typescript
{
  agent_id?: string         // Optional, compacts all if not provided
  days_old?: number         // Default: 30
}
```

### CompactResponse
```typescript
{
  compacted: number
  summaries_created: number
  files_archived: number
  message: string
}
```

---

## Rate Limiting

Rate limits are applied per endpoint. Exceeding limits returns `429 Too Many Requests`.

Current limits (development mode):
- General endpoints: 100 requests/minute
- Search endpoints: 30 requests/minute
- Write endpoints: 50 requests/minute

---

## CORS Configuration

Allowed origins (environment-specific):
- Development: `http://localhost:3000`, `http://localhost:5173`
- Staging: `https://staging.example.com`
- Production: `https://app.example.com`

Credentials: Enabled
Methods: All standard HTTP methods
Headers: All headers allowed

---

## Interactive Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI Schema:** `http://localhost:8000/openapi.json`

---

## SDK Integration Examples

### Python (requests)
```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create workspace
response = requests.post(
    f"{BASE_URL}/workspaces",
    json={"name": "My Workspace", "slug": "my-workspace"}
)
workspace = response.json()

# Create agent
response = requests.post(
    f"{BASE_URL}/agents",
    params={"workspace_id": workspace["id"]},
    json={"name": "Dev Agent", "agent_type": "developer"}
)
agent = response.json()

# Create memory
response = requests.post(
    f"{BASE_URL}/memories",
    json={
        "agent_id": agent["id"],
        "project_id": "my-project",
        "type": "learning",
        "content": "Learned how to use the API",
        "tags": ["api", "integration"]
    }
)
memory = response.json()

# Search memories
response = requests.post(
    f"{BASE_URL}/memories/search",
    json={"query": "api", "agent_id": agent["id"]}
)
results = response.json()
```

### TypeScript (fetch)
```typescript
const BASE_URL = "http://localhost:8000/api/v1";

// Create workspace
const workspace = await fetch(`${BASE_URL}/workspaces`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'My Workspace', slug: 'my-workspace' })
}).then(r => r.json());

// Create agent
const agent = await fetch(`${BASE_URL}/agents?workspace_id=${workspace.id}`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Dev Agent', agent_type: 'developer' })
}).then(r => r.json());

// Create memory
const memory = await fetch(`${BASE_URL}/memories`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    agent_id: agent.id,
    project_id: 'my-project',
    type: 'learning',
    content: 'Learned how to use the API',
    tags: ['api', 'integration']
  })
}).then(r => r.json());

// Search memories
const results = await fetch(`${BASE_URL}/memories/search`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'api', agent_id: agent.id })
}).then(r => r.json());
```

---

## Versioning

Current API version: **v1** (accessed via `/api/v1` prefix)

Breaking changes will result in a new version (v2, v3, etc.) while maintaining backward compatibility for at least 6 months.

---

## Support

- **Documentation Issues:** Create issue in repository
- **API Bugs:** Report via GitHub Issues
- **Feature Requests:** Contact product team

---

**Last Updated:** 2026-03-25
**Maintained By:** Faintech Lab Team
