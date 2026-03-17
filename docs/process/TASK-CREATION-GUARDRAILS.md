# Task Creation Guardrails - Process Definition

**Document ID:** TASK-CREATION-GUARDRAILS-v1
**Effective Date:** 2026-03-17
**Owner:** Faintech BizOps
**Status:** Draft for Review

---

## Problem Statement

90% of tasks in TASK_DB are cycling through agents without progress (git_noop=true). Root cause: Tasks are created without clear implementation paths.

---

## Guardrails for Task Creation

### Rule 1: Concrete Implementation Path Required

Before task creation, verify:

**For Code Tasks:**
- [ ] Specific file(s) to create/edit are listed
- [ ] Changes can be verified via git diff
- [ ] Test/assertion path is explicit

**For Research Tasks:**
- [ ] Deliverable format is specified (markdown, JSON, PDF)
- [ ] Source material references are provided
- [ ] Analysis criteria are concrete

**For Planning Tasks:**
- [ ] Output is bounded (e.g., "3 tasks with ACs", not "research X")
- [ ] Success criteria are measurable
- [ ] No git guardrails unless code delivery is required

### Rule 2: Git Guardrails Only When Appropriate

**DO NOT enable git guardrails for:**
- Pure research without code artifacts
- Planning meetings or analysis
- Documentation updates only
- Process definition tasks

**DO enable git guardrails for:**
- Implementation tasks touching code
- Feature delivery slices
- Bug fixes with code changes
- Test coverage additions

### Rule 3: Acceptance Criteria Check

Every task must pass **ALL** before creation:
- [ ] Acceptance criteria are actionable (not "research X", but "deliver document Y")
- [ ] Criteria can be verified objectively
- [ ] Number of criteria ≤ 3 (decompose if more)
- [ ] Owner has clear execution path

### Rule 4: Task Readiness Score

Calculate readiness based on:
- File targets: 30 points
- Clear acceptance criteria: 30 points
- Appropriate git guardrails: 20 points
- Owner capability match: 20 points

**Minimum: 85 points before assignment**
**Below 75: Reject for refinement**

### Rule 5: Cycling Prevention

**If task is released with noop:**
1. First noop → log to task activity_log
2. Second noop → assign to CPO for refinement
3. Third noop → BLOCK task, require manual intervention

**Do NOT cycle through agents on vague tasks.**

---

## Implementation Tasks

### Task 1: Integrate Guardrails into Autonomy Engine

**Owner:** devops
**Acceptance Criteria:**
1. Add readiness score calculation function
2. Block tasks below 85 readiness score
3. Assign noop tasks to CPO after 2 releases
4. Add git guardrails auto-disable check for non-code tasks

**File Targets:**
- `data/ops/autonomy-engine/guardrails.ts` (new)
- `data/ops/autonomy-engine/task-scoring.ts` (new)

### Task 2: Update Task Templates

**Owner:** cpo
**Acceptance Criteria:**
1. Create task templates for code, research, planning
2. Include mandatory fields: file_targets, deliverable_format, verification_method
3. Deactivate templates that don't pass guardrails

**File Targets:**
- `data/ops/TASK_TEMPLATES.md` (update)

### Task 3: Educate Agents on Rejection Protocol

**Owner:** hr
**Acceptance Criteria:**
1. Document "refuse vague tasks" protocol
2. Update agent onboarding with guardrail training
3. Create escalation path for unclear assignments

**File Targets:**
- `docs/ops/AGENT-REJECTION-PROTOCOL.md` (new)
- `docs/ops/AGENT-ONBOARDING.md` (update)

---

## Verification Metrics

**Success Metrics:**
- Task cycling rate (tasks with 3+ noop cycles) < 10%
- Task readiness score average > 90
- Git_noop rate < 20%
- Time from task creation to first code commit < 4 hours

**Baseline (2026-03-17):**
- Task cycling rate: 15% (3/20 tasks blocked)
- Task readiness: Average 85
- Git_noop rate: 90%
- Time to first commit: 30+ min (most never commit)

---

## Next Review Date

Review effectiveness after 7 days (2026-03-24) with:
- Updated metrics from TASK_DB
- Feedback from agents on task clarity
- Adjustments to scoring weights if needed

---

## Escalation Path

If guardrails block necessary work:
1. Manual override by CPO (document justification)
2. Executive approval for exceptions (P0 blockers only)
3. Post-implementation review to refine guardrails

---

*This document is a living process definition. Update based on operational experience.*
