"""Tests for authentication middleware."""
import pytest
from app.middleware.auth import hash_api_key


def test_hash_api_key():
    """Test API key hashing."""
    api_key = "test-api-key-12345"
    hashed = hash_api_key(api_key)
    
    # Should return a SHA256 hash (64 characters)
    assert len(hashed) == 64
    
    # Same input should produce same hash
    hashed2 = hash_api_key(api_key)
    assert hashed == hashed2
    
    # Different input should produce different hash
    different_key = "different-api-key"
    hashed3 = hash_api_key(different_key)
    assert hashed != hashed3
