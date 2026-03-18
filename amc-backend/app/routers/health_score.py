"""Health Score API Router.

Provides endpoints for calculating user health scores based on beta user engagement,
feature adoption, feedback sentiment, and consistency metrics.

Endpoints:
- POST /v1/health-score/calculate - Calculate health score for a single user
- POST /v1/health-score/batch - Calculate health scores for multiple users
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union
from datetime import datetime

from app.core.health_score import (
    HealthScoreCalculator,
    UserActivityData,
    health_calculator
)


router = APIRouter(prefix="/v1/health-score", tags=["health-score"])


class HealthScoreCalculateRequest(BaseModel):
    """Request model for single user health score calculation."""

    user_id: str = Field(..., description="Unique user identifier")

    # Engagement metrics
    sessions_per_week: float = Field(default=0.0, ge=0, description="Number of sessions per week")
    avg_session_duration_minutes: float = Field(default=0.0, ge=0, description="Average session duration in minutes")
    messages_per_week: float = Field(default=0.0, ge=0, description="Number of messages sent per week")

    # Feature adoption metrics
    agents_created: int = Field(default=0, ge=0, description="Number of agents created")
    agents_active_last_7d: int = Field(default=0, ge=0, description="Number of active agents in last 7 days")
    memories_stored: int = Field(default=0, ge=0, description="Number of memories stored")
    projects_created: int = Field(default=0, ge=0, description="Number of projects created")
    search_queries_per_week: float = Field(default=0.0, ge=0, description="Number of search queries per week")

    # Feedback sentiment metrics
    in_app_rating: Optional[float] = Field(default=None, ge=0, le=5, description="In-app rating (0-5 scale)")
    nps_score: Optional[int] = Field(default=None, ge=0, le=10, description="NPS score (0-10 scale)")
    text_feedback_sentiment: Optional[float] = Field(default=None, ge=0, le=10, description="Text feedback sentiment (0-10 scale)")
    support_ticket_sentiment: Optional[float] = Field(default=None, ge=0, le=10, description="Support ticket sentiment (0-10 scale)")

    # Consistency metrics
    daily_streak_days: int = Field(default=0, ge=0, description="Current daily streak in days")
    weekly_frequency: float = Field(default=0.0, ge=0, le=1, description="Fraction of weeks with activity (0-1)")
    device_consistency: float = Field(default=0.0, ge=0, le=1, description="Fraction of sessions from same device (0-1)")


class HealthScoreBatchRequest(BaseModel):
    """Request model for batch health score calculation."""

    users: List[HealthScoreCalculateRequest] = Field(
        ...,
        description="List of user activity data for batch calculation",
        min_length=1,
        max_length=100
    )


class HealthScoreResponse(BaseModel):
    """Response model for health score calculation."""

    user_id: str
    health_score: float = Field(..., description="Final health score (0-10)")
    components: Dict[str, float] = Field(..., description="Individual component scores")
    health_tier: str = Field(..., description="Health tier classification")
    calculation_details: Dict[str, Union[float, Dict[str, float]]] = Field(
        ...,
        description="Detailed calculation breakdown"
    )
    calculated_at: datetime = Field(default_factory=datetime.utcnow)


class HealthScoreBatchResponse(BaseModel):
    """Response model for batch health score calculation."""

    results: List[HealthScoreResponse] = Field(..., description="List of health score results")
    total_users: int = Field(..., description="Total number of users processed")
    average_health_score: float = Field(..., description="Average health score across all users")
    tier_distribution: Dict[str, int] = Field(
        ...,
        description="Distribution of users across health tiers"
    )
    calculated_at: datetime = Field(default_factory=datetime.utcnow)


def calculate_user_health_score(request: HealthScoreCalculateRequest) -> Dict[str, Union[float, Dict[str, float], str]]:
    """
    Calculate health score for a single user.

    Args:
        request: Health score calculation request with user activity data

    Returns:
        Health score result dictionary
    """
    user_data = UserActivityData(
        user_id=request.user_id,
        sessions_per_week=request.sessions_per_week,
        avg_session_duration_minutes=request.avg_session_duration_minutes,
        messages_per_week=request.messages_per_week,
        agents_created=request.agents_created,
        agents_active_last_7d=request.agents_active_last_7d,
        memories_stored=request.memories_stored,
        projects_created=request.projects_created,
        search_queries_per_week=request.search_queries_per_week,
        in_app_rating=request.in_app_rating,
        nps_score=request.nps_score,
        text_feedback_sentiment=request.text_feedback_sentiment,
        support_ticket_sentiment=request.support_ticket_sentiment,
        daily_streak_days=request.daily_streak_days,
        weekly_frequency=request.weekly_frequency,
        device_consistency=request.device_consistency,
        calculation_date=datetime.utcnow()
    )

    return health_calculator.calculate_health_score(user_data)


@router.post(
    "/calculate",
    response_model=HealthScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate health score for a single user",
    description="Calculates comprehensive health score based on engagement, feature adoption, feedback sentiment, and consistency metrics."
)
async def calculate_health_score(request: HealthScoreCalculateRequest):
    """
    Calculate health score for a single beta user.

    The health score is a composite metric (0-10) that predicts beta user success.
    A score of 7+ indicates a healthy, engaged user. A score below 6 indicates risk of churn.

    Formula:
    Health Score = (Engagement × 0.4) + (FeatureAdoption × 0.3) +
                  (FeedbackSentiment × 0.2) + (Consistency × 0.1)
    """
    try:
        result = calculate_user_health_score(request)

        return HealthScoreResponse(
            user_id=request.user_id,
            health_score=result["health_score"],
            components=result["components"],
            health_tier=result["health_tier"],
            calculation_details=result["calculation_details"],
            calculated_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate health score: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=HealthScoreBatchResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate health scores for multiple users",
    description="Calculates health scores for multiple beta users in a single request."
)
async def calculate_batch_health_scores(request: HealthScoreBatchRequest):
    """
    Calculate health scores for multiple beta users.

    Processes up to 100 users in a single request. Returns individual scores
    along with aggregate statistics and tier distribution.
    """
    try:
        results = []
        health_scores = []
        tier_counts = {"Champion": 0, "Healthy": 0, "At-Risk": 0, "Critical": 0}

        for user_request in request.users:
            result = calculate_user_health_score(user_request)
            health_scores.append(result["health_score"])

            # Update tier distribution
            tier_counts[result["health_tier"]] += 1

            results.append(HealthScoreResponse(
                user_id=user_request.user_id,
                health_score=result["health_score"],
                components=result["components"],
                health_tier=result["health_tier"],
                calculation_details=result["calculation_details"],
                calculated_at=datetime.utcnow()
            ))

        # Calculate average health score
        average_health_score = sum(health_scores) / len(health_scores) if health_scores else 0.0

        return HealthScoreBatchResponse(
            results=results,
            total_users=len(results),
            average_health_score=round(average_health_score, 2),
            tier_distribution=tier_counts,
            calculated_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate batch health scores: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    description="Simple health check to verify health score API is operational."
)
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "health-score-api",
        "timestamp": datetime.utcnow().isoformat()
    }
