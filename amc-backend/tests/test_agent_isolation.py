"""Tests for agent memory isolation (R-LAB-002).

Verifies that authenticated agents/users can ONLY access memories
within their own workspace. Cross-workspace reads, writes and deletes
must return HTTP 403 Forbidden.

Attack scenarios tested:
  1. Unauthenticated request → 401
  2. Agent A cannot list memories of Agent B (cross-workspace)
  3. Agent A cannot read a specific memory owned by Agent B
  4. Agent A cannot update a memory owned by Agent B
  5. Agent A cannot delete a memory owned by Agent B
  6. Agent A cannot enumerate agents in Agent B's workspace
  7. Agent A cannot enumerate projects in Agent B's workspace
  8. Agent A receives only their own memories in list (no data leakage)
"""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from main import app
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User
from app.models.workspace import Workspace
from app.models.memory import Memory
import json


# ---------------------------------------------------------------------------
# Test database
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
async def client(test_session):
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Fixture helpers: two independent workspaces/users
# ---------------------------------------------------------------------------


async def _create_workspace_and_user(
    session: AsyncSession, slug: str, email: str
) -> tuple[Workspace, User, str]:
    """Create a workspace, a user and return (workspace, user, access_token)."""
    workspace = Workspace(name=f"WS {slug}", slug=slug, tier="pro")
    session.add(workspace)
    await session.flush()

    user = User(
        workspace_id=workspace.id,
        email=email,
        password_hash=hash_password("Password123!"),
        full_name="Test User",
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    await session.flush()

    token = create_access_token(subject=user.id, workspace_id=workspace.id, email=email)
    return workspace, user, token


async def _create_memory_for_workspace(
    session: AsyncSession, workspace_id: str, agent_id: str, content: str
) -> Memory:
    """Insert a memory directly into the DB for a given workspace."""
    import hashlib

    memory = Memory(
        workspace_id=workspace_id,
        agent_id=agent_id,
        type="learning",
        content=content,
        content_hash=hashlib.sha256(content.encode()).hexdigest(),
        tags=json.dumps(["test"]),
        meta_data=json.dumps({}),
    )
    session.add(memory)
    await session.commit()
    await session.refresh(memory)
    return memory


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
async def two_agents(test_session: AsyncSession):
    """Create two independent workspaces/users and seed each with one memory."""
    ws_a, user_a, token_a = await _create_workspace_and_user(
        test_session, "workspace-a", "agent-a@example.com"
    )
    ws_b, user_b, token_b = await _create_workspace_and_user(
        test_session, "workspace-b", "agent-b@example.com"
    )
    await test_session.commit()

    mem_a = await _create_memory_for_workspace(
        test_session, ws_a.id, "agent-a", "Secret memory of Agent A"
    )
    mem_b = await _create_memory_for_workspace(
        test_session, ws_b.id, "agent-b", "Secret memory of Agent B"
    )

    return {
        "token_a": token_a,
        "token_b": token_b,
        "workspace_a_id": ws_a.id,
        "workspace_b_id": ws_b.id,
        "mem_a_id": mem_a.id,
        "mem_b_id": mem_b.id,
    }


# ---------------------------------------------------------------------------
# Tests: Unauthenticated access
# ---------------------------------------------------------------------------


class TestUnauthenticated:
    """All memory endpoints must require authentication."""

    @pytest.mark.asyncio
    async def test_list_memories_requires_auth(self, client: AsyncClient):
        response = await client.get("/v1/memories")
        assert response.status_code == 403  # HTTPBearer returns 403 when no token

    @pytest.mark.asyncio
    async def test_get_memory_requires_auth(self, client: AsyncClient):
        response = await client.get("/v1/memories/some-id")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_memory_requires_auth(self, client: AsyncClient):
        response = await client.post(
            "/v1/memories",
            json={
                "agent_id": "x",
                "memory_type": "learning",
                "content": "y",
                "tags": [],
            },
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_memory_requires_auth(self, client: AsyncClient):
        response = await client.patch("/v1/memories/some-id", json={"content": "x"})
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_memory_requires_auth(self, client: AsyncClient):
        response = await client.delete("/v1/memories/some-id")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_list_agents_requires_auth(self, client: AsyncClient):
        response = await client.get("/v1/agents")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_list_projects_requires_auth(self, client: AsyncClient):
        response = await client.get("/v1/projects")
        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Tests: Cross-workspace isolation (the core R-LAB-002 scenarios)
# ---------------------------------------------------------------------------


class TestAgentIsolation:
    """Agent A must not be able to access Agent B's memories."""

    @pytest.mark.asyncio
    async def test_agent_cannot_read_other_agent_memory(
        self, client: AsyncClient, two_agents: dict
    ):
        """GET /memories/{id} owned by workspace B must return 403 for workspace A token."""
        response = await client.get(
            f"/v1/memories/{two_agents['mem_b_id']}",
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_agent_cannot_update_other_agent_memory(
        self, client: AsyncClient, two_agents: dict
    ):
        """PATCH /memories/{id} owned by workspace B must return 403 for workspace A token."""
        response = await client.patch(
            f"/v1/memories/{two_agents['mem_b_id']}",
            json={"content": "Hijacked content"},
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_agent_cannot_delete_other_agent_memory(
        self, client: AsyncClient, two_agents: dict
    ):
        """DELETE /memories/{id} owned by workspace B must return 403 for workspace A token."""
        response = await client.delete(
            f"/v1/memories/{two_agents['mem_b_id']}",
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_list_memories_returns_only_own_workspace(
        self, client: AsyncClient, two_agents: dict
    ):
        """GET /memories must return only the caller's workspace memories."""
        response = await client.get(
            "/v1/memories",
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 200
        data = response.json()

        # Agent A should only see their own memory
        assert data["total"] == 1
        memory_ids = [m["id"] for m in data["memories"]]
        assert two_agents["mem_a_id"] in memory_ids
        assert two_agents["mem_b_id"] not in memory_ids

    @pytest.mark.asyncio
    async def test_list_memories_cannot_query_other_workspace_by_agent_id(
        self, client: AsyncClient, two_agents: dict
    ):
        """Filtering by agent_id='agent-b' while authenticated as workspace A returns 0."""
        response = await client.get(
            "/v1/memories?agent_id=agent-b",
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 200
        data = response.json()
        # workspace A has no 'agent-b' — cross-workspace query returns empty
        assert data["total"] == 0
        assert len(data["memories"]) == 0

    @pytest.mark.asyncio
    async def test_create_memory_uses_jwt_workspace(
        self, client: AsyncClient, two_agents: dict, test_session: AsyncSession
    ):
        """POST /memories must set workspace_id from JWT, ignoring body payload."""
        response = await client.post(
            "/v1/memories",
            json={
                "agent_id": "agent-a",
                "memory_type": "learning",
                "content": "New memory from agent A",
                "tags": [],
            },
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 201
        data = response.json()

        # Verify the memory was stored with workspace A's id
        assert data["workspace_id"] == two_agents["workspace_a_id"]

        # Double-check via DB
        result = await test_session.execute(
            select(Memory).where(Memory.id == data["id"])
        )
        db_memory = result.scalar_one_or_none()
        assert db_memory is not None
        assert db_memory.workspace_id == two_agents["workspace_a_id"]

    @pytest.mark.asyncio
    async def test_list_agents_scoped_to_workspace(
        self, client: AsyncClient, two_agents: dict
    ):
        """GET /agents must only return agents from the caller's workspace."""
        response = await client.get(
            "/v1/agents",
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 200
        data = response.json()

        agent_ids = [a["agent_id"] for a in data["agents"]]
        assert "agent-a" in agent_ids
        assert "agent-b" not in agent_ids

    @pytest.mark.asyncio
    async def test_list_projects_scoped_to_workspace(
        self, client: AsyncClient, test_session: AsyncSession, two_agents: dict
    ):
        """GET /projects must only return projects from the caller's workspace."""
        # Seed a memory with a project_id for each workspace
        import hashlib

        mem_proj_a = Memory(
            workspace_id=two_agents["workspace_a_id"],
            agent_id="agent-a",
            type="learning",
            content="project memory A",
            content_hash=hashlib.sha256(b"project memory A").hexdigest(),
            project_id="project-alpha",
            tags=json.dumps([]),
            meta_data=json.dumps({}),
        )
        mem_proj_b = Memory(
            workspace_id=two_agents["workspace_b_id"],
            agent_id="agent-b",
            type="learning",
            content="project memory B",
            content_hash=hashlib.sha256(b"project memory B").hexdigest(),
            project_id="project-beta",
            tags=json.dumps([]),
            meta_data=json.dumps({}),
        )
        test_session.add(mem_proj_a)
        test_session.add(mem_proj_b)
        await test_session.commit()

        response = await client.get(
            "/v1/projects",
            headers={"Authorization": f"Bearer {two_agents['token_a']}"},
        )
        assert response.status_code == 200
        data = response.json()

        project_ids = [p["project_id"] for p in data["projects"]]
        assert "project-alpha" in project_ids
        assert "project-beta" not in project_ids

    @pytest.mark.asyncio
    async def test_symmetry_agent_b_cannot_read_agent_a_memory(
        self, client: AsyncClient, two_agents: dict
    ):
        """Isolation is symmetric: B cannot read A's memories either."""
        response = await client.get(
            f"/v1/memories/{two_agents['mem_a_id']}",
            headers={"Authorization": f"Bearer {two_agents['token_b']}"},
        )
        assert response.status_code == 403
