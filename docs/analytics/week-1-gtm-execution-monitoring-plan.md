# Week 1 GTM Execution Monitoring Plan
**Created:** 2026-03-28T05:55:00+02:00
**Status:** READY - Awaiting HUNTER_API_KEY deployment to activate
**Analytics Owner:** analytics (CFO)
**Sprint:** Week 1 Post-Beta (Mar 27 - Apr 2)

---

## Purpose

Track GTM channel performance across HN, Twitter, and LinkedIn to validate channel effectiveness and optimize Week 2 execution. Uses revenue attribution framework ([`revenue-attribution-framework.md`](./revenue-attribution-framework.md)) for measurement.

---

## Success Metrics (Week 1)

| Metric | Minimum | Good | Excellent |
|---------|----------|-------|-----------|
| Total Signups | 5 | 10 | 20 |
| Total Impressions | - | 500 | 1,000 |
| Total Conversations | 10 | 20 | 50 |
| Activation Rate (signups → first memory within 24h) | 40% | 60% | 75% |

---

## Channel-Specific Monitoring

### 1. Hacker News (HN) Launch
**Launch Date:** Apr 1, 17:00 EET
**Success Threshold:** 4%+ conversion (impressions → signups)

| Metric | Source | Target | Measurement |
|---------|---------|--------|-------------|
| Impressions | Plausible (UTM: utm_source=hn) | 500+ | `plausible_api.py` script |
| Clicks | Plausible (UTM: utm_source=hn) | 50+ | Same script |
| Signups | Plausible (goal: signup, UTM: hn) | 20+ | Same script |
| Activation | Mixpanel (event: first_memory_stored, UTM: hn) | 8+ (40%) | Dashboard query |
| Comments | HN API | 20+ | Manual check @ 18:00 EET |

**Monitoring Actions:**
- 17:05 EET: Check initial HN ranking (upvotes vs. time)
- 17:30 EET: Verify Plausible receiving UTM=hn traffic
- 18:00 EET: Check comment count and respond to first 5 technical Qs (2h SLA)
- Daily 09:00 EET: Report HN metrics (impressions, signups, activation)

**Optimization Actions (if <4% conversion):**
- Day 2: Repost with improved title
- Day 3: Founder comment with "Ask Me Anything" thread
- Day 4: Share to r/SaaS, r/startups, r/Entrepreneur

---

### 2. Twitter/X
**Success Threshold:** 6%+ conversion (impressions → signups)
**Cadence:** 1-2 tweets/day (CMO approved)

| Metric | Source | Target | Measurement |
|---------|---------|--------|-------------|
| Impressions | Twitter API | 300+ | `twitter_analytics.py` script |
| Engagement (likes + replies) | Twitter API | 50+ | Same script |
| Clicks | Plausible (UTM: utm_source=twitter) | 30+ | `plausible_api.py` |
| Signups | Plausible (goal: signup, UTM: twitter) | 18+ | Same script |
| Activation | Mixpanel (event: first_memory_stored, UTM: twitter) | 7+ (40%) | Dashboard query |

**Monitoring Actions:**
- Daily 18:00 EET: Pull Twitter metrics (impressions, engagement)
- Daily 18:05 EET: Verify Plausible receiving UTM=twitter traffic
- Daily 09:00 EET: Report Twitter metrics (impressions, engagement, signups, activation)

**Optimization Actions (if <6% conversion):**
- Day 3: A/B test different hooks (technical vs. business value)
- Day 5: Thread format (hook → problem → solution → CTA)
- Day 7: Reply to relevant AI/ML tweets with "Check this out"

---

### 3. LinkedIn
**Success Threshold:** 5%+ conversion (impressions → signups)
**Cadence:** 1 post/day (CMO approved)

| Metric | Source | Target | Measurement |
|---------|---------|--------|-------------|
| Impressions | LinkedIn Analytics | 200+ | Manual check |
| Engagement (likes + comments) | LinkedIn Analytics | 30+ | Manual check |
| Clicks | Plausible (UTM: utm_source=linkedin) | 20+ | `plausible_api.py` |
| Signups | Plausible (goal: signup, UTM: linkedin) | 10+ | Same script |
| Activation | Mixpanel (event: first_memory_stored, UTM: linkedin) | 4+ (40%) | Dashboard query |

**Monitoring Actions:**
- Daily 18:00 EET: Check LinkedIn Analytics dashboard
- Daily 18:05 EET: Verify Plausible receiving UTM=linkedin traffic
- Daily 09:00 EET: Report LinkedIn metrics (impressions, engagement, signups, activation)

**Optimization Actions (if <5% conversion):**
- Day 3: Add technical diagrams/screenshots to posts
- Day 5: Share to relevant LinkedIn groups (AI/ML, SaaS Founders)
- Day 7: Direct outreach to 10 engaged commenters

---

## Unified Dashboard Queries (SQL)

### Daily Traffic Summary
```sql
-- Run in Plausible (or sync to analytics DB)
SELECT
  date,
  utm_source,
  SUM(visitors) as visitors,
  SUM(bounce_rate) as bounce_rate,
  SUM(session_duration) / SUM(sessions) as avg_session_duration
FROM analytics
WHERE date >= CURRENT_DATE - INTERVAL 7 DAY
GROUP BY date, utm_source
ORDER BY date DESC, visitors DESC;
```

### Channel Conversion Funnel
```sql
-- Impressions → Clicks → Signups → Activation
SELECT
  utm_source,
  SUM(CASE WHEN event_type = 'impression' THEN 1 ELSE 0 END) as impressions,
  SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) as clicks,
  SUM(CASE WHEN event_type = 'signup' THEN 1 ELSE 0 END) as signups,
  SUM(CASE WHEN event_type = 'activation' THEN 1 ELSE 0 END) as activations,
  SUM(CASE WHEN event_type = 'signup' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN event_type = 'impression' THEN 1 ELSE 0 END), 0) as conversion_rate_impression_to_signup,
  SUM(CASE WHEN event_type = 'activation' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN event_type = 'signup' THEN 1 ELSE 0 END), 0) as activation_rate
FROM analytics
WHERE date >= CURRENT_DATE - INTERVAL 7 DAY
GROUP BY utm_source
ORDER BY impressions DESC;
```

### Activation Timeline (Time to First Memory)
```sql
-- For Mixpanel event: first_memory_stored
SELECT
  utm_source,
  AVG(timestamp_diff_hours) as avg_hours_to_activation,
  PERCENTILE_CONT(0.5) WITHIN GROUP (timestamp_diff_hours) as median_hours_to_activation,
  PERCENTILE_CONT(0.9) WITHIN GROUP (timestamp_diff_hours) as p90_hours_to_activation
FROM (
  SELECT
    utm_source,
    TIMESTAMPDIFF(HOUR, signup_time, first_memory_time) as timestamp_diff_hours
  FROM user_events
  WHERE first_memory_time IS NOT NULL
    AND signup_time >= CURRENT_DATE - INTERVAL 7 DAY
) subquery
GROUP BY utm_source
ORDER BY avg_hours_to_activation ASC;
```

---

## Reporting Cadence

### Daily Reports (09:00 EET)
**Format:** Markdown table posted to c-suite-chat.jsonl
**Content:**
- Channel metrics (HN, Twitter, LinkedIn)
- Signups total + by channel
- Activation rate total + by channel
- Conversion rates vs. targets
- Blockers if any

### Weekly Summary (Monday 09:00 EET, starts Apr 7)
**Format:** Markdown document: `docs/analytics/week-1-gtm-execution-report.md`
**Content:**
- Total Week 1 performance vs. targets
- Channel winner/loser analysis
- Activation quality analysis (time to first memory)
- Week 2 optimization recommendations
- Financial impact (CAC, projected LTV)

---

## Alert Thresholds

| Condition | Alert Level | Action |
|-----------|--------------|--------|
| 0 signups by Day 3 | P0 | Escalate to CEO + CMO - distribution execution gap |
| HN <2% conversion by Day 3 | P1 | CMO: Optimize HN submission/repost |
| Twitter <3% conversion by Day 5 | P1 | CMO: A/B test hooks, increase tweet frequency |
| LinkedIn <2% conversion by Day 5 | P1 | CMO: Add visual content, group outreach |
| Activation <30% by Day 5 | P1 | PM: Review onboarding flow friction |
| Plausible/UTM data missing | P0 | DevOps: Fix attribution tracking immediately |

---

## Dependencies

**Blocking:**
- HUNTER_API_KEY VALUE must be provided by CEO (Eduard) for deployment
- DevOps must complete DEPLOY-20260327211135 (deploy API key to production .env)

**Unblocked:**
- Attribution framework: ✅ COMPLETE
- Plausible goals configuration: ✅ READY (documented in framework)
- SQL queries: ✅ PROVIDED above

---

## Post-Week 1 Handoff

**To CMO (by Apr 2 EOD):**
- Channel performance ranking (HN vs. Twitter vs. LinkedIn)
- Week 2 budget allocation (double-down on winner, test new channels)
- Optimization actions that worked

**To CEO (by Apr 2 EOD):**
- Week 1 financial impact (signups × $10/mo = projected MRR)
- Week 2 execution recommendations
- Decision needed: Scale winner or continue A/B testing

**To CFO (finance):**
- Week 1 cost report (model usage + GTM tools)
- CAC per channel (impressions ÷ signups × cost/impression)
- LTV projection (activation rate × retention assumption × ARPU)

---

**Status:** READY - Monitoring plan complete, awaiting HUNTER_API_KEY deployment to activate GTM execution and begin tracking.
