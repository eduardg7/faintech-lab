"""Centralized error handling middleware for AMC API.

This middleware provides:
1. Catches all unhandled exceptions
2. Returns consistent JSON error responses with error codes
3. Logs errors with stack traces
4. Differentiates between development and production environments
"""

import traceback
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger
from config import settings


logger = get_logger("amc.error_handler")


class ErrorCode:
    """Standard error codes for AMC API."""
    # Client errors (4xx)
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RATE_LIMITED = "RATE_LIMITED"

    # Server errors (5xx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    request_id: str
    timestamp: str
    stack_trace: Optional[str] = None  # Only in development

    class Config:
        json_schema_extra = {
            "example": {
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {"hint": "Contact support with request_id"},
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "timestamp": "2026-03-13T22:00:00Z",
                "stack_trace": None
            }
        }


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware that catches all unhandled exceptions.

    This middleware wraps all requests and provides:
    - Consistent error response format
    - Request ID generation/tracking
    - Structured logging with stack traces
    - Environment-aware error details (dev vs prod)
    """

    def __init__(self, app, is_development: Optional[bool] = None):
        """Initialize the error handling middleware.

        Args:
            app: The FastAPI application
            is_development: Override development mode detection.
                           If None, uses settings.debug
        """
        super().__init__(app)
        self.is_development = is_development if is_development is not None else settings.debug

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and catch any unhandled exceptions."""
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Store request ID in state for access in handlers
        request.state.request_id = request_id

        try:
            response = await call_next(request)
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as exc:
            return await self._handle_exception(request, exc, request_id)

    async def _handle_exception(
        self,
        request: Request,
        exc: Exception,
        request_id: str
    ) -> JSONResponse:
        """Handle an unhandled exception and return appropriate response."""
        # Get exception details
        exc_type = type(exc).__name__
        exc_message = str(exc) or "An unexpected error occurred"
        exc_traceback = traceback.format_exc()

        # Log the error with full details
        self._log_error(
            request=request,
            exc_type=exc_type,
            exc_message=exc_message,
            exc_traceback=exc_traceback,
            request_id=request_id
        )

        # Build error response
        error_response = ErrorResponse(
            error_code=ErrorCode.INTERNAL_ERROR,
            message=self._get_user_friendly_message(exc),
            details=self._build_error_details(request, exc) if self.is_development else None,
            request_id=request_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            stack_trace=exc_traceback if self.is_development else None
        )

        return JSONResponse(
            status_code=500,
            content=error_response.model_dump(exclude_none=True),
            headers={
                "X-Request-ID": request_id,
                "Content-Type": "application/json"
            }
        )

    def _log_error(
        self,
        request: Request,
        exc_type: str,
        exc_message: str,
        exc_traceback: str,
        request_id: str
    ) -> None:
        """Log error with full context and stack trace."""
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_host": request.client.host if request.client else None,
            "exception_type": exc_type,
            "exception_message": exc_message,
        }

        # Always log stack trace (it goes to structured logging)
        logger.error(
            f"Unhandled exception: {exc_type}: {exc_message}",
            extra={"extra": {
                **log_data,
                "stack_trace": exc_traceback
            }},
            exc_info=True
        )

    def _get_user_friendly_message(self, exc: Exception) -> str:
        """Get a user-friendly error message."""
        exc_type = type(exc).__name__

        # Map common exceptions to friendly messages
        friendly_messages = {
            "ConnectionError": "Service temporarily unavailable. Please try again.",
            "TimeoutError": "Request timed out. Please try again.",
            "ValueError": "Invalid data provided.",
            "KeyError": "Required data is missing.",
            "TypeError": "Invalid data type provided.",
            "PermissionError": "Permission denied.",
            "FileNotFoundError": "Required resource not found.",
        }

        return friendly_messages.get(exc_type, "An unexpected error occurred. Please try again later.")

    def _build_error_details(self, request: Request, exc: Exception) -> Dict[str, Any]:
        """Build detailed error information for development mode."""
        return {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "path": request.url.path,
            "method": request.method,
            "hint": "This is a development-only response. Check logs for full stack trace."
        }


class ExceptionHandler:
    """Utility class for handling specific exception types.

    Use this to create custom exception handlers that integrate
    with the error middleware's response format.
    """

    @staticmethod
    def create_error_response(
        error_code: str,
        message: str,
        status_code: int = 500,
        request_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        include_stack_trace: bool = False
    ) -> JSONResponse:
        """Create a standardized error response.

        Args:
            error_code: Error code from ErrorCode class
            message: User-friendly error message
            status_code: HTTP status code
            request_id: Request correlation ID
            details: Additional error details
            include_stack_trace: Whether to include stack trace (dev mode)

        Returns:
            JSONResponse with standardized error format
        """
        response = ErrorResponse(
            error_code=error_code,
            message=message,
            details=details,
            request_id=request_id or str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            stack_trace=traceback.format_exc() if include_stack_trace else None
        )

        return JSONResponse(
            status_code=status_code,
            content=response.model_dump(exclude_none=True),
            headers={"X-Request-ID": response.request_id}
        )

    @staticmethod
    def handle_database_error(
        request: Request,
        exc: Exception,
        is_development: bool = False
    ) -> JSONResponse:
        """Handle database-specific errors."""
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

        logger.error(
            f"Database error: {type(exc).__name__}: {str(exc)}",
            extra={"extra": {
                "request_id": request_id,
                "error_type": "database_error",
                "stack_trace": traceback.format_exc()
            }}
        )

        return ExceptionHandler.create_error_response(
            error_code=ErrorCode.DATABASE_ERROR,
            message="A database error occurred. Please try again.",
            status_code=500,
            request_id=request_id,
            details={"original_error": str(exc)} if is_development else None
        )

    @staticmethod
    def handle_timeout_error(
        request: Request,
        exc: Exception,
        is_development: bool = False
    ) -> JSONResponse:
        """Handle timeout errors."""
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

        logger.warning(
            f"Request timeout: {type(exc).__name__}",
            extra={"extra": {
                "request_id": request_id,
                "path": request.url.path
            }}
        )

        return ExceptionHandler.create_error_response(
            error_code=ErrorCode.TIMEOUT_ERROR,
            message="The request timed out. Please try again.",
            status_code=504,
            request_id=request_id,
            details={"timeout": True} if is_development else None
        )
