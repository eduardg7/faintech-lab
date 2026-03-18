"""Health Score Calculator for Beta User Engagement.

Calculates composite health scores (0-10 scale) for beta users based on:
- Engagement Score (40%): Sessions, duration, messages
- Feature Adoption Score (30%): Agents, memories, projects, searches
- Feedback Sentiment Score (20%): Ratings, NPS, sentiment analysis
- Consistency Score (10%): Streaks, frequency, device consistency

Formula:
Health Score = (Engagement × 0.4) + (FeatureAdoption × 0.3) +
               (FeedbackSentiment × 0.2) + (Consistency × 0.1)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List, Literal
import math


@dataclass
class UserActivityData:
    """User activity data for health score calculation."""

    user_id: str
    calculation_date: datetime = field(default_factory=datetime.utcnow)

    # Engagement metrics
    sessions_per_week: float = 0.0
    avg_session_duration_minutes: float = 0.0
    messages_per_week: float = 0.0

    # Feature adoption metrics
    agents_created: int = 0
    agents_active_last_7d: int = 0
    memories_stored: int = 0
    projects_created: int = 0
    search_queries_per_week: float = 0.0

    # Feedback sentiment metrics
    in_app_rating: Optional[float] = None  # 0-5 scale
    nps_score: Optional[int] = None  # 0-10 scale
    text_feedback_sentiment: Optional[float] = None  # 0-10 scale
    support_ticket_sentiment: Optional[float] = None  # 0-10 scale

    # Consistency metrics
    daily_streak_days: int = 0
    weekly_frequency: float = 0.0  # 0-1 fraction of weeks with activity
    device_consistency: float = 0.0  # 0-1 fraction from same device


@dataclass
class HealthScoreResult:
    """Result of health score calculation."""

    health_score: float  # 0-10 scale
    components: Dict[str, float]
    health_tier: Literal["Champion", "Healthy", "At-Risk", "Critical"]
    calculation_details: Dict[str, float]


# Tier thresholds (on 0-10 scale)
TIER_THRESHOLDS = {
    "Champion": 8.0,
    "Healthy": 6.0,
    "At-Risk": 4.0,
    "Critical": 0.0,
}

# Weight configuration
WEIGHTS = {
    "engagement": 0.40,
    "feature_adoption": 0.30,
    "feedback_sentiment": 0.20,
    "consistency": 0.10,
}


class HealthScoreCalculator:
    """Calculator for beta user health scores."""

    def calculate_health_score(self, data: UserActivityData) -> Dict:
        """
        Calculate comprehensive health score for a user.

        Args:
            data: UserActivityData with all metrics

        Returns:
            Dict with health_score, components, health_tier, calculation_details
        """
        engagement_score = self._calculate_engagement_score(data)
        feature_score = self._calculate_feature_adoption_score(data)
        feedback_score = self._calculate_feedback_sentiment_score(data)
        consistency_score = self._calculate_consistency_score(data)

        # Weighted composite score (0-10 scale)
        health_score = (
            engagement_score * WEIGHTS["engagement"]
            + feature_score * WEIGHTS["feature_adoption"]
            + feedback_score * WEIGHTS["feedback_sentiment"]
            + consistency_score * WEIGHTS["consistency"]
        )

        # Round to 2 decimal places
        health_score = round(max(0.0, min(10.0, health_score)), 2)

        components = {
            "engagement": round(engagement_score, 2),
            "feature_adoption": round(feature_score, 2),
            "feedback_sentiment": round(feedback_score, 2),
            "consistency": round(consistency_score, 2),
        }

        calculation_details = {
            "engagement_raw": round(engagement_score, 4),
            "feature_adoption_raw": round(feature_score, 4),
            "feedback_sentiment_raw": round(feedback_score, 4),
            "consistency_raw": round(consistency_score, 4),
            "weights_applied": WEIGHTS,
            "sub_metrics": {
                "sessions_per_week": data.sessions_per_week,
                "avg_session_duration_minutes": data.avg_session_duration_minutes,
                "messages_per_week": data.messages_per_week,
                "agents_created": data.agents_created,
                "agents_active_last_7d": data.agents_active_last_7d,
                "memories_stored": data.memories_stored,
                "projects_created": data.projects_created,
                "search_queries_per_week": data.search_queries_per_week,
                "daily_streak_days": data.daily_streak_days,
                "weekly_frequency": data.weekly_frequency,
                "device_consistency": data.device_consistency,
            },
        }

        return {
            "health_score": health_score,
            "components": components,
            "health_tier": self._determine_tier(health_score),
            "calculation_details": calculation_details,
        }

    def _calculate_engagement_score(self, data: UserActivityData) -> float:
        """
        Calculate engagement score (0-10 scale).

        Based on:
        - Sessions per week (40% weight)
        - Session duration (30% weight)
        - Messages per week (30% weight)
        """
        score = 0.0

        # Sessions per week component (0-4 points)
        # 5+ sessions/week = max score
        sessions_score = min(4.0, data.sessions_per_week * 0.8)
        score += sessions_score

        # Session duration component (0-3 points)
        # 30+ min average = max score
        duration_score = min(3.0, data.avg_session_duration_minutes * 0.1)
        score += duration_score

        # Messages per week component (0-3 points)
        # 50+ messages/week = max score
        messages_score = min(3.0, data.messages_per_week * 0.06)
        score += messages_score

        return min(10.0, score)

    def _calculate_feature_adoption_score(self, data: UserActivityData) -> float:
        """
        Calculate feature adoption score (0-10 scale).

        Based on:
        - Agents created (25%)
        - Active agents (25%)
        - Memories stored (25%)
        - Projects created (15%)
        - Search queries (10%)
        """
        score = 0.0

        # Agents created (0-2.5 points)
        # 3+ agents = max
        agents_created_score = min(2.5, data.agents_created * 0.83)
        score += agents_created_score

        # Active agents (0-2.5 points)
        # 2+ active agents = max
        active_agents_score = min(2.5, data.agents_active_last_7d * 1.25)
        score += active_agents_score

        # Memories stored (0-2.5 points)
        # 10+ memories = max
        memories_score = min(2.5, data.memories_stored * 0.25)
        score += memories_score

        # Projects created (0-1.5 points)
        # 2+ projects = max
        projects_score = min(1.5, data.projects_created * 0.75)
        score += projects_score

        # Search queries (0-1 point)
        # 10+ queries/week = max
        search_score = min(1.0, data.search_queries_per_week * 0.1)
        score += search_score

        return min(10.0, score)

    def _calculate_feedback_sentiment_score(self, data: UserActivityData) -> float:
        """
        Calculate feedback sentiment score (0-10 scale).

        Based on:
        - In-app rating (30%)
        - NPS score (30%)
        - Text feedback sentiment (20%)
        - Support ticket sentiment (20%)
        """
        scores = []

        # In-app rating (0-5 scale -> 0-10)
        if data.in_app_rating is not None:
            rating_score = data.in_app_rating * 2  # Scale 0-5 to 0-10
            scores.append(rating_score)

        # NPS score (0-10 scale)
        if data.nps_score is not None:
            scores.append(float(data.nps_score))

        # Text feedback sentiment (0-10 scale)
        if data.text_feedback_sentiment is not None:
            scores.append(data.text_feedback_sentiment)

        # Support ticket sentiment (0-10 scale)
        if data.support_ticket_sentiment is not None:
            scores.append(data.support_ticket_sentiment)

        # If no feedback data, return neutral score
        if not scores:
            return 5.0

        # Average all available scores
        return sum(scores) / len(scores)

    def _calculate_consistency_score(self, data: UserActivityData) -> float:
        """
        Calculate consistency score (0-10 scale).

        Based on:
        - Daily streak (50%)
        - Weekly frequency (30%)
        - Device consistency (20%)
        """
        score = 0.0

        # Daily streak (0-5 points)
        # 14+ day streak = max
        streak_score = min(5.0, data.daily_streak_days * 0.36)
        score += streak_score

        # Weekly frequency (0-3 points)
        # Already 0-1 scale, multiply by 3
        frequency_score = data.weekly_frequency * 3
        score += frequency_score

        # Device consistency (0-2 points)
        # Already 0-1 scale, multiply by 2
        device_score = data.device_consistency * 2
        score += device_score

        return min(10.0, score)

    def _determine_tier(self, health_score: float) -> str:
        """Determine health tier based on score."""
        if health_score >= TIER_THRESHOLDS["Champion"]:
            return "Champion"
        elif health_score >= TIER_THRESHOLDS["Healthy"]:
            return "Healthy"
        elif health_score >= TIER_THRESHOLDS["At-Risk"]:
            return "At-Risk"
        else:
            return "Critical"


# Singleton instance
health_calculator = HealthScoreCalculator()


def calculate_health_score(data: UserActivityData) -> Dict:
    """Calculate health score using the global calculator."""
    return health_calculator.calculate_health_score(data)


def calculate_batch_health_scores(users: List[UserActivityData]) -> Dict:
    """Calculate health scores for multiple users."""
    results = []
    health_scores = []
    tier_counts = {"Champion": 0, "Healthy": 0, "At-Risk": 0, "Critical": 0}

    for user in users:
        result = health_calculator.calculate_health_score(user)
        health_scores.append(result["health_score"])
        tier_counts[result["health_tier"]] += 1
        results.append(result)

    avg_score = sum(health_scores) / len(health_scores) if health_scores else 0.0

    return {
        "results": results,
        "total_users": len(results),
        "average_health_score": round(avg_score, 2),
        "tier_distribution": tier_counts,
    }
