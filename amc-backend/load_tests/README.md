# AMC Load Testing Suite

## Overview
Load testing and performance validation for AMC API to validate 100 req/sec target with <100ms p99 latency.

## Requirements
- Python 3.11+
- Locust (installed via requirements-test.txt)

## Test Scenarios

### 1. Memory Lifecycle
- Create memory
- Retrieve memory
- Search memory
- Delete memory

### 2. Search Under Load
- Keyword search
- Semantic search
- Hybrid search

### 3. Agent Operations
- List agents
- Get agent memories

### 4. Mixed Workload
- 60% search operations
- 20% memory creation
- 15% memory retrieval
- 5% agent operations

## Running Tests

### Quick validation (1 min)
```bash
locust -f locustfile.py --headless -u 10 -r 10 -t 60s --host http://localhost:8000
```

### Full load test (5 min)
```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 300s --host http://localhost:8000
```

### With HTML report
```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 300s --host http://localhost:8000 --html report.html
```

## Performance Targets
- **Throughput**: 100 req/sec sustained
- **Latency p50**: <50ms
- **Latency p95**: <80ms
- **Latency p99**: <100ms
- **Error rate**: <1%

## Metrics Collected
- Requests per second
- Response time percentiles (p50, p95, p99)
- Error rate
- Memory usage
- Database query performance

## Reports
Load test reports are saved in `reports/` directory with timestamp:
- `report_YYYY-MM-DD_HH-MM-SS.html` - HTML report with charts
- `metrics_YYYY-MM-DD_HH-MM-SS.json` - Raw metrics data
