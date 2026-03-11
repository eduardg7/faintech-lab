"""Tests for Agents & Projects API (AMC-MVP-203).

Note: All endpoints now require JWT authentication (R-LAB-002 agent isolation).
Tests use a fixture that provides a valid token for an authenticated user.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User
from app.models.workspace import Workspace


# ---------------------------------------------------------------------------
# Test DB setup
# ---------------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine):
    session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session


@pytest.fixture(scope="function")
async def auth_token(test_session: AsyncSession) -> str:
    """Create a workspace + user and return a valid JWT access token."""
    workspace = Workspace(name="Test WS", slug="test-ws-agents", tier="pro")
    test_session.add(workspace)
    await test_session.flush()

    user = User(
        workspace_id=workspace.id,
        email="agents-test@example.com",
        password_hash=hash_password("Password123!"),
        full_name="Agents Test User",
        is_active=True,
        is_verified=True,
    )
    test_session.add(user)
    await test_session.commit()

    return create_access_token(
        subject=user.id, workspace_id=workspace.id, email=user.email
    )


@pytest.fixture(scope="function")
async def client(test_session, auth_token):
    """Create async test client with DB override and auth token."""

    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        ac.headers.update({"Authorization": f"Bearer {auth_token}"})
        yield ac

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAgentsAPI:
    """Test cases for GET /v1/agents endpoint."""

    @pytest.mark.asyncio
    async def test_agents_endpoint_exists(self, client: AsyncClient):
        """Endpoint is accessible and returns 200 when authenticated."""
        response = await client.get("/v1/agents")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_agents_response_shape(self, client: AsyncClient):
        """Response contains agents list and total count."""
        response = await client.get("/v1/agents")
        data = response.json()
        assert "agents" in data
        assert "total" in data
        assert isinstance(data["agents"], list)
        assert isinstance(data["total"], int)

    @pytest.mark.asyncio
    async def test_agents_filter_by_project(self, client: AsyncClient):
        """Filtering by project_id is accepted without error."""
        response = await client.get("/v1/agents", params={"project_id": "test-project"})
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data

    @pytest.mark.asyncio
    async def test_agents_pagination_params(self, client: AsyncClient):
        """Limit and offset query params are accepted."""
        response = await client.get("/v1/agents", params={"limit": 10, "offset": 0})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_agents_invalid_limit(self, client: AsyncClient):
        """Limit above 500 is rejected with 422."""
        response = await client.get("/v1/agents", params={"limit": 501})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_agents_invalid_offset(self, client: AsyncClient):
        """Negative offset is rejected with 422."""
        response = await client.get("/v1/agents", params={"offset": -1})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_agents_entry_shape(self, client: AsyncClient):
        """Each agent entry has required fields if data exists."""
        response = await client.get("/v1/agents")
        data = response.json()
        for agent in data["agents"]:
            assert "agent_id" in agent
            assert "memory_count" in agent
            assert isinstance(agent["memory_count"], int)

    @pytest.mark.asyncio
    async def test_agents_requires_authentication(self, test_session: AsyncSession):
        """Endpoint must return 403 when no token is provided."""

        async def override_get_db():
            yield test_session

        app.dependency_overrides[get_db] = override_get_db

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.get("/v1/agents")

        app.dependency_overrides.clear()
        assert response.status_code == 403


class TestProjectsAPI:
    """Test cases for GET /v1/projects endpoint."""

    @pytest.mark.asyncio
    async def test_projects_endpoint_exists(self, client: AsyncClient):
        """Endpoint is accessible and returns 200 when authenticated."""
        response = await client.get("/v1/projects")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_projects_response_shape(self, client: AsyncClient):
        """Response contains projects list and total count."""
        response = await client.get("/v1/projects")
        data = response.json()
        assert "projects" in data
        assert "total" in data
        assert isinstance(data["projects"], list)
        assert isinstance(data["total"], int)

    @pytest.mark.asyncio
    async def test_projects_pagination_params(self, client: AsyncClient):
        """Limit and offset query params are accepted."""
        response = await client.get("/v1/projects", params={"limit": 20, "offset": 0})
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_projects_invalid_limit(self, client: AsyncClient):
        """Limit above 500 is rejected with 422."""
        response = await client.get("/v1/projects", params={"limit": 501})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_projects_entry_shape(self, client: AsyncClient):
        """Each project entry has required fields if data exists."""
        response = await client.get("/v1/projects")
        data = response.json()
        for project in data["projects"]:
            assert "project_id" in project
            assert "agent_count" in project
            assert "memory_count" in project
            assert isinstance(project["agent_count"], int)
            assert isinstance(project["memory_count"], int)

    @pytest.mark.asyncio
    async def test_projects_requires_authentication(self, test_session: AsyncSession):
        """Endpoint must return 403 when no token is provided."""

        async def override_get_db():
            yield test_session

        app.dependency_overrides[get_db] = override_get_db

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            response = await ac.get("/v1/projects")

        app.dependency_overrides.clear()
        assert response.status_code == 403
