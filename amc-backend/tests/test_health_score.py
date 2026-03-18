"""Tests for Health Score Calculation (ANALYTICS-20260318110700).

Tests the health score calculation logic, API endpoints, and validation
against the documented formula from health-metrics.md.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from app.core.health_score import (
    HealthScoreCalculator,
    UserActivityData,
    health_calculator
)


# ---------------------------------------------------------------------------
# Unit Tests: Health Score Calculator
# ---------------------------------------------------------------------------

class TestEngagementScore:
    """Test engagement score calculation."""
    
    def test_power_user_engagement(self):
        """Power user (daily, multiple sessions)."""
        data = UserActivityData(
            user_id="test-1",
            sessions_per_week=10,  # 2x per day
            avg_session_duration_minutes=30,  # Good duration
            messages_per_week=25  # High usage
        )
        
        result = health_calculator.calculate_engagement_score(data)
        
        assert result == 10.0, f"Expected 10.0, got {result}"
    
    def test_regular_user_engagement(self):
        """Regular user (2-3x/week, moderate usage)."""
        data = UserActivityData(
            user_id="test-2",
            sessions_per_week=3,
            avg_session_duration_minutes=15,
            messages_per_week=15
        )
        
        result = health_calculator.calculate_engagement_score(data)
        
        # (3/5)*3 + (15/15)*3 + (15/20)*4 = 1.8 + 3.0 + 3.0 = 7.8
        assert 7.0 <= result <= 8.0, f"Expected 7-8, got {result}"
    
    def test_casual_user_engagement(self):
        """Casual user (1x/week, light usage)."""
        data = UserActivityData(
            user_id="test-3",
            sessions_per_week=1,
            avg_session_duration_minutes=10,
            messages_per_week=5
        )
        
        result = health_calculator.calculate_engagement_score(data)
        
        # (1/5)*3 + (10/15)*3 + (5/20)*4 = 0.6 + 2.0 + 1.0 = 3.6
        assert 5.0 <= result <= 6.0, f"Expected 5-6, got {result}"
    
    def test_at_risk_user_engagement(self):
        """At-risk user (rare or no usage)."""
        data = UserActivityData(
            user_id="test-4",
            sessions_per_week=0.5,
            avg_session_duration_minutes=5,
            messages_per_week=2
        )
        
        result = health_calculator.calculate_engagement_score(data)
        
        assert 0.0 <= result <= 4.0, f"Expected 0-4, got {result}"
    
    def test_clamps_at_maximum(self):
        """Score is capped at 10.0."""
        data = UserActivityData(
            user_id="test-5",
            sessions_per_week=100,  # Way above target
            avg_session_duration_minutes=300,  # Way above target
            messages_per_week=500  # Way above target
        )
        
        result = health_calculator.calculate_engagement_score(data)
        
        assert result == 10.0, f"Expected cap at 10.0, got {result}"


class TestFeatureAdoptionScore:
    """Test feature adoption score calculation."""
    
    def test_feature_explorer_adoption(self):
        """Feature explorer (uses all features regularly)."""
        data = UserActivityData(
            user_id="test-6",
            agents_created=3,  # Above target
            memories_stored=10,  # Above target
            projects_created=2,  # Above target
            search_queries_per_week=5  # Above target
        )
        
        result = health_calculator.calculate_feature_adoption_score(data)
        
        # (3/2)*3 + (10/5)*2 + (2)*3 + (5/3)*2 = 4.5 + 4.0 + 6.0 + 3.33 = 17.83 -> capped at 10.0
        assert result == 10.0, f"Expected 10.0, got {result}"
    
    def test_productive_user_adoption(self):
        """Productive user (uses key features well)."""
        data = UserActivityData(
            user_id="test-7",
            agents_created=2,
            memories_stored=5,
            projects_created=1,
            search_queries_per_week=3
        )
        
        result = health_calculator.calculate_feature_adoption_score(data)
        
        # (2/2)*3 + (5/5)*2 + (1)*3 + (3/3)*2 = 3.0 + 2.0 + 3.0 + 2.0 = 10.0
        assert result == 10.0, f"Expected 10.0, got {result}"
    
    def test_feature_explorer_adoption(self):
        """Feature explorer (uses 1-2 features)."""
        data = UserActivityData(
            user_id="test-8",
            agents_created=1,
            memories_stored=3,
            projects_created=1,
            search_queries_per_week=1
        )
        
        result = health_calculator.calculate_feature_adoption_score(data)
        
        # (1/2)*3 + (3/5)*2 + (1)*3 + (1/3)*2 = 1.5 + 1.2 + 3.0 + 0.67 = 6.37
        assert 6.0 <= result <= 7.0, f"Expected 6-7, got {result}"
    
    def test_feature_unaware_adoption(self):
        """Feature unaware (minimal feature usage)."""
        data = UserActivityData(
            user_id="test-9",
            agents_created=0,
            memories_stored=1,
            projects_created=0,
            search_queries_per_week=1
        )
        
        result = health_calculator.calculate_feature_adoption_score(data)
        
        # (0/2)*3 + (1/5)*2 + (0)*3 + (1/3)*2 = 0.0 + 0.4 + 0.0 + 0.67 = 1.07
        assert 0.0 <= result <= 4.0, f"Expected 0-4, got {result}"


class TestFeedbackSentimentScore:
    """Test feedback sentiment score calculation."""
    
    def test_promoter_sentiment(self):
        """Promoter (high satisfaction)."""
        data = UserActivityData(
            user_id="test-10",
            in_app_rating=5.0,  # Max in-app rating (0-5)
            nps_score=10,  # Max NPS score
            text_feedback_sentiment=9.0,  # Positive text sentiment
            support_ticket_sentiment=9.0  # Positive support sentiment
        )
        
        result = health_calculator.calculate_feedback_sentiment_score(data)
        
        # (5*2)*0.4 + (10)*0.3 + (9)*0.2 + (9)*0.1 = 4.0 + 3.0 + 1.8 + 0.9 = 9.7
        assert 8.0 <= result <= 10.0, f"Expected 8-10, got {result}"
    
    def test_passive_sentiment(self):
        """Passive (satisfied but not excited)."""
        data = UserActivityData(
            user_id="test-11",
            in_app_rating=3.5,
            nps_score=7,
            text_feedback_sentiment=6.0
        )
        
        result = health_calculator.calculate_feedback_sentiment_score(data)
        
        # (3.5*2)*0.4 + (7)*0.3 + (6)*0.2 = 2.8 + 2.1 + 1.2 = 6.1 (normalized for missing support)
        assert 6.0 <= result <= 7.0, f"Expected 6-7, got {result}"
    
    def test_detractor_sentiment(self):
        """Detractor (at risk of churn)."""
        data = UserActivityData(
            user_id="test-12",
            in_app_rating=1.0,
            nps_score=3,
            text_feedback_sentiment=2.0
        )
        
        result = health_calculator.calculate_feedback_sentiment_score(data)
        
        # (1*2)*0.4 + (3)*0.3 + (2)*0.2 = 0.8 + 0.9 + 0.4 = 2.1
        assert 0.0 <= result <= 5.0, f"Expected 0-5, got {result}"
    
    def test_no_feedback_neutral(self):
        """No feedback data should return neutral score."""
        data = UserActivityData(
            user_id="test-13"
            # No feedback fields set
        )
        
        result = health_calculator.calculate_feedback_sentiment_score(data)
        
        assert result == 5.0, f"Expected 5.0 (neutral), got {result}"


class TestConsistencyScore:
    """Test consistency score calculation."""
    
    def test_highly_consistent(self):
        """Highly consistent (daily, same device)."""
        data = UserActivityData(
            user_id="test-14",
            daily_streak_days=7,  # Daily usage for a week
            weekly_frequency=1.0,  # Active every week
            device_consistency=1.0  # Always same device
        )
        
        result = health_calculator.calculate_consistency_score(data)
        
        # (7/7)*5 + (1.0)*3 + (1.0/0.8)*2 = 5.0 + 3.0 + 2.5 = 10.5 -> capped at 10.0
        assert result == 10.0, f"Expected 10.0, got {result}"
    
    def test_consistent(self):
        """Consistent (regular pattern)."""
        data = UserActivityData(
            user_id="test-15",
            daily_streak_days=3,
            weekly_frequency=0.8,
            device_consistency=0.9
        )
        
        result = health_calculator.calculate_consistency_score(data)
        
        # (3/7)*5 + (0.8)*3 + (0.9/0.8)*2 = 2.14 + 2.4 + 2.25 = 6.79
        assert 7.0 <= result <= 8.0, f"Expected 7-8, got {result}"
    
    def test_semi_consistent(self):
        """Semi-consistent (occasional)."""
        data = UserActivityData(
            user_id="test-16",
            daily_streak_days=1,
            weekly_frequency=0.3,
            device_consistency=0.6
        )
        
        result = health_calculator.calculate_consistency_score(data)
        
        # (1/7)*5 + (0.3)*3 + (0.6/0.8)*2 = 0.71 + 0.9 + 1.5 = 3.11
        assert 5.0 <= result <= 6.0, f"Expected 5-6, got {result}"
    
    def test_inconsistent(self):
        """Inconsistent (no pattern)."""
        data = UserActivityData(
            user_id="test-17",
            daily_streak_days=0,
            weekly_frequency=0.1,
            device_consistency=0.4
        )
        
        result = health_calculator.calculate_consistency_score(data)
        
        # (0/7)*5 + (0.1)*3 + (0.4/0.8)*2 = 0.0 + 0.3 + 1.0 = 1.3
        assert 0.0 <= result <= 4.0, f"Expected 0-4, got {result}"


class TestCompleteHealthScore:
    """Test complete health score calculation with weighting."""
    
    def test_champion_tier(self):
        """Champion (power user, high satisfaction)."""
        data = UserActivityData(
            user_id="test-18",
            sessions_per_week=10,
            avg_session_duration_minutes=30,
            messages_per_week=25,
            agents_created=3,
            memories_stored=10,
            projects_created=2,
            search_queries_per_week=5,
            in_app_rating=5.0,
            nps_score=10,
            daily_streak_days=7,
            weekly_frequency=1.0,
            device_consistency=1.0
        )
        
        result = health_calculator.calculate_health_score(data)
        
        assert result["health_tier"] == "Champion"
        assert result["health_score"] >= 9.0
        assert "components" in result
        assert "calculation_details" in result
    
    def test_healthy_tier(self):
        """Healthy (regular user, good adoption, positive feedback)."""
        data = UserActivityData(
            user_id="test-19",
            sessions_per_week=3,
            avg_session_duration_minutes=15,
            messages_per_week=15,
            agents_created=2,
            memories_stored=5,
            projects_created=1,
            search_queries_per_week=3,
            in_app_rating=3.5,
            nps_score=7,
            daily_streak_days=3,
            weekly_frequency=0.8,
            device_consistency=0.9
        )
        
        result = health_calculator.calculate_health_score(data)
        
        assert result["health_tier"] == "Healthy"
        assert 7.0 <= result["health_score"] < 9.0
    
    def test_at_risk_tier(self):
        """At-Risk (casual usage, minimal adoption, neutral feedback)."""
        data = UserActivityData(
            user_id="test-20",
            sessions_per_week=1,
            avg_session_duration_minutes=10,
            messages_per_week=5,
            agents_created=1,
            memories_stored=3,
            projects_created=1,
            search_queries_per_week=1,
            daily_streak_days=1,
            weekly_frequency=0.3,
            device_consistency=0.6
        )
        
        result = health_calculator.calculate_health_score(data)
        
        assert result["health_tier"] == "At-Risk"
        assert 5.0 <= result["health_score"] < 7.0
    
    def test_critical_tier(self):
        """Critical (no usage, negative feedback)."""
        data = UserActivityData(
            user_id="test-21",
            sessions_per_week=0.5,
            avg_session_duration_minutes=5,
            messages_per_week=2,
            agents_created=0,
            memories_stored=1,
            projects_created=0,
            search_queries_per_week=0,
            in_app_rating=1.0,
            nps_score=3,
            daily_streak_days=0,
            weekly_frequency=0.1,
            device_consistency=0.4
        )
        
        result = health_calculator.calculate_health_score(data)
        
        assert result["health_tier"] == "Critical"
        assert 0.0 <= result["health_score"] < 5.0
    
    def test_weighted_formula(self):
        """Verify the weighted formula is correct."""
        data = UserActivityData(
            user_id="test-22",
            # Set values that give simple component scores
            sessions_per_week=5,  # Engagement = 3.0
            avg_session_duration_minutes=15,  # Engagement = 3.0
            messages_per_week=20,  # Engagement = 4.0
            # Total engagement = 10.0
            
            agents_created=2,  # Adoption = 3.0
            memories_stored=5,  # Adoption = 2.0
            projects_created=1,  # Adoption = 3.0
            search_queries_per_week=3,  # Adoption = 2.0
            # Total adoption = 10.0
            
            in_app_rating=5.0,  # Sentiment (mapped): 10.0 × 0.4 = 4.0
            nps_score=10,  # Sentiment: 10.0 × 0.3 = 3.0
            # Total sentiment = 7.0
            
            daily_streak_days=7,  # Consistency = 5.0
            weekly_frequency=1.0,  # Consistency = 3.0
            device_consistency=1.0  # Consistency = 2.5
            # Total consistency = 10.5 -> capped at 10.0
        )
        
        result = health_calculator.calculate_health_score(data)
        
        # Expected: (10.0 × 0.4) + (10.0 × 0.3) + (7.0 × 0.2) + (10.0 × 0.1)
        # = 4.0 + 3.0 + 1.4 + 1.0 = 9.4
        assert abs(result["health_score"] - 9.4) < 0.01, f"Expected 9.4, got {result['health_score']}"
        assert result["components"]["engagement"] == 10.0
        assert result["components"]["feature_adoption"] == 10.0
        assert abs(result["components"]["feedback_sentiment"] - 7.0) < 0.1
        assert result["components"]["consistency"] == 10.0


class TestBatchCalculation:
    """Test batch health score calculation."""
    
    def test_batch_multiple_users(self):
        """Calculate health scores for multiple users."""
        users = [
            UserActivityData(
                user_id=f"batch-{i}",
                sessions_per_week=i + 1,
                agents_created=i,
                memories_stored=i * 2
            )
            for i in range(5)
        ]
        
        results = health_calculator.calculate_batch_health_scores(users)
        
        assert len(results) == 5
        assert all("health_score" in r for r in results)
        assert all("components" in r for r in results)
        assert all("health_tier" in r for r in results)