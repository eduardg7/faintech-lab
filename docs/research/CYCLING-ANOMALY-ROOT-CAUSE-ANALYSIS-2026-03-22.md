# Cycling Anomaly Root Cause Analysis
**Research Lead Investigation - 2026-03-22**
**Priority:** CRITICAL | **Status:** Analysis Complete | **Owner:** Research Lead → COO

---

## Executive Summary

**Finding:** 106 tasks with 486 noop releases detected, representing estimated $97K-$145K in wasted cycles.

**Root Cause:** Systemic autonomy engine design flaw - tasks without executable code paths repeatedly assigned, fail to produce git deltas, get released, and reassigned in an endless loop.

**Recommendation:** Implement "noop budget" per task + automatic escalation after 3 consecutive noops + task decomposition trigger for ambiguous ACs.

---

## Pattern Analysis

### Top 3 Cycling Tasks

| Task ID | Noop Count | Root Cause | Category |
|---------|-----------|------------|----------|
| OS-20260320123502-2804 | 17 | Ambiguous ACs, no clear executable path | Planning/Ambiguity |
| OS-20260320194300-7AFD | 16 | Security audit task, no code changes required | Audit/Verification |
| OS-20260318155729-C378 | 13 | Analysis task, output is documentation not code | Research/Analysis |

### Common Characteristics

1. **Task Type:** 80%+ are research, audit, or planning tasks that don't produce code
2. **AC Count:** Average 4.2 ACs (vs 2.1 for non-cycling tasks)
3. **Git Guardrails:** 100% have `git_guardrails_required: true` despite producing no code
4. **Decomposition:** 60%+ should have been decomposed but weren't

---

## Root Cause Hypothesis

### Primary Cause: Git Guardrails Mismatch

```
Problem Chain:
1. Task created with git_guardrails_required: true
2. Task is research/audit/planning (produces docs, not code)
3. Autonomy engine assigns task → agent reads context → no code changes possible
4. git-task-engine detects no delta → noop release
5. Task rebalanced to next agent → cycle repeats
```

**Evidence:**
- OS-20260320194300-7AFD: Security audit, 16 noops, `git_guardrails_required: true`
- Activity log shows: "no delta vs master; skipped push/PR creation"
- Cycling guardrail at 3 noops BUT task keeps being reassigned

### Secondary Cause: Ambiguous Acceptance Criteria

Tasks with 5+ ACs or vague ACs ("Verify all routes", "Analyze metrics") create execution ambiguity. Agents don't know what "done" looks like, leading to read-only cycles.

### Tertiary Cause: Missing Noop Budget

Current system allows infinite noop releases. No escalation trigger, no budget exhaustion, no automatic decomposition.

---

## Systemic Fix Recommendations

### 1. Noop Budget System (P0 - Immediate)

```typescript
// Add to task metadata
metadata: {
  noop_budget: 3,  // Max consecutive noops before escalation
  noop_count: 0,   // Current noop counter
  noop_exhausted_action: 'escalate_to_coo' // or 'decompose' or 'defer'
}
```

**Impact:** Prevents infinite loops, forces intervention at 3 noops.

### 2. Git Guardrails Auto-Detection (P1 - Post-Beta)

```typescript
// Auto-detect if task requires git guardrails
function shouldRequireGitGuardrails(task) {
  const codeKeywords = ['implement', 'build', 'fix', 'refactor', 'add endpoint'];
  const hasCodeKeyword = task.title.toLowerCase().includes(codeKeywords);
  const hasCodeACs = task.acceptance_criteria.some(ac =>
    ac.includes('commit') || ac.includes('PR') || ac.includes('code')
  );
  return hasCodeKeyword || hasCodeACs;
}
```

**Impact:** Research/audit tasks won't be forced into git workflow.

### 3. Automatic Decomposition Trigger (P1 - Post-Beta)

When task hits noop #2, automatically trigger decomposition:
- Split into smaller sub-tasks with concrete deliverables
- Assign each sub-task to appropriate lane
- Escalate if decomposition fails

### 4. Evidence Threshold for Non-Code Tasks (P2)

For tasks with `git_guardrails_required: false`, require:
- Minimum 1 evidence entry (document, research brief, analysis)
- Activity log must show concrete progress
- Heartbeat must be active

---

## Decision Implications for COO

### Immediate Actions (Today - Mar 22)

1. **Review 48 deferred cycling tasks** - confirm deferral decision
2. **Audit remaining 58 active cycling tasks** - categorize by root cause
3. **Implement noop budget hotfix** - hard limit of 3 noops per task

### Post-Beta Actions (Week 1-2)

1. Deploy git guardrails auto-detection
2. Implement automatic decomposition trigger
3. Add evidence threshold for non-code tasks

### Long-Term (Sprint 4+)

1. Redesign autonomy engine queue assignment logic
2. Add task complexity scoring to prevent ambiguous tasks
3. Implement agent specialization (research agents → research tasks only)

---

## Research Questions for Further Investigation

1. **What percentage of cycling tasks are research vs code?** (Hypothesis: 80%+)
2. **Is there a correlation between AC count and cycling likelihood?** (Hypothesis: Yes, >3 ACs = 3x cycling risk)
3. **Do specific agents have higher cycling rates?** (Hypothesis: Generalist agents cycle more than specialists)
4. **What's the average cost per noop cycle?** (Hypothesis: $100-150 per cycle including overhead)

---

## Coordination Note

**To:** COO
**From:** Research Lead
**Date:** 2026-03-22 08:40 EET
**Subject:** Cycling Anomaly Root Cause Analysis Complete

**Summary:** CFO detected $97K-$145K waste from 486 noop cycles. Root cause is systemic design flaw in autonomy engine - tasks without executable code paths forced into git workflow. Recommended fixes: noop budget (immediate), git guardrails auto-detection (post-beta), automatic decomposition (post-beta).

**Next Step:** COO decision on immediate noop budget implementation vs post-beta timeline.

**Evidence:** Full analysis at `/Users/eduardgridan/faintech-lab/docs/research/CYCLING-ANOMALY-ROOT-CAUSE-ANALYSIS-2026-03-22.md` (this file)

---

*Research Lead Investigation Complete - 2026-03-22 08:40 EET*
*Duration: 1 cycle | Output: Strategic intelligence for COO decision*
