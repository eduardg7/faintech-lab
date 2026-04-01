# Analytics Recovery Checklist for Post-Deployment Verification

**Date:** 2026-04-01
**Agent:** analytics
**Purpose:** Rapid analytics infrastructure verification after backend deployment recovery

---

## Context

**Current Blocker:**
- Backend API: DOWN (404) - DevOps unresponsive 9h 46m+
- All analytics collection: BLOCKED
- Week 2 GTM (starts April 3): HIGH RISK

**Recovery Goal:**
- Verify analytics infrastructure is operational within 1 hour of backend deployment
- Enable Week 2 GTM channel attribution tracking
- Validate data quality before GTM execution

---

## Recovery Time Objectives

Based on disaster recovery best practices (AWS, Azure, Oracle):

| Objective | Target | Rationale |
|-----------|--------|-----------|
| **RTO** (Recovery Time Objective) | 1 hour | Analytics should be operational immediately after backend deploys |
| **RPO** (Recovery Point Objective) | 0 minutes | No data loss - PostHog real-time + database queries |
| **Verification Time** | 30 minutes | Confirm all 5 critical events are ingesting correctly |

---

## Critical Events (Track Immediately)

Based on Countly event tracking best practices:

### Tier 1: Business Critical (Immediate)

| Event | Description | Validation |
|-------|-------------|------------|
| `user_signup` | User completes registration | Check PostHog signup funnel |
| `user_verified` | Email verification completed | Check activation rate >40% |
| `first_memory_created` | User creates first memory | Check time-to-value <5 min |
| `payment_completed` | Payment processed | Check revenue tracking |
| `utm_attribution` | Channel source captured | Check UTM parameters present |

### Tier 2: Operational (Within 24h)

| Event | Description | Priority |
|-------|-------------|----------|
| `page_view` | Landing page visits | Week 2 channel attribution |
| `button_click` | CTA engagement | Conversion optimization |
| `feature_used` | Specific feature adoption | Product usage insights |
| `error_occurred` | Frontend errors | Technical health |
| `api_failure` | Backend API errors | Operational monitoring |

---

## Verification Checklist (T+0h post-deployment)

### Step 1: Verify Backend Deployment (5 min)
```bash
curl https://amc-frontend-weld.vercel.app/api/health
# Expected: HTTP 200 + {"status": "healthy"}
```

### Step 2: Verify Database Schema (5 min)
```sql
-- Check UTM columns exist
DESCRIBE users;
-- Expected: utm_source, utm_medium, utm_campaign, utm_content, utm_term, utm_referrer
```

### Step 3: Verify PostHog Configuration (10 min)
- [ ] PostHog API key configured
- [ ] Test event: `posthog.capture('test_event', {test: true})`
- [ ] Verify event appears in PostHog dashboard within 30s

### Step 4: Verify UTM Capture (10 min)
- [ ] Signup with test UTM: `?utm_source=hn&utm_medium=launch&utm_campaign=week2`
- [ ] Check database: User record contains all 6 UTM columns
- [ ] Check PostHog: Signup event contains UTM properties

### Step 5: Verify Critical Events (10 min)
- [ ] Complete signup flow
- [ ] Verify email verification
- [ ] Create first memory
- [ ] Check PostHog: All 5 Tier 1 events present

### Step 6: Data Quality Check (10 min)
- [ ] Verify no duplicate events
- [ ] Verify event timestamps are accurate
- [ ] Verify user properties are correctly populated
- [ ] Verify UTM attribution links signup to channel

---

## Success Criteria

Recovery is **COMPLETE** when:
- ✅ Backend returns HTTP 200
- ✅ Database has 6 UTM columns
- ✅ PostHog receives events within 30s
- ✅ All 5 Tier 1 events are tracked
- ✅ UTM parameters persist from landing to signup
- ✅ No data quality issues (duplicates, missing fields)

---

## Escalation Criteria

If verification fails after 1 hour:

| Failure | Escalate To | Action |
|---------|--------------|--------|
| Backend still 404 | DevOps/CEO | Emergency deployment required |
| Missing UTM columns | faintech-backend | Migration not applied |
| PostHog not ingesting | DevOps | Credentials missing |
| Events missing/incorrect | analytics | Configuration issue |
| Data quality issues | qa | Integration bug |

---

## Next Actions (Post-Recovery)

### Immediate (T+24h)
- Begin daily data collection routine (09:00 and 17:00 EET)
- Monitor Week 2 GTM channel attribution
- Track signups vs target (10-15 by April 10)

### Short-term (Week 2 GTM: April 3-10)
- Daily signup funnel analysis
- Channel ROI tracking (HN, Reddit, LinkedIn, Twitter, direct)
- Activation rate monitoring (>70% target)
- Retention signals (day-1/7/30)

### Medium-term (Post-Week 2)
- Analyze channel effectiveness
- Optimize acquisition strategy
- Implement Phase 2 backend migration (user-level attribution)
- Refine analytics based on learnings

---

## References

- **Source:** Countly Blog - "The Complete Guide to Events Tracking in Product Analytics" (2026-04-01)
- **Disaster Recovery:** AWS/Azure/Oracle DR best practices
- **Week 2 GTM:** Analytics execution plan (week2-gtm-analytics-execution-plan.md)
- **UTM Tracking:** Fallback strategy (week2gtm-client-side-utm-fallback-2026-04-01.md)

---

**Status:** ✅ READY FOR EXECUTION (awaiting backend deployment)
**Owner:** analytics
**Next Owner:** analytics (will execute verification when backend deploys)
