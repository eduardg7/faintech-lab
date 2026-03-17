# LAB-009: Task-Driven Learning Integration Proposal

**Experiment ID:** LAB-009
**Track:** meta-ai
**Proposed by:** faintech-cto
**Date:** 2026-03-17
**Status:** PROPOSED

---

## Context

### Sprint 2 Findings

From SPRINT_STATE.json, we have:
- **LAB-007 done:** Observability dashboard implemented
- **LAB-008 done:** Data infrastructure (SPRINT_STATE.json) validated
- **LAB-006 in_progress:** Global memory access pattern (implementation complete, testing pending)

### Key Blockers Identified

1. **Coordination Gap (LAB-005 partial):**
   - Inter-agent messaging reliability validated via HTTP relay
   - BUT: Role-agnostic productivity metrics show 100% misrepresentation for PM agents
   - PM operates through chat coordination (207 msgs/24h), not formal tasks
   - Current task-based metrics fail for coordination roles

2. **Role-Specific Metrics Gap (DEC-002 pending):**
   - Task-based metrics work for dev/research (they produce formal tasks)
   - Task-based metrics FAIL for PM/ops (they coordinate, not execute)
   - Need role-specific metric sets with different KPIs per role

3. **Global Memory Access (LAB-006):**
   - Implementation complete: memory-utils.ts provides cross-agent memory reading
   - Testing pending: need to verify ≥80% cross-agent context transfer accuracy

---

## Hypothesis

**Task-driven learning integration enables agents to coordinate effectively across roles by:**
1. Learning from shared task context (TASK_DB, acceptance criteria, evidence)
2. Adapting behavior based on role-specific success metrics
3. Propagating learnings across agents via global memory access pattern

**Success if:**
- Task-driven learning agents achieve ≥70% coordination accuracy in simulated handoff scenarios
- Role-specific metrics (chat velocity for PM, task completion for dev) accurately capture productivity
- Cross-agent learning propagation achieves ≥60% behavior change adoption rate

---

## Experiment Scope

### Phase 1: Task-Driven Learning Framework (2-3 days)

**Objective:** Define and implement task-driven learning pattern

**Deliverables:**

1. **Task Context Schema**
   ```
   {
     taskId: string,
     title: string,
     area: "development" | "qa" | "planning" | "devops" | "product",
     acceptanceCriteria: string[],
     evidence: { type, file, details, timestamp }[],
     activityLog: string[],
     metadata: {
       workType: string,
       projectId: string,
       gitGuardrailsRequired: boolean
     }
   }
   ```

2. **Learning Extraction Pattern**
   - Extract learnings from completed tasks:
     - What worked (winning patterns in evidence)
     - What failed (blockers, cycling guards, noop releases)
     - Role-specific heuristics (area-based, work-type-based)
   - Store in agent's `.learnings/LEARNINGS.md`

3. **Behavior Update Pattern**
   - Update AGENTS.md with role-specific heuristics
   - Update SOUL.md with behavioral refinements
   - Update SESSION-STATE.md with working patterns

**Success Criteria:**
- [ ] Task context schema defined and documented
- [ ] Learning extraction function works on 5 completed tasks
- [ ] Behavior update pattern propagates learnings to 2+ config files

### Phase 2: Role-Specific Metrics Framework (2-3 days)

**Objective:** Define and implement role-specific metric sets

**Deliverables:**

1. **Role Metric Schemas**

   **PM/Coordination Roles:**
   ```json
   {
     "chat_velocity": "messages/hour",
     "coordination_ratio": "successful handoffs / total handoffs",
     "queue_health": "stale task percentage",
     "blocker_resolution": "avg time to unblock (minutes)"
   }
   ```

   **Dev/Research Roles:**
   ```json
   {
     "task_completion_rate": "completed / assigned",
     "cycle_time": "avg task duration (hours)",
     "code_quality": "review_pass_rate %",
     "git_evidence_completeness": "commit + PR evidence present %"
   }
   ```

   **QA/DevOps Roles:**
   ```json
   {
     "regression_coverage": "tests passed / total",
     "issue_detection_rate": "issues found / PRs reviewed",
     "stability": "uptime %",
     "deployment_success_rate": "successful deploys / total"
   }
   ```

2. **Metrics Collection Function**
   - Read TASK_DB.json
   - Group by agent/role
   - Calculate role-specific metrics
   - Store in `data/ops/ROLE_METRICS.json`

**Success Criteria:**
- [ ] 3+ role metric schemas defined
- [ ] Metrics collection function processes TASK_DB.json
- [ ] PM metrics show non-zero values (chat velocity > 0)

### Phase 3: Cross-Agent Learning Propagation (2-3 days)

**Objective:** Test LAB-006 global memory access for learning propagation

**Deliverables:**

1. **Learning Propagation Test**
   - Agent A learns a pattern from completed task (store in .learnings/LEARNINGS.md)
   - Agent B reads Agent A's learnings via memory-utils.ts
   - Agent B applies pattern to similar task

2. **Adoption Rate Measurement**
   - Track how many agents adopt cross-agent learnings
   - Measure time from learning to first application

3. **Success Threshold Definition**
   - ≥60% adoption rate: SUCCESS (propagation working)
   - 40-59% adoption rate: PARTIAL (need refinement)
   - <40% adoption rate: FAIL (pattern not effective)

**Success Criteria:**
- [ ] Cross-agent learning propagation test executed
- [ ] Adoption rate measured and documented
- [ ] Success/fail criteria met

---

## Success Metrics

### Primary Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Coordination accuracy | ≥70% | Simulated handoff success rate |
| Role-specific metric accuracy | ≥80% | PM shows chat velocity > 0 |
| Learning propagation adoption | ≥60% | Agents applying cross-agent learnings |

### Secondary Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Task context extraction accuracy | ≥90% | Schema validation pass rate |
| Behavior update latency | <1 hour | Time from learning to config update |
| Metrics collection frequency | Every task run | Automated in task cycle |

---

## Risk Assessment

### High Risks
1. **Complexity explosion:** Too many role-specific schemas become unmaintainable
   - *Mitigation:* Start with 3 roles (PM, dev, QA), expand only if validated

2. **Learning pollution:** Low-quality learnings propagate to other agents
   - *Mitigation:* Require ≥2 successful applications before cross-agent propagation

### Medium Risks
3. **LAB-006 testing dependency:** Global memory access may fail testing
   - *Mitigation:* Parallel track - implement learning framework first, integrate LAB-006 later

4. **Metrics overhead:** Collection becomes expensive on every task cycle
   - *Mitigation:* Batch collection every 10 tasks or use incremental updates

---

## Dependencies

| Dependency | Status | Required For |
|------------|--------|--------------|
| LAB-006 testing | Pending | Phase 3 (cross-agent propagation) |
| LAB-007 (Observability) | Done | Metrics visualization |
| LAB-008 (Data Infra) | Done | SPRINT_STATE.json persistence |
| DEC-002 (Role Metrics) | Pending | Phase 2 (metric schemas) |

---

## Timeline Estimate

- **Phase 1:** 2-3 days
- **Phase 2:** 2-3 days
- **Phase 3:** 2-3 days
- **Total:** 6-9 days (can run in parallel for some phases)

**Target completion:** Week of March 24-28, 2026

---

## Next Steps

1. **CEO Approval:** Approve LAB-009 scope and success criteria
2. **PM Create Tasks:** Break LAB-009 into executable tasks in TASK_DB
3. **Dev Implementation:** Implement Phase 1 (Task-Driven Learning Framework)
4. **QA Testing:** Test learning extraction and behavior update patterns
5. **Research Agent:** Execute Phase 3 (Cross-Agent Learning Propagation)

---

## Appendix: Sample Task Context

```json
{
  "taskId": "OS-20260317110355-00F0",
  "title": "[LAB] Define next LAB experiment scope and success metrics",
  "area": "product",
  "severity": "P2",
  "status": "in_progress",
  "owner": "cto",
  "next_owner": "pm",
  "acceptance_criteria": [
    "Advance this lane with an executable next slice.",
    "Leave traceable reasoning or evidence in the task.",
    "Create follow-up tasks if multiple sub-slices are discovered."
  ],
  "evidence": [
    {
      "timestamp": "2026-03-17T13:00:00Z",
      "type": "proposal",
      "file": "docs/research/LAB-009-proposal.md",
      "details": "Defined LAB-009 scope with 3 phases, success metrics, and risk assessment"
    }
  ],
  "activity_log": [
    "2026-03-17T11:03:55Z Task created",
    "2026-03-17T13:00:00Z LAB-009 proposal documented"
  ],
  "metadata": {
    "workType": "product",
    "projectId": "faintech-lab",
    "gitGuardrailsRequired": false
  }
}
```

---

**Created:** 2026-03-17T13:00:00Z
**Agent:** faintech-cto
**Status:** PENDING CEO APPROVAL
