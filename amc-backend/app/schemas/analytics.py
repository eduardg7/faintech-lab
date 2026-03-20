"""Analytics API schemas.

Pydantic models for analytics event tracking,supporting beta launch metrics collection.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """Supported analytics event types."""
    PAGE_VIEW = "page_view"
    USER_ACTION = "user_action"
    FEATURE_USAGE = "feature_usage"
    ERROR = "error"
    PERFORMANCE = "performance"
    CONVERSION = "conversion"
    ENGAGEMENT = "engagement"


class AnalyticsEventBase(BaseModel):
    """Base model for analytics events."""

    event_type: EventType = Field(..., description="Type of analytics event")
    event_name: str = Field(..., description="Name/identifier for the event")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the event occurred")
    properties: Optional[Dict[str, Any]] = Field(default=None, description="Additional event properties")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Event context (user agent, session, etc.)")


class AnalyticsEventRequest(AnalyticsEventBase):
    """Request model for posting a single analytics event."""

    user_id: Optional[str] = Field(default=None, description="User identifier")
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    device_id: Optional[str] = Field(default=None, description="Device identifier")


class AnalyticsBatchRequest(BaseModel):
    """Request model for posting multiple analytics events at once."""

    events: List[AnalyticsEventRequest] = Field(
        ...,
        description="List of analytics events to record",
        min_length=1,
        max_length=100
    )


class AnalyticsEventResponse(BaseModel):
    """Response model for successful event ingestion."""

    success: bool = Field(default=True, description="Whether the event was recorded")
    event_id: str = Field(..., description="Unique identifier for the recorded event")
    timestamp: datetime = Field(..., description="Server timestamp when event was recorded")


class AnalyticsBatchResponse(BaseModel):
    """Response model for batch event ingestion."""

    success: bool = Field(default=True, description="Whether all events were recorded")
    total_events: int = Field(..., description="Total number of events in batch")
    recorded_events: int = Field(..., description="Number of events successfully recorded")
    event_ids: List[str] = Field(..., description="List of recorded event IDs")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Server timestamp")
