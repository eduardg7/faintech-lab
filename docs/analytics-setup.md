# PostHog Analytics Setup Guide

**Task:** OS-20260321012826-D979 - Event Tracking for Beta Launch  
**Last Updated:** 2026-03-23

## Overview

Event tracking is integrated into LAB backend for beta launch metrics. This guide explains how to configure PostHog analytics.

## Prerequisites

1. PostHog account (free tier available at https://posthog.com)
2. PostHog project API key

## Configuration Steps

### 1. Get PostHog API Key

1. Log in to your PostHog dashboard at https://app.posthog.com
2. Navigate to Project Settings → API Keys
3. Copy your Project API Key (starts with `phc_`)

### 2. Configure Environment Variables

Add to your `.env` file:

```bash
# PostHog Analytics
POSTHOG_API_KEY=phc_your_actual_api_key_here
POSTHOG_HOST=https://app.posthog.com
POSTHOG_ENABLED=true
```

**Important:** 
- Replace `phc_your_actual_api_key_here` with your actual PostHog API key
- Never commit `.env` file to git (it's in `.gitignore`)
- Use `.env.example` as template

### 3. Install PostHog SDK (Already Done)

PostHog Python SDK is already in `requirements.txt`:

```python
posthog-node==4.18.0
```

### 4. Verify Installation

The analytics service will:
- Initialize PostHog client if `POSTHOG_API_KEY` is set
- Fall back to logging if PostHog is not configured
- Track events in development mode (logged but not sent)

## Events Tracked

### Core Beta Events (6 total)

✅ **user_signup** - When a new user registers
- Properties: `user_id`, `email`, `workspace_id`
- Location: `/auth/register` endpoint

✅ **user_login** - When a user logs in
- Properties: `user_id`, `auth_method`
- Location: `/auth/login` endpoint

✅ **memory_created** - When a memory is stored
- Properties: `user_id`, `workspace_id`, `memory_type`, `content_length`
- Location: `POST /memories` endpoint

✅ **search_executed** - When a search is performed
- Properties: `user_id`, `query_length`, `results_count`, `search_type`
- Location: 
  - `GET /search/keyword`
  - `POST /search/hybrid`
  - `POST /search/semantic`

❌ **email_verified** - Not implemented (MVP auto-verifies users)
- Reason: Auth flow uses auto-verify for MVP
- Future: Add email verification endpoint if needed

❌ **agent_created** - Not implemented (no endpoint exists)
- Reason: No POST endpoint to create agents (only GET/list)
- Future: Add agent creation endpoint if needed

## Implementation Details

### Analytics Service

Location: `app/services/analytics.py`

Features:
- PostHog integration with graceful fallback
- Environment-based configuration
- Singleton instance
- Convenience methods for each event type

### Routes Instrumented

1. **auth.py** - Authentication routes
   - `/auth/register` → `analytics.track_signup()`
   - `/auth/login` → `analytics.track_user_login()`

2. **memories.py** - Memory management
   - `POST /memories` → `analytics.track_memory_created()`

3. **search.py, hybrid_search.py, semantic.py** - Search endpoints
   - All search endpoints → `analytics.track_search_executed()`

## Testing

Integration tests: `tests/test_analytics_integration.py`

Tests verify:
- Service initialization with/without PostHog
- Event tracking for all implemented event types
- Graceful fallback when PostHog disabled
- Event properties are captured correctly

**Note:** Tests require proper environment setup with all dependencies installed.

## Monitoring

### PostHog Dashboard

Monitor events in PostHog:
1. Navigate to Events tab
2. Filter by event name (e.g., `user_signup`)
3. View event properties and trends

### Key Metrics to Track

For beta launch (Mar 24):
- **Signups** - Daily signup count
- **Activation** - Users who created first memory within 24h
- **Retention** - Users who returned within 7 days
- **Search Usage** - Search queries per user
- **Memory Creation** - Memories created per user

### Alerts to Set Up

In PostHog dashboard:
1. **Low Signup Alert** - < 5 signups/day
2. **High Churn Alert** - > 50% users inactive after 3 days
3. **Search Failure Alert** - 0 searches in 24h (might indicate bug)

## Troubleshooting

### Events Not Appearing in PostHog

1. Check `POSTHOG_API_KEY` is set in `.env`
2. Verify `POSTHOG_ENABLED=true`
3. Check logs for errors: `tail -f amc-backend/backend.log | grep PostHog`
4. Verify service initialization on startup

### Development Mode

Events are logged but not sent to PostHog:
```
[Analytics] Track: user_signup for user_123
```

This is expected when `POSTHOG_API_KEY` is not set.

### Testing Locally

Set environment variable for testing:
```bash
export POSTHOG_API_KEY=phc_test_key
export POSTHOG_ENABLED=true
pytest tests/test_analytics_integration.py
```

## Security Considerations

- ✅ API key stored in `.env` (not in code)
- ✅ `.env` in `.gitignore`
- ✅ Events don't contain sensitive data (only IDs and metadata)
- ✅ User passwords never tracked
- ✅ Memory content not tracked (only content length)

## Cost

PostHog free tier includes:
- 1M events/month free
- Unlimited team members
- 7-day data retention

For beta launch, this should be sufficient.

## Next Steps

Post-beta:
1. Add email verification flow → track `email_verified` event
2. Add agent creation endpoint → track `agent_created` event
3. Set up PostHog dashboards for key metrics
4. Configure alerts for critical thresholds
5. Add funnels analysis in PostHog

## Support

- PostHog docs: https://posthog.com/docs
- Project lead: @faintech-backend
- Related task: OS-20260321012826-D979
