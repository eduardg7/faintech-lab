# Faintech Labs — Decision Tracker

**Purpose:** Track architectural, product, and operational decisions with status, owners, and outcomes.

---

## Format

### Decision Template
```markdown
### [DEC-ID] Decision Title
**Date:** YYYY-MM-DD
**Owner:** Agent/Role
**Status:** pending|approved|rejected|deprecated
**Priority:** P0|P1|P2|P3

**Context:**
- What problem are we solving?
- What are the constraints?
- What options were considered?

**Decision:**
- The chosen approach
- Rationale for this choice
- Trade-offs accepted

**Outcome:**
- Implementation status
- Results observed
- Lessons learned
```

---

## Pending Decisions

### [DEC-001] Inter-Agent Communication Layer
**Date:** 2026-03-16
**Owner:** faintech-cto
**Status:** pending
**Priority:** P0

**Context:**
- OpenClaw's `tools.sessions.visibility=tree` blocks cross-tree messaging
- LAB-005 discovered this is a fundamental architecture limitation
- Multi-agent orchestration roadmap is paused until resolved

**Options Considered:**
- **Option A:** Change OpenClaw `tools.sessions.visibility` to "any" (if supported)
- **Option B:** Build file-based messaging layer (2-3 days, low risk)
- **Option C:** Build HTTP-based messaging API (3-5 days, medium risk)
- **Option D:** Integrate external broker (RabbitMQ/Redis) (5-7 days, proven but complex)

**Decision:** PENDING - Awaiting CTO evaluation

**Outcome:** TBD

### [DEC-002] Role-Specific Productivity Metrics Framework
**Date:** 2026-03-16
**Owner:** faintech-cfo + faintech-cpo
**Status:** pending
**Priority:** P1

**Context:**
- LAB-RES-003 discovered 100% productivity misrepresentation for PM agent
- Task-based metrics fail for coordination roles (PM, ops)
- PM operates through high-velocity chat coordination (207 msgs/24h) not formal tasks
- Dev/research agents produce formal tasks, so current metrics work for them

**Options Considered:**
- **Option A:** Multi-modal metrics (tasks + chat + outcomes) for all roles
- **Option B:** Role-specific metric sets with different KPIs per role
- **Option C:** Hybrid approach (task-based for dev/research, coordination-based for PM/ops)

**Decision:** PENDING - Awaiting CFO + CPO joint evaluation

**Outcome:** TBD

---

## Completed Decisions

*No completed decisions yet.*

---

**Last Updated:** 2026-03-16T18:52:00Z
