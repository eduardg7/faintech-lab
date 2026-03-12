# Load Testing Suite for Agent Memory Cloud MVP

This directory contains k6 load tests for validating the performance and reliability of the AMC MVP API.

## Prerequisites

- [k6](https://k6.io/docs/getting-started/installation/) installed
- Backend server running on `http://localhost:8000` (or set `BASE_URL` env var)

## Test Files

### 1. `load_test.js` - Main Performance Test
**Purpose:** Validate API can handle 100 req/sec with P99 latency < 100ms

**What it tests:**
- Health endpoint
- Memory creation
- Memory search
- Get agent memories
- Get task memories

**Run:**
```bash
k6 run load_test.js
```

**Expected results:**
- P99 latency < 100ms
- Error rate < 5%
- Handles 1000+ concurrent users

### 2. `rate_limit_test.js` - Rate Limiting Validation
**Purpose:** Verify rate limiting works correctly (1000 req/hour per API key)

**What it tests:**
- Sustained requests to trigger rate limits
- Proper 429 responses with retry headers
- Rate limit header presence

**Run:**
```bash
k6 run rate_limit_test.js
```

**Expected results:**
- 429 responses when limit exceeded
- X-RateLimit headers present
- Retry-After header on 429s

### 3. `spike_test.js` - Spike Load Test
**Purpose:** Test system behavior under sudden load spikes

**What it tests:**
- Sudden increase from 10 to 1000 users
- System stability during spike
- Graceful degradation

**Run:**
```bash
k6 run spike_test.js
```

**Expected results:**
- No crashes or timeouts
- P99 latency < 500ms during spike
- Error rate < 10% during spike

## Running All Tests

```bash
# Run main load test
k6 run load_test.js --out json=load-results.json

# Run rate limit test
k6 run rate_limit_test.js --out json=rate-limit-results.json

# Run spike test
k6 run spike_test.js --out json=spike-results.json
```

## Custom Configuration

### Environment Variables

```bash
# Set custom base URL
export BASE_URL=http://your-api-url:8000

# Run test
k6 run load_test.js
```

### Custom Test Duration

```bash
# Run for 5 minutes instead of default
k6 run --duration 5m load_test.js
```

### Custom Virtual Users

```bash
# Run with 2000 users
k6 run --vus 2000 load_test.js
```

## Performance Benchmarks

| Metric | Target | Description |
|--------|--------|-------------|
| P99 Latency | < 100ms | 99% of requests complete within 100ms |
| Throughput | 100 req/sec | API handles 100 requests per second |
| Concurrent Users | 1000+ | Supports 1000+ concurrent users |
| Error Rate | < 5% | Less than 5% of requests fail |
| Memory Usage | < 2GB | Backend memory under load stays under 2GB |
| Rate Limit | 1000 req/hour | Per API key rate limiting |

## Interpreting Results

### Good Results
```
✓ status is 200
✓ P99 latency < 100ms
✓ error rate < 5%
```

### Warning Signs
```
✗ P99 latency > 100ms
✗ error rate > 5%
✗ timeouts or connection refused
```

## CI/CD Integration

Add to your CI pipeline:

```yaml
# .github/workflows/load-test.yml
name: Load Test
on: [push]
jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install k6
        run: |
          sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C4914E6D6891
          echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6
      - name: Run load tests
        run: k6 run projects/new-product/tests/load/load_test.js
```

## Troubleshooting

### "Connection refused"
- Ensure backend is running on the correct port
- Check `BASE_URL` environment variable

### High error rates
- Check backend logs for errors
- Verify database connections
- Check rate limiting configuration

### High latency
- Review database query performance
- Check for N+1 queries
- Verify indexes are created
- Monitor resource usage (CPU, memory)

## Test Data

Tests use randomized data from these pools:
- Agents: `agent-1` through `agent-5`
- Projects: `project-alpha`, `project-beta`, `project-gamma`
- Tasks: `task-001`, `task-002`, `task-00003`

This ensures realistic load distribution across resources.

## Next Steps

1. ✅ Create test scripts
2. ⏳ Run tests against live backend
3. ⏳ Analyze results and identify bottlenecks
4. ⏳ Optimize based on findings
5. ⏳ Document final performance metrics
