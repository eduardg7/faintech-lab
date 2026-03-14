"""Structured error handling system for AMC API."""
from typing import Any, Dict, Optional
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import time
from datetime import datetime


class ErrorCode:
    """Standard error codes for AMC API."""
    # Auth errors (1xxx)
    AUTH_INVALID = "AUTH_INVALID"
    AUTH_EXPIRED = "AUTH_EXPIRED"
    AUTH_MISSING = "AUTH_MISSING"

    # Validation errors (2xxx)
    VALIDATION_FAILED = "VALIDATION_FAILED"
    CONTENT_TOO_LARGE = "CONTENT_TOO_LARGE"
    INVALID_INPUT = "INVALID_INPUT"

    # Resource errors (3xxx)
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"

    # Rate limiting (4xxx)
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

    # Server errors (5xxx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    code: str
    request_id: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation Failed",
                "message": "Content size exceeds 10KB limit",
                "code": "CONTENT_TOO_LARGE",
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2026-03-10T21:47:00Z",
                "details": {
                    "content_size": 15360,
                    "max_size": 10240
                }
            }
        }


class AMCError(HTTPException):
    """Base exception for AMC API errors."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.code = code
        self.message = message
        self.details = details
        self.request_id = str(uuid.uuid4())
        super().__init__(
            status_code=status_code,
            detail=message,
            headers=headers
        )


class ValidationError(AMCError):
    """Validation error (400)."""

    def __init__(
        self,
        message: str = "Validation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=ErrorCode.VALIDATION_FAILED,
            message=message,
            details=details
        )


class NotFoundError(AMCError):
    """Resource not found (404)."""

    def __init__(
        self,
        resource: str,
        identifier: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code=ErrorCode.NOT_FOUND,
            message=f"{resource} not found: {identifier}",
            details=details
        )


class ContentTooLargeError(AMCError):
    """Content exceeds size limit (413)."""

    def __init__(
        self,
        content_size: int,
        max_size: int = 10240
    ):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            code=ErrorCode.CONTENT_TOO_LARGE,
            message=f"Content size {content_size} bytes exceeds {max_size} bytes limit",
            details={
                "content_size": content_size,
                "max_size": max_size
            }
        )


class RateLimitError(AMCError):
    """Rate limit exceeded (429)."""

    def __init__(
        self,
        retry_after: int,
        limit: int,
        window: int
    ):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code=ErrorCode.RATE_LIMIT_EXCEEDED,
            message=f"Rate limit exceeded. Retry after {retry_after} seconds",
            details={
                "retry_after": retry_after,
                "limit": limit,
                "window": window
            },
            headers={"Retry-After": str(retry_after)}
        )


class InternalError(AMCError):
    """Internal server error (500)."""

    def __init__(
        self,
        message: str = "Internal server error",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=ErrorCode.INTERNAL_ERROR,
            message=message,
            details=details
        )


class DatabaseError(AMCError):
    """Database error (500)."""

    def __init__(
        self,
        message: str = "Database operation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=ErrorCode.DATABASE_ERROR,
            message=message,
            details=details
        )


async def amc_error_handler(request: Request, exc: AMCError) -> JSONResponse:
    """Global exception handler for AMC errors."""

    # Generate request ID if not present
    request_id = exc.request_id

    # Build error response
    error_response = ErrorResponse(
        error=exc.__class__.__name__.replace("Error", ""),
        message=exc.message,
        code=exc.code,
        request_id=request_id,
        timestamp=datetime.utcnow().isoformat() + "Z",
        details=exc.details
    )

    # Log error with correlation ID
    print(f"[ERROR] Request ID: {request_id} | Code: {exc.code} | Message: {exc.message}")
    if exc.details:
        print(f"[ERROR] Details: {exc.details}")

    # Prepare headers (including rate limit headers if available)
    headers = exc.headers or {}
    headers["X-Request-ID"] = request_id

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(exclude_none=True),
        headers=headers
    )


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return structured 422 payloads for FastAPI validation failures."""

    request_id = get_request_id(request)
    error_response = ErrorResponse(
        error="ValidationError",
        message="Request validation failed",
        code=ErrorCode.VALIDATION_FAILED,
        request_id=request_id,
        timestamp=datetime.utcnow().isoformat() + "Z",
        details={"errors": exc.errors()},
    )

    print(
        f"[ERROR] Request ID: {request_id} | Code: {ErrorCode.VALIDATION_FAILED} | "
        f"Validation errors: {exc.errors()}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
        headers={"X-Request-ID": request_id},
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for unexpected exceptions."""

    request_id = str(uuid.uuid4())

    error_response = ErrorResponse(
        error="InternalError",
        message="An unexpected error occurred",
        code=ErrorCode.INTERNAL_ERROR,
        request_id=request_id,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

    # Log full error for debugging
    print(f"[ERROR] Request ID: {request_id} | Unexpected error: {type(exc).__name__}: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
        headers={"X-Request-ID": request_id}
    )


def get_request_id(request: Request) -> str:
    """Get or generate request ID for correlation."""
    return request.headers.get("X-Request-ID", str(uuid.uuid4()))


class RetryConfig:
    """Configuration for retry logic."""

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        retry_on: tuple = (500, 502, 503, 504),
        timeout: float = 30.0
    ):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.retry_on = retry_on
        self.timeout = timeout
