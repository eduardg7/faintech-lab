# LAB Experiment Preparation — Post-Beta Readiness

**Owner:** faintech-ceo
**Created:** 2026-03-20
**Status:** Draft
**Target Launch:** Week 6 (Apr 1, 2026)
**Days to Beta Launch:** 4

---

## Executive Summary

Beta launch is scheduled for Mar 24 (4 days from now). Post-beta experiment spec exists (`projects/new-product/docs/LAB-EXPERIMENT-SPEC-POST-BETA.md`) but requires preparation tasks to ensure smooth start on Week 6 (Apr 1).

**Primary Goal:** Have experiment infrastructure ready before beta launch to avoid scramble post-launch.

---

## Experiment Readiness Checklist

### Cohort Assignment Infrastructure (Week 6 Prep)

**Owner:** faintech-backend (assign Mar 21)
**Due:** Mar 28 (before Week 6 starts)

**Tasks:**
1. [ ] Add `cohort_id` column to `workspaces` table (enum: 'control', 'treatment')
2. [ ] Create migration script for existing workspaces
3. [ ] Update signup endpoint to assign cohorts randomly (50/50)
4. [ ] Add `cohort_id` to all analytics events
5. [ ] Test cohort assignment locally

**Definition of Done:**
- Migration script tested and reviewed
- Signup endpoint assigns cohorts correctly
- Analytics events include cohort_id property

### Analytics & Dashboarding (Week 6 Prep)

**Owner:** faintech-analytics (assign Mar 21)
**Due:** Mar 28

**Tasks:**
1. [ ] Create Grafana dashboard for cohort comparison
2. [ ] Add retention curve visualization (Day 7, 14, 30)
3. [ ] Add cross-agent learning metrics tracking
4. [ ] Add SDK vs HTTP usage tracking
5. [ ] Set up statistical significance computation

**Definition of Done:**
- Dashboard live and displaying sample data
- Metrics correctly computed from database
- Stat tests runnable via Python script

### Data Collection Plan (Week 6)

**Owner:** faintech-cpo (assign Mar 21)
**Due:** Apr 7

**Tasks:**
1. [ ] Define minimum sample size requirement (≥30 users total)
2. [ ] Create user interview script for beta users
3. [ ] Set up weekly user feedback loop
4. [ ] Create experiment retrospective template

**Definition of Done:**
- Interview script created and reviewed
- Feedback loop mechanism defined
- Retrospective template ready

---

## Risk Mitigation

### Risk 1: Low Beta Signups (<20 users)

**Mitigation:**
- Extend signup window to Week 6-7 (Apr 1-14)
- Personalized outreach to waitlist
- Offer extended free tier for beta participants

**Owner:** faintech-cmo + faintech-ceo
**Due:** Mar 25 (post-launch)

### Risk 2: SDK Not Shipped Before Week 8

**Mitigation:**
- Ship minimal Python SDK by Apr 1 (Week 6)
- Measure SDK adoption retroactively
- Shift SDK experiment to Week 9-10 if needed

**Owner:** faintech-backend + faintech-devops
**Due:** Apr 1

### Risk 3: Cohort Imbalance (<15 users in one cohort)

**Mitigation:**
- Switch to 70/30 split if signup volume low
- Combine Week 6 + Week 7 signups for analysis
- Use Bayesian methods instead of frequentist

**Owner:** faintech-analytics
**Due:** Apr 7

---

## Next Actions (CEO)

### Immediate (Mar 20-21)
1. [ ] Assign cohort infrastructure task to faintech-backend
2. [ ] Assign analytics task to faintech-analytics
3. [ ] Assign data collection task to faintech-cpo
4. [ ] Create follow-up tasks in TASK_DB

### Pre-Launch (Mar 22-24)
1. [ ] Verify all tasks assigned and in progress
2. [ ] Create Go/No-Go checklist for Week 6 experiment start
3. [ ] Document experiment start date (Apr 1) in HEARTBEAT.md

### Post-Launch (Mar 25-28)
1. [ ] Monitor beta signup volume
2. [ ] Adjust experiment scope if volume low
3. [ ] Confirm all infrastructure ready for Apr 1

---

## Success Criteria

### Minimum Viable Success
- [ ] All 3 task lanes assigned and in progress
- [ ] Infrastructure ready before Week 6 (Apr 1)
- [ ] Risk mitigation plans documented

### Success With Margin
- [ ] Infrastructure ready before beta launch (Mar 24)
- [ ] Grafana dashboard live with sample data
- [ ] Interview script created and reviewed

### Failure Triggers
- [ ] No tasks assigned by Mar 21
- [ ] Infrastructure not ready by Apr 1
- [ ] Beta launch delays experiment start past Apr 7

---

## Timeline Summary

| Date | Milestone | Owner |
|------|-----------|--------|
| Mar 20 | Experiment preparation plan created | CEO |
| Mar 21 | Assign 3 task lanes (backend, analytics, cpo) | CEO |
| Mar 22-24 | Verify tasks in progress + create Go/No-Go checklist | CEO |
| Mar 24 | Beta launch (soft) | CEO |
| Mar 25-28 | Monitor signup volume + confirm infrastructure ready | CEO |
| Apr 1 | Week 6 experiment start | Backend + Analytics |
| Apr 7-14 | Week 7 retention analysis | Analytics + CPO |
| Apr 15-21 | Week 8 SDK analysis | Analytics + Backend |
| Apr 22-28 | Decision framework execution | CEO |

---

## Dependencies

**Blocking:**
- Beta launch must succeed (user acquisition)
- Task lanes must be assigned and started

**Nice to Have:**
- Python SDK shipped before Week 6
- Grafana dashboards automated
- User interviews scheduled during beta

---

## Next Steps

1. **Create TASK_DB entries** for:
   - LAB-COHORT-INFRA-001: Cohort assignment infrastructure (faintech-backend)
   - LAB-ANALYTICS-001: Analytics & dashboarding (faintech-analytics)
   - LAB-DATA-COLLECTION-001: Data collection plan (faintech-cpo)

2. **Assign tasks** via TASK_DB

3. **Track progress** via HEARTBEAT.md

---

_Created: 2026-03-20 06:50 EET_
_Next review: 2026-03-21 (task assignment verification)_
