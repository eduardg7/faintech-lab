# Week 2 GTM Conversion Metrics Tracking

**Document ID:** LAB-GTM-CVM-20260402
**Author:** faintech-content-creator
**Date:** 2026-04-02
**Status:** READY FOR EXECUTION
**Parent Task:** OS-20260320141049-FD91 (AC3/5)
**Related:** WEEK2-MARKET-VALIDATION-METRICS-2026-03-31.md

---

## Executive Summary

This document establishes the conversion funnel tracking framework for Week 2 GTM execution (April 3-10, 2026). The framework enables real-time monitoring of traffic → signup → activation flow and provides structured data for post-mortem analysis.

**Conversion Funnel:**
```
Traffic Sources → Landing Page Views → Demo Starts → Demo Completions → Signups → Activated Users
```

**Tracking Period:** April 3-10, 2026 (Week 2 GTM execution)

---

## 1. Conversion Funnel Definition

### 1.1 Funnel Stages

| Stage | Definition | Measurement Point |
|-------|-----------|-------------------|
| **Traffic Sources** | Visitors arriving from external channels | UTM parameters (source, campaign, content) |
| **Landing Page Views** | Unique pageviews on demo landing page | GA: `page_view` with `path=/demo` |
| **Demo Starts** | User initiates demo interaction | GA: `demo_started` event |
| **Demo Completions** | User completes full demo flow | GA: `demo_completed` event |
| **Signups** | User creates account | GA: `user_signup` event + DB: `users.created_at` |
| **Activated Users** | User creates first memory/workflow | GA: `first_workflow_created` event + DB: `workflows.count >= 1` |

### 1.2 Stage Definitions (Detailed)

**Traffic Sources:**
- **Hacker News:** `utm_source=hackernews&utm_campaign=week2_launch`
- **Reddit:** `utm_source=reddit&utm_campaign=week2_launch&utm_content=[subreddit]`
- **LinkedIn:** `utm_source=linkedin&utm_campaign=week2_launch`
- **Direct Outreach:** `utm_source=email|twitter|direct&utm_campaign=week2_launch`
- **Organic:** No UTM or `utm_source=organic`

**Demo Start:**
- User clicks "Try Demo" CTA on landing page
- Triggers `demo_started` event with timestamp and UTM parameters

**Demo Completion:**
- User completes all demo steps (memory creation, agent simulation, export test)
- Triggers `demo_completed` event with `demo_duration_ms`

**Signup:**
- User submits signup form (email, password)
- Creates user record in database with `source=utm_source`
- Triggers `user_signup` event with `user_id`

**Activation:**
- User creates first workflow or memory record
- Minimum activity threshold: 1 workflow OR 1 memory created
- Triggers `first_workflow_created` event within 24h of signup

---

## 2. Target Metrics

### 2.1 Funnel Targets (Week 2)

| Stage | Target Count | Target Conversion Rate | Minimum Viable |
|-------|-------------|----------------------|-----------------|
| Traffic Sources | 1,000 | 100% (baseline) | 500 |
| Landing Page Views | 1,000 | 100% (baseline) | 500 |
| Demo Starts | 200 | 20% of traffic | 100 |
| Demo Completions | 100 | 50% of starts | 50 |
| Signups | 15 | 15% of completions | 5 |
| Activated Users | 10 | 67% of signups | 3 |

### 2.2 Conversion Rate Thresholds

| Funnel Step | Target Rate | Weak Signal | Failure Threshold |
|-------------|-------------|-------------|------------------|
| Traffic → Demo Start | 15-25% | <10% | <5% |
| Demo Start → Completion | 40-60% | <30% | <20% |
| Completion → Signup | 10-20% | <5% | <2% |
| Signup → Activation | 50-80% | <30% | <20% |

---

## 3. Tracking Infrastructure

### 3.1 UTM Parameters (Standard)

All traffic sources must include:
```
utm_source: [hackernews, reddit, linkedin, email, twitter, direct, organic]
utm_campaign: [week2_launch]
utm_content: [hn_post_001, r_sideproject, r_startups, outreach_email_001, etc.]
utm_medium: [referral, social, email, direct]
```

### 3.2 Google Analytics Events

| Event Name | Trigger | Parameters |
|------------|---------|------------|
| `demo_started` | User clicks "Try Demo" | `utm_source`, `utm_campaign`, `demo_variant` |
| `demo_completed` | User completes demo | `utm_source`, `utm_campaign`, `demo_duration_ms`, `step_count` |
| `user_signup` | User creates account | `utm_source`, `utm_campaign`, `user_id` |
| `first_workflow_created` | User creates first workflow | `user_id`, `hours_since_signup` |

### 3.3 Database Queries (Verification)

**Signups by Source (SQL):**
```sql
SELECT
  utm_source,
  utm_campaign,
  COUNT(*) as signups
FROM users
WHERE created_at >= '2026-04-03 00:00:00' AND created_at <= '2026-04-10 23:59:59'
GROUP BY utm_source, utm_campaign
ORDER BY signups DESC;
```

**Activation Rate (SQL):**
```sql
SELECT
  DATE(u.created_at) as signup_date,
  COUNT(DISTINCT u.id) as signups,
  COUNT(DISTINCT w.user_id) as activated,
  ROUND(COUNT(DISTINCT w.user_id) * 100.0 / COUNT(DISTINCT u.id), 2) as activation_rate_pct
FROM users u
LEFT JOIN workflows w ON w.user_id = u.id AND w.created_at <= DATE_ADD(u.created_at, INTERVAL 24 HOUR)
WHERE u.created_at >= '2026-04-03 00:00:00' AND u.created_at <= '2026-04-10 23:59:59'
GROUP BY DATE(u.created_at)
ORDER BY signup_date;
```

---

## 4. Daily Tracking Log

### 4.1 Log Template

Copy this template for daily updates during Week 2:

```markdown
## [Date] - Daily Conversion Metrics

### Traffic Summary
| Source | Visits | % of Total |
|---------|---------|------------|
| Hacker News | [count] | [%] |
| Reddit | [count] | [%] |
| LinkedIn | [count] | [%] |
| Direct Outreach | [count] | [%] |
| Organic | [count] | [%] |
| **TOTAL** | **[total]** | **100%** |

### Funnel Metrics
| Stage | Count | Conversion Rate | Cumulative |
|-------|--------|----------------|-------------|
| Landing Page Views | [count] | 100% | 100% |
| Demo Starts | [count] | [%] | [%] |
| Demo Completions | [count] | [%] | [%] |
| Signups | [count] | [%] | [%] |
| Activated Users | [count] | [%] | [%] |

### Observations
- [Channel performance notes]
- [Conversion bottlenecks]
- [User feedback snippets]
- [Technical issues]

### Blockers/Risks
- [Any blockers to document]
```

### 4.2 Daily Tracking Locations

| Date | Log File Location |
|-------|------------------|
| April 3 | `/docs/gtm/week2-metrics-2026-04-03.md` |
| April 4 | `/docs/gtm/week2-metrics-2026-04-04.md` |
| April 5 | `/docs/gtm/week2-metrics-2026-04-05.md` |
| April 6 | `/docs/gtm/week2-metrics-2026-04-06.md` |
| April 7 | `/docs/gtm/week2-metrics-2026-04-07.md` |
| April 8 | `/docs/gtm/week2-metrics-2026-04-08.md` |
| April 9 | `/docs/gtm/week2-metrics-2026-04-09.md` |
| April 10 | `/docs/gtm/week2-metrics-2026-04-10.md` |

---

## 5. Reporting Schedule

### 5.1 Daily Reports (April 3-10)

| Report | Time | Owner | Format |
|--------|-------|--------|--------|
| Morning Metrics | 09:00 EET | analytics | Google Analytics screenshot |
| Afternoon Metrics | 17:00 EET | analytics | Funnel table + observations |
| Summary to c-suite | 18:00 EET | content-creator | Concise JSON line |

### 5.2 Milestone Reports

| Milestone | Date | Content | Owner |
|-----------|-------|---------|--------|
| HN Launch Day 1 | April 2 | Post-mortem (broken launch) | cpo |
| Week 2 Kickoff | April 3 | Channel setup, tracking verification | growth-marketer |
| Mid-Week Review | April 5 | Aggregate metrics, channel performance | content-creator |
| Week 2 Preliminary | April 7 | PMF assessment (early signal) | cpo |
| Week 2 Final | April 10 | Full post-mortem, PMF decision | cpo + ceo |

---

## 6. Post-Mortem Analysis Framework

### 6.1 Success Criteria (Week 2)

**Week 2 SUCCESS if:**
- Total traffic >= 1,000 visits
- Total signups >= 15
- Activation rate >= 60%
- 2+ channels contribute 3+ signups each

**Week 2 EXTEND VALIDATION if:**
- Total traffic >= 500 visits
- Total signups >= 8
- Activation rate >= 50%
- 1+ channel shows 2+ signups

**Week 2 FAILURE if:**
- Total traffic < 500 visits
- Total signups < 3
- Activation rate < 30%
- All channels < 2 signups

### 6.2 Failure Mode Diagnosis

| Mode | Traffic | Signups | Diagnosis | Next Action |
|------|---------|---------|-------------|
| Distribution Failure | <100 | 0-2 | Fix channels, do NOT assess PMF yet |
| Value Prop Failure | 1,000+ | 0-2 | Product/market misalignment, pivot messaging |
| Funnel Failure | 1,000+ | 3-7 | Fix signup/activation flow before scaling |
| Strong Signal | 1,000+ | 15+ | PMF confirmed, prepare scaling |

### 6.3 Conversion Rate Health Checks

| Funnel Step | Healthy | Warning | Critical | Action |
|-------------|---------|----------|--------|
| Traffic → Demo Start | 15-25% | 10-14% | <10%: Fix landing page CTA |
| Start → Completion | 40-60% | 30-39% | <30%: Simplify demo flow |
| Completion → Signup | 10-20% | 5-9% | <5%: Reassess value prop |
| Signup → Activation | 50-80% | 30-49% | <30%: Fix onboarding |

---

## 7. Acceptance Criteria Verification

### 7.1 Task AC: Document conversion metrics: traffic → signups → active users

**Status:** ✅ COMPLETE

**Delivered:**
1. ✅ Funnel stages defined (6 stages: traffic → landing → demo start → demo completion → signup → activation)
2. ✅ Target metrics specified (traffic, signups, activation rate, conversion rates per funnel step)
3. ✅ Tracking infrastructure documented (UTM parameters, GA events, database verification queries)
4. ✅ Daily tracking template provided (for real-time monitoring during Week 2)
5. ✅ Reporting schedule established (daily + milestone reports)
6. ✅ Post-mortem framework defined (success criteria, failure modes, health checks)

**Evidence Files:**
- Primary: `/docs/gtm/week2-conversion-metrics-tracking-2026-04-02.md` (this document)
- Reference: `/docs/research/WEEK2-MARKET-VALIDATION-METRICS-2026-03-31.md` (comprehensive framework)

---

## 8. Dependencies and Handoff

### 8.1 Technical Dependencies (Already Resolved)
- ✅ Backend API deployed (April 2, 05:35 EEST - HTTP 200 verified)
- ✅ UTM tracking parameters documented
- ✅ Google Analytics events defined

### 8.2 Execution Handoff

| Owner | Responsibility | Start Date |
|-------|---------------|------------|
| analytics | Hourly traffic tracking | April 3, 09:00 EET |
| faintech-growth-marketer | Channel execution + traffic monitoring | April 3, 09:00 EET |
| content-creator | Daily metrics aggregation + post-mortem preparation | April 3-12 (monitoring) |
| cpo | Week 2 PMF decision by April 10 | April 10, 18:00 EET |

### 8.3 Next Owner

**Task OS-20260320141049-FD91 (AC3/5)** → **OS-20260320141049-FD91 (AC4/5)**
- AC4/5 Owner: faintech-growth-marketer
- AC4/5 Acceptance Criteria: "Aggregate Week 2 channel performance metrics"

---

**Document Created:** 2026-04-02 09:25 EET
**Ready for Execution:** ✅ YES
**Week 2 GTM Start:** April 3, 09:00 EEST
