"""FastAPI application factory and main entry point.

Agent Memory Cloud API - OpenAPI/Swagger Documentation
=======================================================

This API provides a comprehensive memory management system for AI agents,
enabling persistent storage, semantic search, and intelligent retrieval
of memories across workspaces.

Authentication:
- JWT Bearer tokens (for user sessions)
- API Keys (for programmatic access, prefix: amc_)

Rate Limits:
- 60 requests/minute
- 1000 requests/hour

For interactive documentation, visit /v1/docs (Swagger UI) or /v1/redoc.
"""

import time
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from config import settings
from app.core.errors import (
    AMCError,
    amc_error_handler,
    generic_error_handler,
    request_validation_error_handler,
)
from app.core.rate_limit import RateLimitMiddleware
from app.core.logging import setup_logging, get_logger
from app.core.metrics import metrics_store, record_request
from app.core.prometheus_middleware import (
    PrometheusMiddleware,
    metrics as prometheus_metrics,
    set_app_info,
)
from app.middleware.error_handler import ErrorHandlingMiddleware

# Initialise structured logging as early as possible
_root_logger = setup_logging()

# OpenAPI Tags Metadata
TAGS_METADATA = [
    {
        "name": "Authentication",
        "description": """
User authentication and session management.

**Endpoints:**
- Register new user accounts
- Login with email/password
- Refresh access tokens
- Logout and revoke tokens
- Get current user profile

**Authentication Methods:**
- JWT access tokens (expires in 30 minutes)
- JWT refresh tokens (expires in 7 days)
""",
    },
    {
        "name": "Memories",
        "description": """
Memory CRUD operations with workspace isolation.

**Memory Types:**
- `outcome`: Results of completed tasks
- `learning`: Knowledge gained from experiences
- `preference`: User/agent preferences
- `decision`: Important decisions made

**Features:**
- Content size limit: 10KB per memory
- Tag-based categorization
- Metadata support
- Soft delete with recovery
- Agent isolation (workspace-scoped access)
""",
    },
    {
        "name": "Hybrid Search",
        "description": """
Intelligent search combining keyword and vector similarity.

**Scoring:**
- Keyword score: PostgreSQL full-text search ranking
- Vector score: Cosine similarity via pgvector
- Combined score: Weighted blend (default: 40% keyword, 60% vector)

**Performance:**
- Target: <100ms p95 latency
- HNSW index for fast vector search
- Embedding cache for repeated queries
""",
    },
    {
        "name": "Agents & Projects",
        "description": """
Agent and project aggregation endpoints.

**Features:**
- List agents with memory counts
- List projects with agent/memory statistics
- Activity tracking (last memory timestamp)
- Workspace-scoped isolation
""",
    },
    {
        "name": "Billing",
        "description": """
Stripe subscription management.

**Tiers:**
- `starter`: $99/month - Basic features
- `pro`: $199/month - Full features with semantic search

**Webhooks:**
- Handles subscription lifecycle events
- Signature verification required
""",
    },
    {
        "name": "Observability",
        "description": "Health checks and metrics endpoints for monitoring.",
    },
    {
        "name": "Root",
        "description": "Root endpoint with API information.",
    },
]


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    logger = get_logger("amc.app")

    app = FastAPI(
        title="Agent Memory Cloud API",
        summary="Persistent memory management for AI agents with semantic search",
        description="""
# Agent Memory Cloud API

A comprehensive memory management system for AI agents, enabling persistent
storage, semantic search, and intelligent retrieval of memories.

## Key Features

- **Memory Storage**: Store agent memories with types, tags, and metadata
- **Semantic Search**: Hybrid search combining keyword and vector similarity
- **Workspace Isolation**: Multi-tenant architecture with agent isolation
- **Subscription Billing**: Stripe-powered tiered pricing

## Authentication

All API endpoints require authentication via:
- **JWT Bearer Token**: For user sessions (`Authorization: Bearer <token>`)
- **API Key**: For programmatic access (`Authorization: Bearer amc_...`)

## Rate Limits

- 60 requests per minute
- 1000 requests per hour

## Error Handling

Standardized error responses with codes:
- `VALIDATION_ERROR`: Invalid input data
- `NOT_FOUND`: Resource not found
- `UNAUTHORIZED`: Authentication required
- `FORBIDDEN`: Access denied (workspace isolation)
- `CONTENT_TOO_LARGE`: Content exceeds 10KB limit
""",
        version=settings.app_version,
        debug=settings.debug,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url=f"{settings.api_v1_prefix}/docs",
        redoc_url=f"{settings.api_v1_prefix}/redoc",
        openapi_tags=TAGS_METADATA,
        contact={
            "name": "FainTech Lab",
            "email": "support@faintech.ai",
        },
        license_info={
            "name": "Proprietary",
        },
        servers=[
            {
                "url": "/v1",
                "description": "Current server (relative)",
            },
        ],
    )

    # ------------------------------------------------------------------ #
    # Middleware                                                           #
    # ------------------------------------------------------------------ #

    # Prometheus metrics middleware - must be early to capture all requests
    app.add_middleware(PrometheusMiddleware)

    # Set app info for Prometheus metrics
    set_app_info(version=settings.app_version, app_name=settings.app_name)

    # Error handling middleware - catches all unhandled exceptions
    app.add_middleware(ErrorHandlingMiddleware)

    # Rate limiting middleware
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=60,
        requests_per_hour=1000,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------ #
    # Request logging + metrics middleware                                 #
    # ------------------------------------------------------------------ #

    @app.middleware("http")
    async def log_and_record_request(request: Request, call_next):
        """Log every request with method, path, status and duration."""
        start = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)

        path = request.url.path
        method = request.method
        status_code = response.status_code

        record_request(path, method, status_code, duration_ms)

        logger.info(
            "request",
            extra={
                "extra": {
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                }
            },
        )
        return response

    # ------------------------------------------------------------------ #
    # Error handlers                                                       #
    # ------------------------------------------------------------------ #

    app.add_exception_handler(AMCError, amc_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)

    # ------------------------------------------------------------------ #
    # Built-in endpoints                                                   #
    # ------------------------------------------------------------------ #

    @app.get("/health", tags=["Observability"])
    async def health_check():
        """Enhanced health check — includes DB connectivity, uptime and version."""
        from app.core.database import async_session_maker

        db_status = "ok"
        db_error: str | None = None
        try:
            async with async_session_maker() as session:
                await session.execute(text("SELECT 1"))
        except Exception as exc:  # noqa: BLE001
            db_status = "error"
            db_error = str(exc)

        uptime_seconds = round(time.time() - metrics_store._started_at, 1)

        payload: dict = {
            "status": "healthy" if db_status == "ok" else "degraded",
            "version": settings.app_version,
            "uptime_seconds": uptime_seconds,
            "database": {"status": db_status},
        }
        if db_error:
            payload["database"]["error"] = db_error

        return payload

    @app.get("/metrics", tags=["Observability"])
    async def get_metrics():
        """In-process metrics snapshot — request counts, error counts and latency percentiles."""
        from app.core.database import async_session_maker
        from sqlalchemy import func
        from app.models.memory import Memory

        snapshot = metrics_store.snapshot()

        # Append live DB counts
        try:
            from sqlalchemy import select as sa_select

            async with async_session_maker() as session:
                result = await session.execute(
                    sa_select(func.count())
                    .select_from(Memory)
                    .where(Memory.deleted_at.is_(None))
                )
                memories_total = result.scalar() or 0
        except Exception:  # noqa: BLE001
            memories_total = None

        snapshot["memories_total"] = memories_total
        return snapshot

    @app.get("/metrics/prometheus", tags=["Observability"])
    async def get_prometheus_metrics(request: Request):
        """Prometheus-compatible metrics endpoint for monitoring systems.

        Returns metrics in Prometheus text exposition format.
        Metrics include:
        - amc_http_requests_total: Total HTTP requests by method, endpoint, status
        - amc_http_request_duration_seconds: Request latency histogram
        - amc_http_errors_total: Total HTTP errors
        - amc_http_active_connections: Current active connections
        - amc_app_info: Application version and info
        """
        return await prometheus_metrics(request)

    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "docs": f"{settings.api_v1_prefix}/docs",
        }

    # ------------------------------------------------------------------ #
    # Routers                                                              #
    # ------------------------------------------------------------------ #

    from app.routers import (
        agents_router,
        api_keys_router,
        auth_router,
        memories_router,
        search_router,
        hybrid_search_router,
    )
    from app.routers.semantic import router as semantic_router
    from app.routers.billing import router as billing_router
    from app.routers.websocket import router as websocket_router

    app.include_router(memories_router, prefix=settings.api_v1_prefix)
    app.include_router(search_router, prefix=settings.api_v1_prefix)
    app.include_router(semantic_router, prefix=settings.api_v1_prefix)
    app.include_router(hybrid_search_router, prefix=settings.api_v1_prefix)
    app.include_router(agents_router, prefix=settings.api_v1_prefix)
    app.include_router(auth_router, prefix=settings.api_v1_prefix)
    app.include_router(api_keys_router, prefix=settings.api_v1_prefix)
    app.include_router(billing_router, prefix=settings.api_v1_prefix)
    # WebSocket router at root level (not under /v1 prefix)
    app.include_router(websocket_router)

    logger.info(
        "startup",
        extra={
            "extra": {
                "app": settings.app_name,
                "version": settings.app_version,
                "debug": settings.debug,
            }
        },
    )

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
