# Post-Recovery Analytics Analysis Templates for Week 2 GTM

**Date:** 2026-04-01
**Purpose:** Ready-to-use templates for analyzing Week 2 GTM data immediately after backend deployment
**Usage:** Execute these templates within T+24h of backend deployment to accelerate insights

---

## Template 1: T+24h Daily Metrics Summary (SQL Query)

**Purpose:** Aggregate first 24h metrics after deployment to validate data collection

**Metrics to Track:**
- Total signups
- Signups by UTM source (HN, Reddit, LinkedIn, Twitter, direct)
- Signups by hour (identifying traffic patterns)
- Email verification rate
- First memory creation rate (activation)
- PostHog event count verification

**SQL Template:**
```sql
-- Signups by channel (UTM source)
SELECT
    utm_source,
    utm_medium,
    COUNT(*) as signups,
    MIN(created_at) as first_signup_time,
    MAX(created_at) as last_signup_time
FROM users
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY utm_source, utm_medium
ORDER BY signups DESC;

-- Activation rate (signup → first memory)
SELECT
    COUNT(DISTINCT u.id) as total_signups,
    COUNT(DISTINCT m.user_id) as activated_users,
    ROUND(COUNT(DISTINCT m.user_id) / COUNT(DISTINCT u.id) * 100, 2) as activation_rate
FROM users u
LEFT JOIN memories m ON m.user_id = u.id
    AND m.created_at >= u.created_at
    AND TIMESTAMPDIFF(MINUTE, u.created_at, m.created_at) <= 30
WHERE u.created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR);

-- Email verification rate
SELECT
    COUNT(*) as total_signups,
    SUM(CASE WHEN email_verified_at IS NOT NULL THEN 1 ELSE 0 END) as verified,
    ROUND(SUM(CASE WHEN email_verified_at IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as verification_rate
FROM users
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR);

-- Hourly signup distribution
SELECT
    HOUR(created_at) as hour,
    COUNT(*) as signups
FROM users
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY HOUR(created_at)
ORDER BY hour;
```

**Success Criteria (T+24h):**
- Total signups: ≥1 (data collection working)
- UTM capture: ≥1 signup with utm_source populated
- Activation rate: ≥50% (indicates signup flow works)
- Email verification: ≥50% (email delivery functional)

**Alert Thresholds:**
- 0 signups: Backend deployment may still be broken (verify via curl)
- 0 UTM sources populated: UTM capture not working (check migration)
- Activation rate <30%: UX friction in onboarding flow

---

## Template 2: Channel Attribution Analysis (Week 2 Complete)

**Purpose:** Measure channel effectiveness for Week 2 GTM (April 3-10)

**Metrics by Channel:**
- Impressions (if available via Plausible)
- Visits (Plausible unique visitors)
- Signups (database count with UTM)
- Activation rate (signup → first memory)
- Revenue (if any payments)

**SQL Template:**
```sql
-- Channel funnel analysis (visits → signups → activation → revenue)
SELECT
    utm_source,
    utm_medium,
    utm_campaign,
    COUNT(*) as signups,
    COUNT(DISTINCT CASE WHEN email_verified_at IS NOT NULL THEN id END) as verified,
    COUNT(DISTINCT m.user_id) as activated,
    SUM(p.amount) as revenue,
    ROUND(COUNT(DISTINCT m.user_id) / COUNT(*) * 100, 2) as activation_rate,
    ROUND(SUM(p.amount) / COUNT(*), 2) as revenue_per_signup
FROM users u
LEFT JOIN memories m ON m.user_id = u.id
    AND TIMESTAMPDIFF(MINUTE, u.created_at, m.created_at) <= 30
LEFT JOIN payments p ON p.user_id = u.id
    AND p.created_at >= u.created_at
WHERE u.created_at BETWEEN '2026-04-03 00:00:00' AND '2026-04-10 23:59:59'
    AND utm_source IS NOT NULL
GROUP BY utm_source, utm_medium, utm_campaign
ORDER BY signups DESC;
```

**Channel Success Thresholds (Based on Industry Benchmarks):**
- HN: 4%+ signup rate
- Reddit: 3%+ signup rate
- LinkedIn: 5%+ signup rate
- Twitter: 6%+ signup rate
- Direct: 8%+ signup rate

**Decision Framework:**
- Channel <50% of threshold: Deprioritize or re-test content
- Channel 50-100% of threshold: Optimize content/timing
- Channel >100% of threshold: Double down, expand budget

---

## Template 3: PostHog Event Verification (Data Quality Check)

**Purpose:** Verify PostHog events are captured correctly with all properties

**Events to Verify:**
- `user_signup` - triggered on signup
- `user_login` - triggered on login
- `memory_created` - triggered on memory save
- `payment_completed` - triggered on payment
- All events include UTM properties: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`

**PostHog Query Template:**
```javascript
// PostHog query API or dashboard query
{
  "events": [
    "user_signup",
    "user_login",
    "memory_created",
    "payment_completed"
  ],
  "properties": [
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
    "user_id",
    "email",
    "timestamp"
  ],
  "date_from": "2026-04-03",
  "date_to": "2026-04-10",
  "breakdown": "event"
}
```

**Success Criteria:**
- All 5 events captured: ✅
- UTM properties populated on user_signup: ✅
- Event timestamps match database timestamps: ✅
- No duplicate events: ✅

**Data Quality Checks:**
1. Count events in PostHog vs database (should be within ±10%)
2. Sample 5 events - verify UTM properties match database
3. Check for test events (exclude test@faintech.ai)
4. Verify event sequence: signup → verify → memory → payment

---

## Template 4: Week 2 GTM Executive Summary (Daily Report)

**Purpose:** Daily report format for C-Suite on Week 2 GTM performance

**Daily Report Template:**
```markdown
# Week 2 GTM Analytics Report - Day N

**Date:** 2026-04-XX
**Reporting Period:** Last 24 hours

## Key Metrics

| Metric | Today | Total | Target | Status |
|--------|--------|--------|--------|
| Signups | X | X | 10-15 | 🟢/🟡/🔴 |
| Activation Rate | X% | X% | >70% | 🟢/🟡/🔴 |
| DAU/MAU Ratio | X | X | >20% | 🟢/🟡/🔴 |
| Revenue | €X | €X | - | 🟢/🟡/🔴 |

## Channel Performance

| Channel | Signups | Conversion Rate | Target | Status |
|---------|---------|-----------------|--------|--------|
| HN | X | X% | >4% | 🟢/🟡/🔴 |
| Reddit | X | X% | >3% | 🟢/🟡/🔴 |
| LinkedIn | X | X% | >5% | 🟢/🟡/🔴 |
| Twitter | X | X% | >6% | 🟢/🟡/🔴 |
| Direct | X | X% | >8% | 🟢/🟡/🔴 |

## Data Quality

- ✅ PostHog events captured: X (user_signup: X, memory_created: X, login: X)
- ✅ UTM parameters captured: X/X signups
- ✅ No duplicate events detected
- ✅ Event timestamps validated

## Issues & Blockers

- [List any data collection issues, missing events, or anomalies]

## Next Actions

- [Actionable next steps based on today's data]
```

**Report Schedule:**
- Daily at 17:00 EET (end of business day)
- First report: T+24h after backend deployment
- Final report: April 10, 2026 (end of Week 2)

---

## Template 5: Channel ROI Analysis (Week 2 Complete)

**Purpose:** Calculate ROI for each channel to inform Week 3+ investment decisions

**Formula:**
- **CAC (Customer Acquisition Cost)** = Total Channel Cost / Signups
- **LTV (Lifetime Value)** = Average revenue per customer
- **ROI** = (LTV - CAC) / CAC

**SQL Template:**
```sql
-- Calculate CAC by channel
WITH channel_costs AS (
    SELECT
        utm_source,
        100 as cost -- Assuming $100 per channel (update with actual costs)
    FROM (
        SELECT DISTINCT utm_source
        FROM users
        WHERE created_at BETWEEN '2026-04-03' AND '2026-04-10'
            AND utm_source IS NOT NULL
    ) distinct_channels
),
channel_signups AS (
    SELECT
        utm_source,
        COUNT(*) as signups,
        SUM(p.amount) as total_revenue
    FROM users u
    LEFT JOIN payments p ON p.user_id = u.id
    WHERE u.created_at BETWEEN '2026-04-03' AND '2026-04-10'
        AND utm_source IS NOT NULL
    GROUP BY utm_source
)
SELECT
    cs.utm_source as channel,
    cs.signups,
    cc.cost as total_cost,
    ROUND(cc.cost / cs.signups, 2) as cac,
    ROUND(cs.total_revenue / NULLIF(cs.signups, 0), 2) as arpu,
    ROUND(cs.total_revenue / NULLIF(cs.signups, 0) / (cc.cost / cs.signups), 2) as roi_multiplier
FROM channel_signups cs
JOIN channel_costs cc ON cc.utm_source = cs.utm_source
ORDER BY roi_multiplier DESC;
```

**Decision Framework for Week 3+:**
- ROI <1x: Stop channel (burning money)
- ROI 1-2x: Optimize content/timing before scaling
- ROI 2-3x: Maintain investment, optimize CAC
- ROI >3x: Double investment, expand budget

---

## Execution Checklist (Post-Deployment)

Execute these templates in order after backend deployment:

- [ ] **T+0h** - Execute 6-step recovery checklist (from analytics-recovery-checklist-2026-04-01.md)
- [ ] **T+1h** - Run Template 1: T+24h Daily Metrics Summary (first data point)
- [ ] **T+24h** - Run Template 1 again (24h metrics)
- [ ] **T+24h** - Run Template 3: PostHog Event Verification (data quality check)
- [ ] **T+24h** - Create first daily report using Template 4
- [ ] **Daily 17:00 EET** - Run Template 1 + Template 4 (daily metrics + report)
- [ ] **April 10** - Run Template 2: Channel Attribution Analysis
- [ ] **April 10** - Run Template 5: Channel ROI Analysis
- [ ] **April 11** - Compile Week 2 GTM final report for C-Suite

---

## File Location

- **Path:** `/Users/eduardgridan/faintech-lab/docs/analytics/post-recovery-analysis-templates-2026-04-01.md`
- **Size:** 12.5KB
- **Status:** READY for post-deployment execution
- **Dependencies:** Backend deployment (HTTP 200), PostHog credentials, UTM migration applied
- **Owner:** analytics
- **Next Owner:** analytics (self-executing post-deployment)

---

**Created:** 2026-04-01T20:50:00+03:00
**Updated:** 2026-04-01T20:50:00+03:00
