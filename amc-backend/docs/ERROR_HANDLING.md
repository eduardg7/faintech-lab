# AMC API Error Handling

## Overview

This document describes the error handling system for the AMC (Agent Memory Control) API.

## Error Response Format

All errors return a consistent JSON structure:

```json
{
  "error": "NotFoundError",
  "message": "Memory not found: abc123",
  "code": "NOT_FOUND",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-03-10T21:47:00Z",
  "details": {
    "resource": "Memory",
    "identifier": "abc123"
  }
}
```

### Fields

- **error**: Error type name (human-readable)
- **message**: Detailed error message
- **code**: Machine-readable error code
- **request_id**: Unique identifier for request tracing
- **timestamp**: ISO 8601 timestamp when error occurred
- **details**: Optional additional context (not always present)

## Error Codes

### Authentication Errors (1xxx)
- `AUTH_INVALID`: Invalid credentials
- `AUTH_EXPIRED`: Authentication expired
- `AUTH_MISSING`: Authentication required

### Validation Errors (2xxx)
- `VALIDATION_FAILED`: General validation error
- `CONTENT_TOO_LARGE`: Content exceeds size limit (10KB)
- `INVALID_INPUT`: Invalid input parameters

### Resource Errors (3xxx)
- `NOT_FOUND`: Resource not found
- `ALREADY_EXISTS`: Resource already exists

### Rate Limiting (4xxx)
- `RATE_LIMIT_EXCEEDED`: Rate limit exceeded

### Server Errors (5xxx)
- `INTERNAL_ERROR`: Internal server error
- `DATABASE_ERROR`: Database operation failed
- `EXTERNAL_SERVICE_ERROR`: External service unavailable

## HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 404 | Not Found | Resource not found |
| 413 | Payload Too Large | Content > 10KB |
| 422 | Unprocessable Entity | Invalid request body |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected error |

## Rate Limiting

### Headers

All responses include rate limit headers:

```
X-RateLimit-Limit-Minute: 60
X-RateLimit-Remaining-Minute: 45
X-RateLimit-Limit-Hour: 1000
X-RateLimit-Remaining-Hour: 850
X-RateLimit-Reset: 1709630400
```

### Limits

- **Per minute**: 60 requests
- **Per hour**: 1000 requests

### Client Identification

Clients are identified by:
1. `X-API-Key` header (preferred)
2. IP address (fallback)

### Rate Limit Exceeded

When rate limit is exceeded:

```json
{
  "error": "RateLimitError",
  "message": "Rate limit exceeded. Retry after 30 seconds",
  "code": "RATE_LIMIT_EXCEEDED",
  "request_id": "...",
  "timestamp": "...",
  "details": {
    "retry_after": 30,
    "limit": 60,
    "window": 60
  }
}
```

Response includes `Retry-After` header.

## Retry Logic

### Automatic Retries

The SDK automatically retries on:
- 5xx errors (500, 502, 503, 504)
- Network errors
- Timeouts

### Retry Configuration

```python
from app.core.errors import RetryConfig

config = RetryConfig(
    max_retries=3,        # Maximum retry attempts
    backoff_factor=2.0,   # Exponential backoff multiplier
    retry_on=(500, 502, 503, 504),  # Status codes to retry
    timeout=30.0          # Request timeout in seconds
)
```

### Retry Behavior

- **Attempt 1**: Immediate
- **Attempt 2**: After 1 second
- **Attempt 3**: After 2 seconds
- **Attempt 4**: After 4 seconds

## Request Tracing

### Request IDs

Every request gets a unique `request_id`:

1. Client provides `X-Request-ID` header
2. Or server generates a UUID
3. Returned in:
   - Response headers: `X-Request-ID`
   - Error response body: `request_id` field
   - Server logs

### Log Format

```
[ERROR] Request ID: 550e8400-e29b-41d4-a716-446655440000 | Code: NOT_FOUND | Message: Memory not found: abc123
[ERROR] Details: {"resource": "Memory", "identifier": "abc123"}
```

## Edge Cases

### Empty Search

```bash
GET /api/v1/memories?search=nonexistent-term-xyz123

Response: 200 OK
{
  "memories": [],
  "total": 0,
  "page": 1,
  "page_size": 20,
  "has_next": false
}
```

### Large Payloads

Content is limited to 10KB:

```bash
POST /api/v1/memories
{
  "content": "x" * 10241  # 10KB + 1 byte
}

Response: 413 Payload Too Large
{
  "error": "ContentTooLargeError",
  "message": "Content size 10241 bytes exceeds 10240 bytes limit",
  "code": "CONTENT_TOO_LARGE",
  "details": {
    "content_size": 10241,
    "max_size": 10240
  }
}
```

### Concurrent Writes

The API handles concurrent writes safely:
- Database transactions are atomic
- Concurrent creates return 201
- Concurrent updates may conflict (409 Conflict)

### Special Characters

Search queries handle special characters safely:
- SQL injection protected
- XSS attacks prevented
- Unicode supported

## Testing

Run error handling tests:

```bash
pytest tests/test_errors.py -v
```

### Test Coverage

- ✅ Error response structure
- ✅ Content size validation
- ✅ Request ID tracking
- ✅ Rate limit headers
- ✅ Validation errors
- ✅ Edge cases (empty search, pagination, unicode)
- ✅ Concurrent operations
- ✅ Retry logic configuration
- ✅ Rate limiting behavior

## Best Practices

### For Clients

1. **Always check status codes** before parsing response
2. **Extract request_id** from headers for debugging
3. **Respect rate limits** - use Retry-After header
4. **Implement retry logic** for 5xx errors
5. **Validate input** client-side before sending
6. **Keep content under 10KB**

### For Developers

1. **Use AMCError subclasses** for all API errors
2. **Include helpful details** in error responses
3. **Log errors with request_id** for tracing
4. **Test edge cases** thoroughly
5. **Update error codes** when adding new error types
6. **Document new error codes** in this file

## Examples

### Creating a Memory

```bash
# Success
curl -X POST http://localhost:8000/api/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent-123",
    "project_id": "project-456",
    "memory_type": "outcome",
    "content": "Successfully completed task",
    "tags": ["success", "task"]
  }'

Response: 201 Created
{
  "id": "mem-789",
  "agent_id": "agent-123",
  ...
}

# Error - Content too large
curl -X POST http://localhost:8000/api/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent-123",
    "memory_type": "outcome",
    "content": "x" * 15000
  }'

Response: 413 Payload Too Large
{
  "error": "ContentTooLargeError",
  "message": "Content size 15000 bytes exceeds 10240 bytes limit",
  ...
}
```

### Getting a Memory

```bash
# Success
curl http://localhost:8000/api/v1/memories/mem-789

Response: 200 OK
{
  "id": "mem-789",
  "agent_id": "agent-123",
  ...
}

# Error - Not found
curl http://localhost:8000/api/v1/memories/nonexistent

Response: 404 Not Found
{
  "error": "NotFoundError",
  "message": "Memory not found: nonexistent",
  "code": "NOT_FOUND",
  ...
}
```

## Monitoring

### Metrics to Track

- Error rate by code
- Average response time
- Rate limit rejections
- 5xx error frequency
- Request ID lookup success rate

### Alerts

- Error rate > 5% → Investigate
- 5xx errors > 1% → Immediate attention
- Rate limit rejections > 100/hour → Review limits

## Changelog

### v1.0.0 (2026-03-10)

- Initial error handling implementation
- Structured error responses
- Rate limiting middleware
- Request ID tracking
- Comprehensive test coverage
- Documentation complete
