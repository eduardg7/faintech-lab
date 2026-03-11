"""Custom exceptions for Agent Memory Cloud SDK."""

from typing import Optional


class AgentMemoryError(Exception):
    """Base exception for all SDK errors."""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(AgentMemoryError):
    """Raised when authentication fails (401)."""
    pass


class RateLimitError(AgentMemoryError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        status_code: Optional[int] = 429,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code)


class NotFoundError(AgentMemoryError):
    """Raised when a resource is not found (404)."""
    pass


class ValidationError(AgentMemoryError):
    """Raised when request validation fails (422)."""
    pass
