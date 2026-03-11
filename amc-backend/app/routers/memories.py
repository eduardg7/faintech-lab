"""Memory API router with CRUD endpoints.

All endpoints require JWT authentication and enforce workspace-scoped isolation:
- workspace_id is always taken from the JWT token, never from the request body
- Cross-workspace access returns 403 Forbidden (agent isolation - R-LAB-002)
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
import hashlib
import json

from app.core.database import get_db
from app.core.errors import (
    ContentTooLargeError,
    NotFoundError,
    ValidationError,
    DatabaseError,
)
from app.models.memory import Memory
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    MemoryListResponse,
    MemoryFilter,
    MemoryType,
)


router = APIRouter(prefix="/memories", tags=["Memories"])


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new memory",
)
async def create_memory(
    memory_data: MemoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new memory entry.

    Requires JWT authentication. workspace_id is taken from the token —
    the caller cannot create memories in another workspace.

    - **agent_id**: Required. Agent that owns this memory
    - **task_id**: Optional. Associated task
    - **memory_type**: Required. Type of memory (outcome/learning/preference/decision)
    - **content**: Required. Memory content (max 10KB)
    - **tags**: Optional. List of tags for categorization (max 10 tags)
    - **metadata**: Optional. Additional metadata
    """
    # Validate content size (additional check)
    content_size = len(memory_data.content.encode("utf-8"))
    if content_size > 10240:
        # Log validation rejection (AC #7)
        print(
            f"[Validation] Memory rejected: content size {content_size} bytes exceeds 10KB limit"
        )
        raise ContentTooLargeError(content_size=content_size, max_size=10240)

    # Generate content hash
    content_hash = hashlib.sha256(memory_data.content.encode("utf-8")).hexdigest()

    # Create memory instance — workspace_id is always from the JWT token (agent isolation)
    db_memory = Memory(
        workspace_id=current_user.workspace_id,  # Enforced from JWT — never from request
        agent_id=memory_data.agent_id,
        project_id=memory_data.project_id,
        type=memory_data.memory_type.value,
        content=memory_data.content,
        content_hash=content_hash,
        tags=json.dumps(memory_data.tags),
        meta_data=json.dumps(memory_data.metadata or {}),
    )

    db.add(db_memory)
    await db.commit()
    await db.refresh(db_memory)

    # Convert to response format
    return MemoryResponse(
        id=db_memory.id,
        workspace_id=db_memory.workspace_id,
        agent_id=db_memory.agent_id,
        task_id=None,  # Not in model yet
        project_id=db_memory.project_id,
        memory_type=db_memory.type,
        content=db_memory.content,
        tags=db_memory.get_tags(),
        metadata=db_memory.get_metadata(),
        importance=db_memory.importance,
        created_at=db_memory.created_at,
        updated_at=db_memory.updated_at,
    )


@router.get(
    "",
    response_model=MemoryListResponse,
    summary="List memories with pagination and filters",
)
async def list_memories(
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    memory_type: Optional[MemoryType] = Query(
        None, description="Filter by memory type"
    ),
    tag: Optional[str] = Query(None, description="Filter by tag (can be repeated)"),
    search: Optional[str] = Query(None, description="Search in content"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List memories with optional filters and pagination.

    Requires JWT authentication. Results are automatically scoped to the caller's
    workspace — cross-workspace enumeration is not possible (agent isolation R-LAB-002).

    - **agent_id**: Filter by agent ID (within caller's workspace only)
    - **project_id**: Filter by project ID
    - **memory_type**: Filter by memory type
    - **tag**: Filter by tag (can be repeated)
    - **search**: Search term in content
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    """
    # Build query — always scope to caller's workspace (agent isolation)
    query = select(Memory).where(
        and_(
            Memory.deleted_at.is_(None),
            Memory.workspace_id == current_user.workspace_id,
        )
    )

    # Apply filters
    if agent_id:
        query = query.where(Memory.agent_id == agent_id)

    if project_id:
        query = query.where(Memory.project_id == project_id)

    if memory_type:
        query = query.where(Memory.type == memory_type.value)

    if tag:
        # Filter memories that contain this tag
        query = query.where(Memory.tags.contains(f'"{tag}"'))

    if search:
        # Search in content
        query = query.where(Memory.content.ilike(f"%{search}%"))

    # Get total count — workspace filter is mandatory here too
    count_query = select(Memory.id).where(
        and_(
            Memory.deleted_at.is_(None),
            Memory.workspace_id == current_user.workspace_id,
        )
    )
    if agent_id:
        count_query = count_query.where(Memory.agent_id == agent_id)
    if project_id:
        count_query = count_query.where(Memory.project_id == project_id)
    if memory_type:
        count_query = count_query.where(Memory.type == memory_type.value)

    total_result = await db.execute(count_query)
    total = len(total_result.all())

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(Memory.created_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(query)
    memories = result.scalars().all()

    # Convert to response format
    memory_responses = [
        MemoryResponse(
            id=m.id,
            workspace_id=m.workspace_id,
            agent_id=m.agent_id,
            task_id=None,
            project_id=m.project_id,
            memory_type=m.type,
            content=m.content,
            tags=m.get_tags(),
            metadata=m.get_metadata(),
            importance=m.importance,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
        for m in memories
    ]

    # Calculate has_next
    has_next = (offset + page_size) < total

    return MemoryListResponse(
        memories=memory_responses,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next,
    )


@router.get(
    "/{memory_id}", response_model=MemoryResponse, summary="Get a specific memory"
)
async def get_memory(
    memory_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific memory by ID.

    Requires JWT authentication. Returns 403 if the memory belongs to a different
    workspace (agent isolation R-LAB-002).

    - **memory_id**: Memory ID (UUID string)
    """
    query = select(Memory).where(
        and_(Memory.id == memory_id, Memory.deleted_at.is_(None))
    )
    result = await db.execute(query)
    memory = result.scalar_one_or_none()

    if not memory:
        raise NotFoundError(resource="Memory", identifier=memory_id)

    # Workspace ownership check — prevent cross-workspace reads (R-LAB-002)
    if memory.workspace_id != current_user.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: agent isolation",
        )

    return MemoryResponse(
        id=memory.id,
        workspace_id=memory.workspace_id,
        agent_id=memory.agent_id,
        task_id=None,
        project_id=memory.project_id,
        memory_type=memory.type,
        content=memory.content,
        tags=memory.get_tags(),
        metadata=memory.get_metadata(),
        importance=memory.importance,
        created_at=memory.created_at,
        updated_at=memory.updated_at,
    )


@router.patch("/{memory_id}", response_model=MemoryResponse, summary="Update a memory")
async def update_memory(
    memory_id: str,
    memory_data: MemoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing memory.

    Requires JWT authentication. Returns 403 if the memory belongs to a different
    workspace (agent isolation R-LAB-002).

    - **memory_id**: Memory ID (UUID string)
    - **content**: Optional. Updated content (max 10KB)
    - **tags**: Optional. Updated tags
    - **metadata**: Optional. Updated metadata
    """
    query = select(Memory).where(
        and_(Memory.id == memory_id, Memory.deleted_at.is_(None))
    )
    result = await db.execute(query)
    memory = result.scalar_one_or_none()

    if not memory:
        raise NotFoundError(resource="Memory", identifier=memory_id)

    # Workspace ownership check — prevent cross-workspace writes (R-LAB-002)
    if memory.workspace_id != current_user.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: agent isolation",
        )

    # Validate content size if provided
    if memory_data.content:
        content_size = len(memory_data.content.encode("utf-8"))
        if content_size > 10240:
            print(
                f"[Validation] Memory update rejected: content size {content_size} bytes exceeds 10KB limit"
            )
            raise ContentTooLargeError(content_size=content_size, max_size=10240)

    # Update fields
    update_data = memory_data.dict(exclude_unset=True)
    if "content" in update_data:
        memory.content = update_data["content"]
        memory.content_hash = hashlib.sha256(
            update_data["content"].encode("utf-8")
        ).hexdigest()
    if "tags" in update_data:
        memory.tags = json.dumps(update_data["tags"])
    if "metadata" in update_data:
        memory.meta_data = json.dumps(update_data["metadata"])

    memory.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(memory)

    return MemoryResponse(
        id=memory.id,
        workspace_id=memory.workspace_id,
        agent_id=memory.agent_id,
        task_id=None,
        project_id=memory.project_id,
        memory_type=memory.type,
        content=memory.content,
        tags=memory.get_tags(),
        metadata=memory.get_metadata(),
        importance=memory.importance,
        created_at=memory.created_at,
        updated_at=memory.updated_at,
    )


@router.delete(
    "/{memory_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a memory"
)
async def delete_memory(
    memory_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a memory (soft delete).

    Requires JWT authentication. Returns 403 if the memory belongs to a different
    workspace (agent isolation R-LAB-002).

    - **memory_id**: Memory ID (UUID string)
    """
    query = select(Memory).where(
        and_(Memory.id == memory_id, Memory.deleted_at.is_(None))
    )
    result = await db.execute(query)
    memory = result.scalar_one_or_none()

    if not memory:
        raise NotFoundError(resource="Memory", identifier=memory_id)

    # Workspace ownership check — prevent cross-workspace deletes (R-LAB-002)
    if memory.workspace_id != current_user.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: agent isolation",
        )

    # Soft delete
    memory.deleted_at = datetime.utcnow()
    await db.commit()

    return None
