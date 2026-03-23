"""Hybrid search API combining keyword and vector similarity.

Implements AMC-MVP-110: Memory Search Optimization (Vector)
- Combines PostgreSQL full-text search with pgvector similarity
- Weighted scoring: keyword (0.4) + vector (0.6)
- Target: <100ms p95 latency with HNSW index
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, text, func
from pydantic import BaseModel, Field
import time
import os

from app.core.database import get_db
from app.core.cache import get_cache_service, CacheConfig
from app.models.memory import Memory
from app.services.embedding import get_embedding_service
from app.services.analytics import analytics


router = APIRouter(prefix="/search", tags=["Hybrid Search"])


class HybridSearchResult(BaseModel):
    """Hybrid search result with combined relevance scores."""
    id: str
    workspace_id: str
    agent_id: str
    project_id: Optional[str]
    memory_type: str
    content: str
    tags: List[str]
    keyword_score: float = Field(..., ge=0.0, le=1.0, description="Keyword match score")
    vector_score: float = Field(..., ge=0.0, le=1.0, description="Vector similarity score")
    combined_score: float = Field(..., ge=0.0, le=1.0, description="Weighted combined score")
    created_at: datetime


class HybridSearchResponse(BaseModel):
    """Hybrid search response with performance metrics."""
    results: List[HybridSearchResult]
    total: int
    page: int
    page_size: int
    has_next: bool
    query_time_ms: float = Field(..., description="Total query time in milliseconds")
    keyword_time_ms: float = Field(..., description="Keyword search time")
    vector_time_ms: float = Field(..., description="Vector search + embedding time")
    embedding_cache_hit: bool = Field(False, description="Whether embedding was cached")
    database_type: str = Field(..., description="Database type used (postgres/sqlite)")


async def _detect_postgresql(db: AsyncSession) -> bool:
    """Detect if database is PostgreSQL."""
    try:
        result = await db.execute(text("SELECT version()"))
        version = result.scalar()
        return "postgresql" in version.lower()
    except Exception:
        return False


async def _is_pgvector_enabled(db: AsyncSession) -> bool:
    """Check if pgvector extension is available."""
    database_type = os.getenv("DATABASE_TYPE", "sqlite").lower()
    if database_type != "postgres":
        return False

    try:
        result = await db.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
        return result.scalar() is not None
    except Exception:
        return False


@router.post(
    "/hybrid",
    response_model=HybridSearchResponse,
    summary="Hybrid search combining keyword and vector similarity",
    description="""
Perform intelligent search combining PostgreSQL full-text search with vector similarity.

## Scoring Algorithm

```
combined_score = (keyword_weight × keyword_score) + (vector_weight × vector_score)
```

- **Keyword Score**: Normalized ts_rank_cd from PostgreSQL full-text search
- **Vector Score**: Cosine similarity via pgvector HNSW index
- **Default Weights**: 40% keyword, 60% vector (semantic meaning prioritized)

## Performance

- Target: <100ms p95 latency on PostgreSQL with pgvector
- HNSW index for fast approximate nearest neighbor search
- Embedding cache for repeated queries

## Response Fields

- `results`: List of matching memories with scores
- `query_time_ms`: Total query execution time
- `keyword_time_ms`: Time spent on keyword search
- `vector_time_ms`: Time spent on embedding + vector search
- `embedding_cache_hit`: Whether query embedding was cached

## Example

```bash
curl -X POST "/v1/search/hybrid?q=api%20authentication&min_score=0.5"
```
""",
    responses={
        200: {
            "description": "Search results with relevance scores",
            "content": {
                "application/json": {
                    "example": {
                        "results": [
                            {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "workspace_id": "ws_abc123",
                                "agent_id": "agent_001",
                                "project_id": "proj_001",
                                "memory_type": "learning",
                                "content": "Authentication flow uses JWT tokens...",
                                "tags": ["auth", "security"],
                                "keyword_score": 0.85,
                                "vector_score": 0.92,
                                "combined_score": 0.892,
                                "created_at": "2024-01-15T10:30:00Z"
                            }
                        ],
                        "total": 1,
                        "page": 1,
                        "page_size": 10,
                        "has_next": False,
                        "query_time_ms": 45.2,
                        "keyword_time_ms": 12.1,
                        "vector_time_ms": 33.1,
                        "embedding_cache_hit": False,
                        "database_type": "postgres"
                    }
                }
            }
        }
    }
)
async def hybrid_search(
    q: str = Query(
        ...,
        min_length=1,
        max_length=500,
        description="Search query text (1-500 characters)",
        example="how to implement user authentication"
    ),
    agent_id: Optional[str] = Query(
        None,
        description="Filter results to specific agent ID",
        example="agent_001"
    ),
    project_id: Optional[str] = Query(
        None,
        description="Filter results to specific project ID",
        example="proj_abc123"
    ),
    tags: Optional[str] = Query(
        None,
        description="Comma-separated list of tags to filter (OR logic)",
        example="auth,security,api"
    ),
    keyword_weight: float = Query(
        0.4,
        ge=0.0,
        le=1.0,
        description="Weight for keyword matching score (0.0-1.0)"
    ),
    vector_weight: float = Query(
        0.6,
        ge=0.0,
        le=1.0,
        description="Weight for vector similarity score (0.0-1.0)"
    ),
    min_score: float = Query(
        0.3,
        ge=0.0,
        le=1.0,
        description="Minimum combined score threshold (0.0-1.0)"
    ),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=50, description="Results per page (max 50)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Hybrid search combining keyword matching and vector similarity.

    Scoring formula:
    combined_score = (keyword_weight * keyword_score) + (vector_weight * vector_score)

    Default weights: 40% keyword, 60% vector (semantic meaning prioritized)

    Performance target: <100ms p95 with HNSW index on PostgreSQL.
    Falls back to Python-based similarity on SQLite.

    - **q**: Search query text
    - **keyword_weight**: Weight for keyword matching (default: 0.4)
    - **vector_weight**: Weight for vector similarity (default: 0.6)
    - **min_score**: Minimum combined score threshold (default: 0.3)
    """
    start_time = time.perf_counter()
    cache = get_cache_service()

    is_postgresql = await _detect_postgresql(db)
    has_pgvector = await _is_pgvector_enabled(db)
    database_type = "postgres" if has_pgvector else "sqlite"

    # Build base filter conditions
    conditions = [Memory.deleted_at.is_(None)]
    if agent_id:
        conditions.append(Memory.agent_id == agent_id)
    if project_id:
        conditions.append(Memory.project_id == project_id)

    # Tag filtering
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        if tag_list:
            from sqlalchemy import or_
            tag_conditions = [Memory.tags.contains(f'"{tag}"') for tag in tag_list]
            conditions.append(or_(*tag_conditions))

    # --- KEYWORD SEARCH ---
    keyword_start = time.perf_counter()
    keyword_results = {}  # memory_id -> keyword_score

    if is_postgresql:
        # PostgreSQL full-text search with ranking
        keyword_query = text("""
            SELECT id, ts_rank_cd(content_tsvector, plainto_tsquery('english', :query), 32) as rank
            FROM memories
            WHERE deleted_at IS NULL
            AND content_tsvector @@ plainto_tsquery('english', :query)
            ORDER BY rank DESC
            LIMIT 100
        """)
        result = await db.execute(keyword_query, {"query": q})
        for row in result:
            # Normalize ts_rank to 0-1 (ts_rank_cd typically returns 0-0.1)
            keyword_results[str(row[0])] = min(1.0, float(row[1]) * 10)
    else:
        # SQLite LIKE search
        search_term = f"%{q}%"
        like_query = select(Memory.id, Memory.content).where(
            and_(Memory.content.ilike(search_term), *conditions)
        ).limit(100)
        result = await db.execute(like_query)
        for row in result:
            # Simple relevance: 1.0 if query appears, 0.5 if case-insensitive match
            memory_id = str(row[0])
            content = row[1] or ""
            if q in content:
                keyword_results[memory_id] = 1.0
            elif q.lower() in content.lower():
                keyword_results[memory_id] = 0.5
            else:
                keyword_results[memory_id] = 0.3

    keyword_time_ms = (time.perf_counter() - keyword_start) * 1000

    # --- VECTOR SEARCH ---
    vector_start = time.perf_counter()
    vector_results = {}  # memory_id -> vector_score
    embedding_cache_hit = False

    # Get or generate query embedding
    cached_embedding = await cache.get_embedding(q)
    if cached_embedding:
        query_embedding = cached_embedding
        embedding_cache_hit = True
    else:
        embedding_service = get_embedding_service()
        embedding_result = await embedding_service.embed_text(q)
        query_embedding = embedding_result['embedding']
        await cache.set_embedding(q, query_embedding)

    if has_pgvector:
        # Use pgvector for native similarity search with HNSW index
        # Cosine distance = 1 - cosine_similarity, so we use 1 - distance
        vector_query = text("""
            SELECT id, 1 - (embedding <=> :embedding::vector) as similarity
            FROM memories
            WHERE deleted_at IS NULL
            AND embedding IS NOT NULL
            ORDER BY embedding <=> :embedding::vector
            LIMIT 100
        """)
        result = await db.execute(
            vector_query,
            {"embedding": str(query_embedding)}
        )
        for row in result:
            vector_results[str(row[0])] = float(row[1])
    else:
        # Fallback: Python cosine similarity (slower, for SQLite dev)
        import numpy as np

        memories_query = select(Memory.id, Memory.embedding).where(
            and_(Memory.embedding.isnot(None), *conditions)
        ).limit(1000)  # Limit for performance

        result = await db.execute(memories_query)
        query_vec = np.array(query_embedding)
        query_norm = np.linalg.norm(query_vec)

        if query_norm > 0:
            for row in result:
                memory_id = str(row[0])
                embedding = row[1]
                if embedding:
                    mem_vec = np.array(embedding)
                    mem_norm = np.linalg.norm(mem_vec)
                    if mem_norm > 0:
                        similarity = np.dot(query_vec, mem_vec) / (query_norm * mem_norm)
                        vector_results[memory_id] = float(similarity)

    vector_time_ms = (time.perf_counter() - vector_start) * 1000

    # --- COMBINE AND RANK ---
    all_memory_ids = set(keyword_results.keys()) | set(vector_results.keys())

    combined_results = []
    for memory_id in all_memory_ids:
        keyword_score = keyword_results.get(memory_id, 0.0)
        vector_score = vector_results.get(memory_id, 0.0)

        combined_score = (keyword_weight * keyword_score) + (vector_weight * vector_score)

        if combined_score >= min_score:
            combined_results.append({
                'memory_id': memory_id,
                'keyword_score': keyword_score,
                'vector_score': vector_score,
                'combined_score': combined_score
            })

    # Sort by combined score descending
    combined_results.sort(key=lambda x: x['combined_score'], reverse=True)

    # --- FETCH FULL MEMORY DATA ---
    total = len(combined_results)
    offset = (page - 1) * page_size
    paginated_results = combined_results[offset:offset + page_size]
    has_next = (offset + page_size) < total

    # Fetch memory details for paginated results
    search_results = []
    if paginated_results:
        memory_ids = [r['memory_id'] for r in paginated_results]
        memories_query = select(Memory).where(Memory.id.in_(memory_ids))
        result = await db.execute(memories_query)
        memories_by_id = {str(m.id): m for m in result.scalars().all()}

        # Preserve order by combined score
        for item in paginated_results:
            memory = memories_by_id.get(item['memory_id'])
            if memory:
                search_results.append(HybridSearchResult(
                    id=memory.id,
                    workspace_id=memory.workspace_id,
                    agent_id=memory.agent_id,
                    project_id=memory.project_id,
                    memory_type=memory.type,
                    content=memory.content,
                    tags=memory.get_tags(),
                    keyword_score=round(item['keyword_score'], 4),
                    vector_score=round(item['vector_score'], 4),
                    combined_score=round(item['combined_score'], 4),
                    created_at=memory.created_at
                ))

    query_time_ms = (time.perf_counter() - start_time) * 1000

    # Track search execution event
    analytics.track_search_executed(
        user_id="api_user",  # Auth context not available on POST endpoint
        query=q,
        results_count=len(search_results),
        search_type="hybrid"
    )

    return HybridSearchResponse(
        results=search_results,
        total=total,
        page=page,
        page_size=page_size,
        has_next=has_next,
        query_time_ms=round(query_time_ms, 2),
        keyword_time_ms=round(keyword_time_ms, 2),
        vector_time_ms=round(vector_time_ms, 2),
        embedding_cache_hit=embedding_cache_hit,
        database_type=database_type
    )
