"""Authentication middleware for API key validation."""
from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import ApiKey, Workspace
import hashlib
from datetime import datetime

# API Key header scheme
api_key_header = APIKeyHeader(name=settings.api_key_header, auto_error=False)


def hash_api_key(api_key: str) -> str:
    """Hash an API key for secure storage."""
    return hashlib.sha256(api_key.encode()).hexdigest()


async def verify_api_key(
    request: Request,
    api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db)
) -> tuple[Workspace, ApiKey]:
    """
    Verify API key and return workspace and key objects.
    
    Raises:
        HTTPException: If API key is missing, invalid, or revoked.
    
    Returns:
        tuple: (Workspace, ApiKey) objects
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "AUTH_INVALID",
                "message": "API key required. Provide X-API-Key header."
            }
        )
    
    # Hash the provided key
    key_hash = hash_api_key(api_key)
    
    # Look up the key
    db_key = db.query(ApiKey).filter(
        ApiKey.key_hash == key_hash,
        ApiKey.is_active == True,
        ApiKey.revoked_at == None
    ).first()
    
    if not db_key:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "AUTH_INVALID",
                "message": "Invalid or revoked API key"
            }
        )
    
    # Update last used timestamp
    db_key.last_used_at = datetime.utcnow()
    db.commit()
    
    # Get the workspace
    workspace = db.query(Workspace).filter(
        Workspace.id == db_key.workspace_id
    ).first()
    
    if not workspace:
        raise HTTPException(
            status_code=500,
            detail="Workspace not found for API key"
        )
    
    # Store workspace in request state for later use
    request.state.workspace = workspace
    
    return workspace, db_key


def get_current_workspace(request: Request) -> Workspace:
    """
    Extract the current workspace from request state.
    
    Must be used after verify_api_key dependency.
    """
    return request.state.workspace
