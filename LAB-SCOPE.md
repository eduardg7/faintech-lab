# Faintech Lab Scope — Sprint 1

**Version:** 1.0
**Owner:** CEO
**Created:** 2026-03-15
**Status:** Active

---

## Goal

Faintech Lab is the R&D workspace for Faintech Solutions SRL. Its mission is to **de-risk future company bets** by validating or invalidating hypotheses quickly, before committing engineering resources to full production builds.

In Sprint 1, we focus on two parallel tracks:
1. **meta-ai** — Build reusable infrastructure that makes AI agents smarter, more autonomous, and more persistent.
2. **new-product** — Identify a customer-facing product that leverages the meta-ai infrastructure.

---

## What We Test

### Track 1: meta-ai (Agent Infrastructure)

We test whether our agent infrastructure can achieve:
- **Persistent memory**: Agents remember context across sessions without manual prompting
- **Self-improvement loops**: Agents update their own behavior based on learnings (not just log them)
- **Inter-agent communication**: Reliable message passing between agents with delivery guarantees
- **Observability**: Clear visibility into what each agent is doing, why, and whether it worked

### Track 2: new-product (Customer Product)

We test whether we can identify a product-market fit for non-technical teams that need:
- Automated workflow orchestration
- Persistent knowledge management
- Multi-agent collaboration for complex tasks

---

## Success Criteria

### Sprint 1 Success (meta-ai)
- [ ] At least one agent demonstrates persistent memory across 3+ sessions
- [ ] Self-improvement loop produces at least 2 verified behavior changes
- [ ] Inter-agent messaging achieves 100% delivery rate in tests
- [ ] Observability dashboard shows real-time agent status for all active agents

### Sprint 1 Success (new-product)
- [ ] Problem space documented with at least 3 potential customer segments
- [ ] At least 1 hypothesis about customer needs validated or invalidated
- [ ] Initial MVP scope defined with clear success metrics

---

## Experiments (Sprint 1)

### LAB-003: Persistent Agent Memory Validation
**Hypothesis:** File-based structured memory (MEMORY.md + daily notes) enables agents to maintain context across sessions with >80% accuracy on follow-up questions.

**Test:** Ask the same agent questions across 3 sessions about information shared in session 1. Measure recall accuracy.

**Success:** ≥80% recall on factual information, ≥60% on contextual nuance.

### LAB-004: Self-Improvement Loop Effectiveness
**Hypothesis:** Agents can update their own behavior (AGENTS.md, SOUL.md) based on logged learnings without human intervention.

**Test:** Log 3 specific behavior corrections in .learnings/LEARNINGS.md. Check if agent applies them in subsequent sessions.

**Success:** At least 2 of 3 corrections applied without explicit instruction.

### LAB-005: Inter-Agent Messaging Reliability
**Hypothesis:** OpenClaw sessions_send/sessions_spawn tools achieve 100% message delivery between agents.

**Test:** Spawn 2 agents, send 10 messages each direction, verify all received and processed.

**Success:** 100% delivery, 0% message loss, <5s latency.

---

## Non-Goals (Sprint 1)

- Building production-ready features (use faintech-os for that)
- Customer interviews or external validation (defer to Sprint 2)
- Complex multi-agent orchestration (validate basics first)
- Revenue or monetization models (premature)

---

## Governance

- **Task DB:** `/Users/eduardgridan/faintech-os/data/ops/TASK_DB.json`
- **Weekly review:** Friday retro includes lab experiment results
- **Decision log:** All hypothesis validations recorded in `docs/research/`
- **Kill criteria:** Any experiment with 2 consecutive failures gets archived

---

## Next Steps

1. CEO approves this scope → SESSION-STATE.md
2. PM creates LAB-003, LAB-004, LAB-005 tasks in TASK_DB
3. DevOps sets up faintech-lab dev environment (LAB-002)
4. Research agent leads experiment execution

---

*This document is a living scope. Update as hypotheses are validated or invalidated.*
