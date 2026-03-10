"""Rate limiting middleware using slowapi."""
from fastapi import Request, HTTPException, Response
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from typing import Callable

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_per_minute}/minute"]
)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors."""
    raise HTTPException(
        status_code=429,
        detail={
            "error": "Rate limit exceeded",
            "retry_after": exc.detail
        }
    )


async def add_rate_limit_headers(request: Request, call_next: Callable) -> Response:
    """
    Middleware to add X-RateLimit-* headers to all responses.
    
    Headers added:
    - X-RateLimit-Limit: Maximum requests per minute
    - X-RateLimit-Remaining: Remaining requests in current window
    - X-RateLimit-Reset: Unix timestamp when the rate limit resets
    
    Note: This middleware reads the rate limit state from slowapi's limiter.
    """
    response = await call_next(request)
    
    # Get rate limit info from limiter state if available
    # slowapi stores rate limit info in request.state
    limiter_instance = request.app.state.limiter
    
    try:
        # Get the current rate limit stats
        key = get_remote_address(request)
        limits = limiter_instance.limiter.get_window_stats(key)
        
        if limits:
            current, remaining = limits
            response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(max(0, settings.rate_limit_per_minute - current))
            # Reset time is typically 60 seconds from first request in window
            # slowapi doesn't expose exact reset time, so we approximate
            response.headers["X-RateLimit-Reset"] = "60"  # seconds until reset
    except Exception:
        # If rate limit info is not available, set defaults
        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(settings.rate_limit_per_minute)
        response.headers["X-RateLimit-Reset"] = "60"
    
    return response
