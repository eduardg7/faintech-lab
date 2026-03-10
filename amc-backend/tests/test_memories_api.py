"""Tests for Memory API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from main import app
from app.core.database import Base, get_db
from app.models.memory import Memory
from app.models.workspace import Workspace
from datetime import datetime
import json


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
async def db_session():
    """Create test database session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        # Create default workspace
        workspace = Workspace(
            id="default-workspace",
            name="Default Workspace",
            slug="default-workspace"
        )
        session.add(workspace)
        await session.commit()
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session):
    """Create test client with database dependency override."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_memory(client: AsyncClient):
    """Test POST /v1/memories creates memory and returns 201."""
    response = await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "learning",
            "content": "Test memory content",
            "tags": ["test", "example"],
            "metadata": {"key": "value"}
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["agent_id"] == "test-agent"
    assert data["memory_type"] == "learning"
    assert data["content"] == "Test memory content"
    assert data["tags"] == ["test", "example"]
    assert data["metadata"] == {"key": "value"}
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_memory_exceeds_10kb(client: AsyncClient):
    """Test content validation rejects >10KB."""
    # Create content larger than 10KB
    large_content = "x" * 11000  # 11KB
    
    response = await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "learning",
            "content": large_content,
            "tags": []
        }
    )
    
    # Should reject with 422 (Pydantic validation) or 413 (router validation)
    assert response.status_code in [413, 422]
    detail = response.json()["detail"]
    # Handle both Pydantic array format and router string format
    if isinstance(detail, list):
        # Pydantic V2 error format: check for max_length constraint (10240 = 10KB)
        assert any("10KB limit" in str(err) or "exceeds" in str(err) or "10240" in str(err) for err in detail)
    else:
        assert "10KB limit" in detail or "exceeds" in detail


@pytest.mark.asyncio
async def test_list_memories(client: AsyncClient):
    """Test GET /v1/memories lists with pagination and filters."""
    # Create test memories
    for i in range(5):
        await client.post(
            "/v1/memories",
            json={
                "agent_id": f"agent-{i % 2}",
                "memory_type": "learning",
                "content": f"Memory {i}",
                "tags": ["test"]
            }
        )
    
    # Test list all
    response = await client.get("/v1/memories")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["memories"]) == 5
    assert data["page"] == 1
    assert data["has_next"] is False
    
    # Test filter by agent
    response = await client.get("/v1/memories?agent_id=agent-0")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3  # agent-0 has 3 memories (indices 0, 2, 4)
    
    # Test pagination
    response = await client.get("/v1/memories?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["memories"]) == 2
    assert data["has_next"] is True


@pytest.mark.asyncio
async def test_get_memory_by_id(client: AsyncClient):
    """Test GET /v1/memories/{id} returns single memory."""
    # Create memory
    create_response = await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "decision",
            "content": "Test decision",
            "tags": ["important"]
        }
    )
    memory_id = create_response.json()["id"]
    
    # Get by ID
    response = await client.get(f"/v1/memories/{memory_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == memory_id
    assert data["agent_id"] == "test-agent"
    assert data["memory_type"] == "decision"


@pytest.mark.asyncio
async def test_get_nonexistent_memory(client: AsyncClient):
    """Test GET /v1/memories/{id} returns 404 for non-existent memory."""
    response = await client.get("/v1/memories/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_memory(client: AsyncClient):
    """Test PATCH /v1/memories/{id} updates memory."""
    # Create memory
    create_response = await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "learning",
            "content": "Original content",
            "tags": ["original"]
        }
    )
    memory_id = create_response.json()["id"]
    
    # Update memory
    response = await client.patch(
        f"/v1/memories/{memory_id}",
        json={
            "content": "Updated content",
            "tags": ["updated", "modified"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated content"
    assert data["tags"] == ["updated", "modified"]
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_update_memory_exceeds_10kb(client: AsyncClient):
    """Test update validation rejects >10KB content."""
    # Create memory
    create_response = await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "learning",
            "content": "Original",
            "tags": []
        }
    )
    memory_id = create_response.json()["id"]
    
    # Try to update with large content
    large_content = "y" * 11000
    response = await client.patch(
        f"/v1/memories/{memory_id}",
        json={"content": large_content}
    )
    
    # Should reject with 422 (Pydantic validation) or 413 (router validation)
    assert response.status_code in [413, 422]
    detail = response.json()["detail"]
    # Handle both Pydantic array format and router string format
    if isinstance(detail, list):
        # Pydantic V2 error format: check for max_length constraint (10240 = 10KB)
        assert any("10KB limit" in str(err) or "exceeds" in str(err) or "10240" in str(err) for err in detail)
    else:
        assert "10KB limit" in detail or "exceeds" in detail


@pytest.mark.asyncio
async def test_delete_memory(client: AsyncClient):
    """Test DELETE /v1/memories/{id} soft deletes memory."""
    # Create memory
    create_response = await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "learning",
            "content": "To be deleted",
            "tags": []
        }
    )
    memory_id = create_response.json()["id"]
    
    # Delete memory
    response = await client.delete(f"/v1/memories/{memory_id}")
    assert response.status_code == 204
    
    # Verify it's deleted (should return 404)
    response = await client.get(f"/v1/memories/{memory_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_memories(client: AsyncClient):
    """Test search in memory content."""
    # Create memories with different content
    await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "learning",
            "content": "Python is great for AI",
            "tags": []
        }
    )
    await client.post(
        "/v1/memories",
        json={
            "agent_id": "test-agent",
            "memory_type": "learning",
            "content": "JavaScript is versatile",
            "tags": []
        }
    )
    
    # Search for Python (case-insensitive)
    response = await client.get("/v1/memories?search=python")
    assert response.status_code == 200
    data = response.json()
    # SQLite LIKE is case-insensitive by default
    assert data["total"] >= 1
    assert any("python" in m["content"].lower() for m in data["memories"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
