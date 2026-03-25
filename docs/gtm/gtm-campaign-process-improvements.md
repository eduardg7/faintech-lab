# GTM Campaign Process Improvements

**Created:** 2026-03-19T19:04:00Z
**Author:** faintech-marketing-lead
**Source:** Beta Outreach Blocker Lessons (Mar 17-19, 2026)

---

## Executive Summary

This document captures process improvements for future GTM campaigns based on lessons learned from the AMC Beta Launch (Mar 2026). Key issues: single-point-of-failure dependencies, ambiguous SLA definitions, and escalation timeline gaps.

---

## Process Improvements

### 1. Dual-Track Candidate Sourcing

**Problem:** Beta outreach had single dependency on CEO-provided candidate list. When CEO was unavailable for 20+ hours, SLA was breached.

**Solution:** Always run parallel sourcing tracks:
- **Track A (Network):** Internal network (CEO/founders/advisors) - higher trust, faster onboarding
- **Track B (Independent):** Agent-driven research (LinkedIn, communities, existing users) - backup pool

**Implementation:**
- Start both tracks simultaneously when campaign kicks off
- Track A target: 70% of needed users
- Track B target: 30% backup pool
- If Track A delayed >6h, activate Track B candidates

**Example:** Beta launch needed 8 users. Track A would target 5-6 from network, Track B would identify 2-3 backup candidates independently.

---

### 2. Hard vs Soft Deadline Definitions

**Problem:** Original deadline (Mar 12) vs SLA deadline (Mar 17) created confusion about escalation timing.

**Solution:** Define explicit deadline types in campaign brief:

```yaml
deadlines:
  soft_deadline: "2026-03-12"  # Target completion
  hard_deadline: "2026-03-17"  # Must complete or escalate
  escalation_trigger: "hard_deadline - 48h"  # Start escalation
  sla_breach: "hard_deadline + 0h"  # SLA failure point
```

**Rules:**
- Soft deadline = internal target, adjust if needed
- Hard deadline = external commitment, requires escalation if missed
- Escalation starts 48h before hard deadline, not after
- SLA breach = immediate escalation to next level

---

### 3. Escalation Timeline Triggers

**Problem:** First escalation happened at 13:40 UTC (7h before SLA breach), too late for contingency activation.

**Solution:** Pre-define escalation triggers as percentages of timeline:

```yaml
escalation_triggers:
  - trigger: "50% of timeline elapsed"
    action: "Status check, remind owner"
    owner: "task_owner"

  - trigger: "75% of timeline elapsed"
    action: "Escalate to direct manager"
    owner: "manager"

  - trigger: "90% of timeline elapsed (48h before hard deadline)"
    action: "Escalate to C-suite with options"
    owner: "ceo/coo"

  - trigger: "100% (hard deadline)"
    action: "SLA breach, contingency activation"
    owner: "coo"
```

**Example:** If hard deadline is Mar 17 17:00:
- 50% trigger: Mar 15 08:30 (status check)
- 75% trigger: Mar 16 12:45 (manager escalation)
- 90% trigger: Mar 17 09:00 (C-suite with options)
- 100% trigger: Mar 17 17:00 (contingency activation)

---

### 4. Contingency Scenario Documentation

**Problem:** No pre-defined contingency scenarios, created confusion during SLA breach.

**Solution:** Document 4 scenarios before campaign starts:

**Scenario A: On Track**
- All dependencies resolved on time
- Execute original plan

**Scenario B: Minor Delay (<24h)**
- One dependency delayed <24h
- Compress timeline, add parallel execution

**Scenario C: Major Delay (24-48h)**
- Critical dependency delayed 24-48h
- Activate backup track, adjust launch date

**Scenario D: Critical Delay (>48h)**
- Critical dependency delayed >48h
- Postpone launch, communicate to stakeholders

**Decision Matrix:**
```yaml
if delay < 24h:
  scenario: B
  action: compress_timeline
elif delay < 48h:
  scenario: C
  action: backup_track
else:
  scenario: D
  action: postpone_launch
```

---

### 5. Launch Date Buffer

**Problem:** Mar 24 beta launch had no buffer for GTM lead time variations.

**Solution:** Build 48h buffer into all GTM timelines:

```yaml
campaign_timeline:
  content_deadline: "launch_date - 7 days"
  asset_deadline: "launch_date - 5 days"
  approval_deadline: "launch_date - 3 days"  # Was launch_date - 2
  execution_start: "launch_date - 2 days"    # Was launch_date - 1
  buffer: "48h"
```

**Rules:**
- Approvals must complete 3 days before launch (not 2)
- Execution starts 2 days before launch (not 1)
- Buffer absorbs unexpected delays

---

## Application to Current Campaign (AMC Beta)

**Current Status (Mar 19 19:04 UTC):**
- ✅ Tier 1 candidates approved (CEO decision received)
- ✅ Legal documents approved (CEO decision received)
- ✅ All GTM infrastructure complete
- ⏳ External execution pending approval

**Next Campaign Should:**
1. Start dual-track sourcing from Day 1
2. Define hard/soft deadlines in campaign brief
3. Pre-document escalation triggers
4. Create 4 contingency scenarios
5. Build 48h buffer into timeline

---

## Metrics to Track

**Process Health:**
- Time from blocker → escalation (target: <6h)
- Time from escalation → resolution (target: <12h)
- Percentage of campaigns hitting soft deadline (target: >80%)
- Percentage of campaigns requiring contingency (target: <20%)

**Campaign Effectiveness:**
- User acquisition rate (target: per campaign brief)
- Time from launch → first user (target: <24h)
- User activation rate (target: per campaign brief)

---

## Implementation Checklist

For each new GTM campaign:

- [ ] Define hard/soft deadlines
- [ ] Start dual-track candidate sourcing
- [ ] Document escalation triggers (50%, 75%, 90%, 100%)
- [ ] Create 4 contingency scenarios (A, B, C, D)
- [ ] Build 48h buffer into timeline
- [ ] Assign escalation owners (owner, manager, c-suite, coo)
- [ ] Track process health metrics

---

**Next Review:** After next GTM campaign completion
**Owner:** faintech-marketing-lead
**Stakeholders:** CMO, COO, CEO
