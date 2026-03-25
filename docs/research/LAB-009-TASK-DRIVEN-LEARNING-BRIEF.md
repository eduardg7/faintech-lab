# LAB-009: Task-Driven Learning Integration Research Brief

**Created:** 2026-03-20 11:50 EET
**Priority:** P1 (enables role-specific metrics and cross-agent learning)
**Status:** Ready for execution
**Owner:** cto (implementation), cpo (review)
**Timeline:** 6-9 days
**Depends on:** None (independent experiment)

---

## Executive Summary

Integrate task-driven learning into the Faintech OS autonomy loop, enabling agents to learn from completed tasks, extract role-specific metrics, and share learnings across agents. This addresses the CPO productivity misrepresentation issue identified in Sprint 2 (PM productivity appeared lower due to role-specific task patterns not being captured).

---

## Background

### Problem Statement
- CPO productivity was misreported due to role-specific task patterns not being captured
- Agents cannot currently learn from their own completed tasks
- Cross-agent learning is blocked (no shared learning repository)
- Role-specific metrics bias discovered: PM tasks take longer but have higher impact

### Validated Evidence
- **LAB-004 Results:** Self-improvement loop works (2/2 corrections applied)
- **CPO Insight Report:** PM productivity undercounted due to task complexity
- **Pattern:** Same-agent memory excellent (95-100%), but cross-agent learning missing

---

## Scope

### In Scope
1. Task completion analysis (extract patterns from completed tasks)
2. Role-specific metric extraction (task complexity, duration, impact)
3. Learning dashboard (show agent learning progress)
4. Cross-agent learning sharing (via HTTP relay once LAB-010 complete)

### Out of Scope
- External ML models - use rule-based learning first
- Complex NLP analysis - defer to Sprint 4
- Real-time learning - batch processing acceptable

---

## Acceptance Criteria

### AC1: Task Completion Analysis
- [ ] System extracts patterns from completed tasks
- [ ] Patterns include: task type, duration, complexity, outcome
- [ ] Analysis runs automatically after task completion
- [ ] Results stored in agent's learning file

### AC2: Role-Specific Metric Extraction
- [ ] Metrics extracted per role: dev, pm, cpo, cto, etc.
- [ ] Metrics include: avg task duration, complexity distribution, success rate
- [ ] Metrics visible in agent dashboard
- [ ] CPO productivity correctly reflects role-specific patterns

### AC3: Learning Dashboard
- [ ] Dashboard shows learning progress per agent
- [ ] Dashboard shows cross-agent learning count
- [ ] Dashboard shows most common patterns learned
- [ ] Dashboard accessible at `/settings/learnings`

### AC4: Cross-Agent Learning Sharing
- [ ] Agents can share learnings via HTTP relay (depends on LAB-010)
- [ ] Shared learnings tagged by role and task type
- [ ] Agents can query learnings from other agents
- [ ] Learning conflict resolution (newer learning wins)

---

## Implementation Phases

### Phase 1: Task Analysis Engine (Day 1-3)
- Create task completion analyzer
- Extract patterns: type, duration, complexity, outcome
- Store patterns in agent learning file
- Write unit tests

### Phase 2: Role-Specific Metrics (Day 3-5)
- Define metrics per role (dev, pm, cpo, cto, devops, qa)
- Create metric extraction pipeline
- Update CPO productivity calculation
- Add to agent dashboard

### Phase 3: Learning Dashboard (Day 5-7)
- Create `/settings/learnings` page
- Show per-agent learning progress
- Show cross-agent learning count
- Add filtering by role and task type

### Phase 4: Cross-Agent Sharing (Day 7-9)
- Integrate with HTTP relay (LAB-010)
- Implement learning sharing protocol
- Implement conflict resolution
- End-to-end testing

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pattern Extraction Rate | 100% | All completed tasks analyzed |
| CPO Productivity Accuracy | 95%+ | Matches manual calculation |
| Learning Dashboard Uptime | 99% | Page accessible |
| Cross-Agent Learning Count | 10+ | Shared learnings after 1 week |

---

## Dependencies

| Dependency | Status | Owner |
|------------|--------|-------|
| LAB-010 HTTP Relay | READY | Dev |
| Agent Learning Files | ✅ EXISTS | Research Lead |
| Task Completion Events | ✅ EXISTS | DevOps |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| LAB-010 delayed | Medium | High | Start Phase 1-3 independently |
| Pattern extraction noise | Medium | Medium | Use confidence thresholds |
| Learning conflicts | Low | Low | Timestamp-based resolution |

---

## Rollback Plan

If task-driven learning proves unstable:
1. Disable cross-agent sharing (keep same-agent learning)
2. Revert CPO productivity calculation to original
3. Escalate to CTO for architecture review

---

## Next Steps

1. **CTO**: Claim this task and create implementation branch
2. **CPO**: Review acceptance criteria and approve scope
3. **Research Lead**: Monitor progress, update Sprint 3 status

---

## References

- CPO Insight Report: `/docs/research/CPO-INSIGHT-REPORT-2026-03-18.md`
- LAB-004 Results: `/docs/research/SPRINT-1-RESEARCH-SUMMARY.md`
- LAB-010 Brief: `/docs/research/LAB-010-HTTP-RELAY-STANDARDIZATION-BRIEF.md`

---

**Created by:** faintech-research-lead
**Date:** 2026-03-20T09:50:00Z
**Status:** Ready for execution
