# Agent Memory Cloud API - OpenAPI Specification

**Version:** 1.0.0 (MVP)  
**Base URL:** `https://api.agentmemory.cloud/v1`  
**Task:** AMC-MVP-001  
**Author:** faintech-cto  
**Date:** 2026-03-10

---

## Overview

This specification defines the REST API for the Agent Memory Cloud MVP. The API enables external customers to store, search, and manage agent memories across sessions.

### Design Principles

1. **RESTful** - Standard HTTP methods and status codes
2. **Stateless** - JWT-based authentication
3. **Rate-limited** - Protect against abuse
4. **Versioned** - URL-based versioning (`/v1/`)
5. **Consistent** - Uniform error responses and pagination

---

## Authentication

### API Key Authentication

```http
Authorization: Bearer <api_key>
```

All endpoints require a valid API key. Keys are scoped to:
- **Project-level** - Access to specific project memories
- **Organization-level** - Access to all projects in org

### Rate Limits

| Tier | Requests/min | Burst |
|------|--------------|-------|
| Free | 60 | 100 |
| Pro | 600 | 1000 |
| Enterprise | 6000 | 10000 |

Rate limit headers:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1617181729
```

---

## Endpoints

### Memories

#### `POST /memories`

Create a new memory entry.

**Request:**
```json
{
  "agent_id": "string (required)",
  "project_id": "string (required)",
  "task_id": "string (optional)",
  "type": "learning | error | decision | pattern | fact",
  "content": "string (required, max 10KB)",
  "tags": ["string"],
  "metadata": {}
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "agent_id": "string",
  "project_id": "string",
  "task_id": "string",
  "timestamp": "2026-03-10T14:30:00Z",
  "type": "string",
  "content": "string",
  "tags": ["string"],
  "metadata": {},
  "embedding_version": 1
}
```

**Errors:**
- `400 Bad Request` - Invalid input, content too large
- `401 Unauthorized` - Invalid/expired API key
- `429 Too Many Requests` - Rate limit exceeded

**Performance:** <100ms p95

---

#### `GET /memories/{memory_id}`

Retrieve a specific memory entry.

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "agent_id": "string",
  "project_id": "string",
  "task_id": "string",
  "timestamp": "2026-03-10T14:30:00Z",
  "type": "string",
  "content": "string",
  "tags": ["string"],
  "metadata": {},
  "embedding_version": 1
}
```

**Errors:**
- `404 Not Found` - Memory doesn't exist
- `403 Forbidden` - No access to this project

**Performance:** <50ms p95

---

#### `GET /memories`

Search memories with filters.

**Query Parameters:**
```
?query=string (optional, keyword search)
&agent_id=string (optional)
&project_id=string (optional)
&task_id=string (optional)
&type=learning|error|decision|pattern|fact (optional)
&tags=tag1,tag2 (optional, AND logic)
&since=2026-03-01T00:00:00Z (optional, ISO 8601)
&until=2026-03-10T23:59:59Z (optional, ISO 8601)
&limit=10 (optional, default 10, max 100)
&offset=0 (optional, for pagination)
&sort=timestamp|relevance (optional, default: timestamp)
```

**Response:** `200 OK`
```json
{
  "memories": [
    {
      "id": "uuid",
      "agent_id": "string",
      "project_id": "string",
      "task_id": "string",
      "timestamp": "2026-03-10T14:30:00Z",
      "type": "string",
      "content": "string",
      "tags": ["string"],
      "metadata": {}
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

**Performance:** <200ms p95 for 1000 entries

---

#### `PATCH /memories/{memory_id}`

Update memory metadata (not content).

**Request:**
```json
{
  "tags": ["new-tag"],
  "metadata": {
    "important": true
  }
}
```

**Response:** `200 OK` (full memory object)

**Errors:**
- `400 Bad Request` - Trying to update immutable fields (content, timestamp)
- `404 Not Found` - Memory doesn't exist

---

#### `DELETE /memories/{memory_id}`

Delete a memory entry.

**Response:** `204 No Content`

**Errors:**
- `404 Not Found` - Memory doesn't exist

---

### Search (Semantic)

#### `POST /search/semantic`

Semantic search using vector embeddings.

**Request:**
```json
{
  "query": "string (required, natural language)",
  "project_id": "string (optional)",
  "agent_id": "string (optional)",
  "limit": 10
}
```

**Response:** `200 OK`
```json
{
  "results": [
    {
      "memory": {
        "id": "uuid",
        "content": "string",
        "timestamp": "string",
        "type": "string"
      },
      "score": 0.95
    }
  ],
  "query_embedding_time_ms": 12,
  "search_time_ms": 45
}
```

**Performance:** <300ms p95

---

### Agents

#### `GET /agents`

List agents with memory activity.

**Query Parameters:**
```
?project_id=string (optional)
&since=2026-03-01 (optional)
&limit=100 (optional)
```

**Response:** `200 OK`
```json
{
  "agents": [
    {
      "agent_id": "string",
      "project_id": "string",
      "memory_count": 150,
      "last_activity": "2026-03-10T14:30:00Z",
      "types": {
        "learning": 50,
        "error": 20,
        "decision": 30,
        "pattern": 25,
        "fact": 25
      }
    }
  ]
}
```

---

### Projects

#### `GET /projects`

List accessible projects.

**Response:** `200 OK`
```json
{
  "projects": [
    {
      "project_id": "string",
      "name": "string",
      "memory_count": 500,
      "agent_count": 5,
      "created_at": "2026-03-01T00:00:00Z"
    }
  ]
}
```

---

### Health

#### `GET /health`

Service health check.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-03-10T14:30:00Z",
  "components": {
    "database": "healthy",
    "vector_store": "healthy",
    "api": "healthy"
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Content exceeds maximum size (10KB)",
    "details": {
      "field": "content",
      "max_size": 10240,
      "actual_size": 15360
    }
  },
  "request_id": "uuid",
  "timestamp": "2026-03-10T14:30:00Z"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_INPUT` | 400 | Invalid request body |
| `UNAUTHORIZED` | 401 | Missing/invalid API key |
| `FORBIDDEN` | 403 | No access to resource |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Pagination

List endpoints support cursor-based pagination:

```http
GET /memories?limit=10&offset=0
```

Response includes pagination metadata:
```json
{
  "pagination": {
    "total": 150,
    "limit": 10,
    "offset": 0,
    "has_more": true,
    "next_offset": 10
  }
}
```

---

## Webhooks (Phase 2)

Future webhook events:
- `memory.created` - New memory written
- `memory.deleted` - Memory deleted
- `agent.threshold_exceeded` - Agent error rate high

---

## SDK Support

Official SDKs for:
- **Python** - `pip install agentmemory`
- **TypeScript** - `npm install @agentmemory/sdk`
- **Go** - `go get github.com/agentmemory/go-sdk`

SDKs provide:
- Automatic retry logic
- Type-safe interfaces
- Connection pooling
- Built-in rate limit handling

---

## Implementation Notes

### Security

1. **Input validation** - All inputs sanitized, max size limits
2. **SQL injection prevention** - Parameterized queries only
3. **Secrets scanning** - Detect API keys in content before storage
4. **Rate limiting** - Per-key quotas enforced
5. **HTTPS only** - No plaintext traffic

### Performance

1. **Connection pooling** - Reuse DB connections
2. **Index optimization** - Indexes on agent_id, project_id, timestamp, type
3. **Vector index** - IVFFlat for pgvector similarity search
4. **Caching** - Redis cache for hot queries (Phase 2)
5. **Async I/O** - FastAPI async endpoints

### Scalability

1. **Horizontal scaling** - Stateless API servers
2. **Read replicas** - Separate read/write DBs (Phase 2)
3. **Sharding** - By project_id for large customers (Phase 3)

---

## OpenAPI YAML (Reference)

Full OpenAPI 3.0 spec available at:
- **Development:** `http://localhost:8000/openapi.json`
- **Production:** `https://api.agentmemory.cloud/openapi.json`

---

**Document Status:** APPROVED  
**Next Review:** After MVP launch (Week 5)  
**Owner:** faintech-cto
