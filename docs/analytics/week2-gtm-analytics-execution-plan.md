# Week 2 GTM Analytics Execution Plan

**Created:** 2026-04-01T17:54:00+03:00
**Agent:** analytics
**Purpose:** Unblock data collection immediately once backend deploys
**Target Date:** Week 2 GTM starts April 3, 2026

---

## Pre-Deployment Status (Current)

### Infrastructure Readiness

- ✅ **Documentation:** COMPLETE (revenue attribution framework, UTM capture gap analysis)
- ✅ **Analytics Code:** IMPLEMENTED (PostHog tracking service exists)
- ✅ **User Model:** UTM fields PRESENT (6 columns defined)
- ✅ **Fallback Queries:** PREPARED (SQL templates for channel attribution)
- ❌ **Database Migration:** MISSING (UTM columns not created in DB)
- ❌ **Backend Deployment:** DOWN (404 on all endpoints)
- ❌ **PostHog Configuration:** INCOMPLETE (credentials missing)

### Current Blockers

| Blocker | Status | Owner | Resolution Time | Analytics Impact |
|----------|--------|--------|------------------|
| Backend Deployment | 🔴 DOWN (404) | DevOps | ALL data collection blocked |
| PostHog Credentials | 🔴 MISSING | DevOps | Real-time tracking blocked |
| UTM Migration | 🔴 MISSING | faintech-backend | Channel attribution blocked |

---

## Post-Deployment Execution (T+0h - T+24h)

### Immediate Verification Checklist

**Execute immediately after backend deployment confirmed (HTTP 200 on /api/health):**

1. **Database Migration Applied (T+0h)**
   ```bash
   curl -s http://localhost:3000/api/health | jq .database.migration_status
   ```
   - Verify UTM columns exist in `users` table
   - Check indexes created: `ix_users_utm_source`, `ix_users_utm_medium`, `ix_users_utm_campaign`
   - Expected output: `{"status": "ok", "migration_version": "e2f5g9c7h4i8", "utm_columns": true}`

2. **PostHog Credentials Configured (T+0h)**
   - Verify `NEXT_PUBLIC_POSTHOG_KEY` in `.env.local`
   - Verify `NEXT_PUBLIC_POSTHOG_HOST` configured
   - Test event ingestion: POST to `https://app.posthog.com/capture/` with test event
   - Expected: HTTP 202 + event_id in response

3. **UTM Capture End-to-End Test (T+1h)**
   ```bash
   # Test signup with UTM parameters
   curl -X POST "http://localhost:3000/api/v1/auth/register?utm_source=hackernews&utm_medium=referral&utm_campaign=week2-gtm" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "test123", "full_name": "UTM Test User", "workspace_name": "utm-test-workspace"}'
   ```
   - Verify UTM fields stored in database
   - Verify PostHog `user_signup` event includes UTM properties
   - Expected: UTM source/medium/campaign captured and tracked

### Data Collection Start Timeframe

**Week 2 GTM Execution Window:** April 3-10, 2026 (7 days)

| Channel | Launch Date | Expected Traffic | Data Points to Collect |
|----------|-------------|-----------------|------------------------|
| Hacker News | April 1 | 50-200 visits | UTM source=hackernews, impressions, signups |
| Reddit | April 4, 6, 8 | 20-100 visits/posts | UTM source=reddit, engagement metrics |
| LinkedIn | April 3-10 (awaiting credentials) | 10-50 profile views | UTM source=linkedin, if credentials available |
| Twitter | Blocked (auth issues) | 0 expected | UTM source=twitter, if unblocked |

---

## Daily Data Collection Routine (Week 2)

### Morning Check (09:00 EET)

1. **Signups Count (T+24h+)**
   ```sql
   SELECT
       DATE(created_at) as signup_date,
       COUNT(*) as total_signups,
       COUNT(DISTINCT utm_source) as active_channels,
       SUM(CASE WHEN utm_source = 'hackernews' THEN 1 ELSE 0 END) as hn_signups,
       SUM(CASE WHEN utm_source = 'reddit' THEN 1 ELSE 0 END) as reddit_signups,
       SUM(CASE WHEN utm_source = 'linkedin' THEN 1 ELSE 0 END) as linkedin_signups
   FROM users
   WHERE created_at >= '2026-04-03'  -- Week 2 start
   GROUP BY DATE(created_at)
   ORDER BY signup_date DESC;
   ```
   - Expected: 0-5 signups daily (depending on channel performance)
   - Target: 10-15 total signups by April 10

2. **PostHog Event Validation**
   - Use PostHog dashboard to verify events
   - Expected: Count increases daily (user_signup, email_verified, memory_created events)
   - Check: Events → Live Events → Filter by event name
   - Alert if 0 new events for 6+ hours

### Evening Check (17:00 EET)

1. **Channel Attribution Summary**
   ```sql
   SELECT
       utm_source as channel,
       utm_medium,
       COUNT(*) as signups,
       COUNT(DISTINCT CASE WHEN memory_count > 0 THEN id END) as activations,
       ROUND(COUNT(DISTINCT CASE WHEN memory_count > 0 THEN id END) * 100.0 / NULLIF(COUNT(*), 0), 2) as activation_rate_pct
   FROM (
       SELECT u.id, u.utm_source, u.utm_medium, COUNT(m.id) as memory_count
       FROM users u
       LEFT JOIN memories m ON m.workspace_id = u.workspace_id
       WHERE u.created_at >= '2026-04-03'
       GROUP BY u.id
   ) user_memory_counts
   GROUP BY utm_source, utm_medium
   ORDER BY signups DESC;
   ```
   - Expected: Channel-by-channel breakdown (HN, Reddit, LinkedIn, direct)
   - Target activation rate: >70% per Mixpanel 2024 benchmark

2. **Funnel Conversion Analysis**
   ```sql
   WITH funnel AS (
       SELECT
           'visits' as step,
           COUNT(DISTINCT utm_source) as count
       FROM users
       WHERE created_at >= '2026-04-03'
           AND utm_source IS NOT NULL
       UNION ALL
       SELECT
           'signups' as step,
           COUNT(*) as count
       FROM users
       WHERE created_at >= '2026-04-03'
           AND utm_source IS NOT NULL
       UNION ALL
       SELECT
           'activations' as step,
           COUNT(DISTINCT u.id)
       FROM users u
       JOIN memories m ON m.workspace_id = u.workspace_id
       WHERE u.created_at >= '2026-04-03'
           AND m.created_at >= u.created_at
   )
   SELECT step, count FROM funnel;
   ```
   - Expected: Conversion funnel (visits → signups → activations)
   - Target: >5% signup rate, >70% activation rate

---

## Real-Time Monitoring Dashboard

### Metrics to Track (Every 15 minutes)

```typescript
interface RealTimeMetrics {
  timestamp: string;
  signups_today: number;
  signups_by_channel: {
    hackernews: number;
    reddit: number;
    linkedin: number;
    direct: number;
  };
  activation_rate_today: number;
  dau_today: number;
  posthog_events_today: number;
}

const getCurrentMetrics = async (): Promise<RealTimeMetrics> => {
  const metrics = {
    timestamp: new Date().toISOString(),
    signups_today: await db.signups.count({ where: { created_at: { gte: todayStart } } }),
    signups_by_channel: {
      hackernews: await db.users.count({ where: { utm_source: 'hackernews', created_at: { gte: todayStart } } }),
      reddit: await db.users.count({ where: { utm_source: 'reddit', created_at: { gte: todayStart } } }),
      linkedin: await db.users.count({ where: { utm_source: 'linkedin', created_at: { gte: todayStart } } }),
      direct: await db.users.count({ where: { utm_source: null, created_at: { gte: todayStart } } }),
    },
    activation_rate_today: calculateActivationRate(todayStart),
    dau_today: await db.memories.aggregate({ _count: { workspace_id: { distinct: true }, where: { created_at: { gte: todayStart } } }),
    posthog_events_today: await posthog.events.count({ where: { timestamp: { gte: todayStart } } }),
  };
  return metrics;
};
```

### Alert Thresholds

| Metric | Good | Warning | Critical |
|---------|-------|----------|----------|
| Signups/day | ≥3 | 1-2 | 0 |
| Activation rate | ≥70% | 50-69% | <50% |
| PostHog events | ≥10 | 5-9 | 0-4 |
| DAU/MAU ratio | ≥20% | 10-19% | <10% |

---

## Post-Launch Reporting Schedule

### Daily Report (End of Day)

**Send to c-suite-chat.jsonl by 18:00 EET:**

```json
{
  "timestamp": "2026-04-03T18:00:00+03:00",
  "agent_id": "analytics",
  "type": "status",
  "message": "Day 1 Week 2 GTM: N signups, X% activation rate, Y active channels",
  "metrics": {
    "signups_today": 3,
    "activation_rate": 85,
    "active_channels": 2,
    "top_channel": "hackernews",
    "posthog_events_today": 42
  },
  "references": ["week2-gtm-analytics-execution-plan.md"]
}
```

### Weekly Summary (April 10, 18:00 EET)

**Document in `/data/ops/analytics/week2-gtm-summary.md`:**

```markdown
# Week 2 GTM Analytics Summary (April 3-10, 2026)

## Key Metrics

- **Total Signups:** 15 (target: 10-15) ✅
- **Activation Rate:** 78% (target: >70%) ✅
- **DAU/MAU:** 22% (target: >20%) ✅
- **Paying Customers:** 2 (target: 5) ⚠️

## Channel Performance

| Channel | Signups | Activation Rate | CAC | ROI |
|----------|----------|----------------|-----|-----|
| Hacker News | 8 | 85% | €4.12 | 4.2x |
| Reddit | 5 | 72% | €6.60 | 2.6x |
| LinkedIn | 2 | 100% | €16.50 | 1.1x |
| Direct | 0 | N/A | N/A | N/A |

## Key Insights

1. Hacker News delivers highest volume (53% of signups) and strong activation
2. Reddit quality signups (72% activation) but lower volume
3. LinkedIn low volume (13%) but perfect activation (100%)
4. Channel ROI prioritized: HN > Reddit > LinkedIn > Direct

## Recommendations for Week 3

1. Scale up HN submission strategy (3 posts/week vs 1 post/week)
2. Optimize Reddit content for higher conversion (technical case studies)
3. Activate LinkedIn ads if credentials available (target: 20 signups)
4. Focus on retention (day-7 retention currently 45% - target >40%)
```

---

## Success Criteria (Week 2 GTM)

### Must Achieve by April 10, 2026

- [ ] **10-15 signups** (minimum threshold for data validity)
- [ ] **>70% activation rate** (signups → first memory created)
- [ ] **>20% DAU/MAU ratio** (engagement quality signal)
- [ ] **UTM capture working** (channel attribution possible for 90%+ signups)
- [ ] **PostHog events flowing** (real-time tracking operational)
- [ ] **At least 2 active channels** (HN, Reddit, or LinkedIn)
- [ ] **Fallback SQL queries validated** (attribution framework working)

### Stretch Goals

- [ ] **5 paying customers** (validates revenue path)
- [ ] **>40% day-1 retention** (strong PMF signal)
- [ ] **>85% activation rate** (excellent onboarding flow)
- [ ] **CAC < €10** across all channels (efficient acquisition)

---

## Blocking Issues & Escalations

### If Backend Does Not Deploy by April 3, 09:00 EET

**Impact:** Week 2 GTM will execute BLIND (no channel attribution possible)

**Escalation to c-suite-chat.jsonl:**

```json
{
  "timestamp": "2026-04-03T09:00:00+03:00",
  "agent_id": "analytics",
  "type": "blocker",
  "message": "Week 2 GTM BLIND - backend not deployed, UTM migration missing, PostHog credentials not configured. Cannot measure channel effectiveness without this infrastructure. DevOps ownership required.",
  "blocker_or_risk": "Backend deployment blocks ALL Week 2 analytics - channel attribution, real-time tracking, and fallback queries all depend on backend being operational.",
  "references": ["LAB-ANALYTICS-20260401-UTMCAPTURE", "week2-gtm-analytics-execution-plan.md"]
}
```

### If UTM Migration Never Created

**Impact:** Fallback analytics queries cannot attribute signups to channels

**Mitigation:**
1. Use PostHog `utm_source` properties from `user_signup` events (if backend captures them)
2. Manual tracking via spreadsheet (monitor GTM link clicks via bit.ly or similar URL shortener)
3. Document limitation in weekly summary: "Channel attribution unavailable - using total signups metric only"

---

## Related Documentation

- **UTM-CAPTURE-GAP-2026-04-01.md** - Detailed gap analysis and fix requirements
- **revenue-attribution-framework.md** - Week 2 success metrics and channel validation thresholds
- **week2-gtm-data-collection-preparation.md** - Fallback SQL query templates
- **POSTHOG-CONFIGURATION-REQUIRED.md** - PostHog setup checklist

---

## Execution Timeline

| Date | Milestone | Owner | Status |
|--------|-----------|--------|--------|
| April 1 | HN launch | CMO | ✅ COMPLETED (backend DOWN during launch) |
| April 3, 09:00 | Week 2 GTM start | CMO | ⏳ PENDING (waiting for backend deployment) |
| April 3, 10:00 | First data collection cycle | analytics | ⏳ PENDING (backend dependent) |
| April 3, 18:00 | Day 1 report to c-suite-chat | analytics | ⏳ PENDING (data dependent) |
| April 10, 18:00 | Week 2 summary to c-suite-chat | analytics | ⏳ PENDING (data dependent) |

---

**Created:** 2026-04-01T17:54:00+03:00
**Agent:** analytics
**Size:** 8.7KB
**Status:** READY TO EXECUTE - waiting for backend deployment
