"""Health Score API router — ANALYTICS-20260318110700.

POST /v1/health-score/calculate — calculate health score for single user
POST /v1/health-score/batch    — calculate health scores for multiple users

Implements beta user health score calculation per health-metrics.md framework.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.health_score import (
    health_calculator,
    UserActivityData,
    HealthScoreCalculator
)
from app.routers.auth import AuthContext, get_current_auth_context

router = APIRouter(tags=["Health Score"])


# ── Schemas ────────────────────────────────────────────────────────────────────


class UserActivityRequest(BaseModel):
    """Request schema for single user health score calculation."""
    
    # Engagement metrics
    sessions_per_week: float = Field(default=0.0, ge=0.0, description="Sessions per week")
    avg_session_duration_minutes: float = Field(default=0.0, ge=0.0, description="Average session duration in minutes")
    messages_per_week: float = Field(default=0.0, ge=0.0, description="Messages per week")
    
    # Feature adoption metrics
    agents_created: int = Field(default=0, ge=0, description="Number of agents created")
    agents_active_last_7d: int = Field(default=0, ge=0, description="Agents active in last 7 days")
    memories_stored: int = Field(default=0, ge=0, description="Number of memories stored")
    projects_created: int = Field(default=0, ge=0, description="Number of projects created")
    search_queries_per_week: float = Field(default=0.0, ge=0.0, description="Search queries per week")
    
    # Feedback sentiment metrics
    in_app_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0, description="In-app rating (0-5)")
    nps_score: Optional[int] = Field(default=None, ge=0, le=10, description="NPS score (0-10)")
    text_feedback_sentiment: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Text feedback sentiment (0-10)")
    support_ticket_sentiment: Optional[float] = Field(default=None, ge=0.0, le=10.0, description="Support ticket sentiment (0-10)")
    
    # Consistency metrics
    daily_streak_days: int = Field(default=0, ge=0, description="Daily streak in days")
    weekly_frequency: float = Field(default=0.0, ge=0.0, le=1.0, description="Weekly frequency (0-1)")
    device_consistency: float = Field(default=0.0, ge=0.0, le=1.0, description="Device consistency (0-1)")


class HealthScoreResponse(BaseModel):
    """Response schema with complete health score breakdown."""
    
    health_score: float = Field(description="Final health score (0-10)")
    components: dict = Field(description="Component scores")
    health_tier: str = Field(description="Health tier classification")
    calculation_details: dict = Field(description="Full calculation breakdown")


class BatchHealthScoreRequest(BaseModel):
    """Request schema for batch health score calculation."""
    
    user_data_list: List[UserActivityRequest] = Field(
        description="List of user activity data for batch calculation"
    )


class BatchHealthScoreResponse(BaseModel):
    """Response schema for batch health score calculation."""
    
    health_scores: List[HealthScoreResponse] = Field(description="List of health scores")
    total_users: int = Field(description="Total number of users processed")


# ── Endpoints ───────────────────────────────────────────────────────────────────


@router.post("/calculate", response_model=HealthScoreResponse)
async def calculate_health_score(
    user_data: UserActivityRequest,
    auth: AuthContext = Depends(get_current_auth_context)
) -> HealthScoreResponse:
    """
    Calculate health score for a single user.
    
    Returns complete breakdown including:
    - Final health score (0-10)
    - Component scores (engagement, feature_adoption, feedback_sentiment, consistency)
    - Health tier classification (Champion, Healthy, At-Risk, Critical)
    - Full calculation details with weights
    
    Authentication: Requires bearer token or workspace API key.
    """
    # Convert request to domain model
    activity_data = UserActivityData(
        user_id=auth.user_id,
        calculation_date=datetime.utcnow(),
        sessions_per_week=user_data.sessions_per_week,
        avg_session_duration_minutes=user_data.avg_session_duration_minutes,
        messages_per_week=user_data.messages_per_week,
        agents_created=user_data.agents_created,
        agents_active_last_7d=user_data.agents_active_last_7d,
        memories_stored=user_data.memories_stored,
        projects_created=user_data.projects_created,
        search_queries_per_week=user_data.search_queries_per_week,
        in_app_rating=user_data.in_app_rating,
        nps_score=user_data.nps_score,
        text_feedback_sentiment=user_data.text_feedback_sentiment,
        support_ticket_sentiment=user_data.support_ticket_sentiment,
        daily_streak_days=user_data.daily_streak_days,
        weekly_frequency=user_data.weekly_frequency,
        device_consistency=user_data.device_consistency
    )
    
    # Calculate health score
    result = health_calculator.calculate_health_score(activity_data)
    
    return HealthScoreResponse(**result)


@router.post("/batch", response_model=BatchHealthScoreResponse)
async def calculate_batch_health_scores(
    batch_request: BatchHealthScoreRequest,
    auth: AuthContext = Depends(get_current_auth_context)
) -> BatchHealthScoreResponse:
    """
    Calculate health scores for multiple users (batch processing).
    
    Efficiently processes multiple user health calculations in a single request.
    Returns array of health score results with same structure as single calculation.
    
    Authentication: Requires bearer token or workspace API key.
    Rate limit: Maximum 50 users per batch request.
    """
    # Validate batch size
    if len(batch_request.user_data_list) > 50:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Batch size exceeds maximum of 50 users per request"
        )
    
    # Convert requests to domain models
    activity_data_list = [
        UserActivityData(
            user_id=f"{auth.user_id}_batch_{i}",
            calculation_date=datetime.utcnow(),
            sessions_per_week=user.sessions_per_week,
            avg_session_duration_minutes=user.avg_session_duration_minutes,
            messages_per_week=user.messages_per_week,
            agents_created=user.agents_created,
            agents_active_last_7d=user.agents_active_last_7d,
            memories_stored=user.memories_stored,
            projects_created=user.projects_created,
            search_queries_per_week=user.search_queries_per_week,
            in_app_rating=user.in_app_rating,
            nps_score=user.nps_score,
            text_feedback_sentiment=user.text_feedback_sentiment,
            support_ticket_sentiment=user.support_ticket_sentiment,
            daily_streak_days=user.daily_streak_days,
            weekly_frequency=user.weekly_frequency,
            device_consistency=user.device_consistency
        )
        for i, user in enumerate(batch_request.user_data_list)
    ]
    
    # Calculate health scores
    health_scores = health_calculator.calculate_batch_health_scores(activity_data_list)
    
    return BatchHealthScoreResponse(
        health_scores=[HealthScoreResponse(**score) for score in health_scores],
        total_users=len(activity_data_list)
    )