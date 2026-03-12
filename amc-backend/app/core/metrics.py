"""In-memory metrics collection for AMC API.

Tracks request counts, error counts, and latency percentiles
for the last MAX_SAMPLES requests per endpoint.

Usage:
    from app.core.metrics import metrics_store, record_request

    record_request("/v1/memories", "GET", 200, 45.3)
    snapshot = metrics_store.snapshot()
"""

import time
import statistics
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional

# Keep latency data for the last N requests (global)
MAX_SAMPLES = 1000


@dataclass
class _EndpointStats:
    """Per-endpoint counters and latency ring buffer."""

    request_count: int = 0
    error_count: int = 0
    # Ring buffer of duration_ms values
    latencies: Deque[float] = field(default_factory=lambda: deque(maxlen=MAX_SAMPLES))

    def record(self, status_code: int, duration_ms: float) -> None:
        self.request_count += 1
        if status_code >= 400:
            self.error_count += 1
        self.latencies.append(duration_ms)

    def percentiles(self) -> Dict[str, Optional[float]]:
        if not self.latencies:
            return {"p50": None, "p95": None, "p99": None}
        sorted_lat = sorted(self.latencies)
        n = len(sorted_lat)

        def _pct(p: float) -> float:
            idx = int(n * p / 100)
            return round(sorted_lat[min(idx, n - 1)], 2)

        return {
            "p50": _pct(50),
            "p95": _pct(95),
            "p99": _pct(99),
        }


class MetricsStore:
    """Thread-safe (GIL-protected) metrics aggregator."""

    def __init__(self) -> None:
        self._started_at: float = time.time()
        self._endpoints: Dict[str, _EndpointStats] = defaultdict(_EndpointStats)
        # Global latency buffer (all endpoints combined)
        self._global_latencies: Deque[float] = deque(maxlen=MAX_SAMPLES)
        self._global_requests: int = 0
        self._global_errors: int = 0

    def record(
        self, path: str, method: str, status_code: int, duration_ms: float
    ) -> None:
        """Record a single request."""
        key = f"{method} {path}"
        self._endpoints[key].record(status_code, duration_ms)
        self._global_latencies.append(duration_ms)
        self._global_requests += 1
        if status_code >= 400:
            self._global_errors += 1

    def snapshot(self) -> dict:
        """Return a JSON-serialisable metrics snapshot."""
        uptime = round(time.time() - self._started_at, 1)

        sorted_global = sorted(self._global_latencies) if self._global_latencies else []
        n = len(sorted_global)

        def _pct(p: float) -> Optional[float]:
            if not sorted_global:
                return None
            idx = int(n * p / 100)
            return round(sorted_global[min(idx, n - 1)], 2)

        endpoints_data: List[dict] = []
        for key, stats in self._endpoints.items():
            method, _, path = key.partition(" ")
            endpoints_data.append(
                {
                    "method": method,
                    "path": path,
                    "requests_total": stats.request_count,
                    "errors_total": stats.error_count,
                    "latency_ms": stats.percentiles(),
                }
            )

        return {
            "uptime_seconds": uptime,
            "requests_total": self._global_requests,
            "errors_total": self._global_errors,
            "latency_ms": {
                "p50": _pct(50),
                "p95": _pct(95),
                "p99": _pct(99),
            },
            "endpoints": sorted(endpoints_data, key=lambda x: -x["requests_total"]),
        }


# Singleton shared across the process
metrics_store = MetricsStore()


def record_request(
    path: str, method: str, status_code: int, duration_ms: float
) -> None:
    """Convenience wrapper used by request middleware."""
    metrics_store.record(path, method, status_code, duration_ms)
