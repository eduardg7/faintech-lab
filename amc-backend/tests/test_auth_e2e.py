"""E2E tests for authentication flows.

Tests the complete auth flow from HTTP request to response:
- Register, login, logout, refresh flows
- Token expiration handling
- Protected route access
- Error scenarios (invalid credentials, expired tokens)
"""
import pytest
import asyncio
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.models.user import User, RefreshToken
from app.models.workspace import Workspace
from app.core.database import Base, get_db
from main import app


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine):
    """Create test database session."""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


@pytest.fixture(scope="function")
async def client(test_session):
    """Create test client with database override."""
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_session: AsyncSession) -> dict:
    """Create a test user and return credentials."""
    from app.core.security import hash_password
    
    # Create workspace
    workspace = Workspace(
        name="Test Workspace",
        slug="test-workspace",
        tier="pro"
    )
    test_session.add(workspace)
    await test_session.flush()
    
    # Create user
    user = User(
        workspace_id=workspace.id,
        email="test@example.com",
        password_hash=hash_password("password123"),
        full_name="Test User",
        is_active=True,
        is_verified=True,
    )
    test_session.add(user)
    await test_session.commit()
    
    return {
        "id": user.id,
        "email": "test@example.com",
        "password": "password123",
        "workspace_id": workspace.id,
    }


class TestAuthRegisterE2E:
    """E2E tests for registration flow."""
    
    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration."""
        response = await client.post("/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "SecurePass123!",
            "full_name": "New User",
            "workspace_name": "My Workspace"
        })
        
        assert response.status_code == 201
        data = response.json()
        
        # Should return access and refresh tokens
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert "user" in data
        
        # User info should be correct
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["full_name"] == "New User"
        assert data["user"]["is_active"] is True
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user: dict):
        """Test registration with duplicate email returns 409."""
        response = await client.post("/v1/auth/register", json={
            "email": test_user["email"],
            "password": "AnotherPass123!",
            "full_name": "Another User"
        })
        
        assert response.status_code == 409
        assert "already registered" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email returns 422."""
        response = await client.post("/v1/auth/register", json={
            "email": "not-an-email",
            "password": "password123"
        })
        
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_register_short_password(self, client: AsyncClient):
        """Test registration with short password returns 422."""
        response = await client.post("/v1/auth/register", json={
            "email": "user@example.com",
            "password": "short"
        })
        
        assert response.status_code == 422


class TestAuthLoginE2E:
    """E2E tests for login flow."""
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user: dict):
        """Test successful login returns tokens and user info."""
        response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return tokens
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        
        # User info should match
        assert data["user"]["email"] == test_user["email"]
    
    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client: AsyncClient, test_user: dict):
        """Test login with wrong password returns 401."""
        response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent email returns 401."""
        response = await client.post("/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "anypassword"
        })
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_login_missing_fields(self, client: AsyncClient):
        """Test login with missing fields returns 422."""
        response = await client.post("/v1/auth/login", json={
            "email": "test@example.com"
        })
        
        assert response.status_code == 422


class TestAuthRefreshE2E:
    """E2E tests for token refresh flow."""
    
    @pytest.mark.asyncio
    async def test_refresh_success(self, client: AsyncClient, test_user: dict):
        """Test successful token refresh."""
        # First login to get refresh token
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh the token
        response = await client.post("/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return new tokens
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        
        # New tokens should be different
        assert data["access_token"] != login_response.json()["access_token"]
        assert data["refresh_token"] != refresh_token
    
    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, client: AsyncClient):
        """Test refresh with invalid token returns 401."""
        response = await client.post("/v1/auth/refresh", json={
            "refresh_token": "invalid.token.here"
        })
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_refresh_access_token_rejected(self, client: AsyncClient, test_user: dict):
        """Test that access token cannot be used for refresh."""
        # Login to get access token
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        access_token = login_response.json()["access_token"]
        
        # Try to use access token for refresh (should fail)
        response = await client.post("/v1/auth/refresh", json={
            "refresh_token": access_token
        })
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_refresh_token_rotation(self, client: AsyncClient, test_user: dict):
        """Test that old refresh token is revoked after rotation."""
        # Login to get first refresh token
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        old_refresh_token = login_response.json()["refresh_token"]
        
        # First refresh - should succeed
        refresh1 = await client.post("/v1/auth/refresh", json={
            "refresh_token": old_refresh_token
        })
        assert refresh1.status_code == 200
        
        # Try to use old token again - should fail (rotation)
        refresh2 = await client.post("/v1/auth/refresh", json={
            "refresh_token": old_refresh_token
        })
        assert refresh2.status_code == 401


class TestAuthLogoutE2E:
    """E2E tests for logout flow."""
    
    @pytest.mark.asyncio
    async def test_logout_success(self, client: AsyncClient, test_user: dict):
        """Test successful logout revokes refresh token."""
        # Login to get tokens
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout with auth header
        response = await client.post(
            "/v1/auth/logout",
            json={"refresh_token": refresh_token},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        assert "logged out" in response.json()["message"].lower()
        
        # Try to use revoked refresh token - should fail
        refresh_response = await client.post("/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert refresh_response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_logout_requires_auth(self, client: AsyncClient):
        """Test logout requires authentication."""
        response = await client.post("/v1/auth/logout", json={
            "refresh_token": "sometoken"
        })
        
        assert response.status_code in [401, 403]
    
    @pytest.mark.asyncio
    async def test_logout_all_tokens(self, client: AsyncClient, test_user: dict):
        """Test logout without token revokes all user tokens."""
        # Login twice to get multiple tokens
        login1 = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        access1 = login1.json()["access_token"]
        refresh1 = login1.json()["refresh_token"]
        
        login2 = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        refresh2 = login2.json()["refresh_token"]
        
        # Logout without specifying token (should revoke all)
        response = await client.post(
            "/v1/auth/logout",
            json={},
            headers={"Authorization": f"Bearer {access1}"}
        )
        
        assert response.status_code == 200
        
        # Both refresh tokens should now be revoked
        refresh1_response = await client.post("/v1/auth/refresh", json={
            "refresh_token": refresh1
        })
        refresh2_response = await client.post("/v1/auth/refresh", json={
            "refresh_token": refresh2
        })
        
        assert refresh1_response.status_code == 401
        assert refresh2_response.status_code == 401


class TestProtectedRoutesE2E:
    """E2E tests for protected route access."""
    
    @pytest.mark.asyncio
    async def test_me_endpoint_with_valid_token(self, client: AsyncClient, test_user: dict):
        """Test /me endpoint returns user info with valid token."""
        # Login
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        access_token = login_response.json()["access_token"]
        
        # Get current user
        response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]
    
    @pytest.mark.asyncio
    async def test_me_endpoint_without_token(self, client: AsyncClient):
        """Test /me endpoint rejects request without token."""
        response = await client.get("/v1/auth/me")
        
        assert response.status_code in [401, 403]
    
    @pytest.mark.asyncio
    async def test_me_endpoint_with_invalid_token(self, client: AsyncClient):
        """Test /me endpoint rejects invalid token."""
        response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_me_endpoint_with_expired_token(self, client: AsyncClient, test_user: dict):
        """Test /me endpoint rejects expired token."""
        # Create expired token manually
        expired_delta = timedelta(hours=-1)
        expired_token = create_access_token(
            subject=test_user["id"],
            workspace_id=test_user["workspace_id"],
            email=test_user["email"],
            expires_delta=expired_delta
        )
        
        response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_me_endpoint_with_refresh_token_rejected(self, client: AsyncClient, test_user: dict):
        """Test that refresh token cannot access protected routes."""
        # Login to get refresh token
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        refresh_token = login_response.json()["refresh_token"]
        
        # Try to access /me with refresh token
        response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        
        assert response.status_code == 401


class TestTokenExpirationE2E:
    """E2E tests for token expiration handling."""
    
    @pytest.mark.asyncio
    async def test_access_token_expires(self, client: AsyncClient, test_user: dict):
        """Test that access token expires after configured time."""
        # Create token with very short expiration
        short_delta = timedelta(seconds=1)
        token = create_access_token(
            subject=test_user["id"],
            workspace_id=test_user["workspace_id"],
            email=test_user["email"],
            expires_delta=short_delta
        )
        
        # Should work immediately
        response1 = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response1.status_code == 200
        
        # Wait for expiration
        await asyncio.sleep(2)
        
        # Should fail after expiration
        response2 = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response2.status_code == 401
    
    @pytest.mark.asyncio
    async def test_token_contains_correct_claims(self, client: AsyncClient, test_user: dict):
        """Test that token contains all required claims."""
        # Login
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        access_token = login_response.json()["access_token"]
        
        # Decode and verify claims
        from app.core.security import decode_token
        payload = decode_token(access_token)
        
        assert payload is not None
        assert payload["sub"] == test_user["id"]
        assert payload["workspace_id"] == test_user["workspace_id"]
        assert payload["email"] == test_user["email"]
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
        assert "jti" in payload


class TestErrorScenariosE2E:
    """E2E tests for error scenarios."""
    
    @pytest.mark.asyncio
    async def test_malformed_authorization_header(self, client: AsyncClient):
        """Test malformed authorization header returns 401 or 403."""
        response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": "InvalidFormat token"}
        )
        
        # Either 401 (unauthenticated) or 403 (forbidden) is acceptable
        assert response.status_code in [401, 403]
    
    @pytest.mark.asyncio
    async def test_missing_authorization_header(self, client: AsyncClient):
        """Test missing authorization header returns 401."""
        response = await client.get("/v1/auth/me")
        
        assert response.status_code in [401, 403]
    
    @pytest.mark.asyncio
    async def test_empty_authorization_header(self, client: AsyncClient):
        """Test empty authorization header returns 401."""
        response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": ""}
        )
        
        assert response.status_code in [401, 403]
    
    @pytest.mark.asyncio
    async def test_wrong_token_type_in_refresh(self, client: AsyncClient, test_user: dict):
        """Test using wrong token type for refresh returns 401."""
        # Login to get access token
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        access_token = login_response.json()["access_token"]
        
        # Try to refresh with access token (wrong type)
        response = await client.post("/v1/auth/refresh", json={
            "refresh_token": access_token
        })
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_inactive_user_login_rejected(self, client: AsyncClient, test_session: AsyncSession):
        """Test that inactive user cannot login."""
        from app.core.security import hash_password
        
        # Create inactive user
        workspace = Workspace(name="Test", slug="test", tier="pro")
        test_session.add(workspace)
        await test_session.flush()
        
        user = User(
            workspace_id=workspace.id,
            email="inactive@example.com",
            password_hash=hash_password("password123"),
            is_active=False,
            is_verified=True,
        )
        test_session.add(user)
        await test_session.commit()
        
        # Try to login
        response = await client.post("/v1/auth/login", json={
            "email": "inactive@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_concurrent_token_refresh(self, client: AsyncClient, test_user: dict):
        """Test sequential refresh with same token (second should fail after rotation)."""
        # Login to get refresh token
        login_response = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        refresh_token = login_response.json()["refresh_token"]
        
        # First refresh should succeed
        response1 = await client.post("/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert response1.status_code == 200
        
        # Second refresh with same token should fail (rotation)
        response2 = await client.post("/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert response2.status_code == 401


class TestAuthFlowIntegration:
    """Full auth flow integration tests."""
    
    @pytest.mark.asyncio
    async def test_full_auth_flow(self, client: AsyncClient):
        """Test complete auth flow: register -> login -> me -> refresh -> logout."""
        # 1. Register new user
        register_response = await client.post("/v1/auth/register", json={
            "email": "flow@example.com",
            "password": "SecurePass123!",
            "full_name": "Flow User"
        })
        assert register_response.status_code == 201
        access_token = register_response.json()["access_token"]
        refresh_token = register_response.json()["refresh_token"]
        
        # 2. Access protected route
        me_response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "flow@example.com"
        
        # 3. Refresh token
        refresh_response = await client.post("/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert refresh_response.status_code == 200
        new_access_token = refresh_response.json()["access_token"]
        new_refresh_token = refresh_response.json()["refresh_token"]
        
        # 4. Access protected route with new token
        me_response2 = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {new_access_token}"}
        )
        assert me_response2.status_code == 200
        
        # 5. Logout
        logout_response = await client.post(
            "/v1/auth/logout",
            json={"refresh_token": new_refresh_token},
            headers={"Authorization": f"Bearer {new_access_token}"}
        )
        assert logout_response.status_code == 200
        
        # 6. Verify refresh token is revoked
        refresh_after_logout = await client.post("/v1/auth/refresh", json={
            "refresh_token": new_refresh_token
        })
        assert refresh_after_logout.status_code == 401
    
    @pytest.mark.asyncio
    async def test_login_logout_login_cycle(self, client: AsyncClient, test_user: dict):
        """Test login -> logout -> login cycle works correctly."""
        # First login
        login1 = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        assert login1.status_code == 200
        access1 = login1.json()["access_token"]
        refresh1 = login1.json()["refresh_token"]
        
        # Logout
        logout = await client.post(
            "/v1/auth/logout",
            json={"refresh_token": refresh1},
            headers={"Authorization": f"Bearer {access1}"}
        )
        assert logout.status_code == 200
        
        # Login again
        login2 = await client.post("/v1/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        assert login2.status_code == 200
        access2 = login2.json()["access_token"]
        refresh2 = login2.json()["refresh_token"]
        
        # New tokens should be different
        assert access2 != access1
        assert refresh2 != refresh1
        
        # New tokens should work
        me_response = await client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {access2}"}
        )
        assert me_response.status_code == 200
