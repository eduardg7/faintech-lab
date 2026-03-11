"""
Agent Memory Cloud SDK for Python.

Persistent memory infrastructure for AI agent fleets.
"""

__version__ = "1.0.0"
__author__ = "Faintech Solutions"
__email__ = "support@faintech.dev"

from agentmemory.client import MemoryClient
from agentmemory.models import Memory, Agent, Project, SearchResult
from agentmemory.exceptions import (
    AgentMemoryError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

__all__ = [
    "MemoryClient",
    "Memory",
    "Agent",
    "Project",
    "SearchResult",
    "AgentMemoryError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
]
