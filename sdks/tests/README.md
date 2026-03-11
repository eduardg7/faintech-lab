# SDK Integration Tests

This directory contains integration tests for both Python and TypeScript SDKs.

## Prerequisites

- Python 3.8+ (for Python SDK tests)
- Node.js 16+ (for TypeScript SDK tests)

## Running Tests Locally

### Python SDK Tests

```bash
cd sdks/python

# Install test dependencies
pip install -e ".[dev]"

# Run all integration tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agentmemory --cov-report=html

# Run specific test
pytest tests/test_integration.py::TestMemoryClient::test_init_with_api_key -v
```

### TypeScript SDK Tests

```bash
cd sdks/typescript

# Install dependencies
npm ci

# Run all integration tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm run test:watch
```

## Test Structure

### Python SDK (`tests/test_integration.py`)

- **TestMemoryClient**: Client initialization and configuration
- **TestMemoriesResource**: Memory CRUD operations
- **TestAgentsResource**: Agent CRUD operations
- **TestProjectsResource**: Project CRUD operations
- **TestSearchResource**: Keyword and semantic search
- **TestErrorHandling**: Error responses (401, 404, 422, 429, 500)

### TypeScript SDK (`tests/integration.test.ts`)

- MemoryClient initialization
- Memory model parsing
- Agent, Project, SearchResult parsing
- PaginatedResponse handling
- Error handling

## CI/CD Integration

Tests run automatically on:
- Every push to `master`, `main`, `develop` branches
- Every pull request to `master`, `main`, `develop` branches
- Manual workflow dispatch

See `.github/workflows/sdk-tests.yml` for CI configuration.

## Coverage Goals

- Python SDK: >80% code coverage
- TypeScript SDK: >80% code coverage

Coverage reports are uploaded to Codecov on each CI run.
