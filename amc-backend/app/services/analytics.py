"""PostHog Analytics Service for LAB Beta Experiments.

Provides event tracking for beta launch metrics using PostHog.
Events are tracked for:
- user_signup: New user registration
- email_verified: Email confirmation
- agent_created: New agent workspace created
- memory_created: Memory stored in workspace
- search_executed: Hybrid search performed
- user_login: User authentication

Configuration (via environment):
- POSTHOG_API_KEY: PostHog project API key (required for tracking)
- POSTHOG_HOST: PostHog instance URL (default: https://app.posthog.com)
- POSTHOG_ENABLED: Enable/disable tracking (default: true if API key set)

Task: OS-20260321012826-D979 - P0 Event Tracking for LAB Experiments
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from functools import lru_cache

logger = logging.getLogger(__name__)


@lru_cache()
def _get_posthog_client():
    """Lazy-load PostHog client to avoid import errors if not installed."""
    try:
        from posthog import Posthog
        return Posthog
    except ImportError:
        logger.warning("posthog package not installed. Event tracking disabled.")
        return None


class AnalyticsService:
    """PostHog-backed analytics service for beta event tracking.

    Falls back to logging if PostHog is not configured.
    """

    def __init__(self):
        self.api_key = os.getenv("POSTHOG_API_KEY")
        self.host = os.getenv("POSTHOG_HOST", "https://app.posthog.com")
        self.enabled = os.getenv("POSTHOG_ENABLED", "true" if self.api_key else "false").lower() == "true"
        self._client = None

        if self.enabled and self.api_key:
            Posthog = _get_posthog_client()
            if Posthog:
                self._client = Posthog(
                    project_api_key=self.api_key,
                    host=self.host,
                )
                logger.info(f"PostHog analytics initialized (host={self.host})")
            else:
                self.enabled = False
                logger.warning("PostHog client not available. Tracking disabled.")

    def track(
        self,
        event: str,
        distinct_id: str,
        properties: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
    ) -> bool:
        """Track an analytics event.

        Args:
            event: Event name (e.g., "user_signup", "memory_created")
            distinct_id: Unique identifier for the user/entity
            properties: Additional event properties
            timestamp: Event timestamp (defaults to now)

        Returns:
            True if event was tracked successfully, False otherwise
        """
        if not self.enabled:
            logger.debug(f"Analytics disabled. Would track: {event} for {distinct_id}")
            return False

        props = properties or {}
        props["source"] = "amc-backend"
        props["environment"] = os.getenv("ENVIRONMENT", "development")

        try:
            if self._client:
                self._client.capture(
                    distinct_id=distinct_id,
                    event=event,
                    properties=props,
                    timestamp=timestamp or datetime.now(timezone.utc),
                )
                logger.info(f"Tracked event: {event} for {distinct_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to track event {event}: {e}")

        return False

    def identify(
        self,
        distinct_id: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Identify a user with additional properties.

        Args:
            distinct_id: Unique identifier for the user
            properties: User properties (email, name, plan, etc.)

        Returns:
            True if identification was successful, False otherwise
        """
        if not self.enabled or not self._client:
            return False

        try:
            self._client.identify(
                distinct_id=distinct_id,
                properties=properties or {},
            )
            logger.info(f"Identified user: {distinct_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to identify user {distinct_id}: {e}")
            return False

    def track_signup(
        self,
        user_id: str,
        email: str,
        workspace_id: Optional[str] = None,
        utm_source: Optional[str] = None,
        utm_medium: Optional[str] = None,
        utm_campaign: Optional[str] = None,
        utm_content: Optional[str] = None,
        utm_term: Optional[str] = None,
        utm_referrer: Optional[str] = None,
    ) -> bool:
        """Track user signup event.

        Core Event 1/6: user_signup

        Week 2 GTM: Include UTM parameters for channel attribution.
        """
        properties = {
            "email": email,
            "workspace_id": workspace_id,
        }

        # Add UTM parameters for Week 2 GTM channel attribution
        if utm_source:
            properties["utm_source"] = utm_source
        if utm_medium:
            properties["utm_medium"] = utm_medium
        if utm_campaign:
            properties["utm_campaign"] = utm_campaign
        if utm_content:
            properties["utm_content"] = utm_content
        if utm_term:
            properties["utm_term"] = utm_term
        if utm_referrer:
            properties["utm_referrer"] = utm_referrer

        self.identify(user_id, {
            "email": email,
            "signup_date": datetime.now(timezone.utc).isoformat(),
        })
        return self.track(
            event="user_signup",
            distinct_id=user_id,
            properties=properties,
        )

    def track_email_verified(
        self,
        user_id: str,
        email: str,
    ) -> bool:
        """Track email verification event.

        Core Event 2/6: email_verified
        """
        return self.track(
            event="email_verified",
            distinct_id=user_id,
            properties={
                "email": email,
            },
        )

    def track_agent_created(
        self,
        user_id: str,
        agent_id: str,
        agent_name: Optional[str] = None,
    ) -> bool:
        """Track agent creation event.

        Core Event 3/6: agent_created
        """
        return self.track(
            event="agent_created",
            distinct_id=user_id,
            properties={
                "agent_id": agent_id,
                "agent_name": agent_name,
            },
        )

    def track_memory_created(
        self,
        user_id: str,
        workspace_id: str,
        memory_type: Optional[str] = None,
        content_length: Optional[int] = None,
    ) -> bool:
        """Track memory creation event.

        Core Event 4/6: memory_created
        """
        return self.track(
            event="memory_created",
            distinct_id=user_id,
            properties={
                "workspace_id": workspace_id,
                "memory_type": memory_type,
                "content_length": content_length,
            },
        )

    def track_search_executed(
        self,
        user_id: str,
        query: str,
        results_count: int,
        search_type: Optional[str] = None,
    ) -> bool:
        """Track search execution event.

        Core Event 5/6: search_executed
        """
        return self.track(
            event="search_executed",
            distinct_id=user_id,
            properties={
                "query_length": len(query),
                "results_count": results_count,
                "search_type": search_type or "hybrid",
            },
        )

    def track_user_login(
        self,
        user_id: str,
        auth_method: Optional[str] = None,
    ) -> bool:
        """Track user login event.

        Core Event 6/6: user_login
        """
        return self.track(
            event="user_login",
            distinct_id=user_id,
            properties={
                "auth_method": auth_method or "jwt",
            },
        )


# Singleton instance
analytics = AnalyticsService()
