# LAB-006: Global Memory Access Pattern Validation

**Status:** todo
**Priority:** P1
**Sprint:** sprint-2
**Track:** meta-ai
**Owner:** research
**Project:** faintech-lab

## Hypothesis

A standardized global memory access pattern enables agents to read context from other agents' memory files, solving the cross-agent handoff gap identified in LAB-003.

## Background

LAB-003 Session 3 revealed that `memory_search` only searches the requesting agent's memory files, not other agents' files. This created a coordination gap where context didn't transfer between agents.

## Test Method

Create and validate a global memory access pattern:

1. Define a shared memory directory structure (e.g., `memory/shared/` or direct cross-agent file reads)
2. Implement a `read_agent_memory()` utility function that can read any agent's MEMORY.md and daily notes
3. Test cross-agent context handoff using the new pattern
4. Measure accuracy compared to LAB-003 Session 3 (41.7% baseline)

## Acceptance Criteria

- Global memory utility function implemented in `/Users/eduardgridan/.openclaw/agents/ops/lib/memory-utils.ts`
- Cross-agent handoff test achieves ≥80% accuracy (compared to 41.7% baseline)
- Documentation explains how to use global memory access pattern
- Evidence: Test results documented in `docs/research/LAB-006-results.md`

## Success Criteria

≥80% cross-agent context recall using global memory pattern.

## Risk

Direct file reads may violate agent isolation principles. Consider explicit opt-in or memory sharing agreements.

## Timeline

- Est. effort: 4-6 hours
- Dependency: None
