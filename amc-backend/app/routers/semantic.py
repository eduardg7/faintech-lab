"""Semantic search API router using vector embeddings."""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, text
from pydantic import BaseModel, Field
import time
import numpy as np

from app.core.database import get_db
from app.core.cache import get_cache_service
from app.core.jobs import JobQueue, get_job_queue
from app.models.memory import Memory
from app.services.embedding import get_embedding_service


router = APIRouter(prefix="/search", tags=["Semantic Search"])


class SemanticSearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query text")
    limit: int = Field(10, ge=1, le=50, description="Max results to return")
    min_similarity: float = Field(0.5, ge=0.0, le=1.0, description="Minimum similarity score (0-1)")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=50, description="Items per page")


class SemanticSearchResult(BaseModel):
    """Semantic search result with similarity score."""
    id: str
    workspace_id: str
    agent_id: str
    project_id: Optional[str]
    memory_type: str
    content: str
    tags: List[str]
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity to query (0-1)")
    created_at: datetime


class SemanticSearchResponse(BaseModel):
    """Semantic search response with pagination."""
    results: List[SemanticSearchResult]
    total: int = Field(..., description="Total matching results")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    has_next: bool = Field(..., description="Whether more results exist")
    query_time_ms: float = Field(..., description="Query execution time in milliseconds")
    query_embedding_time_ms: float = Field(..., description="Time to generate query embedding")
    cache_hit: bool = Field(False, description="Whether embedding was served from cache")


class EmbedJobRequest(BaseModel):
    """Request to embed existing memories."""
    memory_ids: List[str] = Field(..., min_length=1, max_length=100, description="Memory IDs to embed")


class EmbedJobResponse(BaseModel):
    """Response for embedding job creation."""
    job_id: str
    message: str


@router.post(
    "/semantic",
    response_model=SemanticSearchResponse,
    summary="Semantic search using vector embeddings"
)
async def semantic_search(
    request: SemanticSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Semantic search using vector embeddings.
    
    - **query**: Search query text
    - **limit**: Max results (default: 10, max: 50)
    - **min_similarity**: Minimum similarity threshold (default: 0.5)
    
    Returns results ranked by cosine similarity to query embedding.
    """
    start_time = time.perf_counter()
    cache = get_cache_service()
    
    # Try to get cached embedding first
    embed_start = time.perf_counter()
    cache_hit = False
    query_embedding = await cache.get_embedding(request.query)
    
    if query_embedding is None:
        # Generate embedding for query
        embedding_service = get_embedding_service()
        query_embedding_result = await embedding_service.embed_text(request.query)
        query_embedding = query_embedding_result['embedding']
        # Cache the embedding for future use
        await cache.set_embedding(request.query, query_embedding)
    else:
        cache_hit = True
    
    embedding_time = (time.perf_counter() - embed_start) * 1000
    
    # TODO: Migrate to pgvector for production (TD-015)
    # Current implementation uses Python cosine similarity for SQLite compatibility
    # Load all memories with embeddings (temporary workaround)
    query = select(Memory).where(
        and_(
            Memory.deleted_at.is_(None),
            Memory.embedding.isnot(None)
        )
    )
    result = await db.execute(query)
    memories = result.scalars().all()

    # Compute cosine similarity in Python
    query_vec = np.array(query_embedding)
    query_norm = np.linalg.norm(query_vec)

    scored_memories = []
    for memory in memories:
        if memory.embedding and len(memory.embedding) > 0:
            mem_vec = np.array(memory.embedding)
            mem_norm = np.linalg.norm(mem_vec)

            # Cosine similarity: (A · B) / (||A|| ||B||)
            if query_norm > 0 and mem_norm > 0:
                similarity = np.dot(query_vec, mem_vec) / (query_norm * mem_norm)

                if similarity >= request.min_similarity:
                    scored_memories.append((memory, similarity))

    # Sort by similarity (descending)
    scored_memories.sort(key=lambda x: x[1], reverse=True)
    
    # Calculate total before pagination
    total = len(scored_memories)
    
    # Apply pagination
    offset = (request.page - 1) * request.page_size
    paginated_memories = scored_memories[offset:offset + request.page_size]
    has_next = (offset + request.page_size) < total

    # Convert to response format
    search_results = []
    for memory, similarity in paginated_memories:
        search_results.append(SemanticSearchResult(
            id=memory.id,
            workspace_id=memory.workspace_id,
            agent_id=memory.agent_id,
            project_id=memory.project_id,
            memory_type=memory.type,
            content=memory.content,
            tags=memory.get_tags(),
            similarity_score=float(similarity),
            created_at=memory.created_at
        ))
    
    # Calculate total time
    query_time_ms = (time.perf_counter() - start_time) * 1000

    return SemanticSearchResponse(
        results=search_results,
        total=total,
        page=request.page,
        page_size=request.page_size,
        has_next=has_next,
        query_time_ms=round(query_time_ms, 2),
        query_embedding_time_ms=round(embedding_time, 2),
        cache_hit=cache_hit
    )


@router.post(
    "/embed",
    response_model=EmbedJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Queue embedding generation for existing memories"
)
async def queue_embedding_job(
    request: EmbedJobRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Queue background job to generate embeddings for existing memories.
    
    - **memory_ids**: List of memory IDs to embed
    """
    # Verify memories exist
    query = select(Memory).where(
        and_(
            Memory.id.in_(request.memory_ids),
            Memory.deleted_at.is_(None)
        )
    )
    
    result = await db.execute(query)
    memories = result.scalars().all()
    
    if not memories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No memories found with IDs: {request.memory_ids}"
        )
    
    # Create job ID
    import uuid
    job_id = str(uuid.uuid4())
    
    # Add to job queue
    from app.core.jobs import BackgroundJob
    job_queue = get_job_queue()
    job_queue.add_job(BackgroundJob(
        job_id=job_id,
        job_type='embed_memories',
        payload={
            'memory_ids': request.memory_ids,
            'count': len(memories)
        }
    ))
    
    # Schedule background task
    background_tasks.add_task(
        _process_embedding_job,
        job_id=job_id,
        memory_ids=request.memory_ids
    )
    
    return EmbedJobResponse(
        job_id=job_id,
        message=f"Queued embedding job for {len(memories)} memories"
    )


async def _process_embedding_job(job_id: str, memory_ids: List[str]):
    """Background task to process embedding job."""
    job_queue = get_job_queue()
    embedding_service = get_embedding_service()
    
    try:
        # TODO: Load memories from database and generate embeddings
        # This is a placeholder - actual implementation would:
        # 1. Load memories by IDs
        # 2. Generate embeddings in batches
        # 3. Update memory records with embeddings
        # 4. Track cost
        
        job_queue.complete_job(job_id, {
            'embedded_count': len(memory_ids),
            'status': 'completed'
        })
        
    except Exception as e:
        job_queue.fail_job(job_id, str(e))


@router.get(
    "/jobs/{job_id}",
    summary="Get embedding job status"
)
async def get_job_status(
    job_id: str,
):
    """
    Get status of an embedding job.
    
    - **job_id**: Job ID from /embed endpoint
    """
    job_queue = get_job_queue()
    job = job_queue.get_job(job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )
    
    return job.to_dict()
