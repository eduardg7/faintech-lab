"""Tests for Agents & Projects API (AMC-MVP-203)."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestAgentsAPI:
    """Test cases for GET /v1/agents endpoint."""

    def test_agents_endpoint_exists(self, client):
        """Endpoint is accessible and returns 200."""
        response = client.get("/v1/agents")
        assert response.status_code == 200

    def test_agents_response_shape(self, client):
        """Response contains agents list and total count."""
        response = client.get("/v1/agents")
        data = response.json()
        assert "agents" in data
        assert "total" in data
        assert isinstance(data["agents"], list)
        assert isinstance(data["total"], int)

    def test_agents_filter_by_project(self, client):
        """Filtering by project_id is accepted without error."""
        response = client.get("/v1/agents", params={"project_id": "test-project"})
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data

    def test_agents_pagination_params(self, client):
        """Limit and offset query params are accepted."""
        response = client.get("/v1/agents", params={"limit": 10, "offset": 0})
        assert response.status_code == 200

    def test_agents_invalid_limit(self, client):
        """Limit above 500 is rejected with 422."""
        response = client.get("/v1/agents", params={"limit": 501})
        assert response.status_code == 422

    def test_agents_invalid_offset(self, client):
        """Negative offset is rejected with 422."""
        response = client.get("/v1/agents", params={"offset": -1})
        assert response.status_code == 422

    def test_agents_entry_shape(self, client):
        """Each agent entry has required fields if data exists."""
        response = client.get("/v1/agents")
        data = response.json()
        for agent in data["agents"]:
            assert "agent_id" in agent
            assert "memory_count" in agent
            assert isinstance(agent["memory_count"], int)


class TestProjectsAPI:
    """Test cases for GET /v1/projects endpoint."""

    def test_projects_endpoint_exists(self, client):
        """Endpoint is accessible and returns 200."""
        response = client.get("/v1/projects")
        assert response.status_code == 200

    def test_projects_response_shape(self, client):
        """Response contains projects list and total count."""
        response = client.get("/v1/projects")
        data = response.json()
        assert "projects" in data
        assert "total" in data
        assert isinstance(data["projects"], list)
        assert isinstance(data["total"], int)

    def test_projects_pagination_params(self, client):
        """Limit and offset query params are accepted."""
        response = client.get("/v1/projects", params={"limit": 20, "offset": 0})
        assert response.status_code == 200

    def test_projects_invalid_limit(self, client):
        """Limit above 500 is rejected with 422."""
        response = client.get("/v1/projects", params={"limit": 501})
        assert response.status_code == 422

    def test_projects_entry_shape(self, client):
        """Each project entry has required fields if data exists."""
        response = client.get("/v1/projects")
        data = response.json()
        for project in data["projects"]:
            assert "project_id" in project
            assert "agent_count" in project
            assert "memory_count" in project
            assert isinstance(project["agent_count"], int)
            assert isinstance(project["memory_count"], int)
