"""FastAPI dependencies for API endpoints."""
from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Workspace
from app.middleware.auth import verify_api_key
from typing import Tuple


async def get_workspace(
    request: Request,
    auth_result: Tuple[Workspace, object] = Depends(verify_api_key)
) -> Workspace:
    """
    Dependency that extracts the current workspace from the authenticated request.
    
    This dependency must be used after the verify_api_key dependency has been applied,
    which ensures the request has a valid API key and sets the workspace in request.state.
    
    Args:
        request: The FastAPI request object
        auth_result: The result from verify_api_key dependency (workspace, api_key tuple)
    
    Returns:
        Workspace: The authenticated workspace
    
    Raises:
        HTTPException: If workspace context is not available (500 Internal Server Error)
    
    Example:
        @router.get("/agents")
        async def list_agents(
            workspace: Workspace = Depends(get_workspace),
            db: Session = Depends(get_db)
        ):
            # workspace is guaranteed to be the authenticated user's workspace
            return db.query(Agent).filter(Agent.workspace_id == workspace.id).all()
    """
    workspace, _ = auth_result
    
    if not workspace:
        raise HTTPException(
            status_code=500,
            detail="Workspace context not available"
        )
    
    return workspace


async def get_workspace_and_key(
    auth_result: Tuple[Workspace, object] = Depends(verify_api_key)
) -> Tuple[Workspace, object]:
    """
    Dependency that returns both the workspace and the API key used for authentication.
    
    Use this when you need access to the API key metadata (e.g., for logging, rate limiting
    per key, or tracking usage).
    
    Args:
        auth_result: The result from verify_api_key dependency (workspace, api_key tuple)
    
    Returns:
        Tuple[Workspace, ApiKey]: The authenticated workspace and API key objects
    
    Example:
        @router.post("/memories")
        async def create_memory(
            data: MemoryCreate,
            result: Tuple[Workspace, ApiKey] = Depends(get_workspace_and_key),
            db: Session = Depends(get_db)
        ):
            workspace, api_key = result
            # Log which API key was used
            logger.info(f"Memory created via API key: {api_key.name}")
            ...
    """
    return auth_result
