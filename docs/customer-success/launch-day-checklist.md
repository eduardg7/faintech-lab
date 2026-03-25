# CSM Launch Day Checklist

**Launch Date:** March 24, 2026
**Owner:** CSM
**Version:** 1.0

---

## Pre-Launch (T-0 to T-2h)

### System Readiness
- [ ] Verify beta-tracker.json is empty (no stale test data)
- [ ] Confirm feedback widget is live in UI
- [ ] Test welcome email send functionality
- [ ] Verify survey form links are working

### Communication Setup
- [ ] Prepare personal intro message template for each Tier 2 user
- [ ] Set up Slack/Discord channel for beta user support (if applicable)
- [ ] Confirm CSM availability for first 4 hours post-launch

---

## Launch Day (T+0 to T+24h)

### Hour 0-2: First Signups
- [ ] Monitor beta-tracker.json for new user registrations
- [ ] Send welcome email to each new signup within 30 minutes
- [ ] Log first user in beta-feedback.md with initial observations
- [ ] Check for any onboarding blockers reported

### Hour 2-4: Initial Check-ins
- [ ] Send personal DM/email to first 3 signups: "How's setup going?"
- [ ] Review any in-app feedback submitted
- [ ] Log first feedback patterns in beta-feedback.md

### Hour 4-8: Pattern Detection
- [ ] Identify common friction points (if any)
- [ ] Escalate P0/P1 bugs to dev via cto
- [ ] Update onboarding-flow.md if major blockers discovered

### Hour 8-12: End of Day 1
- [ ] Count total signups and update beta-tracker.json
- [ ] Calculate Day 1 conversion rate (signups / landing page views)
- [ ] Write Day 1 summary for C-Suite chat
- [ ] Set up Day 2 check-in schedule for active users

---

## Day 1 Metrics to Track

| Metric | Target | Actual |
|--------|--------|--------|
| Total signups | 3-5 | ___ |
| First memory entries | 90%+ | ___ |
| Onboarding completion | 80%+ | ___ |
| P0/P1 bugs reported | <2 | ___ |
| NPS (if collected) | 7+ | ___ |
| Time to first value | <15 min | ___ |

---

## Escalation Triggers

**Escalate to CTO immediately if:**
- Any P0 bug blocking all users
- Onboarding flow completely broken
- Data loss or security issue

**Escalate to CPO if:**
- 3+ users report same UX confusion
- Value proposition not clear to users
- Feature requests that could block adoption

**Escalate to CEO if:**
- Zero signups after 12 hours
- Critical PR or reputation risk
- Major blocker requiring business decision

---

## Day 1 Report Template

```markdown
# Beta Day 1 Report — [Date]

## Signups
- Total: X users
- Source: GitHub Issue #90 (X), Direct (X), Other (X)

## Engagement
- Completed first memory: X% (Y/Z users)
- Avg time to first memory: X minutes
- Sessions per user: X

## Feedback
- Total feedback items: X
- P0/P1 bugs: X
- UX issues: X
- Feature requests: X

## Top 3 Issues
1. [Issue] — [Impact] — [Status]
2. [Issue] — [Impact] — [Status]
3. [Issue] — [Impact] — [Status]

## Recommendations
- [Action 1]
- [Action 2]

## Next 24h Focus
- [Priority 1]
- [Priority 2]
```

---

## Quick Reference

**Feedback Response SLAs:**
- P0 (Blocking): 2h response, 24h fix
- P1 (Major): 8h response, 72h fix
- P2 (Medium): 24h response
- P3 (Low): 48h response

**Key Files:**
- Beta tracker: `docs/customer-success/beta-tracker.json`
- Feedback log: `docs/customer-success/beta-feedback.md`
- User health: `docs/customer-success/health-metrics.md`
- Survey forms: `docs/customer-success/beta-survey-forms.md`

**Key Contacts:**
- CTO (technical issues): cto
- CPO (product issues): cpo
- CEO (business issues): ceo
- DevOps (infra issues): devops

---

**Last Updated:** 2026-03-22 22:59 EET
**Next Review:** Mar 24 08:00 EET (Launch Day morning)
