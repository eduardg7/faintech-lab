"""Integration tests for event tracking analytics service.

Tests verify that:
- Analytics service initializes correctly with/without PostHog
- Event tracking functions work correctly
- Events are captured with proper properties
- Graceful fallback when PostHog not configured
"""

import pytest
from unittest.mock import Mock,patch, MagicMock
from datetime import datetime, timezone

from app.services.analytics import AnalyticsService


class TestAnalyticsService:
    """Test analytics service initialization and event tracking."""

    def test_service_initialization_without_posthog(self):
        """Test that service initializes correctly when PostHog is not configured."""
        with patch.dict('os.environ', {}, clear=True):
            service = AnalyticsService()
            assert service.enabled is False
            assert service._client is None

    def test_service_initialization_with_posthog(self):
        """Test that service initializes correctly when PostHog is configured."""
        with patch.dict('os.environ', {
            'POSTHOG_API_KEY': 'test_key',
            'POSTHOG_HOST': 'https://test.posthog.com',
            'POSTHOG_ENABLED': 'true'
        }, clear=True):
            # Mock PostHog client
            with patch('app.services.analytics.Posthog') as mock_posthog:
                mock_client = MagicMock()
                mock_posthog.return_value = mock_client
                
                service = AnalyticsService()
                
                # Service should be enabled
                assert service.enabled is True
                assert service._client is not None

    def test_track_signup_event(self):
        """Test that track_signup works correctly."""
        with patch.dict('os.environ', {
            'POSTHOG_API_KEY': 'test_key',
            'POSTHOG_ENABLED': 'true'
        }, clear=True):
            with patch('app.services.analytics.Posthog') as mock_posthog:
                mock_client = MagicMock()
                mock_posthog.return_value = mock_client
                
                service = AnalyticsService()
                
                # Track signup
                result = service.track_signup(
                    user_id='user_123',
                    email='test@example.com',
                    workspace_id='workspace_456'
                )
                
                # Verify event was tracked
                assert result is True
                # Verify capture was called
                mock_client.capture.assert_called_once()
                
                # Verify identify was called
                mock_client.identify.assert_called_once()

    def test_track_login_event(self):
        """Test that track_user_login works correctly."""
        with patch.dict('os.environ', {
            'POSTHOG_API_KEY': 'test_key',
            'POSTHOG_ENABLED': 'true'
        }, clear=True):
            with patch('app.services.analytics.Posthog') as mock_posthog:
                mock_client = MagicMock()
                mock_posthog.return_value = mock_client
                
                service = AnalyticsService()
                
                # Track login
                result = service.track_user_login(
                    user_id='user_123',
                    auth_method='jwt'
                )
                
                # Verify event was tracked
                assert result is True
                mock_client.capture.assert_called_once()

    def test_track_memory_created_event(self):
        """Test that track_memory_created works correctly."""
        with patch.dict('os.environ', {
            'POSTHOG_API_KEY': 'test_key',
            'POSTHOG_ENABLED': 'true'
        }, clear=True):
            with patch('app.services.analytics.Posthog') as mock_posthog:
                mock_client = MagicMock()
                mock_posthog.return_value = mock_client
                
                service = AnalyticsService()
                
                # Track memory creation
                result = service.track_memory_created(
                    user_id='user_123',
                    workspace_id='workspace_456',
                    memory_type='outcome',
                    content_length=500
                )
                
                # Verify event was tracked
                assert result is True
                mock_client.capture.assert_called_once()

    def test_track_search_executed_event(self):
        """Test that track_search_executed works correctly."""
        with patch.dict('os.environ', {
            'POSTHOG_API_KEY': 'test_key',
            'POSTHOG_ENABLED': 'true'
        }, clear=True):
            with patch('app.services.analytics.Posthog') as mock_posthog:
                mock_client = MagicMock()
                mock_posthog.return_value = mock_client
                
                service = AnalyticsService()
                
                # Track search execution
                result = service.track_search_executed(
                    user_id='user_123',
                    query='test query',
                    results_count=10,
                    search_type='keyword'
                )
                
                # Verify event was tracked
                assert result is True
                mock_client.capture.assert_called_once()

    def test_fallback_when_posthog_disabled(self):
        """Test that events are logged but not sent when PostHog is disabled."""
        with patch.dict('os.environ', {}, clear=True):
            service = AnalyticsService()
            
            # Try to track event
            result = service.track_signup(
                user_id='user_123',
                email='test@example.com'
            )
            
            # Should return False (not tracked)
            assert result is False

    def test_event_properties_include_required_fields(self):
        """Test that tracked events include required properties."""
        with patch.dict('os.environ', {
            'POSTHOG_API_KEY': 'test_key',
            'POSTHOG_ENABLED': 'true'
        }, clear=True):
            with patch('app.services.analytics.Posthog') as mock_posthog:
                mock_client = MagicMock()
                mock_posthog.return_value = mock_client
                
                service = AnalyticsService()
                
                # Track signup
                service.track_signup(
                    user_id='user_123',
                    email='test@example.com',
                    workspace_id='workspace_456'
                )
                
                # Verify capture was called with correct properties
                call_args = mock_client.capture.call_args
                assert call_args is not None
                
                # Verify distinct_id
                assert call_args[1]['distinct_id'] == 'user_123'
                
                # Verify event name
                assert call_args[1]['event'] == 'user_signup'
                
                # Verify properties include workspace_id
                properties = call_args[1]['properties']
                assert properties['workspace_id'] == 'workspace_456'
                assert properties['email'] == 'test@example.com'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
