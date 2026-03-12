"""Rate limiting middleware for AMC API."""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple
import time
from collections import defaultdict


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to add rate limit headers to all responses."""

    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour

        # In-memory rate limit tracking (should use Redis in production)
        self.minute_tracker: Dict[str, list] = defaultdict(list)
        self.hour_tracker: Dict[str, list] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Get client identifier (API key or IP)
        client_id = self._get_client_id(request)

        # Check rate limits
        minute_count, minute_remaining = self._check_rate_limit(
            client_id,
            self.minute_tracker,
            60,
            self.requests_per_minute
        )

        hour_count, hour_remaining = self._check_rate_limit(
            client_id,
            self.hour_tracker,
            3600,
            self.requests_per_hour
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

    def _check_rate_limit(
        self,
        client_id: str,
        tracker: Dict[str, list],
        window_seconds: int,
        limit: int
    ) -> Tuple[int, int]:
        """Check and update rate limit for client."""
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
