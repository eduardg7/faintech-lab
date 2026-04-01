# Week 2 GTM Analytics Execution Strategy

**Date:** 2026-04-01
**Owner:** analytics
**Project:** faintech-lab (AMC MVP)

---

## Executive Summary

Week 2 GTM execution (April 3-10) faces two critical blockers:
1. **PostHog credentials MISSING** (DevOps) - Blocks real-time analytics
2. **UTM capture NOT implemented** (faintech-backend) - Blocks channel attribution

This document provides a decision tree and execution plan for Week 2 GTM analytics based on blocker resolution status by April 3, 09:00 EET.

---

## Decision Tree

### Strategy 3: Real-Time PostHog Analytics (Ideal)
**Trigger:** PostHog configured + UTM capture complete by April 3, 09:00 EET

**Capabilities:**
- Real-time event tracking (user_signup, email_verified, memory_created, search_executed)
- Live funnel monitoring (signup → activation → first memory → first query)
- Channel attribution via UTM parameters
- A/B test variant tracking
- Daily dashboards with automatic updates

**Execution:**
- Activate PostHog event tracking in amc-frontend
- Verify all 6 core events firing correctly
- Monitor Plausible goals for signup funnel
- Daily metrics aggregation from PostHog API
- Weekly performance report with real-time insights

---

### Strategy 1: Descriptive Analytics via Database Queries (Fallback)
**Trigger:** UTM capture complete + PostHog NOT configured

**Capabilities:**
- Manual database queries for daily metrics
- Channel attribution (if UTM captured)
- Retention analysis (day-1/7/30)
- Basic funnel tracking (signup → activation)
- Daily metrics log (manual entry)

**Execution:**
- Run daily SQL queries at 10:00 EET (April 3-10)
- Collect: signups by channel, activation rate, retention, time-to-first-action
- Update daily metrics log template
- Weekly performance report (manual compilation)
- No real-time dashboards, delayed insights

**Limitations:**
- No real-time monitoring
- Delayed data availability (24h lag)
- Requires UTM capture for channel attribution
- No A/B test variant tracking

---

### Strategy 2: No Analytics / Manual Tracking Only (Last Resort)
**Trigger:** UTM capture NOT complete by April 3, 09:00 EET

**Capabilities:**
- Signup count from database (total, no channel attribution)
- Email verification tracking
- Manual user feedback collection
- No behavioral data (retention, engagement)

**Execution:**
- Daily signup count check
- Manual user interview for feedback
- Basic performance metrics (signup rate only)
- Week 2 post-mortem with qualitative data only

**Limitations:**
- NO channel attribution (cannot measure HN vs Reddit vs LinkedIn vs direct)
- NO activation tracking (cannot measure time-to-first-value)
- NO retention analysis (cannot measure day-1/7/30 retention)
- NO optimization guidance (cannot identify friction points)
- Week 2 GTM execution BLIND - cannot iterate or improve

---

## Daily Execution Schedule (April 3-10)

### 10:00 EET Data Collection Routine
**Strategy 1 (Database Queries):**
```sql
-- Signups by channel
SELECT
  utm_source,
  utm_medium,
  utm_campaign,
  COUNT(*) as signups,
  COUNT(DISTINCT u.id) as unique_users
FROM users u
WHERE u.created_at >= CURRENT_DATE
GROUP BY utm_source, utm_medium, utm_campaign;

-- Activation rate
SELECT
  COUNT(DISTINCT CASE WHEN m.created_at IS NOT NULL THEN u.id END) as activated_users,
  COUNT(*) as total_signups,
  ROUND(COUNT(DISTINCT CASE WHEN m.created_at IS NOT NULL THEN u.id END) * 100.0 / COUNT(*), 2) as activation_rate
FROM users u
LEFT JOIN memories m ON u.id = m.user_id
WHERE u.created_at >= CURRENT_DATE;

-- Retention (day-1)
SELECT
  COUNT(DISTINCT CASE WHEN COUNT(m.id) > 1 THEN u.id END) as day1_retained,
  COUNT(*) as total_signups,
  ROUND(COUNT(DISTINCT CASE WHEN COUNT(m.id) > 1 THEN u.id END) * 100.0 / COUNT(*), 2) as retention_rate
FROM users u
LEFT JOIN memories m ON u.id = m.user_id AND m.created_at >= u.created_at
WHERE u.created_at >= CURRENT_DATE - INTERVAL '1 day'
GROUP BY u.id;
```

**Strategy 2 (No Analytics):**
- Count total signups: `SELECT COUNT(*) FROM users WHERE created_at >= CURRENT_DATE;`
- Count verified emails: `SELECT COUNT(*) FROM users WHERE email_verified = TRUE AND created_at >= CURRENT_DATE;`
- Manual user outreach for feedback

### 18:00 EET Daily Summary Update
- Update daily metrics log
- Flag anomalies (zero signups, <50% activation, <30% retention)
- Prepare escalation if metrics below thresholds

---

## Success Metrics (Week 2 GTM)

### Target (Week 2 - April 3-10)
- Total signups: 10-15 (minimum 5-10)
- Activation rate: >70% (minimum 60-70%)
- Day-1 retention: >40% (minimum 30-40%)
- HN conversion: >4% (minimum 2-4%)
- MRR generated: €20-30 (minimum €10-20)

### Fallback (Strategy 2 - No Analytics)
- Total signups: 3-5 (minimum 1-3)
- Cannot measure activation, retention, or conversion
- Manual user feedback only

---

## Risk Mitigation

### Risk 1: PostHog Configuration Delays
**Probability:** High (DevOps priority unclear)
**Impact:** No real-time analytics for HN launch and Week 2 GTM
**Mitigation:**
- Activate Strategy 1 (database queries) at 10:00 EET on April 3
- Manual daily metrics log
- Escalate to DevOps daily until resolved

### Risk 2: UTM Capture Not Implemented
**Probability:** Medium (faintech-backend task LAB-ANALYTICS-20260401-UTMCAPTURE pending)
**Impact:** Channel attribution IMPOSSIBLE - cannot measure HN vs Reddit vs LinkedIn vs direct
**Mitigation:**
- Monitor faintech-backend task status daily
- Escalate to CTO if not in_progress by April 2
- Prepare Strategy 2 (no analytics) as last resort

### Risk 3: Zero Signups (Repeat of Week 1)
**Probability:** Low (Week 1 failed due to external blockers, not PMF)
**Impact:** Cannot validate GTM effectiveness or iterate
**Mitigation:**
- Daily signups tracking (10:00 EET)
- Escalate to CMO within 4h if zero signups for 3 consecutive days
- Distribution execution audit (check Reddit posts, LinkedIn articles, HN submission)

---

## Escalation Protocol

### P0 Blockers (Immediate Escalation Required)
- **PostHog credentials missing** → Escalate to DevOps + COO
- **UTM capture not implemented** → Escalate to CTO + faintech-backend
- **Zero signups for 3 consecutive days** → Escalate to CMO + CEO

### P1 Issues (Escalate within 4h)
- **Daily metrics not collected** → Escalate to analytics owner
- **Database query failures** → Escalate to faintech-backend + DevOps
- **Metrics below thresholds (activation <50%, retention <20%)** → Escalate to CPO + CMO

---

## Next Actions

### April 1, 2026 (HN Launch Day)
- Monitor HN launch traffic via Plausible (no PostHog available)
- Document HN post URL for channel tracking (if UTM capture active)
- Prepare Week 2 execution based on blocker resolution status

### April 2, 2026 (Week 2 Eve)
- **Decision Point (09:00 EET):**
  - If PostHog configured + UTM capture complete → Activate Strategy 3
  - If UTM capture complete + PostHog NOT configured → Activate Strategy 1
  - If UTM capture NOT complete → Activate Strategy 2 (last resort)
- Update analytics execution brief with selected strategy
- Notify CMO and PM of analytics capabilities for Week 2

### April 3, 2026 (Week 2 Day 1)
- Execute first 10:00 EET data collection routine
- Update daily metrics log
- Post status to c-suite-chat with baseline metrics

---

## Related Documents

- Week 2 GTM Analytics Readiness: `/Users/eduardgridan/faintech-lab/docs/analytics/week2-gtm-analytics-readiness-2026-04-01.md` (16.5KB)
- Revenue Attribution Framework: `/Users/eduardgridan/faintech-lab/docs/analytics/revenue-attribution-framework.md` (11.9KB)
- UTM Capture Gap Analysis: `/Users/eduardgridan/faintech-lab/docs/analytics/UTM-CAPTURE-GAP-2026-04-01.md` (13.9KB)
- Weekly Performance Report Template: `/Users/eduardgridan/faintech-lab/data/ops/GTM-WEEK2-ANALYTICS-TEMPLATES.md` (17.8KB)

---

**Status:** Ready for execution starting April 3, 2026, based on blocker resolution by April 2, 09:00 EET.
