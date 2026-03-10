"""FastAPI application factory and main entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url=f"{settings.api_v1_prefix}/docs",
        redoc_url=f"{settings.api_v1_prefix}/redoc",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": settings.app_version}

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "docs": f"{settings.api_v1_prefix}/docs",
        }

    # Include routers
    from app.routers import memories_router, search_router, agents_router
    from app.routers.semantic import router as semantic_router

    app.include_router(memories_router, prefix=settings.api_v1_prefix)
    app.include_router(search_router, prefix=settings.api_v1_prefix)
    app.include_router(semantic_router, prefix=settings.api_v1_prefix)
    app.include_router(agents_router, prefix=settings.api_v1_prefix)

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
