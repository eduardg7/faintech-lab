"""API Key management endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import secrets
import string
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.config import settings
from app.middleware.auth import verify_api_key, hash_api_key
from app.models.models import ApiKey, Workspace
from app.api.schemas import ApiKeyCreate, ApiKeyResponse, ApiKeyCreateResponse

router = APIRouter()


def generate_api_key() -> str:
    """Generate a secure random API key."""
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for _ in range(32))
    return f"amc_{key}"


@router.post("/keys", response_model=ApiKeyCreateResponse)
async def create_api_key(
    request: ApiKeyCreate,
    workspace: Workspace = Depends(verify_api_key),
    db: Session = Depends(get_db)
) -> ApiKeyCreateResponse:
    """
    Create a new API key for the current workspace.

    The full key is only returned once upon creation.
    """
    # Generate new API key
    full_key = generate_api_key()
    key_hash = hash_api_key(full_key)

    # Calculate expiration date if provided
    expires_at = None
    if request.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)

    # Create database record
    db_key = ApiKey(
        workspace_id=workspace.id,
        name=request.name,
        key_hash=key_hash,
        prefix=full_key[:8] + "..." + full_key[-4:],
        is_active=True,
        expires_at=expires_at,
        created_at=datetime.utcnow()
    )

    db.add(db_key)
    db.commit()
    db.refresh(db_key)

    return ApiKeyCreateResponse(
        id=db_key.id,
        name=db_key.name,
        secret=full_key,  # Only returned on creation
        prefix=db_key.prefix,
        created_at=db_key.created_at,
        expires_at=db_key.expires_at
    )


@router.get("/keys", response_model=List[ApiKeyResponse])
async def list_api_keys(
    workspace: Workspace = Depends(verify_api_key),
    db: Session = Depends(get_db)
) -> List[ApiKeyResponse]:
    """
    List all API keys for the current workspace.

    Only returns key prefixes, never the full key.
    """
    keys = db.query(ApiKey).filter(
        ApiKey.workspace_id == workspace.id,
        ApiKey.is_active == True
    ).order_by(ApiKey.created_at.desc()).all()

    return [
        ApiKeyResponse(
            id=key.id,
            name=key.name,
            prefix=key.prefix,
            created_at=key.created_at,
            last_used_at=key.last_used_at,
            expires_at=key.expires_at,
            revoked_at=key.revoked_at
        )
        for key in keys
    ]


@router.delete("/keys/{key_id}", status_code=204)
async def revoke_api_key(
    key_id: str,
    workspace: Workspace = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """
    Revoke (soft-delete) an API key.
    """
    key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.workspace_id == workspace.id,
        ApiKey.is_active == True
    ).first()

    if not key:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "KEY_NOT_FOUND",
                "message": "API key not found or already revoked"
            }
        )

    key.is_active = False
    key.revoked_at = datetime.utcnow()
    db.commit()
