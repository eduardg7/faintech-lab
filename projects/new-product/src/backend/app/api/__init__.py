"""API routers for Agent Memory Cloud."""
from fastapi import APIRouter
from app.api import health, workspaces, agents, memories, keys

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["Workspaces"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
api_router.include_router(memories.router, prefix="/memories", tags=["Memories"])
api_router.include_router(keys.router, tags=["API Keys"])
