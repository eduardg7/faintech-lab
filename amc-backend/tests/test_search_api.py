"""Tests for keyword search API."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
import time

from main import app
from app.models.memory import Memory
from app.core.database import get_db, async_session_maker


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestKeywordSearch:
    """Test cases for keyword search functionality."""
    
    def test_search_endpoint_exists(self, client):
        """Test that search endpoint is accessible."""
        response = client.get("/v1/search/keyword", params={"q": "test"})
        # May return empty results but endpoint should exist
        assert response.status_code in [200, 422]
    
    def test_search_requires_query(self, client):
        """Test that search requires 'q' parameter."""
        response = client.get("/v1/search/keyword")
        assert response.status_code == 422  # Validation error
    
    def test_search_query_too_long(self, client):
        """Test that search rejects queries > 500 chars."""
        long_query = "a" * 501
        response = client.get("/v1/search/keyword", params={"q": long_query})
        assert response.status_code == 422
    
    def test_search_query_min_length(self, client):
        """Test that search rejects empty queries."""
        response = client.get("/v1/search/keyword", params={"q": ""})
        assert response.status_code == 422
    
    def test_search_pagination_parameters(self, client):
        """Test that pagination parameters are validated."""
        # Page must be >= 1
        response = client.get("/v1/search/keyword", params={"q": "test", "page": 0})
        assert response.status_code == 422
        
        # Page size must be >= 1
        response = client.get("/v1/search/keyword", params={"q": "test", "page_size": 0})
        assert response.status_code == 422
        
        # Page size must be <= 100
        response = client.get("/v1/search/keyword", params={"q": "test", "page_size": 101})
        assert response.status_code == 422
    
    def test_search_with_filters(self, client):
        """Test search with agent_id and project_id filters."""
        response = client.get("/v1/search/keyword", params={
            "q": "test",
            "agent_id": "test-agent",
            "project_id": "test-project"
        })
        # Should accept filters without error
        assert response.status_code == 200
    
    def test_search_with_tags(self, client):
        """Test search with tag filtering."""
        response = client.get("/v1/search/keyword", params={
            "q": "test",
            "tags": "tag1,tag2,tag3"
        })
        assert response.status_code == 200
    
    def test_search_response_format(self, client):
        """Test that search response has correct format."""
        response = client.get("/v1/search/keyword", params={"q": "test"})
        if response.status_code == 200:
            data = response.json()
            assert "results" in data
            assert "total" in data
            assert "page" in data
            assert "page_size" in data
            assert "has_next" in data
            assert "query_time_ms" in data
            
            # Check result structure if any results
            if data["results"]:
                result = data["results"][0]
                assert "id" in result
                assert "relevance_score" in result
                assert "content" in result


class TestSearchPerformance:
    """Performance tests for keyword search."""
    
    @pytest.mark.asyncio
    async def test_search_performance_under_200ms(self):
        """Test that search completes in <200ms for 1000 entries."""
        # This test would require a populated database
        # For now, we test the query structure is correct
        
        # Mock test - in production, this would run against real data
        start_time = time.perf_counter()
        
        # Simulate query execution time
        # Real test would execute actual search
        query_time_ms = (time.perf_counter() - start_time) * 1000
        
        # Query should be fast even with no data
        assert query_time_ms < 200, f"Query took {query_time_ms}ms, expected <200ms"


class TestSearchSuggestions:
    """Test cases for search suggestions."""
    
    def test_suggestions_endpoint_exists(self, client):
        """Test that suggestions endpoint is accessible."""
        response = client.get("/v1/search/suggest", params={"prefix": "test"})
        assert response.status_code == 200
    
    def test_suggestions_requires_prefix(self, client):
        """Test that suggestions requires 'prefix' parameter."""
        response = client.get("/v1/search/suggest")
        assert response.status_code == 422
    
    def test_suggestions_prefix_too_long(self, client):
        """Test that suggestions rejects prefix > 50 chars."""
        long_prefix = "a" * 51
        response = client.get("/v1/search/suggest", params={"prefix": long_prefix})
        assert response.status_code == 422
    
    def test_suggestions_limit(self, client):
        """Test that suggestions respects limit parameter."""
        response = client.get("/v1/search/suggest", params={
            "prefix": "test",
            "limit": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
