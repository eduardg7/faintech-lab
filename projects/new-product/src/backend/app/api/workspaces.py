"""Workspaces API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Workspace
from app.api.schemas import WorkspaceCreate, WorkspaceResponse

router = APIRouter()


@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_data: WorkspaceCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new workspace.
    
    Args:
        workspace_data: Workspace creation data
        db: Database session
        
    Returns:
        Created workspace
        
    Raises:
        HTTPException: If workspace with slug already exists
    """
    # Check if slug already exists
    existing = db.query(Workspace).filter(Workspace.slug == workspace_data.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Workspace with slug '{workspace_data.slug}' already exists"
        )
    
    workspace = Workspace(
        name=workspace_data.name,
        slug=workspace_data.slug
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    
    return workspace


@router.get("/", response_model=List[WorkspaceResponse])
async def list_workspaces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all workspaces.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of workspaces
    """
    workspaces = db.query(Workspace).offset(skip).limit(limit).all()
    return workspaces


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a workspace by ID.
    
    Args:
        workspace_id: Workspace ID
        db: Database session
        
    Returns:
        Workspace data
        
    Raises:
        HTTPException: If workspace not found
    """
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace '{workspace_id}' not found"
        )
    
    return workspace


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a workspace.
    
    Args:
        workspace_id: Workspace ID
        db: Database session
        
    Raises:
        HTTPException: If workspace not found
    """
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace '{workspace_id}' not found"
        )
    
    db.delete(workspace)
    db.commit()
