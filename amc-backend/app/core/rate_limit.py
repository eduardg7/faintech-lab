"""Rate limiting middleware for AMC API with Redis backend support."""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple, Optional
import time
import os
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# Optional Redis support
redis_client: Optional[object] = None
REDIS_AVAILABLE = False

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    logger.info("Redis package not installed, using in-memory rate limiting")


async def get_redis_client():
    """Get or create Redis client singleton."""
    global redis_client, REDIS_AVAILABLE

    if not REDIS_AVAILABLE:
        return None

    if redis_client is not None:
        return redis_client

    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        logger.info("REDIS_URL not set, using in-memory rate limiting")
        REDIS_AVAILABLE = False
        return None

    try:
        redis_client = redis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True
        )
        # Test connection
        await redis_client.ping()
        logger.info(f"Redis connected successfully for rate limiting")
        return redis_client
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e}. Falling back to in-memory.")
        REDIS_AVAILABLE = False
        redis_client = None
        return None


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to add rate limit headers with Redis or in-memory backend."""

    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour

        # In-memory rate limit tracking (fallback when Redis unavailable)
        self.minute_tracker: Dict[str, list] = defaultdict(list)
        self.hour_tracker: Dict[str, list] = defaultdict(list)

        # Redis client (lazy initialized)
        self._redis: Optional[redis.Redis] = None
        self._redis_checked = False

    async def _get_redis(self):
        """Lazy initialization of Redis client."""
        if not self._redis_checked:
            self._redis = await get_redis_client()
            self._redis_checked = True
        return self._redis

    async def dispatch(self, request: Request, call_next):
        # Get client identifier (API key or IP)
        client_id = self._get_client_id(request)

        # Check rate limits
        minute_count, minute_remaining = await self._check_rate_limit(
            client_id,
            self.minute_tracker,
            60,
            self.requests_per_minute,
            "minute"
        )

        hour_count, hour_remaining = await self._check_rate_limit(
            client_id,
            self.hour_tracker,
            3600,
            self.requests_per_hour,
            "hour"
        )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(minute_remaining)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(hour_remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + 60))

        return response

    def _get_client_id(self, request: Request) -> str:
        """Get client identifier from request."""
        # Try API key header first
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"apikey:{api_key[:16]}"  # Use first 16 chars

        # Fall back to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0].strip()}"

        return f"ip:{request.client.host if request.client else 'unknown'}"

    async def _check_rate_limit(
        self,
        client_id: str,
        tracker: Dict[str, list],
        window_seconds: int,
        limit: int,
        window_name: str
    ) -> Tuple[int, int]:
        """Check and update rate limit using Redis sliding window or in-memory fallback."""
        redis = await self._get_redis()

        if redis:
            return await self._check_rate_limit_redis(
                client_id, window_seconds, limit, window_name
            )
        else:
            return self._check_rate_limit_memory(
                client_id, tracker, window_seconds, limit
            )

    async def _check_rate_limit_redis(
        self,
        client_id: str,
        window_seconds: int,
        limit: int,
        window_name: str
    ) -> Tuple[int, int]:
        """
        Check rate limit using Redis sliding window algorithm.

        Uses Redis sorted sets for efficient sliding window:
        - Score = timestamp of request
        - Member = unique request ID

        This provides O(log N) complexity per request.
        """
        now = time.time()
        window_start = now - window_seconds
        key = f"ratelimit:{window_name}:{client_id}"

        try:
            # Remove old entries outside the window (atomic with Lua script)
            lua_script = """
            local key = KEYS[1]
            local window_start = tonumber(ARGV[1])
            local now = tonumber(ARGV[2])
            local limit = tonumber(ARGV[3])
            local member = ARGV[4]

            -- Remove old entries
            redis.call('ZREMRANGEBYSCORE', key, '-inf', window_start)

            -- Count current entries
            local count = redis.call('ZCARD', key)

            -- Add new entry if under limit
            if count < limit then
                redis.call('ZADD', key, now, member)
                redis.call('EXPIRE', key, math.ceil(ARGV[5]))
                return {count + 1, limit - count - 1}
            else
                return {count, 0}
            end
            """

            # Generate unique member for this request
            member = f"{now}:{os.urandom(8).hex()}"

            # Execute Lua script atomically
            result = await self._redis.eval(
                lua_script,
                1,
                key,
                window_start,
                now,
                limit,
                member,
                window_seconds
            )

            count = int(result[0])
            remaining = int(result[1])

            return count, remaining

        except Exception as e:
            logger.warning(f"Redis rate limit error: {e}. Falling back to in-memory.")
            # Fallback to in-memory on Redis error
            return self._check_rate_limit_memory(
                client_id,
                self.minute_tracker if window_name == "minute" else self.hour_tracker,
                window_seconds,
                limit
            )

    def _check_rate_limit_memory(
        self,
        client_id: str,
        tracker: Dict[str, list],
        window_seconds: int,
        limit: int
    ) -> Tuple[int, int]:
        """In-memory rate limit check with sliding window (fallback)."""
        now = time.time()
        window_start = now - window_seconds

        # Clean old entries
        tracker[client_id] = [
            ts for ts in tracker[client_id] if ts > window_start
        ]

        # Count requests
        count = len(tracker[client_id])
        remaining = max(0, limit - count)

        # Record this request
        tracker[client_id].append(now)

        return count, remaining


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    def __init__(self, retry_after: int, limit: int, window: int):
        self.retry_after = retry_after
        self.limit = limit
        self.window = window
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds")
