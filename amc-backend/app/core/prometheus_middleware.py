"""Prometheus metrics middleware for AMC API.

Implements comprehensive performance monitoring:
- Request latency (histogram)
- Request count by endpoint (counter)
- Error rate (counter)
- Active connections (gauge)

Usage:
    from app.core.prometheus_middleware import PrometheusMiddleware, metrics

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics/prometheus", metrics)
"""

import time
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    Info,
    CollectorRegistry,
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
)


# ---------------------------------------------------------------------------
# Prometheus Metrics Definitions
# ---------------------------------------------------------------------------

# Request count by method, endpoint, and status
REQUEST_COUNT = Counter(
    "amc_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
    registry=REGISTRY,
)

# Request latency histogram (in seconds)
REQUEST_LATENCY = Histogram(
    "amc_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0),
    registry=REGISTRY,
)

# Error counter by type
ERROR_COUNT = Counter(
    "amc_http_errors_total",
    "Total HTTP errors",
    ["method", "endpoint", "status"],
    registry=REGISTRY,
)

# Active connections gauge
ACTIVE_CONNECTIONS = Gauge(
    "amc_http_active_connections",
    "Number of active HTTP connections",
    registry=REGISTRY,
)

# Application info
APP_INFO = Info(
    "amc_app",
    "Application information",
    registry=REGISTRY,
)


def set_app_info(version: str, app_name: str = "amc-backend") -> None:
    """Set application info metrics."""
    APP_INFO.info({"version": version, "app_name": app_name})


# ---------------------------------------------------------------------------
# Normalize endpoint paths (replace IDs with placeholders)
# ---------------------------------------------------------------------------

def normalize_path(path: str) -> str:
    """Normalize path by replacing dynamic segments with placeholders.

    Examples:
        /v1/memories/abc123 -> /v1/memories/{id}
        /v1/users/user@example.com/memories -> /v1/users/{user_id}/memories
    """
    parts = path.strip("/").split("/")
    normalized = []

    for i, part in enumerate(parts):
        # UUID pattern (8-4-4-4-12)
        if len(part) == 36 and part.count("-") == 4:
            normalized.append("{id}")
        # MongoDB-style ObjectId (24 hex chars)
        elif len(part) == 24 and all(c in "0123456789abcdefABCDEF" for c in part):
            normalized.append("{id}")
        # Numeric ID
        elif part.isdigit():
            normalized.append("{id}")
        # Email pattern (contains @)
        elif "@" in part:
            normalized.append("{email}")
        # AMC API key pattern (starts with amc_)
        elif part.startswith("amc_"):
            normalized.append("{api_key}")
        # Memory ID (alphanumeric, not a common word)
        elif i > 0 and len(part) > 8 and part.isalnum():
            normalized.append("{id}")
        else:
            normalized.append(part)

    result = "/" + "/".join(normalized) if normalized else "/"
    return result


# ---------------------------------------------------------------------------
# Prometheus Middleware
# ---------------------------------------------------------------------------

class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics for each request."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip metrics endpoint itself to avoid recursion
        if request.url.path in ("/metrics/prometheus", "/metrics"):
            return await call_next(request)

        # Increment active connections
        ACTIVE_CONNECTIONS.inc()

        # Record start time
        start_time = time.perf_counter()

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration = time.perf_counter() - start_time

            # Normalize path for metrics grouping
            endpoint = normalize_path(request.url.path)
            method = request.method
            status = str(response.status_code)

            # Record metrics
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

            # Record errors (4xx and 5xx)
            if response.status_code >= 400:
                ERROR_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()

            return response

        except Exception as exc:
            # Record exception as 500 error
            duration = time.perf_counter() - start_time
            endpoint = normalize_path(request.url.path)
            method = request.method

            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="500").inc()
            REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
            ERROR_COUNT.labels(method=method, endpoint=endpoint, status="500").inc()

            raise

        finally:
            # Decrement active connections
            ACTIVE_CONNECTIONS.dec()


# ---------------------------------------------------------------------------
# Metrics Endpoint Handler
# ---------------------------------------------------------------------------

async def metrics(request: Request) -> Response:
    """Expose Prometheus metrics in text format.

    This endpoint returns metrics in Prometheus text exposition format
    for scraping by Prometheus server.
    """
    # Generate latest metrics
    output = generate_latest(REGISTRY)

    return PlainTextResponse(
        content=output.decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
