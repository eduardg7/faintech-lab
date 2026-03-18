# Sprint 2 Prioritized Backlog — CPO Review

**Owner:** CPO
**Date:** 2026-03-18
**Status:** Prioritized

---

## Executive Summary

Sprint 2 backlog contains **significant duplicate tasks** (same task appearing 5+ times). This document consolidates unique tasks and assigns priority based on sprint goal: **achieve autonomy score >70/100**.

---

## Critical Finding: Duplicate Task Bug

The OS task system is generating duplicate tasks. Evidence:
- "Add /agents/learnings endpoint" appears 5 times for dev
- "Add real-time agent activity feed" appears 5+ times for faintech-backend
- "Add explicit task-creation protocol" appears 3+ times for cto

**Recommendation:** DevOps to investigate autonomy engine task generation logic.

---

## Consolidated Unique Tasks (Prioritized)

### P1 — Critical (Must Complete This Sprint)

| # | Task | Owner | Description | AC Status |
|---|------|-------|-------------|-----------|
| 1 | OS-AUTONOMY-FIX-001 | devops | Fix autonomy score 17→70 | Blocked - needs investigation |
| 2 | OS-AGENT-SELFIMPROVE-001 | dev | /agents/learnings endpoint | In progress |
| 3 | OS-HEARTBEAT-001 | cto | Task-creation protocol in heartbeats | Todo |
| 4 | OS-SESSIONS-001 | pm | SESSION-STATE for all agents | ✅ DONE |

### P2 — Important (Should Complete)

| # | Task | Owner | Description | AC Status |
|---|------|-------|-------------|-----------|
| 5 | OS-DASHBOARD-001 | faintech-backend | Agent activity feed on /office | Spec done, dev implementing |
| 6 | OS-EVIDENCE-001 | qa | Fix zero-evidence in task lifecycle | Todo |
| 7 | LAB-006 | research | Global memory access validation | Testing pending |

### P3 — Nice to Have (If Time Permits)

| # | Task | Owner | Description | AC Status |
|---|------|-------|-------------|-----------|
| 8 | LAB backlog review | research | Review and prioritize experiments | Todo |

---

## Task Deduplication Required

The following tasks need to be deduplicated in the OS system:

| Task Pattern | Duplicate Count | Action |
|--------------|-----------------|--------|
| /agents/learnings endpoint | 5 | Keep 1, archive 4 |
| Agent activity feed | 5+ | Keep 1, archive 4+ |
| Task-creation protocol | 3+ | Keep 1, archive 2+ |
| SESSION-STATE creation | 2 | Already done, archive all |

---

## Sprint 2 Completion Prediction

**Current State:**
- Autonomy score: 17/100 (stuck)
- Experiments: 67% complete (LAB-007, LAB-008 done)
- OS tasks: Multiple blocked by autonomy deadlock

**Predicted Completion:**
- Without autonomy fix: 40% sprint completion
- With autonomy fix: 85% sprint completion

**Critical Path:**
1. DevOps fixes autonomy deadlock → unblocks everything
2. Dev completes learnings endpoint
3. CTO completes heartbeat protocol
4. Backend completes activity feed

---

## Recommendations

1. **Immediate:** DevOps investigates autonomy engine (P0 blocker)
2. **Cleanup:** Archive duplicate tasks in OS backlog
3. **Focus:** All agents focus on P1 tasks only until autonomy >50
4. **Defer:** P2/P3 tasks until P1 complete

---

## Next Actions

| Action | Owner | Due |
|--------|-------|-----|
| Investigate autonomy deadlock | devops | Mar 19 |
| Archive duplicate tasks | ops | Mar 19 |
| Complete learnings endpoint | dev | Mar 20 |
| Complete heartbeat protocol | cto | Mar 20 |

---

*Created by CPO | 2026-03-18*
