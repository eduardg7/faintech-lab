# Distribution Campaign KPI Tracking Template

**Project:** Faintech Lab - AMC MVP Launch
**Status:** Ready for execution upon CEO approval
**Created:** 2026-03-27

---

## Core Metrics Definition

### Acquisition Metrics
| Metric | Definition | Target | How to Measure |
|---------|-------------|--------|----------------|
| **Signups** | New user accounts created | 10 (Week 1) | Database count, signup events |
| **Activation Rate** | Signups that create first memory | 80% | User activity logs |
| **Cost Per Signup** | Distribution spend / signups | <$20 | Time tracking on content creation |
| **Conversion Rate** | Visitors → Signups | 3-5% | Analytics (Google Analytics/Vercel) |

### Engagement Metrics
| Metric | Definition | Target | How to Measure |
|---------|-------------|--------|----------------|
| **HN Upvotes** | Total upvotes on launch post | 50+ | HN post page |
| **HN Comments** | Substantive comment count | 20+ | HN thread |
| **Twitter Impressions** | Total thread views | 5,000+ | Twitter Analytics |
| **Twitter Engagement Rate** | (Likes + RTs + Replies) / Impressions | 5%+ | Twitter Analytics |
| **LinkedIn Views** | Article read count | 1,000+ | LinkedIn Analytics |
| **LinkedIn Comments** | Substantive comment count | 15+ | LinkedIn post stats |

### Retention Metrics
| Metric | Definition | Target | How to Measure |
|---------|-------------|--------|----------------|
| **Day 1 Retention** | Signups returning within 24h | 60% | User activity logs |
| **Day 3 Retention** | Signups returning within 72h | 40% | User activity logs |
| **Day 7 Retention** | Signups returning within 7 days | 30% | User activity logs |
| **Feature Usage Depth** | Average features used per user | 3+ | Feature usage analytics |

### Revenue Metrics
| Metric | Definition | Target | How to Measure |
|---------|-------------|--------|----------------|
| **Paying Customers** | Users with active subscription | 5 (Week 1) | Stripe dashboard |
| **MRR (Monthly Recurring Revenue)** | Sum of active subscriptions | $500+ (Week 1) | Stripe dashboard |
| **Conversion to Paid** | Free → Paid conversion rate | 20% | Stripe + user database |

---

## Measurement Approach

### Data Sources
1. **User Database** - Signups, activation, retention
2. **Analytics** - Referral traffic, conversion rates
3. **Platform Analytics** - HN, Twitter, LinkedIn native metrics
4. **Stripe Dashboard** - Revenue, paying customers
5. **Feature Usage Logs** - Retention, feature adoption

### Tracking Frequency
- **Hourly (first 24h):** HN upvotes, Twitter impressions, signups
- **Daily (Day 2-7):** All metrics consolidated
- **Weekly (Day 7):** Full analysis, strategy decision

### Data Collection Tools
- **Manual:** HN upvotes/comments (browser check), Twitter engagement (Twitter Analytics)
- **Automated:** Signups (database), Revenue (Stripe), Referral traffic (Vercel Analytics)
- **Semi-automated:** Retention, feature usage (write queries for dashboard)

---

## Daily Tracking Sheet (Template)

### Day 1 Launch
```
Time | Channel | Metric | Value | Notes
------|----------|--------|-------|
09:00 | HN | Upvotes: ___ Comments: ___ | Title variant: ___
09:00 | Twitter | Impressions: ___ Engagement: ___% | Thread variant: ___
14:00 | LinkedIn | Views: ___ Comments: ___ | Article variant: ___
18:00 | Signups | Total: ___ From HN: ___ From Twitter: ___ From LinkedIn: ___ | Conversion rate: ___%
```

### Day 2-7
```
Date | Signups | HN Upvotes | Twitter Impressions | LinkedIn Views | Retention | Notes
------|---------|-------------|-------------------|---------------|-----------|-------
      |           |             |                   |               |           |
      |           |             |                   |               |           |
```

---

## Week 1 Analysis Framework

### Daily Reporting Template
```markdown
## Day [X] Distribution Report

### Signups
- Total: [count]
- By channel: HN [count], Twitter [count], LinkedIn [count]
- Conversion rate: [%]

### Engagement
- HN: [upvotes] upvotes, [count] comments
- Twitter: [impressions] impressions, [rate]% engagement
- LinkedIn: [views] views, [count] comments

### Retention
- Day 1: [%] returning users
- Day 3: [%] returning users

### Revenue
- Paying customers: [count]
- MRR: $[amount]

### Key Learnings
1. [Best performing message variant]
2. [Most engaged platform]
3. [User feedback theme]
4. [Blocker or issue]

### Next Actions
1. [Specific action based on learnings]
2. [Messaging iteration or continuation]
3. [Escalation if needed]
```

---

## Escalation Triggers & Decision Points

### Trigger 1: Zero Signups by Day 3
**Condition:** 0 signups across all channels at T+72h
**Action:** Escalate to CEO immediately
**Decision Required:** Pivot messaging strategy or actual PMF issue

### Trigger 2: Low Engagement by Day 5
**Condition:** <10 HN upvotes, <2% Twitter engagement, <500 LinkedIn views
**Action:** Iterate messaging, test new variants
**Decision Required:** Continue distribution or pause for strategy review

### Trigger 3: Week 1 Target Miss (<5 signups)
**Condition:** <5 signups by Day 7
**Action:** Strategy review with CEO
**Decision Required:**
- If 2-4 signups: Double down on content, partnerships deferred
- If 0-1 signups: Distribution failure investigation, PMF hypothesis revalidation

### Trigger 4: Partnership Activation
**Condition:** 2-3 signups with positive engagement
**Action:** Activate partnership outreach (per partnership playbook)
**Decision Required:** Which partners to prioritize

---

## Benchmark Comparison

### Week 1 Targets vs Industry Standards
| Metric | Faintech Target | Industry Average | Status |
|---------|------------------|-------------------|--------|
| HN Upvotes | 50+ | 20-30 (successful HN post) | ___ |
| Twitter Engagement Rate | 5%+ | 1-3% | ___ |
| LinkedIn Views | 1,000+ | 500-800 (technical post) | ___ |
| Signups | 10 | 5-20 (B2B SaaS beta) | ___ |
| Day 1 Retention | 60% | 40-50% | ___ |

---

## Success Signals vs PMF Signals

### Positive Distribution Signals (Execution Working)
- HN upvotes >30
- Twitter engagement rate >3%
- LinkedIn comments with technical questions
- Signups from multiple channels (not just one)
- Returning users (retention >50% Day 1)

### PMF Signals (Product-Market Fit)
- Users creating 3+ memories per session
- Feature requests specific to workflow problems
- Repeat usage within 48h
- "I've been looking for this" comments
- Willingness to pay (conversion to paid)

### Warning Signals (Pivot Needed)
- All engagement is generic ("cool tech", no use case)
- Signups but 0 activation (users signing up but not using)
- Negative feedback on core value proposition
- Competitor comparisons where "X does this better"

---

## Analytics Setup Checklist

### Before Launch
- [ ] Google Analytics installed on signup page
- [ ] Referral tracking configured (UTM parameters)
- [ ] Stripe dashboard accessible
- [ ] Feature usage analytics query ready
- [ ] Daily tracking sheet template created
- [ ] Escalation triggers documented in SESSION-STATE

### During Distribution
- [ ] Hourly signups logged (first 24h)
- [ ] Platform metrics checked (HN upvotes, Twitter analytics, LinkedIn views)
- [ ] Engagement quality tracked (substantive comments count)
- [ ] Retention measured (Day 1, Day 3, Day 7)
- [ ] Revenue dashboard monitored (paying customers)

### After Launch (Weekly)
- [ ] Weekly analysis report written
- [ ] Benchmarks compared (Faintech vs industry)
- [ ] Decision made on partnerships activation
- [ ] Learnings documented in shared-learnings.md
- [ ] Strategy decision escalated to CEO if needed

---

*Last updated: 2026-03-27*
