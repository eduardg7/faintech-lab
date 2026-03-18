"""Beta User Health Score Calculation Logic.

Implements comprehensive health score formula from health-metrics.md:
Health Score = (Engagement × 0.4) + (FeatureAdoption × 0.3) + 
                (FeedbackSentiment × 0.2) + (Consistency × 0.1)

Each component is calculated 0-10 and weighted to produce final 0-10 score.
"""

import statistics
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta


@dataclass
class UserActivityData:
    """Raw user activity data for health score calculation."""
    
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
    weekly_frequency: float = 0.0  # 0-1 (fraction of weeks with activity)
    device_consistency: float = 0.0  # 0-1 (fraction of sessions from same device)
    
    # Metadata
    user_id: str
    calculation_date: datetime = field(default_factory=datetime.utcnow)


class HealthScoreCalculator:
    """Calculates user health scores based on activity data."""
    
    def __init__(self):
        self.engagement_weight = 0.4
        self.feature_adoption_weight = 0.3
        self.feedback_sentiment_weight = 0.2
        self.consistency_weight = 0.1
    
    def calculate_engagement_score(self, data: UserActivityData) -> float:
        """
        Calculate engagement score (0-10).
        
        Formula: min(10, (
            (Sessions per week / 5) × 3 +
            (Avg session duration / 15min) × 3 +
            (Messages per week / 20) × 4
        ))
        """
        sessions_score = (data.sessions_per_week / 5.0) * 3.0
        duration_score = (data.avg_session_duration_minutes / 15.0) * 3.0
        messages_score = (data.messages_per_week / 20.0) * 4.0
        
        raw_score = sessions_score + duration_score + messages_score
        return min(10.0, max(0.0, raw_score))
    
    def calculate_feature_adoption_score(self, data: UserActivityData) -> float:
        """
        Calculate feature adoption score (0-10).
        
        Formula: min(10, (
            (Agents created / 2) × 3 +
            (Memories stored / 5) × 2 +
            (Projects created / 1) × 3 +
            (Search queries / 3) × 2
        ))
        """
        agents_score = (data.agents_created / 2.0) * 3.0
        memories_score = (data.memories_stored / 5.0) * 2.0
        projects_score = data.projects_created * 3.0
        search_score = (data.search_queries_per_week / 3.0) * 2.0
        
        raw_score = agents_score + memories_score + projects_score + search_score
        return min(10.0, max(0.0, raw_score))
    
    def calculate_feedback_sentiment_score(self, data: UserActivityData) -> float:
        """
        Calculate feedback sentiment score (0-10).
        
        Formula: (
            (Avg in-app rating × 0.4) +
            (NPS score / 10 × 0.3) +
            (Text feedback sentiment × 0.2) +
            (Support ticket sentiment × 0.1)
        )
        """
        score_components = []
        total_weight = 0.0
        
        # In-app rating (0-5 scale, map to 0-10 by multiplying by 2)
        if data.in_app_rating is not None:
            in_app_normalized = data.in_app_rating * 2.0
            score_components.append((in_app_normalized, 0.4))
            total_weight += 0.4
        
        # NPS score (already 0-10 scale)
        if data.nps_score is not None:
            score_components.append((float(data.nps_score), 0.3))
            total_weight += 0.3
        
        # Text feedback sentiment (0-10 scale)
        if data.text_feedback_sentiment is not None:
            score_components.append((data.text_feedback_sentiment, 0.2))
            total_weight += 0.2
        
        # Support ticket sentiment (0-10 scale)
        if data.support_ticket_sentiment is not None:
            score_components.append((data.support_ticket_sentiment, 0.1))
            total_weight += 0.1
        
        if not score_components:
            return 5.0  # Neutral score when no feedback data
        
        # Weighted average
        weighted_sum = sum(score * weight for score, weight in score_components)
        if total_weight > 0:
            return min(10.0, max(0.0, weighted_sum / total_weight))
        else:
            return 5.0
    
    def calculate_consistency_score(self, data: UserActivityData) -> float:
        """
        Calculate consistency score (0-10).
        
        Formula: min(10, (
            (Daily streak days / 7) × 5 +
            (Weekly frequency / 1.0) × 3 +
            (Device consistency / 0.8) × 2
        ))
        """
        streak_score = (data.daily_streak_days / 7.0) * 5.0
        frequency_score = data.weekly_frequency * 3.0
        device_score = (data.device_consistency / 0.8) * 2.0
        
        raw_score = streak_score + frequency_score + device_score
        return min(10.0, max(0.0, raw_score))
    
    def calculate_health_score(self, data: UserActivityData) -> Dict[str, Union[float, Dict[str, float]]]:
        """
        Calculate complete health score with component breakdown.
        
        Returns:
            {
                "health_score": float,  # Final 0-10 score
                "components": {
                    "engagement": float,
                    "feature_adoption": float, 
                    "feedback_sentiment": float,
                    "consistency": float
                },
                "health_tier": str,  # "Champion", "Healthy", "At-Risk", "Critical"
                "calculation_details": {
                    "weights": Dict[str, float],
                    "component_scores": Dict[str, float]
                }
            }
        """
        # Calculate individual component scores
        engagement = self.calculate_engagement_score(data)
        feature_adoption = self.calculate_feature_adoption_score(data)
        feedback_sentiment = self.calculate_feedback_sentiment_score(data)
        consistency = self.calculate_consistency_score(data)
        
        # Calculate weighted health score
        health_score = (
            engagement * self.engagement_weight +
            feature_adoption * self.feature_adoption_weight +
            feedback_sentiment * self.feedback_sentiment_weight +
            consistency * self.consistency_weight
        )
        
        # Determine health tier
        if health_score >= 9.0:
            health_tier = "Champion"
        elif health_score >= 7.0:
            health_tier = "Healthy"
        elif health_score >= 5.0:
            health_tier = "At-Risk"
        else:
            health_tier = "Critical"
        
        return {
            "health_score": round(health_score, 2),
            "components": {
                "engagement": round(engagement, 2),
                "feature_adoption": round(feature_adoption, 2),
                "feedback_sentiment": round(feedback_sentiment, 2),
                "consistency": round(consistency, 2)
            },
            "health_tier": health_tier,
            "calculation_details": {
                "weights": {
                    "engagement": self.engagement_weight,
                    "feature_adoption": self.feature_adoption_weight,
                    "feedback_sentiment": self.feedback_sentiment_weight,
                    "consistency": self.consistency_weight
                },
                "component_scores": {
                    "engagement": round(engagement, 2),
                    "feature_adoption": round(feature_adoption, 2),
                    "feedback_sentiment": round(feedback_sentiment, 2),
                    "consistency": round(consistency, 2)
                }
            }
        }
    
    def calculate_batch_health_scores(
        self, user_data_list: List[UserActivityData]
    ) -> List[Dict[str, Union[float, Dict[str, float]]]]:
        """
        Calculate health scores for multiple users.
        
        Args:
            user_data_list: List of UserActivityData objects
            
        Returns:
            List of health score results, each containing full calculation
        """
        return [self.calculate_health_score(data) for data in user_data_list]


# Singleton instance
health_calculator = HealthScoreCalculator()