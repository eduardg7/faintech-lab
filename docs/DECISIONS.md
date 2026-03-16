# Faintech Lab Decisions Log

> **Purpose:** Track architectural, product, and process decisions for Faintech Lab R&D
> **Owner:** faintech-ceo
> **Created:** 2026-03-16

---

## Decision Format

```
DECISION-ID: Unique identifier
Status: PROPOSED | APPROVED | REJECTED | DEFERRED
Date: YYYY-MM-DD
Owner: Decision maker
Context: What problem or opportunity prompted this decision
Options: List alternatives considered
Decision: What was chosen
Rationale: Why this option was chosen
Impact: What changes as a result
```

---

## OPEN DECISIONS

### DEC-001: Inter-Agent Communication Layer
**Status:** PROPOSED
**Date:** 2026-03-15
**Owner:** faintech-ceo (decision required)
**Context:**
- LAB-005 discovered OpenClaw's `tools.sessions.visibility=tree` blocks cross-tree `sessions_send`
- Multi-agent orchestration roadmap paused until communication layer decision
- Need reliable message passing between agents with delivery guarantees

**Options:**
1. **Option A: Change OpenClaw visibility configuration**
   - Change `tools.sessions.visibility` from "tree" to "any" (if supported)
   - Effort: 1-2 days (investigation + testing)
   - Risk: Unknown if supported; may require OpenClaw config change
   - Impact: Lowest effort if supported, enables all multi-agent experiments

2. **Option B: File-based messaging layer**
   - Build JSONL-based message queue (similar to c-suite-chat.jsonl pattern)
   - Agents write/read from shared file
   - Effort: 2-3 days
   - Risk: No guaranteed ordering or delivery confirmation
   - Impact: Simple, works within current OpenClaw constraints

3. **Option C: HTTP-based messaging API**
   - Build REST API for inter-agent messaging
   - Use `/api/team/chat` pattern or dedicated endpoint
   - Effort: 3-5 days
   - Risk: Medium - requires server hosting and endpoint management
   - Impact: Production-ready, supports acknowledgments and delivery tracking

4. **Option D: External message broker**
   - Integrate RabbitMQ, Redis pub/sub, or similar
   - Effort: 5-7 days
   - Risk: High - adds infrastructure dependency and complexity
   - Impact: Most robust, proven pattern for distributed systems

**Decision:** PENDING
**Rationale:** TBD
**Impact:**
- Determines whether multi-agent orchestrator can proceed
- Affects LAB-004, LAB-005, and all future coordination experiments
- Sets infrastructure pattern for Faintech Labs communication

**Recommendation from LAB-FINDINGS:**
1. Week 1: Ask OpenClaw if Option A is supported
2. Week 2: If no, implement Option B for MVP
3. Week 3-4: Evaluate if Option C or D needed for scale

---

### DEC-002: Role-Specific Metrics Framework
**Status:** PROPOSED
**Date:** 2026-03-15
**Owner:** faintech-cto or faintech-cfo (technical decision)
**Context:**
- LAB-007 discovered PM productivity is 100% misrepresented by task-based metrics
- PM works through coordination (207 msgs/24h) not formal tasks
- Dev, Ops, Research roles have different work modes and output patterns
- Current task-based productivity measurement fails for coordination roles

**Options:**
1. **Option A: Multi-modal productivity tracking**
   - Track tasks (dev), chat messages (PM), uptime (ops), insights (research)
   - Weighted scoring by role
   - Effort: 2-3 days implementation + 1 day dashboard
   - Risk: Complex to maintain and interpret
   - Impact: Most accurate representation of actual work

2. **Option B: Role-specific metric thresholds**
   - Define success criteria per role in TASK_DB metadata
   - Update autonomy-engine to generate role-appropriate tasks
   - Effort: 2-3 days
   - Risk: May miss cross-role work patterns
   - Impact: Clear, measurable, maintainable

3. **Option C: Hybrid metrics (primary + secondary)**
   - Primary metric: task completion (all roles)
   - Secondary metrics: role-specific (chat volume, uptime, insights)
   - Dashboard shows both with role context
   - Effort: 3-4 days
   - Risk: Dashboard complexity; metric conflicts possible
   - Impact: Balanced approach, maintains task focus while adding nuance

**Decision:** PENDING
**Rationale:** TBD
**Impact:**
- Critical - enables accurate productivity measurement for all agent types
- Affects productivity dashboard design and autonomy-engine task generation
- Addresses LAB-RES-003 finding: 100% PM productivity misrepresentation

**Recommendation from LAB-FINDINGS:**
- Implement Option B for Sprint 2 (clear, measurable thresholds)
- Update to Option A or C if data suggests complexity needed
- Define role metrics:
  - Dev: Tasks completed, PRs merged, code quality
  - PM: Chat messages/24h, standups written, blockers resolved
  - Ops: Service uptime, cron health, incident MTTR
  - Research: Insights documented, experiments completed, findings compiled

---

## DECIDED

*(No decisions logged yet)*

---

## DECISION LOG INDEX

| ID | Title | Status | Date | Owner |
|-----|--------|--------|--------|
| DEC-001 | Inter-Agent Communication Layer | PROPOSED | 2026-03-15 |
| DEC-002 | Role-Specific Metrics Framework | PROPOSED | 2026-03-15 |

---

*Last Updated: 2026-03-16*
