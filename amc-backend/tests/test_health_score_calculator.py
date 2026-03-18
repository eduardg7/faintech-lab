"""Unit tests for Health Score Calculator.

Tests all component calculations and edge cases for the health score
calculation logic defined in health-metrics.md.
"""

import pytest
from datetime import datetime, timedelta

from app.core.health_score import (
    HealthScoreCalculator,
    UserActivityData,
)


@pytest.fixture
def calculator():
    """Health score calculator fixture."""
    return HealthScoreCalculator()


@pytest.fixture
def healthy_user_data():
    """Fixture for a healthy user with good engagement."""
    return UserActivityData(
        user_id="test-healthy-user",
        # Engagement metrics
        sessions_per_week=5.0,
        avg_session_duration_minutes=15.0,
        messages_per_week=20.0,
        # Feature adoption metrics
        agents_created=2,
        agents_active_last_7d=2,
        memories_stored=5,
        projects_created=1,
        search_queries_per_week=3.0,
        # Feedback sentiment metrics
        in_app_rating=5.0,
        nps_score=10,
        text_feedback_sentiment=10.0,
        support_ticket_sentiment=10.0,
        # Consistency metrics
        daily_streak_days=7,
        weekly_frequency=1.0,
        device_consistency=1.0,
        calculation_date=datetime.utcnow()
    )


@pytest.fixture
def critical_user_data():
    """Fixture for a critical user with low engagement."""
    return UserActivityData(
        user_id="test-critical-user",
        # Engagement metrics - all zeros
        sessions_per_week=0.0,
        avg_session_duration_minutes=0.0,
        messages_per_week=0.0,
        # Feature adoption metrics - all zeros
        agents_created=0,
        agents_active_last_7d=0,
        memories_stored=0,
        projects_created=0,
        search_queries_per_week=0.0,
        # Feedback sentiment - neutral/low
        in_app_rating=1.0,
        nps_score=0,
        text_feedback_sentiment=0.0,
        support_ticket_sentiment=0.0,
        # Consistency metrics - all zeros
        daily_streak_days=0,
        weekly_frequency=0.0,
        device_consistency=0.0,
        calculation_date=datetime.utcnow()
    )


class TestEngagementScore:
    """Test engagement score calculation."""

    def test_healthy_engagement(self, calculator, healthy_user_data):
        """Healthy user should get high engagement score."""
        score = calculator.calculate_engagement_score(healthy_user_data)
        assert score == 10.0

    def test_critical_engagement(self, calculator, critical_user_data):
        """Critical user should get zero engagement score."""
        score = calculator.calculate_engagement_score(critical_user_data)
        assert score == 0.0

    def test_partial_engagement(self, calculator):
        """Test partial engagement metrics."""
        data = UserActivityData(
            user_id="test-partial",
            sessions_per_week=2.5,  # Half of target
            avg_session_duration_minutes=7.5,  # Half of target
            messages_per_week=10.0,  # Half of target
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_engagement_score(data)
        # Half metrics should give approximately half score (5.0)
        assert score == 5.0

    def test_engagement_capped_at_10(self, calculator):
        """Excessive engagement should cap at 10."""
        data = UserActivityData(
            user_id="test-excessive",
            sessions_per_week=50.0,  # 10x target
            avg_session_duration_minutes=150.0,  # 10x target
            messages_per_week=200.0,  # 10x target
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_engagement_score(data)
        assert score == 10.0


class TestFeatureAdoptionScore:
    """Test feature adoption score calculation."""

    def test_healthy_adoption(self, calculator, healthy_user_data):
        """Healthy user should get high feature adoption score."""
        score = calculator.calculate_feature_adoption_score(healthy_user_data)
        assert score == 10.0

    def test_critical_adoption(self, calculator, critical_user_data):
        """Critical user should get zero feature adoption score."""
        score = calculator.calculate_feature_adoption_score(critical_user_data)
        assert score == 0.0

    def test_partial_adoption(self, calculator):
        """Test partial feature adoption."""
        data = UserActivityData(
            user_id="test-partial",
            agents_created=1,  # Half of target (2)
            memories_stored=2.5,  # Half of target (5)
            projects_created=0.5,  # Half of target (1)
            search_queries_per_week=1.5,  # Half of target (3)
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_feature_adoption_score(data)
        # Half metrics should give approximately half score (5.0)
        assert score == 5.0

    def test_adoption_capped_at_10(self, calculator):
        """Excessive adoption should cap at 10."""
        data = UserActivityData(
            user_id="test-excessive",
            agents_created=20,  # 10x target
            memories_stored=50,  # 10x target
            projects_created=10,  # 10x target
            search_queries_per_week=30.0,  # 10x target
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_feature_adoption_score(data)
        assert score == 10.0


class TestFeedbackSentimentScore:
    """Test feedback sentiment score calculation."""

    def test_perfect_feedback(self, calculator, healthy_user_data):
        """Perfect feedback should give max score."""
        score = calculator.calculate_feedback_sentiment_score(healthy_user_data)
        assert score == 10.0

    def test_no_feedback_returns_neutral(self, calculator):
        """No feedback data should return neutral score (5.0)."""
        data = UserActivityData(
            user_id="test-no-feedback",
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_feedback_sentiment_score(data)
        assert score == 5.0

    def test_partial_feedback(self, calculator):
        """Test partial feedback with only some metrics."""
        data = UserActivityData(
            user_id="test-partial",
            in_app_rating=2.5,  # Half of 5 (scaled to 5/10)
            nps_score=5,  # Half of 10
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_feedback_sentiment_score(data)
        # Half metrics should give approximately half score (5.0)
        assert score == 5.0

    def test_feedback_capped_at_10(self, calculator):
        """Excessive feedback should cap at 10."""
        data = UserActivityData(
            user_id="test-excessive",
            in_app_rating=10.0,  # Above max (should be capped)
            nps_score=20,  # Above max (should be capped)
            text_feedback_sentiment=20.0,  # Above max
            support_ticket_sentiment=20.0,  # Above max
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_feedback_sentiment_score(data)
        assert score <= 10.0


class TestConsistencyScore:
    """Test consistency score calculation."""

    def test_perfect_consistency(self, calculator, healthy_user_data):
        """Perfect consistency should give max score."""
        score = calculator.calculate_consistency_score(healthy_user_data)
        assert score == 10.0

    def test_no_consistency(self, calculator, critical_user_data):
        """No consistency metrics should give zero score."""
        score = calculator.calculate_consistency_score(critical_user_data)
        assert score == 0.0

    def test_partial_consistency(self, calculator):
        """Test partial consistency metrics."""
        data = UserActivityData(
            user_id="test-partial",
            daily_streak_days=3.5,  # Half of target (7)
            weekly_frequency=0.5,  # Half of target (1.0)
            device_consistency=0.4,  # Half of target (0.8)
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_consistency_score(data)
        # Half metrics should give approximately half score (5.0)
        assert score == 5.0

    def test_consistency_capped_at_10(self, calculator):
        """Excessive consistency should cap at 10."""
        data = UserActivityData(
            user_id="test-excessive",
            daily_streak_days=70,  # 10x target
            weekly_frequency=1.0,  # Max
            device_consistency=1.0,  # Max
            calculation_date=datetime.utcnow()
        )
        score = calculator.calculate_consistency_score(data)
        assert score == 10.0


class TestHealthScoreCalculation:
    """Test complete health score calculation."""

    def test_healthy_user_champion_tier(self, calculator, healthy_user_data):
        """Healthy user should be in Champion tier (9.0-10.0)."""
        result = calculator.calculate_health_score(healthy_user_data)
        assert result["health_score"] == 10.0
        assert result["health_tier"] == "Champion"

    def test_critical_user_critical_tier(self, calculator, critical_user_data):
        """Critical user should be in Critical tier (0.0-4.9)."""
        result = calculator.calculate_health_score(critical_user_data)
        assert result["health_tier"] == "Critical"

    def test_health_tier_boundaries(self, calculator):
        """Test all health tier boundaries."""
        # Champion boundary (9.0)
        champion_data = UserActivityData(
            user_id="test-champion",
            sessions_per_week=4.5,  # High engagement
            avg_session_duration_minutes=13.5,
            messages_per_week=18.0,
            agents_created=2,
            memories_stored=5,
            projects_created=1,
            search_queries_per_week=3.0,
            in_app_rating=5.0,
            nps_score=10,
            daily_streak_days=7,
            weekly_frequency=1.0,
            device_consistency=1.0,
            calculation_date=datetime.utcnow()
        )
        result = calculator.calculate_health_score(champion_data)
        assert result["health_score"] >= 9.0
        assert result["health_tier"] == "Champion"

        # Healthy boundary (7.0)
        healthy_boundary_data = UserActivityData(
            user_id="test-healthy-boundary",
            sessions_per_week=3.5,
            avg_session_duration_minutes=10.5,
            messages_per_week=14.0,
            agents_created=1.5,
            memories_stored=4,
            projects_created=0.75,
            search_queries_per_week=2.25,
            in_app_rating=3.5,
            nps_score=7,
            daily_streak_days=5,
            weekly_frequency=0.75,
            device_consistency=0.75,
            calculation_date=datetime.utcnow()
        )
        result = calculator.calculate_health_score(healthy_boundary_data)
        assert result["health_score"] >= 7.0
        assert result["health_tier"] in ["Champion", "Healthy"]

        # At-Risk boundary (5.0)
        at_risk_data = UserActivityData(
            user_id="test-at-risk",
            sessions_per_week=2.5,
            avg_session_duration_minutes=7.5,
            messages_per_week=10.0,
            agents_created=1,
            memories_stored=2.5,
            projects_created=0.5,
            search_queries_per_week=1.5,
            in_app_rating=2.5,
            nps_score=5,
            daily_streak_days=3.5,
            weekly_frequency=0.5,
            device_consistency=0.5,
            calculation_date=datetime.utcnow()
        )
        result = calculator.calculate_health_score(at_risk_data)
        assert result["health_score"] >= 5.0
        assert result["health_tier"] in ["Healthy", "At-Risk"]

        # Critical boundary (<5.0)
        critical_boundary_data = UserActivityData(
            user_id="test-critical-boundary",
            sessions_per_week=1.0,
            avg_session_duration_minutes=3.0,
            messages_per_week=4.0,
            agents_created=0,
            memories_stored=1,
            projects_created=0,
            search_queries_per_week=0.5,
            in_app_rating=1.0,
            nps_score=2,
            daily_streak_days=1,
            weekly_frequency=0.1,
            device_consistency=0.1,
            calculation_date=datetime.utcnow()
        )
        result = calculator.calculate_health_score(critical_boundary_data)
        assert result["health_score"] < 5.0
        assert result["health_tier"] == "Critical"

    def test_health_score_components_breakdown(self, calculator, healthy_user_data):
        """Test that component breakdown is included in result."""
        result = calculator.calculate_health_score(healthy_user_data)

        assert "components" in result
        assert "engagement" in result["components"]
        assert "feature_adoption" in result["components"]
        assert "feedback_sentiment" in result["components"]
        assert "consistency" in result["components"]

        assert "calculation_details" in result
        assert "weights" in result["calculation_details"]
        assert "component_scores" in result["calculation_details"]

    def test_health_score_weighted_sum(self, calculator, healthy_user_data):
        """Verify health score is correctly weighted sum of components."""
        result = calculator.calculate_health_score(healthy_user_data)

        components = result["components"]
        weights = result["calculation_details"]["weights"]

        # Manual calculation
        expected_score = (
            components["engagement"] * weights["engagement"] +
            components["feature_adoption"] * weights["feature_adoption"] +
            components["feedback_sentiment"] * weights["feedback_sentiment"] +
            components["consistency"] * weights["consistency"]
        )

        # Should match (within rounding)
        assert abs(result["health_score"] - expected_score) < 0.01


class TestBatchHealthScoreCalculation:
    """Test batch health score calculation."""

    def test_single_user_batch(self, calculator, healthy_user_data):
        """Batch with single user should work."""
        results = calculator.calculate_batch_health_scores([healthy_user_data])
        assert len(results) == 1
        assert results[0]["health_score"] == 10.0

    def test_multiple_users_batch(self, calculator, healthy_user_data, critical_user_data):
        """Batch with multiple users should return correct scores."""
        results = calculator.calculate_batch_health_scores([
            healthy_user_data,
            critical_user_data
        ])
        assert len(results) == 2
        assert results[0]["health_score"] == 10.0
        assert results[1]["health_tier"] == "Critical"

    def test_empty_batch(self, calculator):
        """Empty batch should return empty list."""
        results = calculator.calculate_batch_health_scores([])
        assert results == []

    def test_large_batch(self, calculator, healthy_user_data):
        """Batch with many users should handle efficiently."""
        # Create 100 users
        users = [
            UserActivityData(
                user_id=f"test-batch-{i}",
                sessions_per_week=5.0 * (i % 2),  # Alternate 0 and 5
                avg_session_duration_minutes=15.0 * (i % 2),
                messages_per_week=20.0 * (i % 2),
                agents_created=2 * (i % 2),
                memories_stored=5 * (i % 2),
                projects_created=1 * (i % 2),
                search_queries_per_week=3.0 * (i % 2),
                in_app_rating=5.0 * (i % 2),
                nps_score=10 * (i % 2),
                daily_streak_days=7 * (i % 2),
                weekly_frequency=1.0 * (i % 2),
                device_consistency=1.0 * (i % 2),
                calculation_date=datetime.utcnow()
            )
            for i in range(100)
        ]

        results = calculator.calculate_batch_health_scores(users)
        assert len(results) == 100


class TestHealthScoreFormula:
    """Verify health score formula matches documented specification."""

    def test_formula_weights(self, calculator):
        """Verify formula weights match specification."""
        assert calculator.engagement_weight == 0.4
        assert calculator.feature_adoption_weight == 0.3
        assert calculator.feedback_sentiment_weight == 0.2
        assert calculator.consistency_weight == 0.1

    def test_formula_total_weight(self, calculator):
        """Verify total weight sums to 1.0."""
        total_weight = (
            calculator.engagement_weight +
            calculator.feature_adoption_weight +
            calculator.feedback_sentiment_weight +
            calculator.consistency_weight
        )
        assert total_weight == 1.0
