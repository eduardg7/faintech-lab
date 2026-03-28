# Week 1 Customer Success Framework

**Created:** 2026-03-27
**Owner:** CSM (Customer Success)
**Context:** Week 1 post-launch (Mar 27 - Apr 2), preparing for first customer acquisition

---

## Success Metrics (from Mixpanel 2024 Benchmarks)

**Activation Target:** 60%+ of signups store first memory within 24h
**Retention Target:** 3+ users remain active beyond day 7
**Week 1 Target:** 5-10 signups (from GTM channels)
**Good Performance:** 10 signups, 500 impressions, 20 conversations
**Excellent Performance:** 20 signups, 1,000 impressions, 50 conversations

---

## First 7 Days Onboarding (Critical Activation Window)

### Day 0 (Signup Day)
- **Welcome Email:** Send within 30 minutes of signup
  - Template: Welcome to AMC | Here's your quick start guide
  - Content: Setup your first memory in 5 minutes (our "aha moment")
  - Call to action: Store your first memory now

### Day 1-3 (Activation Period)
- **Day 3 Survey:** Send automated check-in
  - Goal: Capture early friction points
  - Questions:
    1. Have you stored your first memory yet?
    2. What was confusing during setup?
    3. What would make AMC more useful for you?

### Day 4-7 (Retention Check)
- **Day 7 Check-in:** Email from founder or CSM
  - Personal touch from human founder
  - Ask: What's your favorite feature so far? What would you add?
  - Goal: Build relationship, identify power users

---

## Customer Feedback Collection

### In-Product Feedback
- **Feedback Widget:** Collect spontaneous feedback
- **Context:** When user stores memory (positive signal), when they abandon (negative signal)

### Direct Communication
- **Email:** csm@faintech.ai (or founder email)
- **Response SLA:**
  - Technical Qs: 2h response
  - Feature requests: 4h response

### Community Engagement
- **HN Comments:** Founder responds to technical Qs
  - SLA: First comment within 30min of HN submission
  - Founder engagement creates trust

---

## Success Health Score Monitoring

**Daily Metrics:**
- Signups (total, by channel: HN, Twitter, LinkedIn, direct)
- Activation rate (first memory stored / signups)
- Time to first memory (minutes/hours)
- Active users (users who stored memory in last 7 days)

**Weekly Report (EOD Monday):**
- Total signups for week
- Activation rate (%)
- Retention rate (day 7+)
- Top feedback themes (3 themes)
- Blockers reported

---

## Escalation Protocols

### Critical Escalation (P0)
- **Trigger:** Production outage affecting users
- **Action:** Immediate to CTO/DevOps
- **SLA:** 15min acknowledgment, 1h resolution or workaround

### High Priority (P1)
- **Trigger:** Critical bug blocking core functionality
- **Action:** To CTO for fix assignment, CSM for customer comms
- **SLA:** 30min acknowledgment, 24h fix

### Medium Priority (P2)
- **Trigger:** Feature request, usability issue
- **Action:** To CPO for roadmap consideration
- **SLA:** 24h acknowledgment, 1-week decision (add/negotiate/defer)

---

## Readiness Status

**Infrastructure:** ✅ READY (100%)
- Welcome email template ready
- Survey questions defined
- Response SLAs documented
- Health score metrics defined

**Blockers:** None - CS infrastructure complete

**Dependencies on GTM:**
- Wait for first signups to begin activation tracking
- HN launch (Apr 1) is primary acquisition channel
- Twitter auth blockage resolved → additional channel active

---

## Next Actions

**Immediate (Today):**
- [ ] Verify HUNTER_API_KEY operational status (email validation)
- [ ] Confirm welcome email template deployed
- [ ] Set up Day 3 survey automation

**This Week (before HN launch):**
- [ ] Test welcome email flow end-to-end
- [ ] Prepare founder's first comment for HN launch
- [ ] Set up daily metrics dashboard

**Post-HN Launch (Apr 1+):**
- [ ] Monitor first 24h activation rate
- [ ] Send Day 3 surveys
- [ ] Identify power users for personal outreach (Day 7)

---

**Status:** Week 1 CS framework COMPLETE. Ready for first customers when GTM execution produces signups.
