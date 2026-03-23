"""Search API router with full-text search using PostgreSQL GIN indexes."""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, text
from pydantic import BaseModel, Field
import time

from app.core.database import get_db
from app.core.cache import get_cache_service, CacheConfig
from app.models.memory import Memory
from app.schemas.memory import MemoryResponse
from app.services.analytics import analytics


router = APIRouter(prefix="/search", tags=["Search"])


class SearchResult(BaseModel):
    """Search result with relevance score."""
    id: str
    workspace_id: str
    agent_id: str
    project_id: Optional[str]
    memory_type: str
    content: str
    tags: List[str]
    relevance_score: float = Field(..., description="Search relevance score (0-1)")
    created_at: datetime
    updated_at: Optional[datetime]


class SearchResponse(BaseModel):
    """Paginated search response."""
    results: List[SearchResult]
    total: int
    page: int
    page_size: int
    has_next: bool
    query_time_ms: float = Field(..., description="Query execution time in milliseconds")


async def _detect_postgresql(db: AsyncSession) -> bool:
    """Detect if database is PostgreSQL."""
    try:
        result = await db.execute(text("SELECT version()"))
        version = result.scalar()
        return "postgresql" in version.lower()
    except Exception:
        return False


@router.get(
    "/keyword",
    response_model=SearchResponse,
    summary="Full-text keyword search with filters"
)
async def keyword_search(
    q: str = Query(..., min_length=1, max_length=500, description="Search query"),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    Full-text keyword search using PostgreSQL GIN indexes.

    - **q**: Search query (required, supports PostgreSQL full-text syntax on PG)
    - **agent_id**: Filter by agent ID
    - **project_id**: Filter by project ID
    - **tags**: Comma-separated list of tags to filter
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)

    Performance target: <200ms for 1000 entries.

    Note: On PostgreSQL, uses full-text search with GIN index.
    On SQLite, falls back to LIKE-based search.

    Results are cached for 5 minutes to improve response times.
    """
    # Check cache first
    cache = get_cache_service()
    cached_results = await cache.get_search_results(
        query=q,
        agent_id=agent_id,
        project_id=project_id,
        tags=tags,
        page=page,
        page_size=page_size
    )

    if cached_results:
        # Return cached results
        return SearchResponse(**cached_results)

    start_time = time.perf_counter()

    is_postgresql = await _detect_postgresql(db)

    # Build filter conditions
    conditions = [Memory.deleted_at.is_(None)]

    if agent_id:
        conditions.append(Memory.agent_id == agent_id)

    if project_id:
        conditions.append(Memory.project_id == project_id)

    # Tag filtering - check if any of the provided tags are in the memory's tags
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_list:
            tag_conditions = [
                Memory.tags.contains(f'"{tag}"') for tag in tag_list
            ]
            conditions.append(or_(*tag_conditions))

    # Build search query based on database type
    if is_postgresql:
        # PostgreSQL: Use full-text search with tsvector
        query = select(
            Memory,
            text("ts_rank(content_tsvector, plainto_tsquery('english', :query)) as rank")
        ).where(
            and_(*conditions, text("content_tsvector @@ plainto_tsquery('english', :query)"))
        ).params(query=q)

        # Order by relevance
        query = query.order_by(text("rank DESC"))
    else:
        # SQLite: Fall back to LIKE search
        search_term = f"%{q}%"
        conditions.append(Memory.content.ilike(search_term))

        query = select(Memory).where(and_(*conditions))

        # Order by creation date for SQLite
        query = query.order_by(Memory.created_at.desc())

    # Get total count
    count_query = select(func.count(Memory.id)).where(and_(*conditions))
    if not is_postgresql:
        # Add content filter for count in SQLite
        search_term = f"%{q}%"
        count_query = count_query.where(Memory.content.ilike(search_term))

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    rows = result.all()

    # Calculate query time
    query_time_ms = (time.perf_counter() - start_time) * 1000

    # Convert to response format
    search_results = []
    for row in rows:
        if is_postgresql:
            memory = row[0]
            rank = row[1] if len(row) > 1 else 0.0
            # Normalize rank to 0-1 range (ts_rank can be > 1)
            relevance_score = min(1.0, float(rank) * 10) if rank else 0.0
        else:
            memory = row[0] if hasattr(row, '__getitem__') else row
            # For SQLite, use simple relevance based on match presence
            relevance_score = 0.5 if q.lower() in memory.content.lower() else 0.0

        search_results.append(SearchResult(
            id=memory.id,
            workspace_id=memory.workspace_id,
            agent_id=memory.agent_id,
            project_id=memory.project_id,
            memory_type=memory.type,
            content=memory.content,
            tags=memory.get_tags(),
            relevance_score=relevance_score,
            created_at=memory.created_at,
            updated_at=memory.updated_at
        ))

    # Calculate has_next
    has_next = (offset + page_size) < total

    response = SearchResponse(
        results=search_results,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next,
        query_time_ms=round(query_time_ms, 2)
    )

    # Cache results for future requests
    await cache.set_search_results(
        query=q,
        agent_id=agent_id,
        project_id=project_id,
        tags=tags,
        page=page,
        page_size=page_size,
        results=response.model_dump()
    )

    # Track search execution event
    analytics.track_search_executed(
        user_id="api_user",  # Auth context not available on GET endpoint
        query=q,
        results_count=len(search_results),
        search_type="keyword"
    )

    return response


@router.get(
    "/suggest",
    response_model=List[str],
    summary="Get search suggestions based on prefix"
)
async def search_suggestions(
    prefix: str = Query(..., min_length=1, max_length=50, description="Search prefix"),
    limit: int = Query(10, ge=1, le=50, description="Max suggestions"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get search suggestions based on prefix.

    Returns distinct words from memory content that start with the prefix.
    """
    is_postgresql = await _detect_postgresql(db)

    if is_postgresql:
        # PostgreSQL: Use ts_stat for word extraction
        query = text("""
            SELECT DISTINCT word
            FROM ts_stat($$
                SELECT to_tsvector('english', content)
                FROM memories
                WHERE deleted_at IS NULL
            $$)
            WHERE word ILIKE :like_pattern
            ORDER BY word
            LIMIT :limit
        """)
    else:
        # SQLite: Simple LIKE query for words
        query = text("""
            SELECT DISTINCT word
            FROM (
                SELECT content as word
                FROM memories
                WHERE deleted_at IS NULL
                AND content LIKE :like_pattern
                LIMIT 1000
            )
            ORDER BY word
            LIMIT :limit
        """)

    result = await db.execute(
        query,
        {"like_pattern": f"{prefix}%", "limit": limit}
    )

    suggestions = [row[0] for row in result.all()]
    return suggestions
