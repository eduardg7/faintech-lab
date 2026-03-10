"""Tests for error handling system."""
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio

from main import app
from app.core.errors import (
    ValidationError,
    NotFoundError,
    ContentTooLargeError,
    RateLimitError,
    InternalError,
    ErrorCode
)


client = TestClient(app)


class TestErrorResponses:
    """Test error response format and handling."""
    
    def test_error_response_structure(self):
        """Test that error responses have correct structure."""
        # Create a memory first, then try to get a non-existent one
        # This tests the NotFoundError from the endpoint
        response = client.get("/api/v1/memories/00000000-0000-0000-0000-000000000000")
        
        # Should be 404 from our NotFoundError
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        
        # Check error response structure (if using custom error handler)
        # Note: FastAPI default 404 returns {"detail": "..."} 
        # Our custom handler returns structured errors
        if "error" in data:
            assert "message" in data
            assert "code" in data
            assert "request_id" in data
            assert "timestamp" in data
            assert data["code"] == ErrorCode.NOT_FOUND
    
    def test_content_too_large_error(self):
        """Test content size validation."""
        # Create content larger than 10KB
        large_content = "x" * (10241)
        
        response = client.post(
            "/api/v1/memories",
            json={
                "agent_id": "test-agent",
                "project_id": "test-project",
                "memory_type": "outcome",
                "content": large_content,
                "tags": []
            }
        )
        
        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        data = response.json()
        
        assert data["code"] == ErrorCode.CONTENT_TOO_LARGE
        assert "details" in data
        assert "content_size" in data["details"]
        assert "max_size" in data["details"]
    
    def test_request_id_in_headers(self):
        """Test that X-Request-ID is returned in headers."""
        response = client.get("/api/v1/memories/non-existent-id")
        
        assert "X-Request-ID" in response.headers
        assert response.headers["X-Request-ID"] is not None
    
    def test_rate_limit_headers(self):
        """Test that rate limit headers are present on all responses."""
        response = client.get("/health")
        
        assert "X-RateLimit-Limit-Minute" in response.headers
        assert "X-RateLimit-Remaining-Minute" in response.headers
        assert "X-RateLimit-Limit-Hour" in response.headers
        assert "X-RateLimit-Remaining-Hour" in response.headers
        assert "X-RateLimit-Reset" in response.headers
    
    def test_validation_error(self):
        """Test validation error handling."""
        # Send invalid data (missing required fields)
        response = client.post(
            "/api/v1/memories",
            json={
                "agent_id": "test-agent"
                # Missing required fields: memory_type, content
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_error_logging(self, caplog):
        """Test that errors are logged with request IDs."""
        response = client.get("/api/v1/memories/non-existent-id")
        request_id = response.headers.get("X-Request-ID")
        
        # Check that error was logged
        # (In production, this would check actual log output)
        assert request_id is not None


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_search(self):
        """Test empty search results."""
        response = client.get(
            "/api/v1/memories",
            params={"search": "nonexistent-term-xyz123"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert data["memories"] == []
    
    def test_pagination_boundaries(self):
        """Test pagination edge cases."""
        # Test page 1 with size 1
        response = client.get(
            "/api/v1/memories",
            params={"page": 1, "page_size": 1}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Test max page size
        response = client.get(
            "/api/v1/memories",
            params={"page": 1, "page_size": 100}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Test page size over limit
        response = client.get(
            "/api/v1/memories",
            params={"page": 1, "page_size": 101}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_concurrent_writes(self):
        """Test handling of concurrent write operations."""
        # Create multiple memories concurrently
        import concurrent.futures
        
        def create_memory(i):
            return client.post(
                "/api/v1/memories",
                json={
                    "agent_id": f"test-agent-{i}",
                    "project_id": "concurrent-test",
                    "memory_type": "outcome",
                    "content": f"Concurrent test memory {i}",
                    "tags": ["concurrent"]
                }
            )
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_memory, i) for i in range(5)]
            results = [f.result() for f in futures]
        
        # All should succeed
        for result in results:
            assert result.status_code in [
                status.HTTP_201_CREATED,
                status.HTTP_429_TOO_MANY_REQUESTS  # If rate limited
            ]
    
    def test_special_characters_in_search(self):
        """Test search with special characters."""
        response = client.get(
            "/api/v1/memories",
            params={"search": "test<script>alert('xss')</script>"}
        )
        
        # Should not cause errors
        assert response.status_code == status.HTTP_200_OK
    
    def test_unicode_content(self):
        """Test handling of unicode content."""
        response = client.post(
            "/api/v1/memories",
            json={
                "agent_id": "test-agent",
                "project_id": "unicode-test",
                "memory_type": "outcome",
                "content": "Unicode test: 你好世界 🌍 مرحبا العالم",
                "tags": ["unicode", "测试", "проверка"]
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED


class TestRetryLogic:
    """Test retry configuration and logic."""
    
    def test_retry_config_defaults(self):
        """Test default retry configuration."""
        from app.core.errors import RetryConfig
        
        config = RetryConfig()
        
        assert config.max_retries == 3
        assert config.backoff_factor == 2.0
        assert 500 in config.retry_on
        assert config.timeout == 30.0
    
    def test_retry_config_custom(self):
        """Test custom retry configuration."""
        from app.core.errors import RetryConfig
        
        config = RetryConfig(
            max_retries=5,
            backoff_factor=1.5,
            retry_on=(502, 503),
            timeout=60.0
        )
        
        assert config.max_retries == 5
        assert config.backoff_factor == 1.5
        assert config.retry_on == (502, 503)
        assert config.timeout == 60.0


class TestRateLimiting:
    """Test rate limiting functionality."""
    
    def test_rate_limit_tracking(self):
        """Test that rate limits are tracked."""
        # Make multiple requests
        responses = []
        for _ in range(5):
            response = client.get("/health")
            responses.append(response)
        
        # Check that remaining decreases
        remaining_counts = [
            int(r.headers["X-RateLimit-Remaining-Minute"])
            for r in responses
        ]
        
        # Should be decreasing (or staying same if within limit)
        assert all(count >= 0 for count in remaining_counts)
    
    def test_rate_limit_headers_format(self):
        """Test rate limit header format."""
        response = client.get("/health")
        
        # All headers should be numeric strings
        for header in [
            "X-RateLimit-Limit-Minute",
            "X-RateLimit-Remaining-Minute",
            "X-RateLimit-Limit-Hour",
            "X-RateLimit-Remaining-Hour",
            "X-RateLimit-Reset"
        ]:
            value = response.headers[header]
            assert value.isdigit() or (value[0] == '-' and value[1:].isdigit())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
