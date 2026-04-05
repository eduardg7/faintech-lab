# Week 2 GTM Success Metrics Framework
**Created:** 2026-04-02T21:36:00+02:00
**Owner:** strategy
**Launch Date:** April 3, 09:00 EET
**Measurement Period:** April 3-10, 2026 (7 days)

---

## Executive Summary

Week 2 GTM launches April 3, 09:00 EET. This document defines SMART (Specific, Measurable, Achievable, Relevant, Time-bound) success metrics to evaluate launch performance across acquisition, activation, engagement, and revenue.

**Primary Goal:** 10-15 qualified signups by April 10
**Success Threshold:** ≥10 signups with >5% conversion and >70% activation

---

## Success Metrics

### 1. Acquisition Metrics

**Metric 1.1: Total Signups**
- **Definition:** Number of new user accounts created via any channel
- **Target:** 10-15 signups by April 10
- **Measurement:** Database query, daily count
- **Success Threshold:** ≥10 signups
- **Stretch Goal:** ≥15 signups
- **Tracking:** Daily at 09:00 and 17:00 EET

**Metric 1.2: Channel-Specific Signups**
- **Definition:** Signups attributed to specific channels (HN, Reddit, LinkedIn, Twitter, Direct)
- **Target:** Minimum 1 signup per active channel
- **Measurement:** UTM parameters + referral tracking
- **Success Threshold:** ≥1 signup per channel
- **Tracking:** Continuous (UTM fallback active)

**Metric 1.3: Traffic-to-Signup Conversion Rate**
- **Definition:** (Signups / Unique Visitors) × 100
- **Target:** >5%
- **Measurement:** Google Analytics / Vercel Analytics
- **Success Threshold:** ≥5%
- **Stretch Goal:** ≥7%
- **Tracking:** Daily aggregation

### 2. Activation Metrics

**Metric 2.1: First Memory Creation Rate**
- **Definition:** % of signups who create ≥1 memory within 24h of signup
- **Target:** >70%
- **Measurement:** Database query (memories table, created_at within 24h of user creation)
- **Success Threshold:** ≥70%
- **Stretch Goal:** ≥80%
- **Tracking:** Daily at 18:00 EET

**Metric 2.2: Time to First Memory**
- **Definition:** Median time between signup and first memory creation
- **Target:** <10 minutes
- **Measurement:** Timestamp comparison (user.created_at vs first_memory.created_at)
- **Success Threshold:** <10 minutes
- **Tracking:** Continuous

### 3. Engagement Metrics

**Metric 3.1: DAU/MAU Ratio**
- **Definition:** Daily Active Users / Monthly Active Users
- **Target:** >20%
- **Measurement:** Unique users with ≥1 action per day / unique users with ≥1 action per 30 days
- **Success Threshold:** ≥20%
- **Stretch Goal:** ≥30%
- **Tracking:** Daily at 18:00 EET

**Metric 3.2: Average Memories per User**
- **Definition:** Total memories created / Total active users
- **Target:** ≥3 memories per user by April 10
- **Measurement:** Database query
- **Success Threshold:** ≥3
- **Tracking:** Daily aggregation

**Metric 3.3: Return Visit Rate**
- **Definition:** % of signups who return within 7 days
- **Target:** >50%
- **Measurement:** Session tracking, unique visitor matching
- **Success Threshold:** ≥50%
- **Tracking:** End of Week 2 (April 10)

### 4. Revenue Indicators

**Metric 4.1: Customer Acquisition Cost (CAC)**
- **Definition:** Total GTM costs / Number of signups
- **Target:** <€100 per signup
- **Measurement:** (Model usage costs + tool costs) / signups
- **Success Threshold:** <€100
- **Stretch Goal:** <€50
- **Tracking:** End of Week 2

**Metric 4.2: Revenue per Signup**
- **Definition:** Projected annual revenue per signup (based on pricing tier)
- **Target:** Track for future LTV analysis
- **Measurement:** User tier selection at signup (if implemented)
- **Tracking:** Post-launch analysis

### 5. Operational Metrics

**Metric 5.1: Backend Uptime**
- **Definition:** % time backend returns HTTP 200
- **Target:** >99%
- **Measurement:** Vercel monitoring, health check endpoints
- **Success Threshold:** ≥99%
- **Current Status:** HTTP 200 (verified 20:27 EET, 34h+ issue resolved)
- **Tracking:** Continuous

**Metric 5.2: Page Load Time**
- **Definition:** Median time to interactive for landing page
- **Target:** <3 seconds
- **Measurement:** Vercel Analytics
- **Success Threshold:** <3s
- **Tracking:** Continuous

---

## Measurement Methodology

### Data Collection
- **Primary Source:** Application database (users, memories tables)
- **Secondary Source:** UTM parameters (client-side capture, PostHog when credentials available)
- **Tertiary Source:** Vercel Analytics (traffic, performance)
- **Manual Tracking:** Social engagement (upvotes, comments, shares)

### Reporting Cadence
- **Daily Brief:** 18:00 EET (signups, activation rate, DAU/MAU)
- **Weekly Report:** April 10, 18:00 EET (comprehensive analysis)
- **Real-time Dashboard:** When PostHog credentials available

### Success Criteria Framework
- **FAIL:** <10 signups OR <5% conversion OR <70% activation
- **PASS:** 10-12 signups, ≥5% conversion, ≥70% activation
- **SUCCESS:** 13-15 signups, ≥6% conversion, ≥75% activation
- **EXCEEDS:** >15 signups, ≥7% conversion, ≥80% activation

---

## Risk Factors

**Risk 1: PostHog Credentials Missing**
- **Impact:** Partial attribution (UTM fallback active)
- **Mitigation:** Client-side UTM capture operational
- **Status:** DevOps blocker, tracking continues with fallback

**Risk 2: Backend Instability**
- **Impact:** Signup failures, poor user experience
- **Mitigation:** HTTP 200 confirmed, monitoring active
- **Status:** Resolved (verified 20:27 EET)

**Risk 3: Low Channel Engagement**
- **Impact:** Below-target signups
- **Mitigation:** Multiple channels (HN, Reddit, LinkedIn, Twitter, Direct)
- **Status:** Content ready (67KB), channels prepared

---

## Next Actions

1. **April 3, 09:00 EET:** Week 2 GTM launch
2. **April 3, 18:00 EET:** First daily metrics report
3. **April 10, 18:00 EET:** Week 2 comprehensive analysis
4. **Post-Week 2:** Partnership activation (if >5% conversion, >70% activation, CAC <€100)

---

**Document Owner:** strategy agent
**Last Updated:** 2026-04-02T21:36:00+02:00
**Next Review:** April 3, 18:00 EET (first daily metrics report)
