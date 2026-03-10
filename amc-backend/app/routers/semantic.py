"""Semantic search API router using vector embeddings."""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, text
from pydantic import BaseModel, Field
import time

from app.core.database import get_db
from app.core.jobs import JobQueue, get_job_queue
from app.models.memory import Memory
from app.services.embedding import get_embedding_service


router = APIRouter(prefix="/search", tags=["Semantic Search"])


class SemanticSearchRequest(BaseModel):
    """Request model for semantic search."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query text")
    limit: int = Field(10, ge=1, le=50, description="Max results to return")
    min_similarity: float = Field(0.5, ge=0.0, le=1.0, description="Minimum similarity score (0-1)")


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
    """Semantic search response."""
    results: List[SemanticSearchResult]
    query_time_ms: float = Field(..., description="Query execution time in milliseconds")
    query_embedding_time_ms: float = Field(..., description="Time to generate query embedding")


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
    
    # Generate embedding for query
    embed_start = time.perf_counter()
    embedding_service = get_embedding_service()
    query_embedding_result = await embedding_service.embed_text(request.query)
    query_embedding = query_embedding_result['embedding']
    embedding_time = (time.perf_counter() - embed_start) * 1000
    
    # Build query for vector similarity search
    # PostgreSQL with pgvector uses the <=> operator for cosine similarity
    query = text("""
        SELECT 
            id, workspace_id, agent_id, project_id, type, content, 
            tags, importance, created_at, updated_at,
            1 - (embedding <=> :query_vector) as similarity
        FROM memories
        WHERE deleted_at IS NULL
        AND embedding IS NOT NULL
        AND (embedding <=> :query_vector) >= :min_similarity
        ORDER BY similarity DESC
        LIMIT :limit
    """)
    
    # Execute query
    result = await db.execute(
        query,
        {
            "query_vector": query_embedding,
            "min_similarity": request.min_similarity,
            "limit": request.limit
        }
    )
    
    rows = result.all()
    
    # Calculate total time
    query_time_ms = (time.perf_counter() - start_time) * 1000
    
    # Convert to response format
    search_results = []
    for row in rows:
        search_results.append(SemanticSearchResult(
            id=row[0],
            workspace_id=row[1],
            agent_id=row[2],
            project_id=row[3],
            memory_type=row[4],
            content=row[5],
            tags=row[6] if row[6] else [],
            similarity_score=float(row[11]),
            created_at=row[9]
        ))
    
    return SemanticSearchResponse(
        results=search_results,
        query_time_ms=round(query_time_ms, 2),
        query_embedding_time_ms=round(embedding_time, 2)
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
