"""Agents API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Workspace, Agent
from app.api.schemas import AgentCreate, AgentUpdate, AgentResponse

router = APIRouter()


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    workspace_id: str,
    db: Session = Depends(get_db)
):
    """
    Create a new agent in a workspace.
    
    Args:
        agent_data: Agent creation data
        workspace_id: Workspace ID
        db: Database session
        
    Returns:
        Created agent
        
    Raises:
        HTTPException: If workspace not found
    """
    # Verify workspace exists
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace '{workspace_id}' not found"
        )
    
    agent = Agent(
        workspace_id=workspace_id,
        name=agent_data.name,
        agent_type=agent_data.agent_type,
        metadata_json=agent_data.metadata_json
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    workspace_id: str,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    List agents in a workspace.
    
    Args:
        workspace_id: Workspace ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        active_only: Filter to active agents only
        db: Database session
        
    Returns:
        List of agents
    """
    query = db.query(Agent).filter(Agent.workspace_id == workspace_id)
    
    if active_only:
        query = query.filter(Agent.is_active == True)
    
    agents = query.offset(skip).limit(limit).all()
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """
    Get an agent by ID.
    
    Args:
        agent_id: Agent ID
        db: Database session
        
    Returns:
        Agent data
        
    Raises:
        HTTPException: If agent not found
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an agent.
    
    Args:
        agent_id: Agent ID
        agent_data: Agent update data
        db: Database session
        
    Returns:
        Updated agent
        
    Raises:
        HTTPException: If agent not found
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    update_data = agent_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(agent, key, value)
    
    db.commit()
    db.refresh(agent)
    
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an agent.
    
    Args:
        agent_id: Agent ID
        db: Database session
        
    Raises:
        HTTPException: If agent not found
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found"
        )
    
    db.delete(agent)
    db.commit()
