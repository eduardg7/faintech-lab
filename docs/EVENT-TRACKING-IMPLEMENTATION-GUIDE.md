# Event Tracking Implementation Guide — PostHog

> **Status:** READY FOR IMPLEMENTATION
> **Priority:** P0 CRITICAL
> **Deadline:** Before Mar 23 (beta end) — TODAY
> **Owner:** CPO (product decision) → devops + faintech-backend (implementation)

---

## Product Decision (COMPLETE)

**Selected Solution:** PostHog

**Rationale:**
- Open-source option available (self-host or cloud)
- Strong event tracking + analytics
- Good DX (developer experience)
- GDPR compliant
- Free tier sufficient for beta

---

## Required Events (6 Core Events)

### 1. user_signup
**Trigger:** User completes registration
**Properties:**
- `user_id`: string (required)
- `email`: string (required)
- `signup_method`: string (email/google/github)
- `timestamp`: datetime (auto)

### 2. email_verified
**Trigger:** User confirms email address
**Properties:**
- `user_id`: string (required)
- `email`: string (required)
- `timestamp`: datetime (auto)

### 3. agent_created
**Trigger:** User creates new agent
**Properties:**
- `user_id`: string (required)
- `agent_id`: string (required)
- `agent_name`: string
- `agent_type`: string (if applicable)
- `timestamp`: datetime (auto)

### 4. memory_created
**Trigger:** Agent stores new memory
**Properties:**
- `user_id`: string (required)
- `agent_id`: string (required)
- `memory_id`: string (required)
- `memory_type`: string (pattern/fact/preference)
- `workspace_id`: string
- `timestamp`: datetime (auto)

### 5. search_executed
**Trigger:** Agent searches memories
**Properties:**
- `user_id`: string (required)
- `agent_id`: string (required)
- `query`: string (search terms)
- `results_count`: integer
- `latency_ms`: integer
- `timestamp`: datetime (auto)

### 6. user_login
**Trigger:** User authenticates
**Properties:**
- `user_id`: string (required)
- `login_method`: string (email/google/github)
- `timestamp`: datetime (auto)

---

## Implementation Steps

### Step 1: PostHog Account Setup (devops)
**Time estimate:** 30 minutes

1. Create PostHog account (cloud or self-hosted)
2. Generate project API key
3. Add environment variables to deployment:
   - `NEXT_PUBLIC_POSTHOG_KEY=<api_key>`
   - `NEXT_PUBLIC_POSTHOG_HOST=<host_url>`
4. Document credentials in team vault

### Step 2: SDK Integration (faintech-backend)
**Time estimate:** 1 hour

Frontend (Next.js):
```bash
npm install posthog-js
```

Backend (FastAPI):
```bash
pip install posthog
```

### Step 3: Event Instrumentation (faintech-backend)
**Time estimate:** 2-3 hours

Instrument all 6 events at their trigger points:
- Auth endpoints (signup, verify, login)
- Agent creation endpoint
- Memory creation endpoint
- Search endpoint

### Step 4: Staging Verification (devops + faintech-backend)
**Time estimate:** 30 minutes

1. Deploy to staging
2. Execute test user flows
3. Verify events appear in PostHog dashboard
4. Validate all required properties captured

### Step 5: Production Deployment (devops)
**Time estimate:** 30 minutes

1. Deploy to production
2. Monitor PostHog dashboard for live events
3. Verify beta users generating events

---

## Acceptance Criteria Verification

- [ ] PostHog account created and API keys generated
- [ ] SDK integrated in frontend and backend
- [ ] All 6 events instrumented with required properties
- [ ] Events verified in staging environment
- [ ] Production deployment completed before Mar 23
- [ ] Beta users generating tracked events

---

## Risk Mitigation

**If PostHog unavailable:**
- Fallback: Simple event log to database (user_events table)
- Minimum viable: Log events with JSON payload to file
- Post-beta: Migrate to proper tracking system

**If time runs out:**
- Priority: user_signup, agent_created, memory_created (core funnel)
- Defer: search_executed (nice-to-have for beta)

---

## Success Metrics (Post-Beta)

- Event capture rate: >95% of user actions
- Data completeness: All required properties present
- Latency: <100ms event submission
- Dashboard: Real-time visibility into beta user behavior

---

**Created by:** CPO
**Date:** 2026-03-23
**Status:** Ready for devops + faintech-backend execution
