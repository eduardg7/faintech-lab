# Product Metrics Framework — Agent Memory Cloud

Owner: faintech-cpo | Created: 2026-03-10 | Status: Draft

---

## Purpose

Define measurable metrics for Agent Memory Cloud product success. Framework covers:
- Leading indicators (predictive)
- Lagging indicators (outcome-based)
- Health metrics (quality/reliability)
- Business metrics (revenue/growth)

---

## North Star Metric

**Weekly Active Agents (WAA)**

**Definition:** Number of unique agents writing to memory at least once per week.

**Why this metric:**
- Direct measure of product usage
- Correlates with customer value (more active agents = more value extracted)
- Leading indicator for retention and expansion
- Simple to understand and communicate

**Target:**
- Month 1: 20 WAA
- Month 3: 100 WAA
- Month 6: 500 WAA

---

## Acquisition Metrics

### Traffic & Awareness

| Metric | Definition | Target (Month 1) |
|--------|-----------|------------------|
| Website visitors | Unique visitors to landing page | 1,000 |
| GitHub stars (SDK) | Stars on open-source SDK repo | 200 |
| Twitter mentions | Mentions of product/brand | 50 |
| HN upvotes | Upvotes on launch post | 100+ (front page) |

### Signups & Activation

| Metric | Definition | Target (Month 1) |
|--------|-----------|------------------|
| Signups | New workspace registrations | 100 |
| Activated accounts | ≥1 agent writing memory | 40 (40% activation) |
| Time to first memory | Minutes from signup to first write | <10 min |
| SDK installs | `pip install` or `npm install` | 500 |

**Activation Funnel:**
```
Signup → Install SDK → First write → 10 writes → Activated
  100%      80%          60%          50%         40%
```

---

## Engagement Metrics

### Usage Intensity

| Metric | Definition | Target (Month 1) |
|--------|-----------|------------------|
| Memories per agent/week | Average writes per active agent | 50 |
| Search queries/week | Number of memory searches | 200 |
| Cross-agent learning events | Agent B reads Agent A's memory | 100 |
| Compression ratio | % reduction from raw memories | 40% |

### Retention

| Metric | Definition | Target |
|--------|-----------|--------|
| Week 1 retention | % return after first week | 70% |
| Week 4 retention | % active after month 1 | 50% |
| DAU/WAA ratio | Daily active / weekly active | 0.3 |

### Quality Signals

| Metric | Definition | Target |
|--------|-----------|-------------------|
| Memory write success rate | % writes that succeed | 99.9% |
| Search relevance score | % searches with clicks | 60% |
| Learning application rate | % memories used in decisions | 30% |

---

## Business Metrics

### Revenue

| Metric | Definition | Target (Month 1) |
|--------|-----------|------------------|
| MRR | Monthly recurring revenue | $500 |
| ARPU | Average revenue per user | $50 |
| Paying customers | Customers on paid plan | 5 |
| Free → Paid conversion | % free users upgrading | 5% |

### Customer Acquisition

| Metric | Definition | Target |
|--------|-----------|--------|
| CAC | Customer acquisition cost | <$100 |
| LTV | Lifetime value | >$600 |
| LTV:CAC ratio | Value to cost ratio | >6:1 |

### Expansion

| Metric | Definition | Target |
|--------|-----------|--------|
| NRR | Net revenue retention | >120% |
| Upgrade rate | % customers upgrading plans | 10%/month |
| Workspace expansion | Agents added per workspace | +2/month |

---

## Health Metrics (Quality & Reliability)

### Performance

| Metric | Definition | Target |
|--------|-----------|--------|
| Write latency (p99) | 99th percentile write time | <100ms |
| Search latency (p99) | 99th percentile search time | <150ms |
| Uptime | Service availability | 99.9% |
| Error rate | % requests returning 5xx | <0.1% |

### Security & Trust

| Metric | Definition | Target |
|--------|-----------|--------|
| Security incidents | Breaches or vulnerabilities | 0 |
| Data loss events | Memories lost due to bugs | 0 |
| Auth failures | % failed authentications | <0.01% |

### Support

| Metric | Definition | Target |
|--------|-----------|--------|
| Support tickets/week | Customer support requests | <20 |
| Response time (avg) | Time to first response | <4 hours |
| Resolution time | Time to close ticket | <24 hours |
| CSAT | Customer satisfaction score | >4.5/5 |

---

## Product-Market Fit Metrics

### PMF Score (Superhuman Method)

**Question:** "How would you feel if you could no longer use Agent Memory Cloud?"
- [ ] Very disappointed ← Target: 40%+
- [ ] Somewhat disappointed
- [ ] Not disappointed

**Target:** 40%+ "very disappointed" = strong PMF signal

### Willingness to Pay

**Question:** "What would you expect to pay for this?"
- Track distribution of price expectations
- Compare to actual pricing
- Adjust pricing if mismatch >20%

### Word of Mouth

| Metric | Definition | Target |
|--------|-----------|--------|
| NPS | Net promoter score | >50 |
| Referral rate | % users who invite others | 20% |
| Viral coefficient | New users per existing user | >1.0 |

---

## Metric Review Cadence

### Daily Review (Health Metrics)
- Uptime, error rate, latency
- Support tickets
- Security alerts

### Weekly Review (Engagement & Growth)
- WAA (North Star)
- Activation rate
- Retention cohorts
- Signups & conversions

### Monthly Review (Business & PMF)
- MRR, ARPU, paying customers
- CAC, LTV, LTV:CAC
- PMF score (survey)
- NPS score
- Competitive landscape changes

---

## Metric Thresholds & Alerts

### 🔴 Critical (Immediate Action)
- Uptime <99%
- Error rate >1%
- Security incident
- WAA decline >20% week-over-week

### 🟡 Warning (Investigate)
- Activation rate <30%
- Week 1 retention <50%
- Write latency >150ms
- PMF score <30%

### 🟢 Healthy (Maintain)
- WAA growing >10%/week
- MRR growing >20%/month
- NPS >50
- Zero critical incidents

---

## Implementation Plan

### Week 1: Instrumentation
- [ ] Add analytics to API (writes, searches, errors)
- [ ] Set up dashboard (Grafana/Datadog)
- [ ] Create automated reports (daily/weekly/monthly)

### Week 2: Baselines
- [ ] Establish baseline metrics from beta users
- [ ] Set initial targets based on baselines
- [ ] Document metric definitions in code comments

### Week 3+: Iteration
- [ ] Weekly metric review in team standup
- [ ] Monthly metric report to CEO
- [ ] Quarterly metric framework review

---

## Open Questions

1. **Attribution:** How do we attribute signups to specific channels?
2. **Cohorts:** How do we define user cohorts (signup date, first write, first 10 writes)?
3. **Learning rate:** How do we measure "learning" vs just "storing memories"?
4. **Competitive benchmarking:** What are Mem0/LangChain's WAA numbers?

---

**Status:** Draft — Ready for review after PROD-001 approval
**Next Update:** After MVP launch with real data
