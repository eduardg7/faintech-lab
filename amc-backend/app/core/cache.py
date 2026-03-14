"""Redis caching layer for search optimization."""
import json
import hashlib
from typing import Optional, Any, List
from datetime import timedelta
import redis.asyncio as redis
from pydantic import BaseModel

from config import settings


class CacheConfig:
    """Cache configuration."""
    # TTL for different cache types
    SEARCH_RESULTS_TTL = 300  # 5 minutes
    EMBEDDING_TTL = 3600  # 1 hour
    MEMORY_TTL = 600  # 10 minutes

    # Cache key prefixes
    SEARCH_PREFIX = "search:"
    EMBEDDING_PREFIX = "embed:"
    MEMORY_PREFIX = "memory:"


class CacheService:
    """Redis-based caching service."""

    def __init__(self):
        self._client: Optional[redis.Redis] = None
        self._enabled = bool(getattr(settings, 'redis_url', None))

    async def connect(self) -> None:
        """Connect to Redis."""
        if not self._enabled:
            return

        redis_url = getattr(settings, 'redis_url', 'redis://localhost:6379/0')
        self._client = redis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True
        )

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()
            self._client = None

    @property
    def is_connected(self) -> bool:
        """Check if Redis is connected."""
        return self._client is not None

    def _generate_cache_key(self, prefix: str, *args) -> str:
        """Generate a cache key from arguments."""
        key_parts = [str(arg) for arg in args if arg is not None]
        key_string = ":".join(key_parts)
        key_hash = hashlib.sha256(key_string.encode()).hexdigest()[:16]
        return f"{prefix}{key_hash}"

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.is_connected:
            return None

        try:
            value = await self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception:
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 300
    ) -> bool:
        """Set value in cache with TTL."""
        if not self.is_connected:
            return False

        try:
            serialized = json.dumps(value, default=str)
            await self._client.setex(key, ttl, serialized)
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.is_connected:
            return False

        try:
            await self._client.delete(key)
            return True
        except Exception:
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        if not self.is_connected:
            return 0

        try:
            keys = await self._client.keys(pattern)
            if keys:
                return await self._client.delete(*keys)
            return 0
        except Exception:
            return 0

    async def get_or_compute(
        self,
        key: str,
        compute_fn,
        ttl: int = 300
    ) -> Any:
        """Get from cache or compute and cache result."""
        cached = await self.get(key)
        if cached is not None:
            return cached

        result = await compute_fn()
        await self.set(key, result, ttl)
        return result

    # Search-specific methods

    async def get_search_results(
        self,
        query: str,
        agent_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Optional[dict]:
        """Get cached search results."""
        key = self._generate_cache_key(
            CacheConfig.SEARCH_PREFIX,
            "keyword",
            query,
            agent_id,
            project_id,
            tags,
            page,
            page_size
        )
        return await self.get(key)

    async def set_search_results(
        self,
        query: str,
        agent_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        results: dict = None
    ) -> bool:
        """Cache search results."""
        key = self._generate_cache_key(
            CacheConfig.SEARCH_PREFIX,
            "keyword",
            query,
            agent_id,
            project_id,
            tags,
            page,
            page_size
        )
        return await self.set(key, results, CacheConfig.SEARCH_RESULTS_TTL)

    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get cached embedding for text."""
        key = self._generate_cache_key(
            CacheConfig.EMBEDDING_PREFIX,
            text[:100]  # Use first 100 chars for key
        )
        return await self.get(key)

    async def set_embedding(self, text: str, embedding: List[float]) -> bool:
        """Cache embedding for text."""
        key = self._generate_cache_key(
            CacheConfig.EMBEDDING_PREFIX,
            text[:100]
        )
        return await self.set(key, embedding, CacheConfig.EMBEDDING_TTL)

    async def invalidate_memory_cache(self, memory_id: str) -> int:
        """Invalidate all cache entries for a memory."""
        return await self.delete_pattern(f"{CacheConfig.MEMORY_PREFIX}*{memory_id}*")


# Global cache service instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get or create cache service instance."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service


async def init_cache() -> None:
    """Initialize cache connection."""
    cache = get_cache_service()
    await cache.connect()


async def close_cache() -> None:
    """Close cache connection."""
    cache = get_cache_service()
    await cache.disconnect()
