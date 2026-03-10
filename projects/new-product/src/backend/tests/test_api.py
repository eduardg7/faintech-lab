"""Tests for health check endpoint."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """Test health check endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data
    assert "dependencies" in data


def test_root_endpoint():
    """Test root endpoint returns app info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data


def test_api_docs():
    """Test API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
