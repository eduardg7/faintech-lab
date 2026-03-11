"""Integration tests for Agent Memory Cloud Python SDK.

These tests require a running backend server.
Run with: pytest tests/test_integration.py
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

import httpx

from agentmemory import MemoryClient
from agentmemory.models import (
    Memory,
    MemoryType,
    Agent,
    Project,
    SearchResult,
)
from agentmemory.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


@pytest.fixture
def mock_api_key():
    """Mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def mock_client(mock_api_key):
    """Create a mock client for testing."""
    with patch('agentmemory.client.httpx.Client') as mock_httpx:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_httpx.return_value.request.return_value = mock_response

        client = MemoryClient(api_key=mock_api_key)
        yield client
        client.close()


@pytest.fixture
def sample_memory_data():
    """Sample memory data for testing."""
    return {
        "id": "mem-001",
        "agent_id": "agent-001",
        "memory_type": "outcome",
        "content": "Task completed successfully",
        "created_at": "2026-03-11T10:00:00Z",
        "updated_at": "2026-03-11T10:00:00Z",
        "tags": ["deployment", "success"],
        "metadata": {"env": "production"},
        "confidence": 0.95,
        "project_id": "proj-001",
        "workspace_id": "ws-001",
    }


@pytest.fixture
def sample_agent_data():
    """Sample agent data for testing."""
    return {
        "id": "agent-001",
        "name": "Test Agent",
        "description": "Test agent for integration tests",
        "created_at": "2026-03-11T09:00:00Z",
        "metadata": {"version": "1.0"},
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "id": "proj-001",
        "name": "Test Project",
        "description": "Test project for integration tests",
        "created_at": "2026-03-11T08:00:00Z",
        "metadata": {"team": "engineering"},
    }


class TestMemoryClient:
    """Test MemoryClient initialization and configuration."""

    def test_init_with_api_key(self, mock_api_key):
        """Test client initialization with explicit API key."""
        with patch('agentmemory.client.httpx.Client'):
            client = MemoryClient(api_key=mock_api_key)
            assert client.api_key == mock_api_key
            assert client.base_url == "https://api.faintech.dev/v1"
            assert client.timeout == 30.0
            client.close()

    def test_init_with_env_var(self):
        """Test client initialization using environment variable."""
        with patch.dict(os.environ, {'AGENT_MEMORY_API_KEY': 'env-api-key'}):
            with patch('agentmemory.client.httpx.Client'):
                client = MemoryClient()
                assert client.api_key == 'env-api-key'
                client.close()

    def test_init_missing_api_key(self):
        """Test that missing API key raises AuthenticationError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(AuthenticationError) as exc_info:
                MemoryClient()
            assert "API key required" in str(exc_info.value)

    def test_init_custom_base_url(self, mock_api_key):
        """Test client initialization with custom base URL."""
        with patch('agentmemory.client.httpx.Client'):
            client = MemoryClient(
                api_key=mock_api_key,
                base_url="http://localhost:8000/api/v1"
            )
            assert client.base_url == "http://localhost:8000/api/v1"
            client.close()

    def test_context_manager(self, mock_api_key):
        """Test client as context manager."""
        with patch('agentmemory.client.httpx.Client') as mock_httpx:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_httpx.return_value.request.return_value = mock_response

            mock_client_instance = Mock()
            mock_httpx.return_value = mock_client_instance

            with MemoryClient(api_key=mock_api_key) as client:
                assert client.api_key == mock_api_key
                mock_client_instance.close.assert_not_called()

            mock_client_instance.close.assert_called_once()


class TestMemoriesResource:
    """Test memories resource operations."""

    def test_create_memory(self, mock_client, sample_memory_data):
        """Test creating a memory."""
        mock_client._request.return_value = sample_memory_data

        memory = mock_client.memories.create(
            agent_id="agent-001",
            memory_type=MemoryType.OUTCOME,
            content="Task completed successfully",
            tags=["deployment", "success"],
            confidence=0.95,
        )

        assert isinstance(memory, Memory)
        assert memory.id == "mem-001"
        assert memory.agent_id == "agent-001"
        assert memory.memory_type == MemoryType.OUTCOME
        assert memory.content == "Task completed successfully"
        assert memory.tags == ["deployment", "success"]
        assert memory.confidence == 0.95

        mock_client._request.assert_called_once_with(
            "POST",
            "/memories",
            json={
                "agent_id": "agent-001",
                "memory_type": "outcome",
                "content": "Task completed successfully",
                "tags": ["deployment", "success"],
                "confidence": 0.95,
            },
        )

    def test_get_memory(self, mock_client, sample_memory_data):
        """Test getting a memory by ID."""
        mock_client._request.return_value = sample_memory_data

        memory = mock_client.memories.get("mem-001")

        assert isinstance(memory, Memory)
        assert memory.id == "mem-001"
        mock_client._request.assert_called_once_with("GET", "/memories/mem-001")

    def test_list_memories(self, mock_client):
        """Test listing memories with filters."""
        mock_client._request.return_value = {
            "items": [],
            "total": 0,
            "limit": 20,
            "offset": 0,
        }

        response = mock_client.memories.list(
            agent_id="agent-001",
            memory_type="outcome",
            tags=["success"],
            limit=20,
            offset=0,
        )

        assert response.items == []
        assert response.total == 0
        assert response.limit == 20
        assert response.offset == 0
        assert not response.has_more

        mock_client._request.assert_called_once_with(
            "GET",
            "/memories",
            params={
                "agent_id": "agent-001",
                "memory_type": "outcome",
                "tags": "success",
                "limit": 20,
                "offset": 0,
            },
        )

    def test_update_memory(self, mock_client, sample_memory_data):
        """Test updating a memory."""
        updated_data = sample_memory_data.copy()
        updated_data["content"] = "Updated content"
        updated_data["tags"] = ["updated"]
        mock_client._request.return_value = updated_data

        memory = mock_client.memories.update(
            "mem-001",
            content="Updated content",
            tags=["updated"],
        )

        assert memory.content == "Updated content"
        assert memory.tags == ["updated"]

        mock_client._request.assert_called_once_with(
            "PUT",
            "/memories/mem-001",
            json={"content": "Updated content", "tags": ["updated"]},
        )

    def test_delete_memory(self, mock_client):
        """Test deleting a memory."""
        mock_client._request.return_value = {}

        mock_client.memories.delete("mem-001")

        mock_client._request.assert_called_once_with("DELETE", "/memories/mem-001")

    def test_compact_memories(self, mock_client):
        """Test compacting memories."""
        mock_client._request.return_value = {
            "memories_processed": 100,
            "memories_created": 10,
            "memories_archived": 90,
        }

        result = mock_client.memories.compact(
            agent_id="agent-001",
            project_id="proj-001",
            max_age_days=30,
        )

        assert result["memories_processed"] == 100
        assert result["memories_created"] == 10
        assert result["memories_archived"] == 90

        mock_client._request.assert_called_once_with(
            "POST",
            "/memories/compact",
            json={
                "agent_id": "agent-001",
                "project_id": "proj-001",
                "max_age_days": 30,
            },
        )


class TestAgentsResource:
    """Test agents resource operations."""

    def test_create_agent(self, mock_client, sample_agent_data):
        """Test creating an agent."""
        mock_client._request.return_value = sample_agent_data

        agent = mock_client.agents.create(
            name="Test Agent",
            description="Test agent for integration tests",
        )

        assert isinstance(agent, Agent)
        assert agent.id == "agent-001"
        assert agent.name == "Test Agent"
        assert agent.description == "Test agent for integration tests"

        mock_client._request.assert_called_once_with(
            "POST",
            "/agents",
            json={
                "name": "Test Agent",
                "description": "Test agent for integration tests",
            },
        )

    def test_get_agent(self, mock_client, sample_agent_data):
        """Test getting an agent by ID."""
        mock_client._request.return_value = sample_agent_data

        agent = mock_client.agents.get("agent-001")

        assert isinstance(agent, Agent)
        assert agent.id == "agent-001"

        mock_client._request.assert_called_once_with("GET", "/agents/agent-001")

    def test_list_agents(self, mock_client):
        """Test listing all agents."""
        mock_client._request.return_value = {
            "items": [],
            "total": 0,
            "limit": 20,
            "offset": 0,
        }

        response = mock_client.agents.list(limit=20, offset=0)

        assert response.items == []
        assert response.total == 0
        assert response.limit == 20
        assert response.offset == 0

        mock_client._request.assert_called_once_with(
            "GET",
            "/agents",
            params={"limit": 20, "offset": 0},
        )


class TestProjectsResource:
    """Test projects resource operations."""

    def test_create_project(self, mock_client, sample_project_data):
        """Test creating a project."""
        mock_client._request.return_value = sample_project_data

        project = mock_client.projects.create(
            name="Test Project",
            description="Test project for integration tests",
        )

        assert isinstance(project, Project)
        assert project.id == "proj-001"
        assert project.name == "Test Project"
        assert project.description == "Test project for integration tests"

        mock_client._request.assert_called_once_with(
            "POST",
            "/projects",
            json={
                "name": "Test Project",
                "description": "Test project for integration tests",
            },
        )

    def test_get_project(self, mock_client, sample_project_data):
        """Test getting a project by ID."""
        mock_client._request.return_value = sample_project_data

        project = mock_client.projects.get("proj-001")

        assert isinstance(project, Project)
        assert project.id == "proj-001"

        mock_client._request.assert_called_once_with("GET", "/projects/proj-001")

    def test_list_projects(self, mock_client):
        """Test listing all projects."""
        mock_client._request.return_value = {
            "items": [],
            "total": 0,
            "limit": 20,
            "offset": 0,
        }

        response = mock_client.projects.list(limit=20, offset=0)

        assert response.items == []
        assert response.total == 0
        assert response.limit == 20
        assert response.offset == 0

        mock_client._request.assert_called_once_with(
            "GET",
            "/projects",
            params={"limit": 20, "offset": 0},
        )


class TestSearchResource:
    """Test search resource operations."""

    def test_keyword_search(self, mock_client, sample_memory_data):
        """Test keyword search."""
        mock_client._request.return_value = {
            "results": [
                {
                    "memory": sample_memory_data,
                    "score": 0.95,
                }
            ]
        }

        results = mock_client.search.keyword(
            query="redis caching",
            agent_id="agent-001",
            limit=10,
        )

        assert len(results) == 1
        assert isinstance(results[0], SearchResult)
        assert results[0].score == 0.95
        assert results[0].memory.id == "mem-001"

        mock_client._request.assert_called_once_with(
            "GET",
            "/search/keyword",
            params={
                "query": "redis caching",
                "agent_id": "agent-001",
                "limit": 10,
            },
        )

    def test_semantic_search(self, mock_client, sample_memory_data):
        """Test semantic search."""
        mock_client._request.return_value = {
            "results": [
                {
                    "memory": sample_memory_data,
                    "score": 0.87,
                }
            ]
        }

        results = mock_client.search.semantic(
            query="How did we improve performance?",
            limit=5,
        )

        assert len(results) == 1
        assert isinstance(results[0], SearchResult)
        assert results[0].score == 0.87

        mock_client._request.assert_called_once_with(
            "GET",
            "/search/semantic",
            params={
                "query": "How did we improve performance?",
                "limit": 5,
            },
        )


class TestErrorHandling:
    """Test error handling."""

    def test_authentication_error(self, mock_api_key):
        """Test 401 authentication error."""
        with patch('agentmemory.client.httpx.Client') as mock_httpx:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_httpx.return_value.request.return_value = mock_response

            with pytest.raises(AuthenticationError) as exc_info:
                client = MemoryClient(api_key=mock_api_key)
                client.memories.list()

            assert "Invalid API key" in str(exc_info.value)
            assert exc_info.value.status_code == 401
            client.close()

    def test_not_found_error(self, mock_client):
        """Test 404 not found error."""
        mock_client._client.request.side_effect = [
            Mock(status_code=404),
        ]

        with pytest.raises(NotFoundError) as exc_info:
            mock_client.memories.get("nonexistent-id")

        assert "Resource not found" in str(exc_info.value)
        assert exc_info.value.status_code == 404

    def test_validation_error(self, mock_client):
        """Test 422 validation error."""
        mock_client._client.request.side_effect = [
            Mock(
                status_code=422,
                json=lambda: {"detail": "Invalid memory type"}
            ),
        ]

        with pytest.raises(ValidationError) as exc_info:
            mock_client.memories.create(
                agent_id="agent-001",
                memory_type="invalid",
                content="test",
            )

        assert "Validation failed" in str(exc_info.value)
        assert exc_info.value.status_code == 422

    def test_rate_limit_error(self, mock_client):
        """Test 429 rate limit error."""
        mock_client._client.request.side_effect = [
            Mock(
                status_code=429,
                headers={"Retry-After": "60"}
            ),
        ]

        with pytest.raises(RateLimitError) as exc_info:
            mock_client.memories.list()

        assert "Rate limit exceeded" in str(exc_info.value)
        assert exc_info.value.retry_after == 60
        assert exc_info.value.status_code == 429

    def test_generic_api_error(self, mock_client):
        """Test generic 500 API error."""
        mock_client._client.request.side_effect = [
            Mock(
                status_code=500,
                text="Internal server error"
            ),
        ]

        from agentmemory.exceptions import AgentMemoryError
        with pytest.raises(AgentMemoryError) as exc_info:
            mock_client.memories.list()

        assert "API error: 500" in str(exc_info.value)
        assert exc_info.value.status_code == 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
