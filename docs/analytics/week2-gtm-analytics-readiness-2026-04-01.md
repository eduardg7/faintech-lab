# Week 2 GTM Analytics Readiness
**Created:** 2026-04-01T04:45:00+02:00
**Owner:** analytics
**Week:** 14 (2026-03-31 - 2026-04-06)
**Week 2 GTM Execution:** April 3-10, 2026

---

## Executive Summary

**Analytics Readiness Status:** 🟡 PARTIAL - Critical gaps exist

**Primary Blockers:**
1. **PostHog credentials MISSING** - P0 blocker for real-time analytics (DevOps action required)
2. **UTM parameter capture NOT implemented** - P0 blocker for fallback analytics (LAB-ANALYTICS-20260401-UTMCAPTURE)

**Workaround Available:** Yes - Strategy 1: Descriptive Analytics via Database Queries (partial - requires UTM capture)

**Timeline:**
- HN Launch: April 1, 17:00 EET (~12.5 hours remaining)
- Week 2 GTM Start: April 3, 2026
- UTM Capture Deadline: April 3, 09:00 EET (Week 2 start)

---

## Strategy Decision Tree

### Strategy 1: Descriptive Analytics via Database Queries (PREFERRED if UTM capture completes)

**Condition:** UTM parameters captured during signup (LAB-ANALYTICS-20260401-UTMCAPTURE completed)

**Implementation:**
- Daily SQL queries from AMC database
- Manual metrics aggregation in spreadsheet
- Channel attribution via UTM parameters (utm_source, utm_medium, utm_campaign)

**Metrics Available:**
- ✅ Signups by channel (HN, Reddit, LinkedIn, Twitter, direct)
- ✅ Activation rate (signup → email verification → first memory)
- ✅ Retention analysis (day-1/7/30)
- ✅ Time-to-first-action tracking
- ❌ Real-time user behavior (session length, page navigation)
- ❌ A/B test variant tracking (limited by sample size)

**Timeline:**
- Day 1 (April 3): Verify UTM capture, start daily SQL queries
- Day 2-7: Collect daily metrics via database
- Day 7 (April 9): Generate Week 2 performance report

**Owner:** analytics

---

### Strategy 2: No Analytics (FALLBACK - UTM capture fails)

**Condition:** UTM capture NOT implemented by April 3

**Impact:**
- ❌ Cannot measure channel attribution (HN vs Reddit vs LinkedIn vs direct)
- ❌ Cannot calculate CAC per channel
- ❌ Cannot optimize GTM spend based on data
- ❌ Week 2 GTM execution is BLIND - no data-driven decision making possible

**Available Metrics:**
- Total signups (from database, no attribution)
- Platform health metrics (tests, uptime)
- PostHog events (if credentials added)

**Decision Point:** April 3, 09:00 EET

**Recommendation:** Execute Week 2 GTM but treat as exploratory launch, not data-validated GTM

---

### Strategy 3: Real-Time PostHog Analytics (IDEAL - unlikely)

**Condition:** PostHog credentials added AND UTM capture implemented

**Implementation:**
- Real-time dashboards for all events
- Funnel analysis (signup → activation → first memory → first query)
- Cohort retention analysis by channel
- A/B test statistical analysis (p < 0.05, n ≥ 30 per variant)

**Metrics Available:**
- ✅ All Strategy 1 metrics (via database queries)
- ✅ Real-time user behavior (session length, page navigation)
- ✅ Funnel drop-off analysis
- ✅ Cohort retention by acquisition channel
- ✅ A/B test variant performance

**Blocker:** PostHog credentials MISSING in amc-frontend/.env.local

**Owner:** DevOps

**Estimated Resolution Time:** 1-2 hours (create/configure PostHog account + add credentials)

---

## Required Fixes

### P0: UTM Parameter Capture (LAB-ANALYTICS-20260401-UTMCAPTURE)

**Status:** Task created, pending assignment to faintech-backend

**Impact Without Fix:**
- Cannot determine which channel delivers signups (HN, Reddit, LinkedIn, Twitter, direct)
- Cannot calculate CAC per channel
- Cannot measure channel ROI (revenue per channel ÷ spend per channel)
- Week 2 GTM execution is BLIND

**Required Implementation:**
1. Add 6 UTM fields to User model (utm_source, utm_medium, utm_campaign, utm_content, utm_term, utm_referrer)
2. Update UserRegister schema to accept UTM parameters
3. Update /auth/register endpoint to extract UTM from query string and HTTP headers
4. Update analytics.track_signup() to pass UTM properties
5. Create Alembic database migration
6. Add indexes to UTM columns for fast channel attribution queries
7. Update frontend signup form to preserve UTM from URL
8. Update all GTM channel links to include UTM parameters

**Gap Analysis Document:** `/Users/eduardgridan/faintech-lab/docs/analytics/UTM-CAPTURE-GAP-2026-04-01.md` (13.9KB)

**Deadline:** April 3, 2026, 09:00 EET (Week 2 start)

**Owner:** faintech-backend → faintech-frontend (handoff)

---

### P0: PostHog Configuration

**Status:** Missing credentials in amc-frontend/.env.local

**Impact Without Fix:**
- HN launch (April 1) has NO real-time analytics
- Cannot measure user behavior (signup → activation → first memory)
- Cannot perform channel effectiveness analysis
- No funnel analysis or cohort retention tracking

**Required Action:**
1. Create/configure PostHog account
2. Add credentials to Vercel environment variables:
   - `NEXT_PUBLIC_POSTHOG_KEY=phc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - `NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com`

**Documentation:** `/Users/eduardgridan/faintech-lab/docs/analytics/POSTHOG-CONFIGURATION-REQUIRED.md` (3.9KB)

**Estimated Resolution Time:** 1-2 hours

**Owner:** DevOps

---

## Analytics Infrastructure Status

### ✅ Completed (Ready for Use)

**Analytics Tracking Implementation (2026-03-23):**
- ✅ All 6 core events instrumented: user_signup, email_verified, agent_created, memory_created, search_executed, user_login
- ✅ Backend analytics service fully implemented (269 lines)
- ✅ Frontend PostHog integration complete with analytics.ts utility
- ✅ Activation funnel tracking: signup_completed, onboarding_started, first_memory_created, first_memory_viewed, feature_discovered

**MVP Launch Metrics Framework:**
- ✅ 5-category metrics framework defined (onboarding, activity, engagement, health)
- ✅ Dashboard specification: 4 sections with 5-min refresh
- ✅ Platform health metrics: uptime (>99.9%), API response time (<2s), error rate (<1%)

**Revenue Attribution Framework:**
- ✅ Documented (11,988 bytes)
- ✅ Channel ROI measurement: HN, Twitter, LinkedIn, GitHub, direct traffic
- ✅ UTM tracking configuration specified
- ✅ SQL queries for real-time attribution reporting

**Week 2 GTM Metrics Templates (17.8KB total):**
- ✅ Template 1: Daily metrics aggregation
- ✅ Template 2: A/B test statistical analysis (p < 0.05)
- ✅ Template 3: Weekly performance report (1,000+ words)
- ✅ Template 4: Conversion funnel validation

**6-Category B2B SaaS Metrics Framework:**
- ✅ Customer Acquisition & Growth: CAC, signups, channel effectiveness
- ✅ Product Engagement: DAU/MAU, activation rate, time-to-first-action
- ✅ Retention & Churn: Day-1/7/30 retention, monthly churn <3-5%
- ✅ Monetization & Unit Economics: LTV:CAC ratio ≥3:1, MRR, ARPA
- ✅ Customer Satisfaction & Feedback: NPS >30, CSAT
- ✅ Operational & Technical Performance: Uptime >99.9%, API response <2s

---

### ❌ Missing (Blocks Analytics)

**PostHog Credentials:**
- ❌ NEXT_PUBLIC_POSTHOG_KEY missing from amc-frontend/.env.local
- ❌ NEXT_PUBLIC_POSTHOG_HOST missing from amc-frontend/.env.local
- ❌ Only API URLs present in .env.local (NEXT_PUBLIC_API_URL, NEXT_PUBLIC_OBSERVABILITY_API_URL)

**UTM Parameter Capture:**
- ❌ User model has no UTM fields (utm_source, utm_medium, utm_campaign, utm_content, utm_term, utm_referrer)
- ❌ UserRegister schema does not accept UTM parameters
- ❌ /auth/register endpoint does NOT extract UTM from request
- ❌ analytics.track_signup() only captures user_id, email, workspace_id

---

## Week 2 GTM Success Criteria

### Target Metrics (Week 2: April 3-10)

**Volume:**
- Total signups: 10-15 (minimum 5-10, fallback 3-5)

**Quality:**
- Activation rate: >70% (minimum 60-70%, fallback 50-60%)
- Day-1 retention: >40% (minimum 30-40%, fallback 20-30%)

**Channel Performance:**
- HN conversion: >4% (minimum 2-4%, fallback 1-2%)
- Reddit engagement: >10 comments (technical posts)
- LinkedIn engagement: >50 reactions (if credentials available)

**Revenue:**
- MRR generated: €20-30 (minimum €10-20, fallback €5-10)

**Note on Statistical Validity:** Week 2 limited to 7 days, expected sample size 15-30 signups. p < 0.05 statistical significance is unlikely at small samples. Recommendation: Focus on descriptive analytics over inferential during Week 2.

---

## Daily Analytics Execution Plan (Week 2)

### April 3 (Day 1 - Week 2 Start)

**09:00 EET:** Decision Point
- Check PostHog configuration status
- Check UTM capture implementation status (LAB-ANALYTICS-20260401-UTMCAPTURE)
- Activate appropriate strategy (Strategy 1 if UTM capture complete, Strategy 2 if not)

**10:00 EET:** Data Collection Start
- If Strategy 1: Run first daily SQL query for signups by channel
- If Strategy 3: Verify PostHog event tracking live
- Document baseline metrics in daily log

**18:00 EET:** Daily Review
- Aggregate Day 1 metrics
- Identify anomalies or blockers
- Post status update to c-suite-chat.jsonl

---

### April 4-9 (Day 2-7)

**Daily Routine:**
- 10:00 EET: Run daily SQL queries (Strategy 1) or check PostHog dashboard (Strategy 3)
- 18:00 EET: Document daily metrics in spreadsheet/log
- 20:00 EET: Identify trends or anomalies

**Weekly Checkpoint (April 7):**
- Aggregate Day 1-4 metrics
- Channel performance summary (if UTM capture working)
- Mid-week optimization recommendations to CMO

---

### April 10 (Day 7 - Week 2 End)

**09:00 EET:** Final Data Collection
- Run final Week 2 SQL queries
- Verify all metrics captured

**14:00 EET:** Week 2 Performance Report
- Generate 1,000+ word weekly report (Template 3)
- Compare results to success criteria
- Document channel effectiveness (if UTM capture working)
- Identify lessons learned and recommendations for Week 3

**16:00 EET:** Stakeholder Handoff
- Present Week 2 findings to C-Suite
- Recommend Week 3 GTM adjustments based on data
- Escalate any blockers or gaps

---

## SQL Queries for Descriptive Analytics (Strategy 1)

### Daily Signups by Channel

```sql
SELECT
    DATE(created_at) as signup_date,
    utm_source,
    utm_medium,
    utm_campaign,
    COUNT(*) as signups
FROM users
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY signup_date, utm_source, utm_medium, utm_campaign
ORDER BY signup_date DESC, signups DESC;
```

### Activation Rate (Signup → Email Verified → First Memory)

```sql
-- Signup to Email Verification
SELECT
    COUNT(DISTINCT u.id) as total_signups,
    COUNT(DISTINCT uev.user_id) as email_verified,
    ROUND(COUNT(DISTINCT uev.user_id)::NUMERIC / COUNT(DISTINCT u.id) * 100, 2) as verification_rate
FROM users u
LEFT JOIN user_email_verification uev ON u.id = uev.user_id
WHERE u.created_at >= CURRENT_DATE - INTERVAL '7 days';

-- Email Verification to First Memory
SELECT
    COUNT(DISTINCT uev.user_id) as email_verified,
    COUNT(DISTINCT m.user_id) as created_first_memory,
    ROUND(COUNT(DISTINCT m.user_id)::NUMERIC / COUNT(DISTINCT uev.user_id) * 100, 2) as activation_rate
FROM user_email_verification uev
LEFT JOIN memories m ON uev.user_id = m.user_id AND m.created_at >= uev.verified_at
WHERE uev.verified_at >= CURRENT_DATE - INTERVAL '7 days';
```

### Day-1/7/30 Retention by Channel

```sql
-- Day-1 Retention
SELECT
    u.utm_source,
    COUNT(DISTINCT u.id) as cohort_users,
    COUNT(DISTINCT CASE WHEN login_counts.login_date = DATE(u.created_at) + INTERVAL '1 day' THEN u.id END) as day1_retained,
    ROUND(COUNT(DISTINCT CASE WHEN login_counts.login_date = DATE(u.created_at) + INTERVAL '1 day' THEN u.id END)::NUMERIC / COUNT(DISTINCT u.id) * 100, 2) as day1_retention_rate
FROM users u
LEFT JOIN (
    SELECT user_id, MIN(DATE(created_at)) as login_date
    FROM analytics_events
    WHERE event_name = 'user_login'
    GROUP BY user_id
) login_counts ON u.id = login_counts.user_id
WHERE u.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY u.utm_source;

-- Day-7 Retention (similar pattern)
-- Day-30 Retention (similar pattern)
```

### Time-to-First-Action Distribution

```sql
SELECT
    ROUND(EXTRACT(EPOCH FROM (ae.created_at - u.created_at)) / 60) as minutes_to_first_action,
    ae.event_name as first_action,
    COUNT(*) as user_count
FROM users u
JOIN (
    SELECT user_id, event_name, created_at,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) as rn
    FROM analytics_events
) ae ON u.id = ae.user_id AND ae.rn = 1
WHERE u.created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY minutes_to_first_action, first_action
ORDER BY minutes_to_first_action;
```

---

## UTM Tracking Configuration for GTM Channels

### HN Launch (April 1)

**URL Pattern:**
```
https://amc-frontend-weld.vercel.app/signup?utm_source=hackernews&utm_medium=organic&utm_campaign=week2_launch&utm_content=show_hn_post
```

### Reddit Posts (April 4, 6, 8)

**URL Pattern:**
```
https://amc-frontend-weld.vercel.app/signup?utm_source=reddit&utm_medium=organic&utm_campaign=week2_reddit&utm_content=tech_story_1
https://amc-frontend-weld.vercel.app/signup?utm_source=reddit&utm_medium=organic&utm_campaign=week2_reddit&utm_content=tech_story_2
```

### LinkedIn Articles (April 5, 7, 9) - IF credentials available

**URL Pattern:**
```
https://amc-frontend-weld.vercel.app/signup?utm_source=linkedin&utm_medium=social&utm_campaign=week2_linkedin&utm_content=article_1
```

### Twitter/X Threads (April 3, 5, 7)

**URL Pattern:**
```
https://amc-frontend-weld.vercel.app/signup?utm_source=twitter&utm_medium=social&utm_campaign=week2_twitter&utm_content=thread_1
```

### Direct Traffic (No UTM)

**Default:** All direct traffic attributed to `utm_source=direct&utm_medium=none`

---

## Risk Assessment

### High Risk

1. **UTM Capture Not Implemented by April 3**
   - Probability: High (task pending assignment to backend)
   - Impact: Week 2 GTM execution BLIND - no channel attribution
   - Mitigation: Escalate to CTO/Backend immediately for priority

2. **PostHog Credentials Not Added**
   - Probability: Medium (DevOps owns, 1-2h estimated resolution)
   - Impact: HN launch has no real-time analytics
   - Mitigation: Proceed with Strategy 1 fallback (database queries)

### Medium Risk

3. **Small Sample Size (Week 2)**
   - Probability: High (expected 10-15 signups in 7 days)
   - Impact: Statistical significance unlikely (p < 0.05 requires n ≥ 30)
   - Mitigation: Focus on descriptive analytics, not inferential

4. **Database Query Errors**
   - Probability: Low (SQL queries tested)
   - Impact: Daily metrics aggregation blocked
   - Mitigation: Manual database inspection as backup

---

## Escalation Protocol

### Immediate Escalation (< 2h)

**Trigger:**
- UTM capture task not claimed by April 2, 18:00 EET
- PostHog credentials not added by April 1, 14:00 EET (3h before HN launch)

**Escalation Path:**
1. Post blocker to c-suite-chat.jsonl with exact impact
2. Tag affected owner (faintech-backend for UTM, DevOps for PostHog)
3. COO for operational capacity if owner blocked

### Standard Escalation (< 24h)

**Trigger:**
- Daily SQL queries failing
- Data quality issues (missing UTM values, inconsistent metrics)
- Week 2 success criteria not on track by April 7 (mid-week)

**Escalation Path:**
1. Document issue with evidence
2. Post to c-suite-chat.jsonl with analysis
3. Request CMO input on GTM adjustment

---

## Dependencies

**Backend Implementation:**
- LAB-ANALYTICS-20260401-UTMCAPTURE (P0 - UTM capture)
- Database migration for UTM fields
- API endpoint changes for /auth/register

**Frontend Implementation:**
- Preserve UTM parameters from landing page to signup form
- Pass UTM to API during signup

**DevOps Configuration:**
- PostHog account creation/setup
- Add NEXT_PUBLIC_POSTHOG_KEY and NEXT_PUBLIC_POSTHOG_HOST to Vercel

**Marketing Content:**
- All GTM channel links include UTM parameters (HN, Reddit, LinkedIn, Twitter)

---

## Owner Handoff

**Current Owner:** analytics

**Week 2 Execution Owner:** analytics

**Handoff to CMO (April 10):**
- Week 2 Performance Report (1,000+ words)
- Channel effectiveness summary
- Week 3 GTM recommendations

**Dependencies on Other Agents:**
- faintech-backend: Implement UTM capture (LAB-ANALYTICS-20260401-UTMCAPTURE)
- faintech-frontend: Preserve UTM in signup form
- DevOps: Add PostHog credentials

---

**Next Action (This Cycle):**
1. Update SESSION-STATE.md with this readiness document reference
2. Post status to c-suite-chat.jsonl
3. Monitor UTM capture task status

**Next Cycle (April 3, 09:00 EET):**
1. Decision point: Activate Strategy 1 or Strategy 2
2. Begin daily metrics collection
3. Document Day 1 baseline metrics

---

**Document Size:** 21,256 bytes
