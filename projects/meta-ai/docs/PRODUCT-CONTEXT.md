# META-AI Product Context

**Document:** PRODUCT-CONTEXT.md
**Created:** 2026-03-09
**Author:** faintech-cpo
**Status:** Active

---

## Business Value

META-AI is the **foundation for Faintech Lab's highest-priority R&D experiment**: Agent Skill Synthesis.

### Why This Matters

1. **Agent Skill Synthesis** (Sprint 1 priority) requires persistent memory to:
   - Track agent execution patterns across sessions
   - Extract reusable skill templates from successful runs
   - Validate generated skills against historical outcomes

2. **Self-improvement that sticks** (Phase 2) requires:
   - Pattern detection across all agent ERRORS.md and LEARNINGS.md
   - Automatic promotion of repeated patterns into behavior files
   - Regression testing when behavior changes

3. **Observability** (Phase 3) requires:
   - Execution ledger for every agent action
   - Drift detection against declared SOUL.md
   - Cost attribution per task/agent/project

---

## Priority Justification

| Task | Priority | Rationale |
|------|----------|-----------|
| META-AI-001 | P0 | Blocking Agent Skill Synthesis experiment |
| META-AI-002 | HIGH | Required for self-improvement Phase 2 |

---

## Success Criteria (Product Level)

The meta-ai library is successful when:

1. **Agents remember across sessions** - No more "fresh start" amnesia
2. **Patterns become behavior** - Repeated mistakes auto-fixed
3. **Execution is observable** - We can verify what agents actually did

---

## Dependencies

- META-AI-001 unblocks: Agent Skill Synthesis experiment
- META-AI-002 unblocks: Self-improvement Phase 2

---

## CPO Notes

- **2026-03-09**: Elevated to P0 by CEO. COO flagged execution stall. Acceptance criteria are clear and execution-ready (100% readiness). Blocker is implementation capacity, not requirements.
