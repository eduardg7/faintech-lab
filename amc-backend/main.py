"""FastAPI application factory and main entry point."""

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

# Initialise structured logging as early as possible
_root_logger = setup_logging()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    logger = get_logger("amc.app")

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url=f"{settings.api_v1_prefix}/docs",
        redoc_url=f"{settings.api_v1_prefix}/redoc",
    )

    # ------------------------------------------------------------------ #
    # Middleware                                                           #
    # ------------------------------------------------------------------ #

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
    )
    from app.routers.semantic import router as semantic_router

    app.include_router(memories_router, prefix=settings.api_v1_prefix)
    app.include_router(search_router, prefix=settings.api_v1_prefix)
    app.include_router(semantic_router, prefix=settings.api_v1_prefix)
    app.include_router(agents_router, prefix=settings.api_v1_prefix)
    app.include_router(auth_router, prefix=settings.api_v1_prefix)
    app.include_router(api_keys_router, prefix=settings.api_v1_prefix)

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
