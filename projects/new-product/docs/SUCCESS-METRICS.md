# Success Metrics — Agent Memory Cloud Beta

**Owner:** faintech-pm
**Created:** 2026-03-11
**Review Cadence:** Weekly (every Monday)

---

## North Star Metric

**Beta-to-Paid Conversion Rate**

**Definition:** % of beta users who convert to paid subscription within 30 days of beta end

**Target:** 30% (3 of 10 beta users)

**Why this metric:** It's the ultimate signal of product-market fit. If beta users won't pay, we haven't solved their problem.

---

## Primary Metrics (Week 1-4)

### Acquisition
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| Beta signups | 50 | Unique emails in beta waitlist | Daily |
| API keys created | 30 | Active API keys in dashboard | Daily |
| First API call | 20 users | Users who make ≥1 API call | Daily |
| SDK downloads | 100 | PyPI + npm downloads | Daily |

### Activation
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| Write first memory | 15 users | Users who call POST /v1/memories | Daily |
| Search memories | 10 users | Users who call POST /v1/search | Daily |
| Multi-agent usage | 5 users | Users with ≥2 agent_ids | Daily |
| Cross-agent learning | 3 users | Users querying across agents | Daily |

### Retention
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| Day 7 retention | 40% | Users active on day 7 | Weekly |
| Day 14 retention | 30% | Users active on day 14 | Weekly |
| Day 30 retention | 20% | Users active on day 30 | Monthly |
| Weekly API calls | 1,000 | Total API calls per week | Weekly |

### Engagement
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| Avg memories per user | 50 | Total memories / active users | Weekly |
| Avg searches per user | 20 | Total searches / active users | Weekly |
| Avg API calls per day | 10 | Daily API calls / active users | Daily |
| P99 response time | <200ms | API latency (99th percentile) | Daily |

### Revenue (Early Signals)
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| Payment method added | 10 users | Users with payment on file | Weekly |
| Upgrade intent | 5 users | Users who click "upgrade" | Weekly |
| Wilingness to pay | $500 MRR | Projected from beta users | Monthly |

---

## Secondary Metrics

### Product Usage Patterns
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| Memories per agent | 10 avg | Avg memories per agent_id | Weekly |
| Agents per user | 3 avg | Avg agent_ids per user | Weekly |
| Projects per user | 1.5 avg | Avg project_ids per user | Weekly |
| Search relevance | 80% positive | User feedback on search results | Weekly |

### Technical Health
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| API uptime | 99.9% | Uptime over 30 days | Daily |
| Error rate | <0.1% | 5xx responses / total requests | Daily |
| P95 response time | <100ms | API latency (95th percentile) | Daily |
| Database query time | <50ms | Avg query execution time | Daily |

### Support Quality
| Metric | Target | Measurement | Frequency |
|--------|--------|-------------|-----------|
| First response time | <4 hours | Time to first human response | Daily |
| Resolution time | <24 hours | Time to close support ticket | Daily |
| CSAT score | 4.5/5 | User satisfaction rating | Weekly |
| Support tickets | <20/week | Total tickets opened | Weekly |

---

## Qualitative Metrics

### User Feedback Themes
Track and categorize feedback weekly:

**Positive Signals:**
- "This is exactly what I needed"
- "Saved me weeks of building"
- "Cross-agent learning is a game-changer"
- "API is simple to use"
- "Finally, agent memory that works"

**Negative Signals:**
- "Missing feature X"
- "Documentation is unclear"
- "Performance is slow"
- "Pricing is too high"
- "Integration was harder than expected"

### User Interview Questions
Conduct 10 user interviews in first 4 weeks:

1. **What problem were you trying to solve?**
2. **How were you handling agent memory before?**
3. **What's working well?**
4. **What's missing or frustrating?**
5. **Would you pay $99/month for this? Why/why not?**
6. **What would make this a no-brainer purchase?**
7. **Who else should we talk to?**

---

## Success Criteria (4-Week Beta)

### Must Have (P0)
- [ ] **30 beta signups** (of 50 target)
- [ ] **10 active users** (made API call in last 7 days)
- [ ] **5 power users** (using cross-agent learning)
- [ ] **3 paying customers** (converted from beta)
- [ ] **99% uptime** (no SEV-1 incidents)

### Should Have (P1)
- [ ] **50 beta signups** (full target)
- [ ] **20 active users**
- [ ] **10 user interviews completed**
- [ ] **<4 hour first response time** for support
- [ ] **80% positive search feedback**

### Nice to Have (P2)
- [ ] **100 beta signups** (2x target)
- [ ] **5 paid upgrades before beta ends**
- [ ] **Feature request backlog** prioritized
- [ ] **Case study drafted** from power user
- [ ] **HN front page** (top 5 for >1 hour)

---

## Failure Criteria (Pivot Signals)

If we see these signals, we need to reassess:

- **<10 beta signups in first week** → Marketing/positioning problem
- **0 active users after 2 weeks** → Product doesn't solve real problem
- **0 payment methods added after 3 weeks** → Value proposition unclear
- **>50% churn in first week** → Onboarding/activation broken
- **<10% search relevance** → Core feature doesn't work

---

## Tracking Dashboard

**Metrics to display in Grafana:**

1. **Funnel:** Signups → API keys → First call → Active user → Payment added
2. **Cohort retention:** Day 1, 7, 14, 30 retention by cohort
3. **API health:** Requests, errors, latency (P50, P95, P99)
4. **Business:** MRR, signups, churn, conversion rate
5. **Support:** Tickets, response time, CSAT

---

## Reporting Cadence

| Report | Audience | Frequency | Owner |
|--------|----------|-----------|-------|
| Daily standup metrics | Team | Daily | PM |
| Weekly metrics review | CEO + C-suite | Weekly | PM |
| Beta user interviews | CPO | Bi-weekly | PM |
| Technical health | CTO | Daily | DevOps |
| Financial update | CFO | Monthly | PM |

---

## Data Sources

| Metric | Source | API/Tool |
|--------|--------|----------|
| Beta signups | Database | PostgreSQL |
| API calls | Logs | Logflare |
| SDK downloads | PyPI/npm | APIs |
| Revenue | Stripe | Dashboard |
| Uptime | Status page | UptimeRobot |
| Support tickets | Email/GitHub | Manual |
| User feedback | Interviews | Notion |

---

## Next Actions

- [ ] Set up Grafana dashboard with all metrics
- [ ] Create automated daily metrics email to team
- [ ] Schedule weekly metrics review with CEO
- [ ] Set up alerts for failure criteria triggers
- [ ] Create user interview scheduling template

---

_Created: 2026-03-11 | Last updated: 2026-03-11_
_Next review: 2026-03-18_
