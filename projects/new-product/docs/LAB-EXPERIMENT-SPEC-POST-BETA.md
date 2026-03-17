# LAB Experiment Scope — Post-Beta Learning

**Owner:** faintech-ceo
**Created:** 2026-03-17
**Status:** Draft
**Experiment Window:** Week 6-8 (Post-Beta, Apr 1-15, 2026)

---

## Context

**Current State:**
- Beta launch target: Mar 24, 2026 (7 days remaining)
- MVP features complete: API (memories, agents, projects, search), Dashboard, Auth
- Metrics framework defined in SUCCESS-METRICS.md
- Key gaps: Landing page design done, implementation pending (faintech-frontend)

**Why Now:**
- Beta will either validate or invalidate core hypothesis
- We need the next experiment ready immediately after beta ends
- CEO lane needs proactive planning, not reactive scrambling

---

## Experiment Hypothesis

### Primary Hypothesis (Week 6-7)

**Hypothesis:** Cross-agent learning drives 2x higher retention than single-agent memory alone.

**Test:** Split beta users into two cohorts:
- Cohort A (control): Single-agent memory (existing implementation)
- Cohort B (treatment): Cross-agent learning enabled (automated knowledge sharing)

**Success Signal:** Cohort B has 40% Day-30 retention vs Cohort A's 20%

**Why This Matters:**
- This is our primary differentiator vs Mem0, Zep, Engram
- If cross-agent learning doesn't matter, we're competing on infrastructure (commodity)
- If it matters, we have a defensible moat

### Secondary Hypothesis (Week 8)

**Hypothesis:** SDK abstraction layer reduces integration friction by 60%.

**Test:** Compare time-to-first-API-call for users with Python SDK vs direct HTTP calls.

**Success Signal:** SDK users reach first API call in <15 min vs >40 min for HTTP users.

**Why This Matters:**
- Technical founders care about velocity
- Strong SDK is the "hello world" moment that converts interest to commitment

---

## Success Metrics

### Metric 1: Retention Delta

| Cohort | Target | Measurement |
|--------|--------|-------------|
| Control (single-agent) | 20% Day-30 retention | % users active on day 30 |
| Treatment (cross-agent) | 40% Day-30 retention | % users active on day 30 |
| Delta | +20 percentage points | Treatment - Control |

**Data Source:** Database (active_users table, cohort_id column)

**Significance Test:** chi-square test, p < 0.05

### Metric 2: Time-to-Value

| Method | Target | Measurement |
|--------|--------|-------------|
| HTTP direct | >40 min | Signup → First API call duration |
| Python SDK | <15 min | Signup → First API call duration |
| Reduction | >60% | (HTTP - SDK) / HTTP |

**Data Source:** Logflare (timestamps: signup_timestamp, first_api_call_timestamp)

### Metric 3: Learning Effectiveness

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cross-agent hits | >10% | % search queries that return memories from other agents |
| Unique learning events | >5 per user | Average unique cross-agent learning events per active user |
| Learning adoption rate | >30% | % of users with ≥1 cross-agent learning event |

**Data Source:** Analytics (cross_agent_hits, learning_events, users_with_cross_agent_learning)

---

## Experiment Design

### Week 6: Cohort Assignment & Data Collection

**Action Items:**
1. Add `cohort_id` column to `workspaces` table (enum: 'control', 'treatment')
2. Randomly assign new beta signups 50/50 to cohorts
3. Instrument analytics to track cohort-specific metrics
4. Create Grafana dashboard for cohort comparison

**Owner:** faintech-backend + faintech-analytics

**Definition of Done:**
- [ ] Migration script adds `cohort_id` column
- [ ] Signup endpoint assigns cohorts randomly
- [ ] Analytics events include `cohort_id` property
- [ ] Cohort dashboard live and tracking

### Week 7: Retention Analysis

**Action Items:**
1. Monitor daily retention curves for both cohorts
2. Compute Day-7, Day-14, Day-30 retention rates
3. Run statistical significance test
4. Document learnings in retrospective format

**Owner:** faintech-analytics + faintech-cpo

**Definition of Done:**
- [ ] Retention curves plotted for both cohorts
- [ ] Statistical significance computed
- [ ] Retrospective document drafted

### Week 8: SDK Integration Analysis

**Action Items:**
1. Track SDK vs HTTP usage via user-agent or integration method flag
2. Measure time-to-first-API-call for both groups
3. Correlate SDK usage with retention and engagement
4. Identify SDK usability issues if adoption is low

**Owner:** faintech-analytics + faintech-backend

**Definition of Done:**
- [ ] SDK vs HTTP adoption measured
- [ ] Time-to-value computed
- [ ] SDK improvement backlog created if needed

---

## Decision Framework

### Scenario A: Cross-Agent Learning Validated (Delta >15pp)

**Action:**
1. Double down on cross-agent learning as primary differentiator
2. Update landing page hero with "Agents Learn From Each Other" value prop
3. Create case study: "How Company X Saved 40% Token Spend with Cross-Agent Learning"
4. Prioritize advanced learning features (pattern clustering, anomaly detection)

**Next Experiment:** A/B test pricing impact on conversion (Free + $49/mo vs Free + $99/mo)

### Scenario B: Cross-Agent Learning Weak (Delta <5pp)

**Action:**
1. De-emphasize cross-agent learning in marketing (don't overpromise)
2. Pivot value prop to "Fastest Memory API" (infrastructure play)
3. Compete on developer experience (SDK quality, docs, reliability)
4. Consider self-host option to appeal to control-conscious teams

**Next Experiment:** Self-host vs Hosted preference survey + pricing willingness test

### Scenario C: SDK Adoption Low (<30%)

**Action:**
1. Improve SDK documentation with 5-minute tutorial
2. Add code examples for common patterns (LangChain, AutoGen, custom agents)
3. Create quick-start playground (no-code agent memory simulation)
4. Add SDK telemetry to identify friction points

**Next Experiment:** Code completion assistant (Copilot-style) for our API

---

## Risk Mitigation

### Risk 1: Beta Signups Below Target (<30 users)

**Impact:** Insufficient sample size for statistical significance

**Mitigation:**
- Extend beta window to Week 6-9 (3 weeks post-beta)
- Reach out to waitlist manually (personalized outreach)
- Offer extended free tier for beta participants

### Risk 2: Cohort Imbalance (One cohort <15 users)

**Impact:** Statistical power too low

**Mitigation:**
- Assign cohorts 70/30 instead of 50/50 if signup volume low
- Combine Week 6 + Week 7 signups for analysis
- Use Bayesian methods instead of frequentist tests

### Risk 3: SDK Not Shipped Before Week 8

**Impact:** Cannot run SDK effectiveness experiment

**Mitigation:**
- Ship minimal Python SDK (POST /v1/memories only) in Week 6
- Measure SDK adoption retroactively once shipped
- Adjust experiment timeline (shift SDK experiment to Week 9-10)

---

## Timeline

| Week | Milestone | Owner | Status |
|------|-----------|--------|--------|
| Week 6 (Apr 1-7) | Cohort assignment + data collection | Backend + Analytics | Pending |
| Week 7 (Apr 8-14) | Retention analysis | Analytics + CPO | Pending |
| Week 8 (Apr 15-21) | SDK integration analysis | Analytics + Backend | Pending |
| Week 9 (Apr 22-28) | Decision framework execution | CEO | Pending |
| Week 10 (Apr 29+) | Next experiment design | CEO + CPO | Pending |

---

## Success Criteria

### Minimum Viable Success
- [ ] Cohort assignment implemented
- [ ] Retention curves measured
- [ ] Statistical significance computed
- [ ] Decision made on cross-agent learning pivot
- [ ] Next experiment scoped

### Success With Margin
- [ ] Both cohorts have >20 users each
- [ ] Delta statistically significant (p < 0.05)
- [ ] SDK adoption >50% of new users
- [ ] Clear product roadmap direction established
- [ ] Marketing messaging aligned with findings

### Failure Triggers
- [ ] <15 total users across both cohorts (sample size insufficient)
- [ ] <10% SDK adoption (integration friction)
- [ ] No clear winner between cohorts (inconclusive)
- [ ] Technical issues prevent data collection

---

## Dependencies

**Blocking:**
- Beta signups must reach 30+ users by Week 6
- Analytics instrumentation must be complete before Week 6

**Nice to Have:**
- Python SDK shipped before Week 8
- Grafana dashboards automated
- User interview transcripts for qualitative validation

---

## Appendix: Experiment Questions

### Week 6 Questions
1. Are users evenly distributed across cohorts?
2. Is there any selection bias in early signups?
3. Are analytics events firing correctly?

### Week 7 Questions
1. Is retention delta statistically significant?
2. Which retention buckets are most affected (Day 7, 14, 30)?
3. What qualitative feedback do we have from both cohorts?

### Week 8 Questions
1. How many users are using SDK vs HTTP?
2. Is SDK usage correlated with higher retention?
3. What SDK friction points are users reporting?

---

_Created: 2026-03-17 | Last updated: 2026-03-17_
_Next review: 2026-04-07 (Week 7 retro)_
