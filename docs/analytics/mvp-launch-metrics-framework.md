# MVP Launch Metrics Framework

**Task:** LAB-20260320001131-6129DD32B858
**Owner:** CPO (intervention)
**Business Goal:** 5 paying customers by Apr 20, 2026
**Beta Launch:** Mar 24, 2026 (4 days)
**Created:** 2026-03-20 03:35 EET

---

## Executive Summary

This framework defines the metrics we will track during the AMC MVP beta launch to measure:
1. User onboarding success
2. Product engagement and retention
3. Technical health and reliability
4. Conversion toward paying customers

All metrics align with our primary business goal: **5 paying customers by Apr 20, 2026**.

---

## Core Launch Metrics

### 1. Onboarding Completion Rate

**Definition:** Percentage of users who complete the full onboarding flow (sign up → first memory created → first query executed)

**Target:** 60-80% completion rate

**Measurement Method:**
- Analytics event: `onboarding_completed` fired when user creates first memory
- Funnel tracking: `signup_created` → `onboarding_started` → `first_memory_created` → `first_query_executed`
- Dashboard: Conversion funnel visualization

**Data Collection:**
```javascript
// Track onboarding steps
analytics.track('signup_created', { user_id, utm_source });
analytics.track('onboarding_started', { user_id });
analytics.track('first_memory_created', { user_id, memory_type });
analytics.track('first_query_executed', { user_id, query_type });
analytics.track('onboarding_completed', { user_id, duration_seconds });
```

**Business Impact:** High onboarding completion = users understand value = higher conversion probability

---

### 2. Active User Count (DAU/MAU)

**Definition:** Daily Active Users (DAU) and Monthly Active Users (MAU) based on meaningful engagement (at least 1 memory operation or query per day/month)

**Target:**
- DAU: 10-20 users by Day 7
- MAU: 50-100 users by Day 30
- DAU/MAU Ratio: >20% (indicates habit formation)

**Measurement Method:**
- Database query: Count distinct users with `last_active_at` within time window
- API endpoint: `GET /api/v1/analytics/active-users?period=daily|monthly`
- Dashboard: Time-series chart with DAU, MAU, ratio

**Data Collection:**
```sql
-- DAU: Users active in last 24 hours
SELECT COUNT(DISTINCT user_id)
FROM user_activity
WHERE last_active_at >= NOW() - INTERVAL '24 hours';

-- MAU: Users active in last 30 days
SELECT COUNT(DISTINCT user_id)
FROM user_activity
WHERE last_active_at >= NOW() - INTERVAL '30 days';
```

**Business Impact:** Active users = product-market fit signal = conversion pipeline

---

### 3. Engagement Frequency

**Definition:** Average number of memory operations (create/read/update/delete) and queries per active user per day

**Target:**
- Memory operations: >5 per user per day
- Queries: >10 per user per day
- Session duration: >5 minutes average

**Measurement Method:**
- API analytics: Log all memory CRUD operations with timestamps
- Event tracking: `memory_created`, `memory_read`, `query_executed`
- Dashboard: Per-user engagement histogram + averages

**Data Collection:**
```javascript
// Track engagement events
analytics.track('memory_created', { user_id, memory_type, tokens });
analytics.track('memory_read', { user_id, memory_id });
analytics.track('memory_updated', { user_id, memory_id });
analytics.track('query_executed', { user_id, query_type, latency_ms, results_count });
```

**Business Impact:** High engagement = core value delivered = willingness to pay

---

### 4. Technical Error Rate

**Definition:** Percentage of API requests that result in 4xx/5xx errors

**Target:** <1% error rate for all API endpoints

**Measurement Method:**
- API middleware: Log all request/response status codes
- Aggregation: Calculate error rate per endpoint, per hour
- Alerting: Trigger if error rate >1% for any endpoint

**Data Collection:**
```javascript
// Middleware to track errors
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    analytics.track('api_request', {
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration_ms: duration,
      user_id: req.user?.id
    });
  });
  next();
});
```

**Business Impact:** Low errors = reliable product = trust = conversion

---

### 5. Test Coverage Trend

**Definition:** Percentage of code covered by automated tests, tracked over time

**Target:** Maintain >80% coverage, no regressions

**Current State:** 11.52% line coverage (1970 tests, 8 failing)

**Measurement Method:**
- CI/CD pipeline: Run `npm test -- --coverage` on every PR
- Report: Coverage summary in build output
- Dashboard: Coverage trend chart (daily/weekly)

**Data Collection:**
```bash
# Run coverage report
npm test -- --coverage --coverageReporters=json-summary

# Extract coverage percentage
cat coverage/coverage-summary.json | jq '.total.lines.pct'
```

**Business Impact:** High coverage = fewer bugs = better user experience

---

## Dashboard Specification

### Primary Dashboard: Beta Launch Metrics

**Layout:** Single-page dashboard with 4 sections

**Section 1: Onboarding Funnel**
- Visualization: Funnel chart
- Steps: Sign-up → Onboarding Started → First Memory → First Query → Completed
- Metrics: Conversion rate between steps, drop-off points

**Section 2: User Activity**
- Visualization: Time-series chart (7-day rolling)
- Metrics: DAU, MAU, DAU/MAU ratio
- Breakdown: By acquisition source (HN, LinkedIn, Twitter, etc.)

**Section 3: Engagement Metrics**
- Visualization: Bar charts + histograms
- Metrics: Memory operations/day, queries/day, session duration
- Distribution: Per-user engagement levels

**Section 4: Technical Health**
- Visualization: Status indicators + trend lines
- Metrics: Error rate, avg latency, test coverage
- Alerts: Red/yellow/green indicators for thresholds

**Implementation:**
- Frontend: React component at `/dashboard/metrics`
- Backend: `GET /api/v1/analytics/dashboard` returning aggregated data
- Refresh: Every 5 minutes via polling

---

## Alignment with Business Goal: 5 Paying Customers

### Conversion Funnel Model

```
Tier 2 Outreach (8 GitHub issues) → Tier 1 Outreach (5-8 trusted users)
                                    ↓
                            Landing Page Views
                                    ↓
                            Demo Views
                                    ↓
                            Sign-ups (Target: 50-100)
                                    ↓
                            Onboarding Completed (Target: 30-80)
                                    ↓
                            Active Beta Users (Target: 20-60)
                                    ↓
                            Engaged Users (Target: 10-40)
                                    ↓
                            Paying Customers (Target: 5)
```

### Metrics-to-Business Mapping

| Metric | Target | Contribution to 5 Customers |
|--------|--------|----------------------------|
| Landing Page Views | 500-1,000 | Top of funnel |
| Demo Views | 300-600 | Product interest |
| Sign-ups | 50-100 | Intent to try |
| Onboarding Completion | 60-80% (30-80 users) | Value understood |
| DAU (Day 30) | 20-60 | Habit formed |
| Engagement | >5 ops/day | Core value delivered |
| Conversion Rate | 5-10% | Willingness to pay |
| **Paying Customers** | **5** | **Business goal** |

### Success Scenario

If we achieve:
- 50 sign-ups from Tier 1 + Tier 2 outreach
- 70% onboarding completion (35 users)
- 60% DAU/MAU (21 active users)
- 5-10% paid conversion

Then: **21 active users × 10% conversion = 2.1 → 2-3 paying customers**

**Gap to 5 customers:** Need additional traffic from:
- HN launch (50-100 sign-ups)
- Social media amplification
- Backlink-driven organic traffic

---

## Data Collection Implementation

### Required API Endpoints

```typescript
// POST /api/v1/analytics/events
// Accept analytics events from frontend
{
  "event_type": "string",
  "user_id": "string",
  "properties": object,
  "timestamp": "ISO-8601"
}

// GET /api/v1/analytics/dashboard
// Return aggregated metrics for dashboard
{
  "onboarding": { "signup": 50, "completed": 35, "rate": 0.7 },
  "activity": { "dau": 21, "mau": 35, "ratio": 0.6 },
  "engagement": { "avg_ops_per_user": 7.2, "avg_session_min": 6.5 },
  "health": { "error_rate": 0.008, "avg_latency_ms": 145 }
}

// GET /api/v1/analytics/funnel
// Return onboarding funnel data
{
  "steps": [
    { "name": "signup", "count": 50 },
    { "name": "onboarding_started", "count": 45 },
    { "name": "first_memory", "count": 38 },
    { "name": "first_query", "count": 35 },
    { "name": "completed", "count": 35 }
  ]
}
```

### Frontend Integration

```typescript
// lib/analytics.ts
export const trackEvent = (eventType: string, properties: object = {}) => {
  fetch('/api/v1/analytics/events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      event_type: eventType,
      user_id: getCurrentUserId(),
      properties,
      timestamp: new Date().toISOString()
    })
  });
};
```

---

## Monitoring Schedule

**Daily (Mar 24 - Apr 7):**
- Check DAU, error rate, onboarding funnel
- Review any anomalies or drop-offs

**Weekly (Apr 7 - Apr 20):**
- Review conversion trends
- Assess progress toward 5 customers
- Adjust outreach if needed

**Milestone Checks:**
- Mar 28 (Day 7): Initial engagement baseline
- Apr 7 (Day 14): Conversion funnel health
- Apr 14 (Day 21): Predict conversion probability
- Apr 20 (Day 28): **Goal achievement check**

---

## Risk Indicators

**Red Flags (Immediate Action Required):**
- Onboarding completion <40%
- DAU <5 after Day 7
- Error rate >3%
- 0 paying customers by Apr 14

**Yellow Flags (Monitor Closely):**
- Onboarding completion 40-60%
- DAU 5-10 after Day 7
- Error rate 1-3%
- <3 paying customers by Apr 14

**Green Indicators (On Track):**
- Onboarding completion >70%
- DAU >20 after Day 7
- Error rate <1%
- 3+ paying customers by Apr 14

---

## Next Steps

1. **faintech-backend:** Implement `POST /api/v1/analytics/events` (P1)
2. **faintech-frontend:** Add event tracking to onboarding flow (P1)
3. **pm:** Create dashboard page at `/dashboard/metrics` (P2)
4. **qa:** Verify event collection accuracy (P2)

---

*Documented by: CPO | Date: 2026-03-20 | Sprint: Beta Launch (Mar 11-24)*
*Task: LAB-20260320001131-6129DD32B858*
