# DEC-001 Decision: Inter-Agent Communication Layer

**Decision Date:** 2026-03-18
**Decision Owner:** CTO
**Priority:** P0 (Blocks LAB-005 coordination, multi-agent orchestration)
**Status:** ✅ DECISION MADE

---

## Executive Summary

**Decision:** Implement Option C — HTTP-based messaging API with SSE support for real-time updates

**Rationale:** HTTP-based messaging provides the best balance of feasibility (uses existing OpenClaw HTTP capabilities), architectural fit (REST APIs already in use), risk (medium vs high for external broker), and functionality (real-time via SSE, industry-standard patterns).

**Timeline:** 4 days implementation → 1 day testing → Total 5 days

---

## Options Evaluation

### Option A: Change `tools.sessions.visibility` to "any"
**Time:** 1 day
**Risk:** Low
**Status:** ❌ NOT FEASIBLE

**Analysis:**
- OpenClaw session visibility controls security boundaries
- Changing to "any" may expose private agent sessions
- Not documented as supported configuration
- Would require testing and security review

**Pros:**
- Zero code changes
- Immediate fix

**Cons:**
- Security risk (cross-agent session access)
- May not be supported by OpenClaw
- Bypasses OpenClaw's access controls
- Hard to validate without documentation

**Verdict:** High security risk, not documented. Escalate to CEO if this path is desired.

---

### Option B: File-based messaging layer
**Time:** 2-3 days
**Risk:** Low
**Status:** ❌ NOT RECOMMENDED

**Analysis:**
- Agents write messages to shared directory (e.g., `/tmp/faintech-messages/`)
- Polling required to detect new messages
- Simple implementation but poor user experience

**Pros:**
- Low risk (filesystem operations are well-understood)
- Simple implementation
- No infrastructure dependencies

**Cons:**
- Polling overhead (agents must repeatedly check for messages)
- No real-time guarantees
- Concurrency issues (multiple agents reading same file)
- File locking complexity
- Poor scalability (many agents = many files)
- Not industry-standard for agent orchestration

**Verdict:** Too primitive for production-grade orchestration. Acceptable only as fallback.

---

### Option C: HTTP-based messaging API
**Time:** 3-5 days
**Risk:** Medium
**Status:** ✅ CHOSEN

**Analysis:**
- Implement REST API for message passing (`/v1/agent-messages/{from}/{to}`)
- Use SSE (Server-Sent Events) for real-time updates
- Agents push messages via HTTP POST, receive via SSE or polling
- Fits existing Faintech architecture (REST APIs already used in faintech-lab)

**Pros:**
- Uses existing OpenClaw HTTP capabilities
- Industry-standard pattern (REST + SSE)
- Real-time possible via SSE
- No additional infrastructure
- Scales to many agents
- Easy to debug (HTTP logs)
- Auth can reuse existing `/v1/auth/*` infrastructure

**Cons:**
- Medium implementation complexity (3-5 days)
- Requires HTTP server management (but OpenClaw handles this)
- SSE fallback to polling for broader compatibility

**Verdict:** Best balance of feasibility, risk, and functionality. Recommended.

---

### Option D: External broker (RabbitMQ/Redis)
**Time:** 5-7 days
**Risk:** High (infrastructure complexity)
**Status:** ❌ NOT RECOMMENDED (defer to Sprint 4 if needed)

**Analysis:**
- Deploy message broker (RabbitMQ or Redis Pub/Sub)
- Agents connect via client libraries
- Proven pattern for distributed systems
- Highest reliability and scalability

**Pros:**
- Proven, battle-tested pattern
- Excellent reliability guarantees
- Scales to thousands of agents
- Rich feature set (routing, filtering, persistence)

**Cons:**
- High implementation complexity (5-7 days)
- Adds infrastructure dependency (must run broker process)
- Adds operations overhead (monitoring, scaling, backups)
- Overkill for current scale (10-20 agents)
- Adds attack surface (broker must be secured)
- Not aligned with Faintech's "run on existing hardware" philosophy

**Verdict:** Overkill for current scale. Defer to Sprint 4 if HTTP-based proves insufficient.

---

## Decision Matrix

| Criterion | Option A | Option B | Option C | Option D |
|-----------|-----------|-----------|-----------|-----------|
| **Implementation Time** | 1 day | 2-3 days | 3-5 days | 5-7 days |
| **Risk Level** | High (security) | Low | Medium | High (complexity) |
| **Real-Time** | Yes | No (polling) | Yes (SSE) | Yes |
| **Scalability** | Limited | Poor | Good | Excellent |
| **Infrastructure** | None | None | Existing | New (broker) |
| **Industry Standard** | No | No | Yes | Yes |
| **Security** | ⚠️ Bypasses controls | ✅ File permissions | ✅ Auth reuse | ✅ Broker auth |
| **Debuggability** | ✅ HTTP logs | ⚠️ File I/O | ✅ HTTP logs | ⚠️ Broker logs |
| **Fit with Faintech** | ⚠️ Risky | ⚠️ Primitive | ✅ Fits architecture | ❌ Overkill |

**Score:** Option C wins (6/7 optimal criteria)

---

## Implementation Plan (Option C)

### Phase 1: API Design (Day 1)
**Tasks:**
- [x] Define message schema (JSON: `{id, from, to, content, timestamp, type}`)
- [x] Define endpoint structure
- [x] Document API specification

**Endpoints:**
```
POST   /v1/agent-messages                    # Send message
GET    /v1/agent-messages/{agent_id}          # Receive messages (SSE)
GET    /v1/agent-messages/{agent_id}/history # Get message history
DELETE  /v1/agent-messages/{message_id}       # Clean up messages
```

**Message Schema:**
```json
{
  "id": "msg-20260318-001",
  "from": "faintech-frontend",
  "to": "faintech-backend",
  "content": {
    "type": "coordination",
    "data": { ... }
  },
  "timestamp": "2026-03-18T12:40:00Z",
  "ttl": 3600
}
```

### Phase 2: Implementation (Days 2-3)
**Tasks:**
- [ ] Implement message storage (in-memory or SQLite)
- [ ] Implement POST endpoint (message sending)
- [ ] Implement SSE endpoint (real-time receive)
- [ ] Implement history endpoint (batch retrieval)
- [ ] Implement cleanup endpoint (TTL-based deletion)
- [ ] Add authentication middleware (reuse `/v1/auth/*`)

**Tech Stack:**
- Existing faintech-lab backend (TypeScript, Express)
- In-memory message store (fast, simple) or SQLite (persistent)
- SSE for real-time (standard web API)

### Phase 3: Integration (Days 4)
**Tasks:**
- [ ] Update LAB-005 coordination workflow to use HTTP messaging
- [ ] Create agent messaging helper library (`lib/agent-messaging.ts`)
- [ ] Update docs for inter-agent communication

### Phase 4: Testing (Day 5)
**Tasks:**
- [ ] Unit tests for message passing (send, receive, history)
- [ ] Integration tests for SSE connection
- [ ] Load tests (100 concurrent agents, 1000 messages/sec)
- [ ] Security tests (auth, cross-agent message access)
- [ ] Validate LAB-005 coordination works end-to-end

---

## Success Criteria

**Functional:**
- [ ] Agent A can send message to Agent B via HTTP POST
- [ ] Agent B receives message via SSE within 500ms
- [ ] Message history retrievable (last 100 messages)
- [ ] Messages auto-expire after TTL (1 hour default)
- [ ] Auth required for all endpoints (reuse `/v1/auth/*`)
- [ ] LAB-005 coordination workflow works with HTTP messaging

**Non-Functional:**
- [ ] SSE connection stable for 1+ hour
- [ ] 100 concurrent agents supported without degradation
- [ ] 1000 messages/sec throughput achievable
- [ ] <5% message loss rate
- [ ] <100ms API response time (p95)

---

## Risk Mitigation

### Risk 1: SSE Not Supported in OpenClaw
**Impact:** No real-time, must fall back to polling
**Probability:** Low (SSE is standard web API)
**Mitigation:**
- Test SSE support first (Day 1)
- If unsupported, implement polling fallback (5-second interval)

### Risk 2: Message Store Memory Exhaustion
**Impact:** Service crashes if too many messages buffered
**Probability:** Medium (in-memory store)
**Mitigation:**
- Enforce TTL (1 hour default, 24 hour max)
- Enforce per-agent limits (1000 messages max)
- Monitor memory usage (add LAB-007 metric for message store size)

### Risk 3: Cross-Agent Message Spoofing
**Impact:** Agent pretends to be another agent
**Probability:** Low (auth required)
**Mitigation:**
- Auth middleware enforces `from` field matches authenticated agent
- Validate `to` field is valid agent ID
- Audit log all message passing

---

## Rollback Plan

If HTTP-based messaging proves unstable or unusable:

1. **Immediate Fallback (Day 3):** Implement Option B (file-based) as backup
2. **If Both Fail:** Escalate to CEO for external solution (Option D or cloud broker)
3. **Time Budget:** 2 days for fallback + 1 day for escalation

---

## Next Steps

**Immediate (Today - Mar 18):**
1. Document this decision in DECISION-TRACKER.md
2. Update experiment backlog with DEC-001 status
3. Begin Phase 1 implementation (API design complete, move to Phase 2)

**Week of Mar 18-22:**
4. Complete Phase 2 implementation (Days 2-3)
5. Complete Phase 3 integration (Day 4)
6. Complete Phase 4 testing (Day 5)
7. Hand off to QA for regression testing

**Mar 23:**
8. DEC-001 marked as complete
9. LAB-005 coordination gap resolved
10. LAB-010 HTTP Relay unblocked (can use same messaging infrastructure)

---

## Decision Owner Signoff

**CTO:** Faintech CTO
**Date:** 2026-03-18T12:40:00Z
**Status:** ✅ APPROVED FOR IMPLEMENTATION

**CEO Review:** Pending (required for security decision on Option A if future escalation needed)

---

**Document Path:** `/Users/eduardgridan/faintech-lab/docs/research/DEC-001-DECISION-INTER-AGENT-COMMUNICATION.md`
**Task Reference:** DEC-001-EVAL (from EXPERIMENT-BACKLOG-PRIORITIZATION-2026-03-18.md)
