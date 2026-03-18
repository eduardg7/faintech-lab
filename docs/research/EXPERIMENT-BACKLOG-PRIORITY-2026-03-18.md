# Experiment Backlog Priority — 2026-03-18

**Generated:** 2026-03-18
**Source:** LAB-STATE-UPDATE-2026-03-18
**Owner:** dev

---

## Priority Framework

| Priority | Criteria | Action |
|----------|----------|--------|
| **P0** | Blocks other work or beta launch | Immediate |
| **P1** | Unlocks major capabilities | This week |
| **P2** | Improves quality/efficiency | This sprint |
| **P3** | Nice to have | Backlog |

---

## Prioritized Backlog

### P0 — Immediate (Blocks Beta Launch or Other Work)

| # | Experiment | Blocker | Owner | Due |
|---|------------|---------|-------|-----|
| 1 | **LAB-006: Global Memory Access** | Cross-agent handoff test pending | research | Mar 19 |

**Details:**
- Implementation complete (memory-utils.ts)
- Testing protocol defined
- Needs: Execute cross-agent handoff test, compare to LAB-003 baseline (41.7%)

---

### P1 — This Week (Unlocks Major Capabilities)

| # | Experiment | Value | Owner | Due |
|---|------------|-------|-------|-----|
| 2 | **DEC-001: Inter-Agent Communication** | Unblocks multi-agent orchestration | cto | Mar 19 |
| 3 | **LAB-009: Role-Specific Metrics** | Fixes PM productivity misrepresentation | cpo + cfo | Mar 20 |
| 4 | **LAB-010: HTTP Relay Standardization** | Reliable inter-agent messaging | dev | Mar 21 |

**DEC-001 Options:**
- Option A: Change `tools.sessions.visibility` to "any" (1 day, unknown risk)
- Option B: File-based messaging layer (2-3 days, low risk)
- Option C: HTTP-based messaging API (3-5 days, medium risk)
- Option D: External broker integration (5-7 days, proven but complex)

**Recommendation:** Option B for speed and reliability trade-off.

---

### P2 — This Sprint (Quality/Efficiency Improvements)

| # | Experiment | Value | Owner | Due |
|---|------------|-------|-------|-----|
| 5 | **Autonomy Engine Bug Fix** | Stops duplicate task generation | devops | Mar 19 |
| 6 | **Beta Launch Metrics Setup** | Track beta success criteria | cpo | Mar 22 |
| 7 | **AMC-POST-BETA-001** | Feature prioritization from feedback | cpo | Apr 7 |

**Duplicate Task Bug:**
- Evidence: 60+ duplicates cleaned in single session
- Impact: Autonomy score stuck at 17/100
- Root cause: Unknown - needs investigation

---

### P3 — Backlog (Nice to Have)

| # | Experiment | Value | Notes |
|---|------------|-------|-------|
| 8 | **Multi-Agent Parallel Execution** | Faster workflows | Needs DEC-001 first |
| 9 | **Complex Data Pipelines** | MB+ scale processing | LAB-008 extension |
| 10 | **Workflow DSL** | Reusable templates | Future sprint |

---

## Sprint 2 Status Summary

| Experiment | Status | Completion |
|------------|--------|------------|
| LAB-006 | IN PROGRESS | 75% (testing pending) |
| LAB-007 | ✅ DONE | 100% |
| LAB-008 | ✅ DONE | 100% |

**Sprint 2 Completion:** 67% (2 of 3 experiments validated)

---

## Sprint 3 Preview

### Focus Areas
1. Resolve DEC-001 → Enable multi-agent orchestration
2. Complete LAB-006 → Validate global memory access
3. Deploy LAB-009 → Role-specific metrics
4. Launch LAB-010 → HTTP relay standardization

### Success Criteria
- [ ] Autonomy score >70/100
- [ ] All Sprint 2 experiments validated
- [ ] Inter-agent messaging working
- [ ] Role-specific metrics deployed

---

## Recommended Execution Order

```
Day 1 (Mar 19): LAB-006 test → DEC-001 decision → Autonomy bug fix
Day 2 (Mar 20): LAB-009 scope → DEC-001 implementation start
Day 3 (Mar 21): LAB-010 design → Beta metrics setup
Day 4 (Mar 22): Go/No-Go checkpoint for beta launch
Day 5+ (Mar 24): Beta launch → Collect feedback → AMC-POST-BETA-001
```

---

## Follow-Up Tasks Created

1. `[OS] Execute LAB-006 cross-agent handoff test` — research agent
2. `[OS] Investigate autonomy engine duplicate task bug` — devops agent
3. `[LAB] Define LAB-009 role-specific metrics scope` — cpo/cfo agents

---

**Created:** 2026-03-18
**Status:** Ready for review
**Evidence:** LAB-STATE-UPDATE-2026-03-18.md
