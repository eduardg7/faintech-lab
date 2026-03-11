"""Agents & Projects API router — AMC-MVP-203.

GET /v1/agents   — list agents with memory counts and last activity, scoped by project
GET /v1/projects — list projects accessible to the caller with memory counts

All endpoints require bearer authentication and are scoped to the caller's workspace
(agent isolation R-LAB-002). Bearer auth accepts JWT access tokens or workspace API keys.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.memory import Memory
from app.routers.auth import AuthContext, get_current_auth_context

router = APIRouter(tags=["Agents & Projects"])


# ── Schemas ────────────────────────────────────────────────────────────────────


class AgentSummary(BaseModel):
    agent_id: str
    project_id: Optional[str] = None
    memory_count: int
    last_activity: Optional[datetime] = None

    class Config:
        from_attributes = True


class AgentListResponse(BaseModel):
    agents: list[AgentSummary]
    total: int


class ProjectSummary(BaseModel):
    project_id: str
    agent_count: int
    memory_count: int
    last_activity: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: list[ProjectSummary]
    total: int


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.get(
    "/agents",
    response_model=AgentListResponse,
    summary="List agents with activity aggregation",
    description=(
        "Returns a list of distinct agents derived from memory records in the caller's workspace. "
        "Optionally filter by project_id for project isolation. "
        "Each entry includes total memory count and timestamp of last activity."
    ),
)
async def list_agents(
    project_id: Optional[str] = Query(None, description="Filter agents by project"),
    limit: int = Query(100, ge=1, le=500, description="Max number of agents to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
    auth_context: AuthContext = Depends(get_current_auth_context),
):
    """
    List agents with aggregated memory statistics.

    Requires JWT authentication. Results are scoped to the caller's workspace —
    agents from other workspaces are never visible (agent isolation R-LAB-002).

    Project isolation: when *project_id* is supplied only agents that have at
    least one memory tagged to that project are returned (RLS emulation).
    """
    # Base filter — exclude soft-deleted memories and enforce workspace isolation
    filters = [
        Memory.deleted_at.is_(None),
        Memory.workspace_id == auth_context.workspace_id,
    ]
    if project_id:
        filters.append(Memory.project_id == project_id)

    # Aggregate per (agent_id, project_id)
    stmt = (
        select(
            Memory.agent_id,
            Memory.project_id,
            func.count(Memory.id).label("memory_count"),
            func.max(Memory.created_at).label("last_activity"),
        )
        .where(*filters)
        .group_by(Memory.agent_id, Memory.project_id)
        .order_by(func.max(Memory.created_at).desc())
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.fetchall()

    agents = [
        AgentSummary(
            agent_id=row.agent_id,
            project_id=row.project_id,
            memory_count=row.memory_count,
            last_activity=row.last_activity,
        )
        for row in rows
    ]

    # Count distinct agents for pagination
    count_stmt = select(func.count(func.distinct(Memory.agent_id))).where(*filters)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    return AgentListResponse(agents=agents, total=total)


@router.get(
    "/projects",
    response_model=ProjectListResponse,
    summary="List accessible projects",
    description=(
        "Returns all projects in the caller's workspace that have at least one memory record. "
        "Includes agent count and total memory count per project. "
        "Memories without a project_id are excluded."
    ),
)
async def list_projects(
    limit: int = Query(
        100, ge=1, le=500, description="Max number of projects to return"
    ),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
    auth_context: AuthContext = Depends(get_current_auth_context),
):
    """
    List projects with aggregated memory and agent statistics.

    Requires JWT authentication. Results are scoped to the caller's workspace —
    projects from other workspaces are never visible (agent isolation R-LAB-002).

    Only projects with at least one active (non-deleted) memory appear.
    Memories that have no project_id set are not included.
    """
    filters = [
        Memory.deleted_at.is_(None),
        Memory.workspace_id == auth_context.workspace_id,
        Memory.project_id.isnot(None),
        Memory.project_id != "",
    ]

    stmt = (
        select(
            Memory.project_id,
            func.count(func.distinct(Memory.agent_id)).label("agent_count"),
            func.count(Memory.id).label("memory_count"),
            func.max(Memory.created_at).label("last_activity"),
        )
        .where(*filters)
        .group_by(Memory.project_id)
        .order_by(func.max(Memory.created_at).desc())
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(stmt)
    rows = result.fetchall()

    projects = [
        ProjectSummary(
            project_id=row.project_id,
            agent_count=row.agent_count,
            memory_count=row.memory_count,
            last_activity=row.last_activity,
        )
        for row in rows
    ]

    count_stmt = select(func.count(func.distinct(Memory.project_id))).where(*filters)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    return ProjectListResponse(projects=projects, total=total)
