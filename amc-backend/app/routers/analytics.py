"""Analytics API Router.

Provides endpoints for tracking analytics events for beta launch metrics.
Supports single event and batch event ingestion.

Endpoints:
- POST /v1/analytics/events - Record a single analytics event
- POST /v1/analytics/events/batch - Record multiple analytics events
- GET /v1/analytics/events - Query analytics events (placeholder for future)
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from typing import List
import uuid
import logging

from app.schemas.analytics import (
    AnalyticsEventRequest,
    AnalyticsEventResponse,
    AnalyticsBatchRequest,
    AnalyticsBatchResponse,
    EventType,
)


router = APIRouter(prefix="/v1/analytics", tags=["analytics"])
logger = logging.getLogger(__name__)


# In-memory event store for MVP (replace with database in production)
_events_store: List[dict] = []


@router.post(
    "/events",
    response_model=AnalyticsEventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a single analytics event",
    description="Records an analytics event for beta launch metrics tracking. Events are used to measure user engagement, feature adoption, and conversion."
)
async def record_event(request: AnalyticsEventRequest):
    """
    Record a single analytics event.

    This endpoint accepts analytics events from the frontend dashboard
    and stores them for later analysis. Events are associated with users,
    sessions, or devices for tracking purposes.

    Supported event types:
    - page_view: User viewed a page
    - user_action: User performed an action (click, form submit, etc.)
    - feature_usage: User used a specific feature
    - error: Application error occurred
    - performance: Performance metric recorded
    - conversion: Conversion event (signup, purchase, etc.)
    - engagement: Engagement metric (time on page, scroll depth, etc.)
    """
    try:
        event_id = str(uuid.uuid4())
        event_time = datetime.utcnow()

        event_data = {
            "event_id": event_id,
            "event_type": request.event_type.value,
            "event_name": request.event_name,
            "timestamp": request.timestamp or event_time,
            "user_id": request.user_id,
            "session_id": request.session_id,
            "device_id": request.device_id,
            "properties": request.properties or {},
            "context": request.context or {},
            "server_timestamp": event_time,
        }

        # Store event (in-memory for MVP)
        _events_store.append(event_data)

        logger.info(
            f"Analytics event recorded: {request.event_type.value}/{request.event_name}",
            extra={
                "event_id": event_id,
                "user_id": request.user_id,
                "session_id": request.session_id,
            }
        )

        return AnalyticsEventResponse(
            success=True,
            event_id=event_id,
            timestamp=event_time,
        )
    except Exception as e:
        logger.error(f"Failed to record analytics event: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record analytics event: {str(e)}"
        )


@router.post(
    "/events/batch",
    response_model=AnalyticsBatchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record multiple analytics events",
    description="Records multiple analytics events in a single request. Maximum 100 events per batch."
)
async def record_events_batch(request: AnalyticsBatchRequest):
    """
    Record multiple analytics events in a single request.

    More efficient for high-volume event tracking. Processes up to 100
    events per request.
    """
    try:
        event_ids = []
        event_time = datetime.utcnow()

        for event in request.events:
            event_id = str(uuid.uuid4())
            event_ids.append(event_id)

            event_data = {
                "event_id": event_id,
                "event_type": event.event_type.value,
                "event_name": event.event_name,
                "timestamp": event.timestamp or event_time,
                "user_id": event.user_id,
                "session_id": event.session_id,
                "device_id": event.device_id,
                "properties": event.properties or {},
                "context": event.context or {},
                "server_timestamp": event_time,
            }

            _events_store.append(event_data)

        logger.info(
            f"Analytics batch recorded: {len(event_ids)} events",
            extra={
                "event_count": len(event_ids),
                "event_types": list(set(e.event_type.value for e in request.events)),
            }
        )

        return AnalyticsBatchResponse(
            success=True,
            total_events=len(request.events),
            recorded_events=len(event_ids),
            event_ids=event_ids,
            timestamp=event_time,
        )
    except Exception as e:
        logger.error(f"Failed to record analytics batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record analytics events: {str(e)}"
        )


@router.get(
    "/events",
    status_code=status.HTTP_200_OK,
    summary="Query analytics events (placeholder)",
    description="Query analytics events. This is a placeholder endpoint for future implementation."
)
async def query_events(
    event_type: EventType = None,
    limit: int = 100,
):
    """
    Query analytics events.

    This is a placeholder endpoint for MVP. In production, this would
    query the database with proper filtering and pagination.
    """
    events = _events_store

    if event_type:
        events = [e for e in events if e["event_type"] == event_type.value]

    return {
        "events": events[:limit],
        "total": len(events),
        "limit": limit,
    }


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Analytics API health check",
    description="Simple health check to verify analytics API is operational."
)
async def health_check():
    """
    Health check endpoint for analytics API monitoring.
    """
    return {
        "status": "healthy",
        "service": "analytics-api",
        "events_stored": len(_events_store),
        "timestamp": datetime.utcnow().isoformat()
    }
