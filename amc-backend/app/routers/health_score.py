"""Health Score API endpoints.

Provides single and batch health score calculation endpoints
for beta user monitoring and analytics.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..core.health_score import HealthScoreCalculator, UserActivityData

router = APIRouter(prefix="/v1/health-score", tags=["health-score"])

# Singleton calculator instance
calculator = HealthScoreCalculator()


class UserActivityRequest(BaseModel):
    """Request model for single user health score calculation."""

    # Engagement metrics
    sessions_per_week: float = Field(default=0.0, ge=0.0)
    avg_session_duration_minutes: float = Field(default=0.0, ge=0.0)
    messages_per_week: float = Field(default=0.0, ge=0.0)

    # Feature adoption metrics
    agents_created: int = Field(default=0, ge=0)
    agents_active_last_7d: int = Field(default=0, ge=0)
    memories_stored: int = Field(default=0, ge=0)
    projects_created: int = Field(default=0, ge=0)
    search_queries_per_week: float = Field(default=0.0, ge=0.0)

    # Feedback sentiment metrics (optional)
    in_app_rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    nps_score: Optional[int] = Field(default=None, ge=0, le=10)
    text_feedback_sentiment: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    support_ticket_sentiment: Optional[float] = Field(default=None, ge=0.0, le=10.0)

    # Consistency metrics
    daily_streak_days: int = Field(default=0, ge=0)
    weekly_frequency: float = Field(default=0.0, ge=0.0, le=1.0)
    device_consistency: float = Field(default=0.0, ge=0.0, le=1.0)

    # Metadata
    user_id: str = Field(..., description="Unique user identifier")


class BatchHealthScoreRequest(BaseModel):
    """Request model for batch health score calculation."""

    users: List[UserActivityRequest] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of user activity data for batch processing"
    )


class HealthScoreResponse(BaseModel):
    """Response model for health score calculation."""

    user_id: str
    health_score: float
    health_tier: str
    components: Dict[str, float]
    calculation_details: Dict[str, Any]
    calculated_at: datetime


class BatchHealthScoreResponse(BaseModel):
    """Response model for batch health score calculation."""

    scores: List[HealthScoreResponse]
    total_users: int
    average_score: Optional[float] = None
    tier_distribution: Dict[str, int]


def _convert_request_to_data(
    request: UserActivityRequest
) -> UserActivityData:
    """Convert API request to UserActivityData domain model."""
    return UserActivityData(
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


def _convert_result_to_response(
    result: Dict[str, Any],
    user_id: str
) -> HealthScoreResponse:
    """Convert calculation result to API response."""
    return HealthScoreResponse(
        user_id=user_id,
        health_score=result["health_score"],
        health_tier=result["health_tier"],
        components=result["components"],
        calculation_details=result["calculation_details"],
        calculated_at=datetime.utcnow()
    )


@router.post(
    "/calculate",
    response_model=HealthScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate health score for a single user",
    description="""
    Calculates a comprehensive health score (0-10) for a single user based on
    engagement, feature adoption, feedback sentiment, and consistency metrics.

    The health score is calculated as:
    Health Score = (Engagement × 0.4) + (FeatureAdoption × 0.3) +
                   (FeedbackSentiment × 0.2) + (Consistency × 0.1)

    Health tiers:
    - Champion (9.0-10.0): Highly engaged, consistent users
    - Healthy (7.0-8.9): Active users with good engagement
    - At-Risk (5.0-6.9): Users showing declining engagement
    - Critical (0.0-4.9): Users at risk of churn
    """
)
async def calculate_health_score(
    request: UserActivityRequest
) -> HealthScoreResponse:
    """
    Calculate health score for a single user.

    Args:
        request: User activity data including engagement, adoption,
                 feedback, and consistency metrics

    Returns:
        HealthScoreResponse: Complete health score with component breakdown
    """
    try:
        # Convert request to domain model
        user_data = _convert_request_to_data(request)

        # Calculate health score
        result = calculator.calculate_health_score(user_data)

        # Convert to response model
        return _convert_result_to_response(result, request.user_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate health score: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=BatchHealthScoreResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate health scores for multiple users",
    description="""
    Batch calculates health scores for up to 100 users in a single request.
    Returns individual scores plus aggregate statistics.

    Aggregates provided:
    - Average health score across all users
    - Distribution of users across health tiers
    - Total users processed
    """
)
async def calculate_batch_health_scores(
    request: BatchHealthScoreRequest
) -> BatchHealthScoreResponse:
    """
    Calculate health scores for multiple users.

    Args:
        request: Batch request containing list of user activity data

    Returns:
        BatchHealthScoreResponse: Individual scores plus aggregate statistics
    """
    try:
        # Convert all requests to domain models
        user_data_list = [
            _convert_request_to_data(user_req)
            for user_req in request.users
        ]

        # Calculate batch health scores
        results = calculator.calculate_batch_health_scores(user_data_list)

        # Convert to response models
        scores = [
            _convert_result_to_response(result, user_data.user_id)
            for result, user_data in zip(results, user_data_list)
        ]

        # Calculate aggregate statistics
        total_users = len(scores)
        if total_users > 0:
            average_score = sum(s.health_score for s in scores) / total_users
        else:
            average_score = None

        # Calculate tier distribution
        tier_distribution: Dict[str, int] = {
            "Champion": 0,
            "Healthy": 0,
            "At-Risk": 0,
            "Critical": 0
        }
        for score in scores:
            tier_distribution[score.health_tier] += 1

        return BatchHealthScoreResponse(
            scores=scores,
            total_users=total_users,
            average_score=average_score,
            tier_distribution=tier_distribution
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate batch health scores: {str(e)}"
        )


@router.get(
    "/formula",
    status_code=status.HTTP_200_OK,
    summary="Get health score calculation formula",
    description="""
    Returns the health score calculation formula and weight distribution
    for transparency and debugging purposes.
    """
)
async def get_health_score_formula() -> Dict[str, Any]:
    """
    Get health score calculation formula.

    Returns:
        Dictionary containing formula, weights, and tier thresholds
    """
    return {
        "formula": "Health Score = (Engagement × 0.4) + (FeatureAdoption × 0.3) + (FeedbackSentiment × 0.2) + (Consistency × 0.1)",
        "weights": {
            "engagement": calculator.engagement_weight,
            "feature_adoption": calculator.feature_adoption_weight,
            "feedback_sentiment": calculator.feedback_sentiment_weight,
            "consistency": calculator.consistency_weight
        },
        "component_ranges": {
            "engagement": "0-10 (sessions, duration, messages)",
            "feature_adoption": "0-10 (agents, memories, projects, search)",
            "feedback_sentiment": "0-10 (ratings, NPS, text sentiment, support)",
            "consistency": "0-10 (streak, frequency, device)"
        },
        "health_tiers": {
            "Champion": {
                "range": "9.0-10.0",
                "description": "Highly engaged, consistent users"
            },
            "Healthy": {
                "range": "7.0-8.9",
                "description": "Active users with good engagement"
            },
            "At-Risk": {
                "range": "5.0-6.9",
                "description": "Users showing declining engagement"
            },
            "Critical": {
                "range": "0.0-4.9",
                "description": "Users at risk of churn"
            }
        }
    }
