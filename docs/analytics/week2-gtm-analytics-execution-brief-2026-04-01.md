# Week 2 GTM Analytics Execution Brief

**Created:** 2026-04-01T07:11:00+02:00
**Agent:** analytics
**Purpose:** Execute bounded analytics tracking for Week 2 GTM (April 3-10, 2026)

---

## Decision Tree - Which Strategy to Activate?

At **April 3, 09:00 EET**, activate one strategy:

### Strategy 3: Real-Time PostHog Analytics (Ideal)
**Activation Condition:**
- ✅ PostHog credentials configured (`NEXT_PUBLIC_POSTHOG_KEY` and `NEXT_PUBLIC_POSTHOG_HOST` in `.env.local`)
- ✅ UTM capture implemented (LAB-ANALYTICS-20260401-UTMCAPTURE done)

**Execution:**
- Monitor PostHog dashboard for real-time events: `user_signup`, `email_verified`, `agent_created`, `memory_created`, `search_executed`, `user_login`
- Track activation funnel: signup → email verification → first memory → first query
- Channel attribution via UTM parameters in PostHog events
- Daily metrics aggregation using Template 1 (17.8KB)
- Weekly performance report using Template 3 (1,000+ words)

### Strategy 1: Descriptive Analytics via Database Queries (Fallback)
**Activation Condition:**
- ❌ PostHog NOT configured
- ✅ UTM capture implemented (LAB-ANALYTICS-20260401-UTMCAPTURE done)

**Execution:**
- Daily SQL queries at 10:00 EET (from readiness document):
  ```sql
  -- Signups by channel
  SELECT utm_source, COUNT(*) as signups
  FROM users
  WHERE created_at >= '2026-04-03'
  GROUP BY utm_source;

  -- Activation rate
  SELECT
    COUNT(DISTINCT u.id) as signups,
    COUNT(DISTINCT m.user_id) as activated_users,
    ROUND(COUNT(DISTINCT m.user_id) * 100.0 / COUNT(DISTINCT u.id), 2) as activation_rate
  FROM users u
  LEFT JOIN memories m ON u.id = m.user_id
  WHERE u.created_at >= '2026-04-03';

  -- Day-1 retention
  SELECT
    COUNT(DISTINCT u.id) as day0_signups,
    COUNT(DISTINCT r.user_id) as day1_active,
    ROUND(COUNT(DISTINCT r.user_id) * 100.0 / COUNT(DISTINCT u.id), 2) as retention_rate
  FROM users u
  LEFT JOIN (SELECT DISTINCT user_id FROM memories WHERE created_at >= date('2026-04-04') AND created_at < date('2026-04-05')) r ON u.id = r.user_id
  WHERE u.created_at >= '2026-04-03' AND u.created_at < '2026-04-04';
  ```
- Manual metrics log using template from readiness document
- Weekly performance report using Template 3 (1,000+ words)

### Strategy 2: No Analytics (Worst Case)
**Activation Condition:**
- ❌ PostHog NOT configured
- ❌ UTM capture NOT implemented

**Execution:**
- Manual tracking only (Google Analytics via Plausible for pageviews)
- No channel attribution possible
- No signup-to-activation funnel metrics
- Only measure: Plausible pageviews, visits, referrers
- Weekly report: "Unable to measure Week 2 GTM effectiveness due to missing analytics infrastructure"

---

## Data Collection Schedule (Week 2)

### Daily at 10:00 EET (April 3-10)
- **Metric 1:** Total signups (cumulative)
- **Metric 2:** Signups by channel (UTM source)
- **Metric 3:** Activation rate (signup → first memory)
- **Metric 4:** Day-1 retention (users who return next day)
- **Metric 5:** Time-to-first-action (median time from signup to first memory)

### Weekly on April 10, 18:00 EET
- Generate Week 2 Performance Report (1,000+ words)
- Sections: Channel effectiveness, activation funnel, retention analysis, recommendations

---

## Success Metrics (Week 2 GTM)

**Target (from Francesca Tabor B2B SaaS benchmarks):**
- Total signups: 10-15 (minimum 5-10, fallback 3-5)
- Activation rate: >70% (minimum 60-70%, fallback 50-60%)
- Day-1 retention: >40% (minimum 30-40%, fallback 20-30%)
- HN conversion: >4% (minimum 2-4%, fallback 1-2%)
- MRR generated: €20-30 (minimum €10-20, fallback €5-10)

---

## Critical Dependencies

| Dependency | Status | Owner | Deadline |
|------------|--------|--------|----------|
| PostHog credentials | ❌ MISSING | DevOps | April 1, 17:00 EET |
| UTM capture (LAB-ANALYTICS-20260401-UTMCAPTURE) | ⏳ PENDING | faintech-backend | April 3, 09:00 EET |

---

## Current Blocker Status (2026-04-01 07:11 EET)

**PostHog Configuration:**
- ❌ NOT configured (verified at 07:11 EET)
- `amc-frontend/.env.local` contains only API URLs
- Missing: `NEXT_PUBLIC_POSTHOG_KEY`, `NEXT_PUBLIC_POSTHOG_HOST`
- Impact: HN launch (April 1) will have NO attribution data
- Resolution time: 1-2 hours (DevOps creates/configures PostHog account)

**UTM Capture:**
- ⏳ PENDING (LAB-ANALYTICS-20260401-UTMCAPTURE)
- Owner: faintech-backend
- No git activity on UTM-related files today
- Impact: Fallback Strategy 1 BLOCKED without UTM capture
- Resolution time: 3-4 hours (backend implementation + frontend updates)

---

## Next Actions

**Analytics (this cycle):**
- ✅ Created Week 2 GTM analytics execution brief (this document)
- ✅ Documented strategy decision tree
- ✅ Updated SESSION-STATE.md with blocker status

**Week 2 Execution (April 3, 09:00 EET):**
1. Check PostHog configuration status
2. Check UTM capture task completion
3. Activate appropriate strategy (1, 2, or 3)
4. Begin daily data collection

**If Blockers Persist:**
- Week 2 GTM execution will be **BLIND** (Strategy 2)
- Cannot measure channel effectiveness
- Cannot optimize GTM spend
- Revenue attribution impossible
- Escalate to CEO at April 3, 09:00 EET if both blockers unresolved

---

## Document References

- Week 2 GTM Analytics Readiness: `/Users/eduardgridan/faintech-lab/docs/analytics/week2-gtm-analytics-readiness-2026-04-01.md` (16.5KB)
- UTM Capture Gap Analysis: `/Users/eduardgridan/faintech-lab/docs/analytics/UTM-CAPTURE-GAP-2026-04-01.md` (13.9KB)
- Revenue Attribution Framework: `/Users/eduardgridan/faintech-lab/docs/analytics/revenue-attribution-framework.md` (11.9KB)
- Week 2 GTM Templates: `/Users/eduardgridan/faintech-lab/data/ops/GTM-WEEK2-ANALYTICS-TEMPLATES.md` (17.8KB)

---

**End of Execution Brief**
