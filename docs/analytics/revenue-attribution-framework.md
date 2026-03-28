# Revenue Attribution Framework

**Owner:** analytics
**Created:** 2026-03-27
**Purpose:** Track and validate channel effectiveness for AMC MVP revenue generation

---

## Context

**Post-Launch Status:** Day 4 (T+96h), 0 signups, 0 social posts
**Root Cause:** Distribution execution gap (NOT PMF failure)
**Blocker:** CEO decisions pending (Twitter Auth 70h+, HUNTER_API_KEY 82h+)

**Business Question:** Which distribution channels deliver quality signups that convert to revenue?

---

## Attribution Model

### Acquisition Channels

| Channel | Identifier | Tracking Method | Activation Status |
|----------|-------------|------------------|------------------|
| Hacker News | Referrer: `news.ycombinator.com` | 🟢 Not started |
| Twitter/X | Referrer: `twitter.com` + UTM parameters | 🔴 Blocked (auth) |
| LinkedIn | Referrer: `linkedin.com` + UTM parameters | 🟢 Not started |
| GitHub | Referrer: `github.com` (repo traffic) | 🟢 Active |
| Direct | No referrer (direct/bookmark) | 🟢 Active |

### Conversion Funnel

```
┌─────────────────────────────────────────────┐
│ Channel Traffic                              │
│     ↓                                        │
│ Landing Page Visit                           │
│     ↓                                        │
│ Click "Try AMC" / "Get Started"         │
│     ↓                                        │
│ Signup Form                                  │
│     ↓                                        │
│ Email Verification                            │
│     ↓                                        │
│ First Memory Stored (Activation)           │
│     ↓                                        │
│ First Payment (Revenue)                      │
└─────────────────────────────────────────────┘
```

### Key Metrics per Channel

| Metric | Definition | Target | Week 1 |
|---------|--------------|--------|----------|
| Impressions | Content views / post reach | - | Measure |
| Visits | Unique landing page visitors | - | Measure |
| Signups | Completed signup forms | 5-10 | **0** |
| Activations | First memory stored (day 1) | 60%+ | **0** |
| Revenue | First payment | - | **€0** |
| CAC (Customer Acquisition Cost) | Spend ÷ Signups | <$50 | - |
| LTV (Lifetime Value) | Revenue ÷ Customers | - | - |

---

## Implementation Steps

### Step 1: Configure PostHog Goals

**Location:** PostHog Dashboard → Data Management → Actions

**Funnel Events:**
1. `user_signup` - Track form submissions (already implemented in analytics.ts)
2. `email_verified` - Track email verification (already implemented in analytics.ts)
3. `signup_complete` - Track successful registration (user_signup event)
4. `memory_created` - Track activation (first memory, already implemented in analytics.ts)
5. `payment_complete` - Track first payment (revenue) - TO BE IMPLEMENTED

**PostHog Funnel Steps:**
1. Landing page visit → 2. User signup → 3. Email verified → 4. Memory created (activation) → 5. Payment complete

**Channel Filters (Breakdown by Referrer):**
- HN: Filter events where referrer contains `news.ycombinator.com`
- Twitter: Filter events where referrer contains `twitter.com`
- LinkedIn: Filter events where referrer contains `linkedin.com`
- GitHub: Filter events where referrer contains `github.com`
- Direct: Filter events with no referrer

### Step 2: Add UTM Parameters

**Template:** `?utm_source={channel}&utm_medium=social&utm_campaign=amc-launch`

**Channel-Specific UTMs:**
- HN: `utm_source=hackernews&utm_medium=referral&utm_campaign=amc-launch-v1`
- Twitter: `utm_source=twitter&utm_medium=social&utm_campaign=amc-launch-v1`
- LinkedIn: `utm_source=linkedin&utm_medium=social&utm_campaign=amc-launch-v1`
- GitHub: `utm_source=github&utm_medium=referral&utm_campaign=repo-readme`

### Step 3: Create Attribution Dashboard

**Queries to Track:**

**Weekly Report (Week 1):**
```sql
-- Signups by channel
SELECT
  referrer,
  COUNT(DISTINCT user_id) as signups,
  COUNT(DISTINCT CASE WHEN first_memory_at IS NOT NULL THEN user_id END) as activations,
  SUM(CASE WHEN first_payment_at IS NOT NULL THEN 1 ELSE 0 END) as revenue_users
FROM user_signups
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY referrer
ORDER BY signups DESC;
```

**Conversion Funnel by Channel:**
```sql
-- Funnel analysis
SELECT
  referrer,
  COUNT(DISTINCT session_id) as visits,
  COUNT(DISTINCT CASE WHEN event_type = 'signup_form_submit' THEN user_id END) as form_submissions,
  COUNT(DISTINCT CASE WHEN event_type = 'signup_verify_email' THEN user_id END) as email_verified,
  COUNT(DISTINCT CASE WHEN event_type = 'signup_complete' THEN user_id END) as signups,
  COUNT(DISTINCT CASE WHEN event_type = 'memory_create' THEN user_id END) as activations,
  COUNT(DISTINCT CASE WHEN event_type = 'payment_complete' THEN user_id END) as revenue_users
FROM attribution_events
WHERE event_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY referrer;
```

### Step 4: Monitor Channel Performance

**Success Signals (Week 1):**
- ✅ **Channel validates:** 10+ signups in first 7 days
- ✅ **Channel amplifies:** Other channels show organic traffic spike
- ⚠️ **Channel weak:** 0-5 signups with high CAC

**KPI Thresholds:**
- **Minimum CAC:** <$50 (acceptable)
- **Acceptable activation rate:** 60%+ (Mixpanel 2024 benchmark)
- **Week 1 target:** 5-10 signups across all channels

---

## Channel Launch Validation

### Hacker News (Day 1 Priority)

**Launch Date:** TBD (pending CEO decision)
**Content:** "Show HN: Agent Memory Cloud - AI-driven note-taking with privacy-first architecture"

**Success Metrics (24h post-launch):**
- Impression: 50+ upvotes on HN
- Visits: 100+ unique visitors to landing page
- Signups: 2-5 from HN referrer
- Comments: 10+ substantive discussions

**Validation:**
- If HN converts at 4%+ (5/125 visitors) → **SUCCESS** - invest more in HN
- If HN converts at <2% (0-2/125 visitors) → **WEAK** - focus on content quality

### Twitter/X (Post-Auth Priority)

**Launch Date:** TBD (pending Twitter auth approval)
**Content:** Thread structure
  1. Problem: "Developers hate context switching between tools"
  2. Solution: "AMC unifies all your workspaces in one place"
  3. Proof: 2-minute demo GIF, technical breakdown

**Success Metrics (7 days post-launch):**
- Impression: 1,000+ views (thread + profile link)
- Clicks: 100+ link clicks
- Visits: 50+ landing page visits from Twitter
- Signups: 3-8 from Twitter referrer
- Engagement: 50+ replies/bookmarks

**Validation:**
- If Twitter converts at 6%+ (8/133 visitors) → **SUCCESS** - engage daily
- If Twitter converts at <3% (0-2/133 visitors) → **WEAK** - improve content tone

### LinkedIn (Week 1 Priority)

**Launch Date:** TBD (pending distribution strategy decision)
**Content:** Article format
  - Title: "How AI Agents Manage Project Context for Developers"
  - Problem: "Technical documentation is scattered across repos, wikis, Notion"
  - Solution: "AMC provides unified workspace with Git repo sync"
  - Proof: Architecture diagram, 3-minute walkthrough video

**Success Metrics (14 days post-launch):**
- Impressions: 2,000+ views (article + reposts)
- Visits: 80+ landing page visits from LinkedIn
- Signups: 4-10 from LinkedIn referrer

**Validation:**
- If LinkedIn converts at 5%+ (8/160 visitors) → **SUCCESS** - expand LinkedIn network
- If LinkedIn converts at <3% (0-4/160 visitors) → **WEAK** - improve targeting

---

## Attribution Reporting

### Daily Report Format

**Date:** 2026-03-27
**Status:** Pre-Distribution (all channels blocked)

**Summary:**
```
Channel Impressions Visits Signups Activations Revenue CAC
HN           0           0       0          0          -     -
Twitter       0           0       0          0          -     -
LinkedIn       0           0       0          0          -     -
GitHub        0           0       0          0          -     -
Direct        0           0       0          0          -     -
--------------------------------------------------------
TOTAL         0           0       0          0          -     -
```

**Blocker:** All channels awaiting CEO decision (Twitter Auth 70h+, HUNTER_API_KEY 82h+)

### Weekly Report Format (Week 1: Mar 27 - Apr 2)

**Target:** 5-10 signups, €0 revenue, CAC <€50

**Actual:** Will populate as distribution executes

**ROI Calculation:**
- Total spend: $0 (organic distribution)
- Revenue: €0 × average LTV (estimate €200/user/month × 12 months) = €0
- ROI: N/A (no revenue yet)

---

## Decisions Required

### Immediate (Before Distribution Launch)

1. **Twitter Authorization**
   - Owner: CEO (Eduard)
   - Impact: Blocks Twitter distribution channel
   - Revenue risk: Missing 20-40% of potential signups

2. **HUNTER_API_KEY**
   - Owner: CEO (Eduard)
   - Impact: Blocks integration with lead enrichment (Hunter.io)
   - Revenue risk: Lower email capture rate, lower conversion

### Ongoing (Week 1-4 Monitoring)

1. **Channel Investment Decision**
   - If HN converts at 4%+ → Double down on HN content calendar
   - If Twitter converts at 6%+ → Daily posting cadence (1-2 tweets/day)
   - If LinkedIn converts at 5%+ → Weekly article cadence (1 article/week)
   - If any channel <2% conversion → Deactivate, pivot resources

2. **Partnership Activation Trigger**
   - Week 2-3 criteria: 10+ signups + 60%+ activation rate
   - Partnerships amplify successful distribution, don't create traction

---

## Learning Loop

### Week 1 Hypotheses

**Hypothesis 1:** HN delivers highest-converting developer audience
**Success metric:** 40%+ of Week 1 signups come from HN referrer
**Learn by:** 2026-04-02 (Week 1 end)

**Hypothesis 2:** Twitter drives early engagement, LinkedIn drives consideration
**Success metric:** Twitter: 50%+ of Week 1 impressions, LinkedIn: 60%+ of Week 1 visits
**Learn by:** 2026-04-02

**Hypothesis 3:** Direct traffic validates product-market fit
**Success metric:** 30%+ of Week 1 signups from direct referrer
**Learn by:** 2026-04-02

### Optimization Actions

If **HN converts <4%:**
- Improve landing page copy (emphasize privacy, security, developer trust)
- Add technical architecture diagram to HN post (developers love visuals)
- Test alternative HN submission timing (different day/time)

If **Twitter converts <6%:**
- Shift tone from promotional to educational (build trust first, pitch second)
- Add technical GIFs showing product in action
- Engage in developer Twitter conversations (reply to related tweets)

If **LinkedIn converts <5%:**
- Target specific developer groups (not general audience)
- Focus on B2B SaaS value (save time, reduce context switching)
- Add customer testimonial section once first 5 signups achieved

---

## Appendix: Attribution Query Examples

### Real-time Signups by Channel
```sql
-- Today's signups by acquisition source
SELECT
  DATE(created_at) as date,
  CASE
    WHEN referrer LIKE '%news.ycombinator.com%' THEN 'HN'
    WHEN referrer LIKE '%twitter.com%' THEN 'Twitter'
    WHEN referrer LIKE '%linkedin.com%' THEN 'LinkedIn'
    WHEN referrer LIKE '%github.com%' THEN 'GitHub'
    WHEN referrer IS NULL OR referrer = '' THEN 'Direct'
    ELSE 'Other'
  END as channel,
  COUNT(*) as signups
FROM user_signups
WHERE DATE(created_at) = CURRENT_DATE
GROUP BY DATE(created_at), channel
ORDER BY date DESC, signups DESC;
```

### Funnel Conversion Rate
```sql
-- Conversion rate by channel (signup ÷ visit)
SELECT
  channel,
  SUM(signups) as total_signups,
  SUM(visits) as total_visits,
  ROUND(SUM(signups) * 100.0 / NULLIF(SUM(visits), 0), 2) as conversion_rate
FROM attribution_summary
WHERE date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY channel
HAVING total_visits > 0
ORDER BY conversion_rate DESC;
```

### Revenue Attribution
```sql
-- First payment by acquisition channel
SELECT
  channel,
  COUNT(DISTINCT CASE WHEN first_payment_at IS NOT NULL THEN user_id END) as paying_users,
  SUM(CASE WHEN first_payment_at IS NOT NULL THEN 1 ELSE 0 END) as first_month_revenue_eur,
  ROUND(AVG(DATEDIFF(first_payment_at, created_at)), 1) as avg_days_to_payment
FROM user_signups
WHERE first_payment_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY channel
ORDER BY paying_users DESC;
```

---

**Status:** Framework ready for implementation
**Next Step:** Configure PostHog goals and create attribution dashboard once distribution unblocks
**Owner:** analytics
