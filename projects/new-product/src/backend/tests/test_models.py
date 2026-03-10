"""Tests for database models."""
import pytest
from app.models.models import Workspace, Agent, Memory, ApiKey


def test_workspace_model():
    """Test Workspace model creation."""
    workspace = Workspace(
        name="Test Workspace",
        slug="test-workspace"
    )
    assert workspace.name == "Test Workspace"
    assert workspace.slug == "test-workspace"
    assert workspace.id is None  # Not yet persisted


def test_agent_model():
    """Test Agent model creation."""
    agent = Agent(
        workspace_id="workspace-123",
        name="Test Agent",
        agent_type="claude",
        is_active=True  # Explicitly set for Python-level test
    )
    assert agent.name == "Test Agent"
    assert agent.agent_type == "claude"
    assert agent.is_active == True


def test_memory_model():
    """Test Memory model creation."""
    memory = Memory(
        agent_id="agent-123",
        content="Test memory content",
        memory_type="episodic",
        importance_score=0  # Explicitly set for Python-level test
    )
    assert memory.content == "Test memory content"
    assert memory.memory_type == "episodic"
    assert memory.importance_score == 0


def test_api_key_model():
    """Test ApiKey model creation."""
    api_key = ApiKey(
        workspace_id="workspace-123",
        key_hash="hashed-key-123",
        name="Test Key",
        is_active=True  # Explicitly set for Python-level test
    )
    assert api_key.name == "Test Key"
    assert api_key.is_active == True
    assert api_key.revoked_at is None
