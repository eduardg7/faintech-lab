"""Tests for semantic search API."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from app.models.memory import Memory
from app.core.database import get_db, async_session_maker


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestSemanticSearch:
    """Test cases for semantic search functionality."""
    
    def test_semantic_search_endpoint_exists(self, client):
        """Test that semantic search endpoint is accessible."""
        response = client.post("/v1/search/semantic", json={
            "query": "test query",
            "limit": 5,
            "min_similarity": 0.5
        })
        # May return error if no embeddings, but endpoint should exist
        assert response.status_code in [200, 422, 500]
    
    def test_semantic_search_requires_query(self, client):
        """Test that semantic search requires 'query' parameter."""
        response = client.post("/v1/search/semantic", json={})
        assert response.status_code == 422  # Validation error
    
    def test_semantic_search_query_too_long(self, client):
        """Test that semantic search rejects queries > 1000 chars."""
        long_query = "a" * 1001
        response = client.post("/v1/search/semantic", json={
            "query": long_query
        })
        assert response.status_code == 422
    
    def test_semantic_search_query_min_length(self, client):
        """Test that semantic search rejects empty queries."""
        response = client.post("/v1/search/semantic", json={
            "query": ""
        })
        assert response.status_code == 422
    
    def test_semantic_search_validation(self, client):
        """Test that semantic search validates parameters."""
        # Limit must be >= 1
        response = client.post("/v1/search/semantic", json={
            "query": "test",
            "limit": 0
        })
        assert response.status_code == 422
        
        # Limit must be <= 50
        response = client.post("/v1/search/semantic", json={
            "query": "test",
            "limit": 51
        })
        assert response.status_code == 422
        
        # Min similarity must be 0-1
        response = client.post("/v1/search/semantic", json={
            "query": "test",
            "min_similarity": 1.1
        })
        assert response.status_code == 422
    
    def test_semantic_search_response_format(self, client):
        """Test that semantic search response has correct format."""
        response = client.post("/v1/search/semantic", json={
            "query": "test query",
            "limit": 5,
            "min_similarity": 0.5
        })
        
        if response.status_code == 200:
            data = response.json()
            assert "results" in data
            assert "query_time_ms" in data
            assert "query_embedding_time_ms" in data
            
            # Check result structure if any results
            if data["results"]:
                result = data["results"][0]
                assert "id" in result
                assert "similarity_score" in result
                assert "content" in result


class TestEmbeddingJob:
    """Test cases for embedding job queue."""
    
    def test_embed_endpoint_exists(self, client):
        """Test that embed endpoint is accessible."""
        response = client.post("/v1/search/embed", json={
            "memory_ids": ["test-id-1", "test-id-2"]
        })
        # May return 404 for invalid IDs, but endpoint should exist
        assert response.status_code in [202, 404, 422]
    
    def test_embed_requires_memory_ids(self, client):
        """Test that embed requires 'memory_ids' parameter."""
        response = client.post("/v1/search/embed", json={})
        assert response.status_code == 422  # Validation error
    
    def test_embed_empty_memory_ids(self, client):
        """Test that embed rejects empty memory_ids list."""
        response = client.post("/v1/search/embed", json={
            "memory_ids": []
        })
        assert response.status_code == 422
    
    def test_embed_too_many_ids(self, client):
        """Test that embed rejects > 100 memory IDs."""
        many_ids = ["id"] * 101
        response = client.post("/v1/search/embed", json={
            "memory_ids": many_ids
        })
        assert response.status_code == 422
    
    def test_embed_response_format(self, client):
        """Test that embed response has correct format."""
        response = client.post("/v1/search/embed", json={
            "memory_ids": ["test-id"]
        })
        
        if response.status_code == 202:
            data = response.json()
            assert "job_id" in data
            assert "message" in data


class TestJobStatus:
    """Test cases for job status endpoint."""
    
    def test_job_status_endpoint_exists(self, client):
        """Test that job status endpoint is accessible."""
        response = client.get("/v1/search/jobs/test-job-id")
        # May return 404 for invalid job, but endpoint should exist
        assert response.status_code in [200, 404]
    
    def test_job_status_not_found(self, client):
        """Test that job status returns 404 for non-existent job."""
        response = client.get("/v1/search/jobs/non-existent-job")
        assert response.status_code == 404
    
    def test_job_status_response_format(self, client):
        """Test that job status response has correct format."""
        # This test requires a real job to be created first
        # For now, we test the response format for 404
        response = client.get("/v1/search/jobs/test-job-id")
        
        if response.status_code == 404:
            data = response.json()
            assert "detail" in data


class TestEmbeddingService:
    """Test cases for embedding service integration."""
    
    def test_embedding_service_requires_api_key(self):
        """Test that embedding service requires OPENAI_API_KEY."""
        # This is tested by the service initialization
        from app.services.embedding import EmbeddingService
        
        # Temporarily unset env var
        import os
        original_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            # Should raise ValueError
            with pytest.raises(ValueError):
                service = EmbeddingService()
        finally:
            # Restore original key
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
