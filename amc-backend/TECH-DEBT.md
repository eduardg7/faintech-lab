# AMC Backend — Technical Debt Registry

| ID     | Title                                   | Status     | Priority | Notes                                             |
|--------|-----------------------------------------|------------|----------|---------------------------------------------------|
| TD-010 | Observability stack (logging / metrics) | ✅ RESOLVED | HIGH     | Implemented 2026-03-11 — see details below        |
| TD-015 | Migrate embeddings to pgvector          | OPEN       | MEDIUM   | Currently stored as JSON; blocked on Postgres      |
| TD-020 | Pydantic v1 → v2 migration              | OPEN       | LOW      | @validator deprecation warnings throughout schemas |

---

## TD-010 — Observability Stack  ✅ RESOLVED (2026-03-11)

### Problem
No centralised logging, no metrics, no tracing → debugging was effectively blind.

### Solution Implemented

#### 1. Structured JSON Logging — `app/core/logging.py`
- `JSONFormatter`: every log line is a valid JSON object with `timestamp`, `level`, `message`, `module`, `logger` fields.
- Extra context (request metadata, event details) merged into the JSON via the `extra` kwarg.
- Full exception info (type, message, traceback list) attached when `exc_info` is set.
- `setup_logging()` replaces the root handler and silences noisy third-party loggers.
- `get_logger(name)` returns a named child logger.

#### 2. In-Process Metrics — `app/core/metrics.py`
- `MetricsStore`: singleton that tracks per-endpoint request counts, error counts, and latency ring-buffers (last 1 000 samples).
- `record_request(path, method, status_code, duration_ms)` convenience function.
- `snapshot()` returns a JSON-serialisable dict with uptime, global counters, p50/p95/p99 latencies, and per-endpoint breakdown.

#### 3. Request Logging Middleware — `main.py`
Every HTTP request is timed and logged as structured JSON:
```json
{"timestamp":"...","level":"INFO","message":"request","method":"GET","path":"/health","status_code":200,"duration_ms":3.14}
```

#### 4. Enhanced `/health` Endpoint
- DB connectivity check (`SELECT 1`)
- `uptime_seconds`
- `version`
- `database.status` (`ok` | `error`)

#### 5. `/metrics` Endpoint
```json
{
  "uptime_seconds": 42.1,
  "requests_total": 150,
  "errors_total": 3,
  "latency_ms": {"p50": 12.4, "p95": 45.0, "p99": 98.3},
  "memories_total": 27,
  "endpoints": [
    {"method": "GET", "path": "/v1/memories", "requests_total": 80, "errors_total": 0, "latency_ms": {...}}
  ]
}
```

### Files Created / Modified
| File | Action |
|------|--------|
| `app/core/logging.py` | **Created** |
| `app/core/metrics.py` | **Created** |
| `app/core/__init__.py` | Modified — exports `setup_logging`, `get_logger`, `metrics_store`, `record_request` |
| `main.py` | Modified — structured logging init, request middleware, enhanced `/health`, new `/metrics` |
| `tests/test_observability.py` | **Created** — 18 tests, all passing |

### Tests
```
tests/test_observability.py  18 passed ✅
```
