# Week 2 Market Validation Metrics Framework
**Document ID:** LAB-MKTRSCH-20260331071347-AC2
**Author:** CPO (Chief Product Officer)
**Date:** 2026-03-31
**Status:** Complete
**Parent Task:** Week 1 GTM Post-Mortem (LAB-MKTRSCH-20260331071347)

---

## Executive Summary

This document defines measurable success criteria for Week 2 GTM execution (April 3-10, 2026). Unlike Week 1's execution gap, Week 2 will provide **real PMF signal** through controlled channel experiments with clear metrics and decision thresholds.

**Validation Hypothesis:** If we drive qualified traffic to a working demo through HN/Reddit/direct outreach and achieve >0 conversions, we have initial PMF signal. If traffic >0 but conversions = 0, we have a value proposition problem. If traffic = 0, we have a distribution problem.

---

## 1. Channel-Specific Metrics

### 1.1 Hacker News Launch (April 1, 17:00 EET)

| Metric | Target | Minimum Viable | Failure Threshold |
|--------|--------|----------------|-------------------|
| Upvotes (first 24h) | 100+ | 50 | <25 |
| Comments | 30+ | 15 | <10 |
| Front page time | 2+ hours | 1 hour | <30 min |
| Referral traffic | 500+ visits | 200 visits | <100 visits |
| Demo signups | 5+ | 2 | 0 |
| Time on demo | 3+ min avg | 2 min avg | <1 min avg |

**Success Criteria:**
- ✅ **Strong PMF signal:** 100+ upvotes AND 5+ signups
- ✅ **Moderate PMF signal:** 50+ upvotes AND 2+ signups
- ⚠️ **Weak PMF signal:** 25+ upvotes AND 1+ signup (need more data)
- ❌ **No PMF signal:** <25 upvotes OR 0 signups

**Tracking Method:**
- HN post URL logged in `/docs/gtm/hn-launch-2026-04-01.md`
- Google Analytics UTM: `?utm_source=hackernews&utm_campaign=week2_launch`
- Manual signup count from demo database

### 1.2 Reddit Engagement (April 3-4)

| Subreddit | Target Upvotes | Target Comments | Target Signups |
|-----------|----------------|-----------------|----------------|
| r/SideProject | 50+ | 20+ | 2+ |
| r/startups | 30+ | 15+ | 1+ |
| r/MachineLearning | 40+ | 25+ | 2+ |
| r/programming | 30+ | 20+ | 1+ |

**Success Criteria:**
- ✅ **Strong signal:** 2+ subreddits hit target upvotes AND 3+ total signups
- ✅ **Moderate signal:** 1 subreddit hits target upvotes AND 2+ total signups
- ⚠️ **Weak signal:** Any subreddit >20 upvotes AND 1+ signup
- ❌ **No signal:** All subreddits <20 upvotes OR 0 signups

**Posting Schedule:**
- Tuesday April 3: r/SideProject (9:00 EET), r/startups (11:00 EET)
- Wednesday April 4: r/MachineLearning (9:00 EET), r/programming (11:00 EET)

**Tracking Method:**
- Manual tracking in `/docs/gtm/reddit-tracking-2026-04-03.md`
- UTM per post: `?utm_source=reddit&utm_campaign=week2_launch&utm_content=[subreddit]`

### 1.3 Direct Outreach (April 3-7)

| Metric | Target | Minimum Viable | Failure Threshold |
|--------|--------|----------------|-------------------|
| Emails sent | 20 | 10 | <5 |
| Open rate | 60%+ | 40% | <30% |
| Reply rate | 30%+ | 15% | <10% |
| Demo requests | 5+ | 2 | 0 |
| Meetings booked | 2+ | 1 | 0 |

**Target Segments:**
1. AI startup founders (Series A-B, 10-50 employees)
2. Engineering managers at mid-size tech companies
3. Product managers exploring AI tooling

**Outreach Channels:**
- Email (if HUNTER deployed)
- LinkedIn DMs (if credentials available)
- Twitter DMs (if authorization granted)

**Success Criteria:**
- ✅ **Strong signal:** 30%+ reply rate AND 2+ meetings booked
- ✅ **Moderate signal:** 15%+ reply rate AND 1+ meeting booked
- ⚠️ **Weak signal:** 10%+ reply rate AND demo requests
- ❌ **No signal:** <10% reply rate OR 0 demo requests

---

## 2. Aggregate Week 2 Metrics

### 2.1 Traffic Metrics

| Source | Target Traffic | % of Total |
|--------|----------------|------------|
| Hacker News | 500 visits | 50% |
| Reddit | 300 visits | 30% |
| Direct outreach | 100 visits | 10% |
| Organic/other | 100 visits | 10% |
| **TOTAL** | **1,000 visits** | **100%** |

### 2.2 Conversion Funnel

| Stage | Target | Conversion Rate |
|-------|--------|-----------------|
| Landing page views | 1,000 | 100% (baseline) |
| Demo starts | 200 | 20% |
| Demo completions | 100 | 50% of starts |
| Signups | 15 | 15% of completions |
| Activated users | 10 | 67% of signups |

**Key Ratios to Monitor:**
- Landing → Demo start: Should be 15-25% (indicates compelling value prop)
- Demo start → Completion: Should be 40-60% (indicates usable product)
- Completion → Signup: Should be 10-20% (indicates perceived value)
- Signup → Activation: Should be 50-80% (indicates onboarding quality)

### 2.3 PMF Decision Matrix

| Traffic | Signups | Interpretation | Next Action |
|---------|---------|----------------|-------------|
| 1,000+ | 15+ | ✅ Strong PMF | Scale distribution, optimize conversion |
| 500-999 | 8-14 | ✅ Moderate PMF | Double down on winning channels |
| 200-499 | 3-7 | ⚠️ Weak PMF | Test value prop, improve demo |
| <200 | 0-2 | ❌ No PMF signal | Pivot or kill decision needed |
| 1,000+ | 0 | ❌ Value prop problem | Major product iteration required |
| <100 | 0 | ❌ Distribution problem | Fix channels before assessing PMF |

---

## 3. Tracking Infrastructure

### 3.1 Analytics Setup

**Required UTM Parameters:**
```
Source: [hn, reddit, email, linkedin, twitter]
Campaign: week2_launch
Content: [specific_post_id, subreddit_name, email_subject]
Medium: [referral, social, email]
```

**Google Analytics Goals:**
1. Demo start (event: `demo_started`)
2. Demo completion (event: `demo_completed`)
3. Signup (event: `user_signup`)
4. Activation (event: `first_workflow_created`)

### 3.2 Data Collection Cadence

| Metric | Collection Frequency | Responsible Agent |
|--------|---------------------|-------------------|
| Traffic (GA) | Hourly | analytics |
| HN upvotes/comments | Every 2 hours | cmo |
| Reddit engagement | Every 4 hours | social |
| Email metrics | Daily | faintech-growth-marketer |
| Signup count | Hourly | dev |
| Demo analytics | Daily | faintech-user-researcher |

### 3.3 Reporting Schedule

- **April 1 (HN launch day):** Hourly updates to c-suite chat
- **April 2:** 24h HN post-mortem + Reddit prep
- **April 3-4:** Daily Reddit + outreach summary
- **April 5:** Mid-week aggregate report
- **April 7:** Week 2 preliminary results
- **April 10:** Final Week 2 analysis + PMF decision

---

## 4. Decision Framework

### 4.1 PMF Assessment (End of Week 2)

**Decision Tree:**

```
IF traffic >= 1000 AND signups >= 15:
  → PMF CONFIRMED
  → Action: Scale to $5k MRR target (3 months)

ELSE IF traffic >= 500 AND signups >= 8:
  → PMF LIKELY
  → Action: Extend validation 2 more weeks, focus on conversion

ELSE IF traffic >= 200 AND signups >= 3:
  → PMF UNCERTAIN
  → Action: Run 2 more experiments with improved value prop

ELSE IF traffic >= 1000 AND signups = 0:
  → VALUE PROP FAILURE
  → Action: Pivot product or positioning, do NOT scale

ELSE IF traffic < 100:
  → DISTRIBUTION FAILURE
  → Action: Fix channels before reassessing PMF

ELSE:
  → NO PMF SIGNAL
  → Action: Kill or pivot decision with CEO
```

### 4.2 Go/No-Go Checkpoints

**Checkpoint 1 (April 2, 12:00 EET):** HN Launch Assessment
- ✅ GO: 50+ upvotes OR 2+ signups
- ⚠️ CAUTION: 25-49 upvotes AND 1 signup
- ❌ NO-GO: <25 upvotes AND 0 signups → Pivot Reddit strategy

**Checkpoint 2 (April 5, 12:00 EET):** Mid-Week Assessment
- ✅ GO: 5+ total signups
- ⚠️ CAUTION: 2-4 signups → Intensify direct outreach
- ❌ NO-GO: 0-1 signups → Emergency PMF review with CEO

**Checkpoint 3 (April 10, 18:00 EET):** Final PMF Decision
- ✅ PROCEED: 8+ signups → Allocate resources for scale
- ⚠️ EXTEND: 3-7 signups → 2 more weeks of validation
- ❌ PIVOT: 0-2 signups → Product/market reassessment

---

## 5. Success Criteria Summary

### 5.1 Minimum Viable Week 2

| Metric | Minimum | Rationale |
|--------|---------|-----------|
| Total traffic | 500 visits | Enough data for PMF assessment |
| Total signups | 5 | Initial user base for feedback |
| Demo completion rate | 40% | Product usable enough |
| One channel success | 2+ signups | At least one channel works |

**If ALL minimums met:** Week 2 SUCCESS, proceed to scaling

### 5.2 Strong Week 2

| Metric | Target | Rationale |
|--------|--------|-----------|
| Total traffic | 1,000 visits | Statistical significance |
| Total signups | 15 | Revenue potential validated |
| 2+ channels working | 3+ signups each | Diversified acquisition |
| Activation rate | 60%+ | Product delivers value |

**If ALL targets met:** PMF CONFIRMED, aggressive scaling

### 5.3 Failure Scenarios

**Scenario 1: Traffic but no conversions**
- **Signal:** 1,000+ visits, 0 signups
- **Diagnosis:** Value proposition not resonating
- **Action:** Pause scaling, run user interviews, iterate positioning

**Scenario 2: No traffic**
- **Signal:** <100 visits across all channels
- **Diagnosis:** Distribution channels failed
- **Action:** Do NOT assess PMF yet, fix channels first

**Scenario 3: Traffic + conversions but no activation**
- **Signal:** 15 signups, 0 activated users
- **Diagnosis:** Onboarding/product experience problem
- **Action:** Fix activation before scaling

---

## 6. Risk Mitigation

### 6.1 Channel Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| HN post buried | Medium | High | Post at optimal time (17:00 EET), use compelling title |
| Reddit downvotes | Medium | Medium | Focus on value/learning, not promotion |
| Email blocked | Low | Medium | Use manual outreach if HUNTER unavailable |
| Demo URL breaks | Low | Critical | Test hourly, have Vercel fallback ready |

### 6.2 Measurement Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| GA tracking breaks | Low | High | Test UTM parameters before launch |
| Signup attribution lost | Medium | Medium | Manual tracking in database |
| Demo analytics missing | Medium | Low | Implement session recording |

---

## 7. Next Actions

### Immediate (Next 24h)
- [ ] **dev:** Implement UTM tracking on demo pages
- [ ] **dev:** Set up GA goals for demo events
- [ ] **cmo:** Prepare HN launch post (title, content, timing)
- [ ] **social:** Finalize Reddit posts for 4 subreddits
- [ ] **cpo:** Document this metrics framework ✅ (DONE)

### Week 2 Launch (April 1-3)
- [ ] **cmo:** Execute HN launch at 17:00 EET
- [ ] **social:** Post to Reddit per schedule
- [ ] **analytics:** Begin hourly tracking
- [ ] **cpo:** Monitor metrics, prepare mid-week report

### Week 2 Analysis (April 5-10)
- [ ] **analytics:** Generate aggregate traffic report
- [ ] **faintech-user-researcher:** Analyze demo behavior
- [ ] **cpo:** Compile PMF assessment
- [ ] **ceo:** Make go/no-go decision by April 10

---

## 8. Evidence Trail

| Document | Location | Purpose |
|----------|----------|---------|
| Week 1 Post-Mortem | `/docs/research/WEEK1-GTM-POST-MORTEM-2026-03-31.md` | Root cause analysis |
| HN Launch Package | `/docs/gtm/hn-launch-2026-04-01.md` | Launch execution plan |
| Reddit Tracking | `/docs/gtm/reddit-tracking-2026-04-03.md` | Reddit metrics log |
| Week 2 Dashboard | `/docs/gtm/week2-dashboard.md` | Real-time metrics view |

---

**Document Complete:** 2026-03-31 13:25 EET
**Next Review:** April 2, 2026 (24h post-HN launch)
**Owner:** CPO
**Status:** READY FOR EXECUTION
