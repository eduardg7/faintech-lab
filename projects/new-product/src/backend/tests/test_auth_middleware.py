"""Tests for authentication middleware and dependencies."""
import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.middleware.auth import verify_api_key, hash_api_key, get_current_workspace
from app.api.dependencies import get_workspace, get_workspace_and_key
from app.models.models import Workspace, ApiKey
from app.core.database import get_db, Base, engine
from datetime import datetime
import hashlib


# Create test app
test_app = FastAPI()


@test_app.get("/test-workspace")
async def test_workspace_endpoint(workspace: Workspace = Depends(get_workspace)):
    return {"workspace_id": workspace.id, "workspace_name": workspace.name}


@test_app.get("/test-auth")
async def test_auth_endpoint(auth_result: tuple = Depends(verify_api_key)):
    workspace, api_key = auth_result
    return {"workspace_id": workspace.id, "api_key_name": api_key.name}


# Make pytest ignore these as test functions
test_workspace_endpoint.__test__ = False
test_auth_endpoint.__test__ = False


# Setup test database
@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    test_app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(test_app) as c:
        yield c
    
    test_app.dependency_overrides.clear()


@pytest.fixture
def test_workspace(db_session):
    """Create a test workspace."""
    workspace = Workspace(
        id="test-ws-001",
        name="Test Workspace",
        slug="test-workspace"
    )
    db_session.add(workspace)
    db_session.commit()
    return workspace


@pytest.fixture
def test_api_key(db_session, test_workspace):
    """Create a test API key."""
    raw_key = "test-api-key-12345"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    
    api_key = ApiKey(
        id="test-key-001",
        workspace_id=test_workspace.id,
        key_hash=key_hash,
        name="Test API Key",
        is_active=True
    )
    db_session.add(api_key)
    db_session.commit()
    
    return raw_key, api_key


class TestHashApiKey:
    """Tests for hash_api_key function."""
    
    def test_hash_api_key_returns_sha256_hexdigest(self):
        """Hash should be SHA-256 hex digest."""
        result = hash_api_key("my-secret-key")
        expected = hashlib.sha256("my-secret-key".encode()).hexdigest()
        assert result == expected
    
    def test_hash_api_key_is_consistent(self):
        """Same input should produce same hash."""
        key = "another-key"
        assert hash_api_key(key) == hash_api_key(key)
    
    def test_hash_api_key_different_inputs(self):
        """Different inputs should produce different hashes."""
        assert hash_api_key("key1") != hash_api_key("key2")


class TestVerifyApiKey:
    """Tests for verify_api_key dependency."""
    
    def test_missing_api_key_returns_401(self, client):
        """Missing API key should return 401 with AUTH_INVALID."""
        response = client.get("/test-auth")
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error"] == "AUTH_INVALID"
    
    def test_invalid_api_key_returns_401(self, client):
        """Invalid API key should return 401 with AUTH_INVALID."""
        response = client.get("/test-auth", headers={"X-API-Key": "invalid-key"})
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error"] == "AUTH_INVALID"
    
    def test_valid_api_key_returns_workspace(self, client, test_api_key, test_workspace):
        """Valid API key should return workspace and key info."""
        raw_key, _ = test_api_key
        response = client.get("/test-auth", headers={"X-API-Key": raw_key})
        assert response.status_code == 200
        data = response.json()
        assert data["workspace_id"] == test_workspace.id
    
    def test_revoked_api_key_returns_401(self, client, db_session, test_api_key):
        """Revoked API key should return 401."""
        raw_key, api_key = test_api_key
        api_key.revoked_at = datetime.utcnow()
        db_session.commit()
        
        response = client.get("/test-auth", headers={"X-API-Key": raw_key})
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error"] == "AUTH_INVALID"
    
    def test_inactive_api_key_returns_401(self, client, db_session, test_api_key):
        """Inactive API key should return 401."""
        raw_key, api_key = test_api_key
        api_key.is_active = False
        db_session.commit()
        
        response = client.get("/test-auth", headers={"X-API-Key": raw_key})
        assert response.status_code == 401
        data = response.json()
        assert data["detail"]["error"] == "AUTH_INVALID"


class TestGetWorkspace:
    """Tests for get_workspace dependency."""
    
    def test_get_workspace_returns_workspace(self, client, test_api_key, test_workspace):
        """get_workspace should return the authenticated workspace."""
        raw_key, _ = test_api_key
        response = client.get("/test-workspace", headers={"X-API-Key": raw_key})
        assert response.status_code == 200
        data = response.json()
        assert data["workspace_id"] == test_workspace.id
        assert data["workspace_name"] == test_workspace.name


class TestWorkspaceIsolation:
    """Tests for workspace isolation."""
    
    def test_workspace_isolation_enforced(self, db_session, client):
        """Workspace should only access its own resources."""
        # Create two workspaces
        ws1 = Workspace(id="ws-1", name="Workspace 1", slug="ws-1")
        ws2 = Workspace(id="ws-2", name="Workspace 2", slug="ws-2")
        db_session.add_all([ws1, ws2])
        db_session.commit()
        
        # Create API keys for each workspace
        key1 = "ws1-key"
        key1_hash = hashlib.sha256(key1.encode()).hexdigest()
        api_key1 = ApiKey(
            id="key-1",
            workspace_id=ws1.id,
            key_hash=key1_hash,
            name="WS1 Key",
            is_active=True
        )
        
        key2 = "ws2-key"
        key2_hash = hashlib.sha256(key2.encode()).hexdigest()
        api_key2 = ApiKey(
            id="key-2",
            workspace_id=ws2.id,
            key_hash=key2_hash,
            name="WS2 Key",
            is_active=True
        )
        
        db_session.add_all([api_key1, api_key2])
        db_session.commit()
        
        # Verify each key only accesses its own workspace
        response1 = client.get("/test-workspace", headers={"X-API-Key": key1})
        assert response1.json()["workspace_id"] == ws1.id
        
        response2 = client.get("/test-workspace", headers={"X-API-Key": key2})
        assert response2.json()["workspace_id"] == ws2.id


# Import SessionLocal for tests
from app.core.database import SessionLocal
