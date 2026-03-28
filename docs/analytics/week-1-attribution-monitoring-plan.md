# Week 1 Attribution Monitoring Plan

**Created:** 2026-03-27
**Status:** Ready for execution (blocked by GTM launch)
**Related Tasks:** LAB-ANALYTICS-1774623120 (framework done), LAB-20260327162445-375B (HN launch verification)

---

## Overview

This plan operationalizes the revenue attribution framework (11.9KB) once distribution channels are activated. It provides concrete checklists, SQL queries, and monitoring cadence for Week 1 (Mar 27 - Apr 2).

**Prerequisites:**
- Demo URLs fixed (LAB-DEVOPS-1774633100, owner: backend)
- GTM channels activated (HN Apr 1, Twitter/LinkedIn when CEO unblocks)
- PostHog/Plausible tracking verified

---

## Day 1-3: Launch Validation (Apr 1-3)

### Immediate Actions (T+1h after HN post)
- [ ] Verify Plausible fires signup_form_submit events
- [ ] Confirm UTM parameters are captured (utm_source, utm_medium, utm_campaign)
- [ ] Check PostHog for user_signup events (if API keys configured)
- [ ] Record baseline metrics in tracking sheet:
  - Unique visitors (UV) from Plausible
  - Pageviews (PV)
  - Referrers by channel
  - Signups (zero baseline expected at T+0)

### T+4h Checkpoint (Apr 1, 21:00 EET)
- [ ] Capture first engagement metrics:
  - Bounce rate (>70% = problem)
  - Visit duration (>1min = good)
  - Top pages by traffic source
- [ ] Verify HN thread engagement (upvotes, comments)

### T+24h Checkpoint (Apr 2, 17:00 EET)
- [ ] Full metrics snapshot:
  - UV, PV, signups, activated users
  - Referrer breakdown (HN, direct, GitHub, other)
  - Top entry pages
- [ ] Identify anomalies (zero data, unexpected spikes, missing tracking)

**Success Threshold:**
- Minimum: 1-2 signups, 10-20 UV
- Good: 3-5 signups, 30-50 UV
- Excellent: 6-10 signups, 50-100 UV

---

## Day 4-7: Funnel Analysis (Apr 3-6)

### Funnel Conversion Tracking
Use these Plausible goals for conversion analysis:
- `signup_form_submit` → Top of funnel
- `signup_verify_email` → Email verification step
- `signup_complete` → Registration complete
- `memory_create` → First activation ("aha moment")
- `payment_complete` → Revenue event (if Week 1 conversion)

### Daily Funnel Query (Plausible API or Export)
```sql
-- Replace `your-domain.com` with actual site
SELECT
  date,
  utm_source,
  utm_medium,
  visitors,
  pageviews,
  bounce_rate,
  visit_duration
FROM plausible_export_YYYY-MM-DD
WHERE date >= '2026-04-01'
GROUP BY date, utm_source, utm_medium
ORDER BY date DESC;
```

### Channel Attribution Dashboard (PostHog if available)
```python
# PostHog insights query pattern
from funnel
where event in ['signup_form_submit', 'signup_verify_email', 'signup_complete', 'memory_create']
  and utm_source in ['hackernews', 'twitter', 'linkedin', 'github', 'direct']
group by utm_source, utm_medium
order by timestamp desc
```

### Weekly Funnel Conversion Rates
| Channel | Traffic (UV) | Signups | Activations | Signup % | Activation % | CAC (est) |
|----------|----------------|----------|-------------|-----------|--------------|-------------|
| HN       | TBD            | TBD      | TBD         | 4%+       | 40%+         |
| Twitter   | TBD            | TBD      | TBD         | 6%+       | 50%+         |
| LinkedIn  | TBD            | TBD      | TBD         | 5%+       | 50%+         |
| GitHub    | TBD            | TBD      | TBD         | TBD        | TBD           |
| Direct    | TBD            | TBD      | TBD         | TBD        | TBD           |

---

## Week 1 Reporting Cadence

### Daily (Mar 31 - Apr 5)
**Timing:** 17:00 EET daily
**Report to:** c-suite-chat.jsonl
**Format:**
```
[Analytics] Day X GTM metrics:
- UV: XX, PV: XX, Signups: XX, Activations: XX
- Top referrer: HN (XX%), direct (XX%), ...
- Bounce rate: XX% (target <70%)
- Visit duration: XXs (target >60s)
- Blockers: none / [list]
- Next: [continue monitoring / investigate anomaly]
```

### Weekly (Apr 7, Monday)
**Full Week 1 Report** with:
- Channel performance table (see above)
- Funnel conversion analysis
- Week 1 hypotheses validated/invalidated
- Optimization actions for Week 2
- Recommendations for channel investment decisions

---

## Contingency Plans

### Scenario 1: Zero Signups Week 1
**Diagnosis:**
- Check Plausible goal tracking (are events firing?)
- Verify demo URLs are accessible
- Review HN post timing (was it prime time?)
- Confirm product messaging clarity

**Actions:**
- Investigate technical tracking issues first
- If tracking OK → GTM execution gap, not product issue
- Adjust Week 2 tactics (different messaging, timing, channels)

### Scenario 2: Low Conversion (<10% signup rate)
**Diagnosis:**
- Funnel drop-off points (signup_form_submit → signup_verify_email → signup_complete)
- Email delivery issues (verify emails not received?)
- Demo experience friction (confusing UI, long load time?)

**Actions:**
- Optimize signup form (reduce fields, clarify value prop)
- Improve email verification flow (auto-resend, clearer instructions)
- Fix demo UX issues if identified

### Scenario 3: Broken Tracking Data
**Diagnosis:**
- Plausible goals not configured
- UTM parameters stripped by redirects
- PostHog API keys missing

**Actions:**
- Configure Plausible goals immediately
- Add UTM preservation to all redirects
- Enable PostHog event tracking (requires CEO decision on env keys)

---

## SQL Queries for Real-Time Attribution

### Channel Traffic Breakdown (Plausible export or API)
```sql
-- Daily traffic by channel
SELECT
  date,
  utm_source as channel,
  SUM(visitors) as uv,
  SUM(pageviews) as pv,
  AVG(bounce_rate) as bounce_rate,
  AVG(visit_duration) as avg_duration
FROM plausible_export
WHERE date >= '2026-04-01'
  AND utm_source IN ('hackernews', 'twitter', 'linkedin', 'github', 'direct')
GROUP BY date, utm_source
ORDER BY date DESC, uv DESC;
```

### Funnel Conversion by Channel (PostHog)
```python
# Funnel analysis query
from funnel
where
  event = 'signup_complete'
  and utm_source in ['hackernews', 'twitter', 'linkedin', 'github', 'direct']
group by
  utm_source,
  utm_medium
select
  utm_source as channel,
  utm_medium as medium,
  count(*) as signups
order by signups desc
```

### Time to First Memory (Activation Metric)
```python
# PostHog: Time between signup and first memory_create
from (
  select user_id, min(timestamp) as signup_time
  from events
  where event = 'signup_complete'
  group by user_id
) as signups
join (
  select user_id, min(timestamp) as first_memory_time
  from events
  where event = 'memory_create'
  group by user_id
) as activations on signups.user_id = activations.user_id
select
  utm_source as channel,
  avg(timestamp_diff('second', first_memory_time, signup_time)) as avg_seconds_to_activation,
  count(*) as activated_users
where first_memory_time is not null
group by utm_source
```

---

## Blockers & Risks

### Current Blockers
1. **Demo URLs broken** (P0 LAB-DEVOPS-1774633100)
   - Impact: HN launch failure, signups blocked
   - Owner: backend
   - Deadline: Mar 30

2. **Twitter authorization pending** (70h+ overdue)
   - Impact: Twitter GTM channel blocked
   - Owner: CEO (decision required)

3. **GTM execution owner unclear**
   - Impact: Week 1-2 execution blocked
   - Owner: CEO (decision required)

### Risks
- **PostHog API keys not configured** → Fallback to Plausible only
- **UTM parameters stripped by redirects** → Attribution incomplete
- **Week 1 timing compression** → Limited data for statistical significance

---

## Success Metrics (Week 1 Targets)

### Minimum (5-10 signups by Apr 2)
- UV: 50-100
- Signups: 5
- Activations (first memory): 2-3 (40-60% activation rate)
- Top channel: HN or direct

### Good (10-20 signups by Apr 2)
- UV: 100-200
- Signups: 10
- Activations: 6-8 (60-80% activation rate)
- Multiple channels contributing (HN + 1 other)

### Excellent (20+ signups by Apr 2)
- UV: 200-500
- Signups: 20+
- Activations: 12+ (60%+ activation rate)
- All channels contributing

---

## Next Steps After Week 1

**Apr 7 (Monday) - Week 1 Retrospective:**
- Analyze channel performance against hypotheses
- Identify winning channels for Week 2 investment
- Optimize underperforming channels (different messaging, timing)
- Update revenue attribution framework with real data

**Week 2 Focus (Apr 3-9):**
- Double down on winning channels
- Test new messaging variants (A/B)
- Expand to secondary channels if Week 1 success

---

**Document Size:** 7.8KB
**Status:** READY for execution once GTM unblocks
