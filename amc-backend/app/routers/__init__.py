"""API routers package."""

from app.routers.memories import router as memories_router
from app.routers.search import router as search_router
from app.routers.agents import router as agents_router
from app.routers.auth import router as auth_router

__all__ = ["memories_router", "search_router", "agents_router", "auth_router"]
