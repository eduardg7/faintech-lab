"""Memories API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.api.schemas import (
    MemoryCreate,
    MemorySearchRequest,
    MemoryResponse,
    MemoryListResponse,
    CompactRequest,
    CompactResponse,
    MemoryType
)
from app.services.memory_service import get_memory_service, MemoryService

router = APIRouter()


def _to_response(memory_dict: dict) -> MemoryResponse:
    """Convert memory dict to response model."""
    return MemoryResponse(
        id=memory_dict["id"],
        agent_id=memory_dict["agent_id"],
        project_id=memory_dict.get("project_id", ""),
        task_id=memory_dict.get("task_id"),
        timestamp=memory_dict["timestamp"],
        type=memory_dict["type"],
        content=memory_dict["content"],
        tags=memory_dict.get("tags", []),
        metadata=memory_dict.get("metadata", {})
    )


@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    memory_data: MemoryCreate,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """
    Create a new memory entry.
    
    Args:
        memory_data: Memory creation data
        memory_service: Memory service instance
        
    Returns:
        Created memory entry
    """
    entry = memory_service.write(
        agent_id=memory_data.agent_id,
        content=memory_data.content,
        project_id=memory_data.project_id,
        task_id=memory_data.task_id,
        entry_type=memory_data.type,
        tags=memory_data.tags,
        metadata=memory_data.metadata
    )
    
    return _to_response(entry)


@router.post("/search", response_model=MemoryListResponse)
async def search_memories(
    search_request: MemorySearchRequest,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """
    Search memory entries.
    
    Args:
        search_request: Search parameters
        memory_service: Memory service instance
        
    Returns:
        List of matching memories
    """
    entries = memory_service.search(
        query=search_request.query,
        agent_id=search_request.agent_id,
        project_id=search_request.project_id,
        task_id=search_request.task_id,
        entry_type=search_request.entry_type,
        tags=search_request.tags,
        limit=search_request.limit,
        since=search_request.since,
        until=search_request.until
    )
    
    memories = [_to_response(e) for e in entries]
    
    return MemoryListResponse(
        memories=memories,
        total=len(memories)
    )


@router.get("/agent/{agent_id}", response_model=MemoryListResponse)
async def get_agent_memories(
    agent_id: str,
    limit: int = Query(default=10, ge=1, le=100),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """
    Get recent memories for an agent.
    
    Args:
        agent_id: Agent ID
        limit: Maximum results
        memory_service: Memory service instance
        
    Returns:
        List of recent memories
    """
    entries = memory_service.get_for_agent(agent_id, limit)
    memories = [_to_response(e) for e in entries]
    
    return MemoryListResponse(
        memories=memories,
        total=len(memories)
    )


@router.get("/task/{project_id}/{task_id}", response_model=MemoryListResponse)
async def get_task_memories(
    project_id: str,
    task_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """
    Get memories for a specific task.
    
    Args:
        project_id: Project ID
        task_id: Task ID
        limit: Maximum results
        memory_service: Memory service instance
        
    Returns:
        List of task memories
    """
    entries = memory_service.get_for_task(project_id, task_id, limit)
    memories = [_to_response(e) for e in entries]
    
    return MemoryListResponse(
        memories=memories,
        total=len(memories)
    )


@router.post("/compact", response_model=CompactResponse)
async def compact_memories(
    compact_request: CompactRequest,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """
    Compact old memories into summaries.
    
    Args:
        compact_request: Compaction parameters
        memory_service: Memory service instance
        
    Returns:
        Compaction statistics
    """
    result = memory_service.compact(
        agent_id=compact_request.agent_id,
        days_old=compact_request.days_old
    )
    
    return CompactResponse(
        compacted=result.get("compacted", 0),
        summaries_created=result.get("summaries_created", 0),
        files_archived=result.get("files_archived", 0),
        message=result.get("message", "")
    )
