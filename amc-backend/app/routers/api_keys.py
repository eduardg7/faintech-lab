"""Workspace API key management endpoints."""
from datetime import datetime

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.errors import NotFoundError, ValidationError
from app.core.security import API_KEY_PREFIX, generate_api_key
from app.models.api_key import ApiKey
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.api_key import (
    ApiKeyCreateRequest,
    ApiKeyCreateResponse,
    ApiKeyListResponse,
    ApiKeySummary,
)


router = APIRouter(prefix="/api-keys", tags=["API Keys"])


def _build_key_preview(api_key: ApiKey) -> str:
    """Return a masked preview that is safe to show after creation."""
    return f"{API_KEY_PREFIX}{api_key.key_prefix}..."


@router.post(
    "",
    response_model=ApiKeyCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a workspace API key",
)
async def create_api_key(
    payload: ApiKeyCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new API key for the caller's workspace."""
    name = payload.name.strip()
    if not name:
        raise ValidationError(message="API key name cannot be blank")

    raw_key, key_hash, key_prefix = generate_api_key()
    api_key = ApiKey(
        workspace_id=current_user.workspace_id,
        name=name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        scopes="read,write",
        is_active=True,
    )

    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)

    return ApiKeyCreateResponse(
        id=api_key.id,
        key=raw_key,
        created_at=api_key.created_at,
    )


@router.get(
    "",
    response_model=ApiKeyListResponse,
    summary="List workspace API keys",
)
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List API keys for the caller's workspace."""
    query = (
        select(ApiKey)
        .where(ApiKey.workspace_id == current_user.workspace_id)
        .order_by(ApiKey.created_at.desc())
    )
    result = await db.execute(query)
    api_keys = result.scalars().all()

    return ApiKeyListResponse(
        api_keys=[
            ApiKeySummary(
                id=api_key.id,
                name=api_key.name,
                key_preview=_build_key_preview(api_key),
                is_active=api_key.is_active,
                created_at=api_key.created_at,
                last_used_at=api_key.last_used_at,
                revoked_at=api_key.revoked_at,
                expires_at=api_key.expires_at,
            )
            for api_key in api_keys
        ],
        total=len(api_keys),
    )


@router.delete(
    "/{api_key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke a workspace API key",
)
async def revoke_api_key(
    api_key_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Revoke an API key in the caller's workspace."""
    query = select(ApiKey).where(
        and_(
            ApiKey.id == api_key_id,
            ApiKey.workspace_id == current_user.workspace_id,
        )
    )
    result = await db.execute(query)
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise NotFoundError(resource="API key", identifier=api_key_id)

    if api_key.is_active:
        api_key.is_active = False
        api_key.revoked_at = datetime.utcnow()

    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
