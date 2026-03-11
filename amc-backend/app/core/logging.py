"""Structured JSON logging for AMC API."""

import logging
import json
import traceback
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "logger": record.name,
        }

        # Merge any extra fields passed via the `extra` kwarg
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_data.update(record.extra)

        # Attach exception info when present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info),
            }

        return json.dumps(log_data, default=str)


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure root logger with JSON output and return named logger."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    # Replace all existing handlers on the root logger
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # Silence noisy third-party loggers
    for noisy in ("uvicorn.access", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    return logging.getLogger("amc")


def get_logger(name: str = "amc") -> logging.Logger:
    """Return a named logger (assumes setup_logging was already called)."""
    return logging.getLogger(name)
