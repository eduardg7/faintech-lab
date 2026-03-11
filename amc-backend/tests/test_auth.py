"""Unit tests for JWT authentication."""
import pytest
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token,
    TokenData,
)
from app.models.user import User, RefreshToken
from app.models.workspace import Workspace
from app.core.database import Base


class TestPasswordHashing:
    """Tests for password hashing functions."""

    def test_hash_password_returns_hash(self):
        """Test that hash_password returns a hash string."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed != password
        assert len(hashed) > 0

    def test_hash_password_creates_different_hashes(self):
        """Test that same password creates different hashes (bcrypt salt)."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test verify_password with correct password."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verify_password with incorrect password."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password("wrongpassword", hashed) is False

    def test_verify_password_empty(self):
        """Test verify_password with empty password."""
        password = "testpassword123"
        hashed = hash_password(password)

        assert verify_password("", hashed) is False


class TestAccessToken:
    """Tests for access token creation and verification."""

    def test_create_access_token_returns_string(self):
        """Test that create_access_token returns a string."""
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com"
        )

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_contains_claims(self):
        """Test that access token contains expected claims."""
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com"
        )

        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["workspace_id"] == "workspace-456"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
        assert "jti" in payload

    def test_create_access_token_custom_expiry(self):
        """Test access token with custom expiration."""
        custom_delta = timedelta(hours=1)
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com",
            expires_delta=custom_delta
        )

        payload = decode_token(token)
        assert payload is not None

        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)

        # Should expire in about 1 hour
        assert (exp - now).total_seconds() > 3500  # ~58 minutes
        assert (exp - now).total_seconds() < 3700  # ~62 minutes

    def test_create_access_token_additional_claims(self):
        """Test access token with additional claims."""
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com",
            additional_claims={"role": "admin", "permissions": ["read", "write"]}
        )

        payload = decode_token(token)

        assert payload["role"] == "admin"
        assert payload["permissions"] == ["read", "write"]


class TestRefreshToken:
    """Tests for refresh token creation."""

    def test_create_refresh_token_returns_tuple(self):
        """Test that create_refresh_token returns (token, hash, expires_at)."""
        result = create_refresh_token(
            subject="user-123",
            workspace_id="workspace-456"
        )

        assert len(result) == 3
        token, token_hash, expires_at = result

        assert isinstance(token, str)
        assert isinstance(token_hash, str)
        assert isinstance(expires_at, datetime)
        assert expires_at.tzinfo is None

    def test_create_refresh_token_contains_claims(self):
        """Test that refresh token contains expected claims."""
        token, _, _ = create_refresh_token(
            subject="user-123",
            workspace_id="workspace-456"
        )

        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["workspace_id"] == "workspace-456"
        assert payload["type"] == "refresh"

    def test_refresh_token_hash_is_sha256(self):
        """Test that token hash is SHA-256 format (64 hex chars)."""
        token, token_hash, _ = create_refresh_token(
            subject="user-123",
            workspace_id="workspace-456"
        )

        assert len(token_hash) == 64
        assert all(c in "0123456789abcdef" for c in token_hash)


class TestTokenVerification:
    """Tests for token verification."""

    def test_verify_access_token_valid(self):
        """Test verifying a valid access token."""
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com"
        )

        payload = verify_token(token, expected_type="access")

        assert payload is not None
        assert payload["sub"] == "user-123"

    def test_verify_token_wrong_type(self):
        """Test that verify_token rejects wrong token type."""
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com"
        )

        # Try to verify access token as refresh token
        payload = verify_token(token, expected_type="refresh")

        assert payload is None

    def test_verify_token_invalid(self):
        """Test that verify_token rejects invalid token."""
        payload = verify_token("invalid.token.here", expected_type="access")

        assert payload is None

    def test_verify_token_expired(self):
        """Test that verify_token rejects expired token."""
        # Create token that expired 1 hour ago
        expired_delta = timedelta(hours=-1)
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com",
            expires_delta=expired_delta
        )

        payload = verify_token(token, expected_type="access")

        assert payload is None


class TestTokenData:
    """Tests for TokenData class."""

    def test_token_data_from_valid_token(self):
        """Test creating TokenData from valid token."""
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com"
        )

        token_data = TokenData.from_token(token, expected_type="access")

        assert token_data is not None
        assert token_data.user_id == "user-123"
        assert token_data.workspace_id == "workspace-456"
        assert token_data.email == "test@example.com"
        assert token_data.token_type == "access"

    def test_token_data_from_invalid_token(self):
        """Test creating TokenData from invalid token returns None."""
        token_data = TokenData.from_token("invalid.token", expected_type="access")

        assert token_data is None

    def test_token_data_repr(self):
        """Test TokenData string representation."""
        token = create_access_token(
            subject="user-123",
            workspace_id="workspace-456",
            email="test@example.com"
        )

        token_data = TokenData.from_token(token, expected_type="access")

        repr_str = repr(token_data)

        assert "user-123" in repr_str
        assert "workspace-456" in repr_str


class TestAuthEndpoints:
    """Integration tests for auth API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        from main import app
        return TestClient(app)

    def test_register_endpoint_exists(self, client):
        """Test that /v1/auth/register endpoint exists."""
        response = client.post("/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "password123"
        })

        # Should not return 404
        assert response.status_code != 404

    def test_login_endpoint_exists(self, client):
        """Test that /v1/auth/login endpoint exists."""
        response = client.post("/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })

        # Should not return 404
        assert response.status_code != 404

    def test_refresh_endpoint_exists(self, client):
        """Test that /v1/auth/refresh endpoint exists."""
        response = client.post("/v1/auth/refresh", json={
            "refresh_token": "some.token.here"
        })

        # Should not return 404
        assert response.status_code != 404

    def test_me_endpoint_requires_auth(self, client):
        """Test that /v1/auth/me requires authentication."""
        response = client.get("/v1/auth/me")

        # Should return 401 or 403
        assert response.status_code in [401, 403]
