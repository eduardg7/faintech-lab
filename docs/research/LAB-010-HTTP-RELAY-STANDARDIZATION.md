# LAB-010: HTTP Relay Standardization for Inter-Agent Communication

**Status:** PROPOSED
**Track:** meta-ai
**Owner:** ciso (proposed) → dev (implementation)
**Priority:** P1 (blocks Sprint 3 multi-agent workflows)
**Estimated Duration:** 3-5 days

---

## Context

### Problem Statement
Following DEC-001 approval for HTTP-based messaging API (Option C), Faintech lacks a standardized protocol for reliable inter-agent communication. LAB-005 validated HTTP relay feasibility but revealed coordination gaps:

1. **Lane Mapping Issue:** Messages routed incorrectly between agent lanes (dev vs research vs ops)
2. **Delivery Acknowledgement:** No confirmation mechanism for message delivery
3. **Message Persistence:** Messages lost if recipient agent is offline
4. **Error Recovery:** No retry logic for failed deliveries
5. **Observability Gap:** No centralized logging of inter-agent messages

### Constraints
- **Timeline:** Sprint 3 starts Mar 19, 2026 (1 day)
- **Integration:** Must work with existing OpenClaw HTTP capabilities
- **Infrastructure:** No external brokers (RabbitMQ/Redis deferred to Sprint 4)
- **Observability:** Must integrate with LAB-007 execution ledger
- **Security:** Must validate sender identity and enforce least-privilege message routing

### Success Criteria
| # | Criterion | Target | Measurement |
|---|-----------|---------|-------------|
| 1 | Message delivery reliability | ≥99% | Success rate over 100 test messages |
| 2 | Lane mapping accuracy | 100% | No misrouted messages in tests |
| 3 | Delivery acknowledgement | <500ms average latency | End-to-end acknowledgment time |
| 4 | Offline agent persistence | 100% | Messages queued until agent comes online |
| 5 | Observability coverage | 100% | All messages logged to EXECUTION_LEDGER.jsonl |
| 6 | Security validation | 100% | All senders authenticated, lane access enforced |
| 7 | Retry success rate | ≥95% | Failed deliveries recover within 3 retries |

---

## Experiment Design

### Phase 1: Protocol Design (Day 1)
**Deliverable:** `/Users/eduardgridan/faintech-lab/docs/research/HTTP-RELAY-PROTOCOL.md`

#### Message Schema
```typescript
interface InterAgentMessage {
  id: string;                    // UUID v4
  timestamp: string;               // ISO 8601
  sender_agent_id: string;         // From AGENT.md identity
  recipient_agent_id: string;      // Target agent ID
  recipient_lane: string;          // dev, research, ops, etc.
  message_type: "task_handoff" | "request" | "response" | "notification";
  payload: Record<string, unknown>; // Encrypted JSON payload
  priority: "low" | "normal" | "high";
  requires_ack: boolean;          // Delivery acknowledgement required
  expires_at?: string;            // ISO 8601, optional TTL
  signature: string;              // HMAC-SHA256 for authenticity
}
```

#### API Endpoints
```
POST   /v1/relay/send              // Send message to agent
POST   /v1/relay/broadcast         // Broadcast to lane
GET    /v1/relay/inbox             // Retrieve inbox for agent
GET    /v1/relay/message/:id       // Get specific message
POST   /v1/relay/ack/:id          // Acknowledge message receipt
DELETE /v1/relay/message/:id       // Delete processed message
POST   /v1/relay/health           // Relay service health check
```

#### Lane Mapping Table
| Agent Role        | Lane       | Priority |
|------------------|------------|----------|
| ceo, cto, coo   | c-suite    | 1 |
| dev, qa, devops  | dev        | 2 |
| research, cfo    | research   | 2 |
| ops, pm          | ops        | 3 |
| marketing, sales | growth     | 4 |

### Phase 2: Implementation (Days 2-3)
**Deliverable:** `/Users/eduardgridan/faintech-lab/projects/meta-ai/src/relay/`

#### Components
1. **HTTP Relay Server** (`relay_server.ts`)
   - Express.js server with `/v1/relay/*` endpoints
   - Message queue with in-memory persistence (SQLite upgrade Sprint 4)
   - Retry logic with exponential backoff (1s, 2s, 4s)
   - Lane mapping enforcement

2. **Message Queue Manager** (`queue_manager.ts`)
   - FIFO queue per agent lane
   - Offline agent detection (heartbeat monitoring)
   - Message expiration handling
   - Delivery acknowledgment tracking

3. **Security Layer** (`relay_security.ts`)
   - Sender authentication (JWT validation against agent identity)
   - Lane access control (ACL: who can send to which lanes)
   - Message signature verification (HMAC-SHA256)
   - Rate limiting per agent (100 messages/min)

4. **Observability Integration** (`relay_ledger.ts`)
   - Emit all relay events to EXECUTION_LEDGER.jsonl
   - Event types: `relay_send`, `relay_deliver`, `relay_ack`, `relay_fail`, `relay_retry`
   - Metrics: delivery latency, retry count, queue depth

### Phase 3: Testing (Day 4)
**Deliverable:** `/Users/eduardgridan/faintech-lab/docs/research/LAB-010-results.md`

#### Test Suite
```typescript
// test/relay_test_suite.ts
describe('HTTP Relay Standardization', () => {
  test('TC1: Basic message delivery', async () => {
    // Send message from dev to research
    // Verify receipt <500ms
    // Verify acknowledgment sent
  });

  test('TC2: Lane mapping accuracy', async () => {
    // Send to c-suite, dev, research, ops, growth lanes
    // Verify correct routing 100%
  });

  test('TC3: Offline agent persistence', async () => {
    // Stop recipient agent
    // Send 10 messages
    // Verify messages queued
    // Start recipient, verify all 10 delivered
  });

  test('TC4: Retry logic', async () => {
    // Simulate network failure
    // Verify 3 retries with exponential backoff
    // Verify recovery ≥95% success
  });

  test('TC5: Message expiration', async () => {
    // Send message with TTL=1s
    // Verify expired message not delivered
  });

  test('TC6: Security validation', async () => {
    // Attempt message without signature
    // Verify rejected (401 Unauthorized)
    // Attempt lane violation (dev → c-suite without auth)
    // Verify rejected (403 Forbidden)
  });

  test('TC7: High-volume stress test', async () => {
    // Send 100 messages across all lanes
    // Verify ≥99% delivery rate
    // Verify no queue overflow
  });
});
```

#### Success Metrics Collection
```bash
# Run test suite
npm run test:relay

# Generate metrics report
npm run report:relay-metrics

# Expected output:
{
  "total_tests": 7,
  "passed": 7,
  "failed": 0,
  "delivery_rate": 99.5,
  "lane_accuracy": 100,
  "avg_ack_latency_ms": 342,
  "retry_success_rate": 96.7,
  "offline_persistence": 100,
  "security_validation": 100
}
```

### Phase 4: Integration (Day 5)
**Deliverable:** `/Users/eduardgridan/faintech-lab/docs/research/LAB-010-INTEGRATION-GUIDE.md`

#### Agent Integration Checklist
- [ ] Add `send_message()` utility to each agent's TOOLKIT.md
- [ ] Configure relay base URL in agent SESSION-STATE.md
- [ ] Test inter-agent handoff (dev → research)
- [ ] Test lane broadcast (c-suite → all lanes)
- [ ] Verify ledger integration (messages logged to EXECUTION_LEDGER.jsonl)
- [ ] Update LAB-006 cross-agent handoff test to use HTTP relay

---

## Security Considerations

### Threat Model
1. **Message Spoofing:** Attacker impersonates agent
   - **Mitigation:** HMAC-SHA256 signature verification

2. **Lane Privilege Escalation:** Dev agent sends to c-suite lane
   - **Mitigation:** ACL enforcement in `relay_security.ts`

3. **Message Replay:** Attacker resends old message
   - **Mitigation:** Message ID uniqueness check (deduplication)

4. **Denial of Service:** Agent floods relay with messages
   - **Mitigation:** Rate limiting (100 messages/min per agent)

5. **Man-in-the-Middle:** Attacker intercepts messages
   - **Mitigation:** TLS for all relay endpoints (HTTPS only)

### Security Acceptance Criteria
| # | Control | Verification Method |
|---|---------|---------------------|
| 1 | All messages signed | Verify HMAC-SHA256 signature in test suite |
| 2 | Lane ACL enforced | Attempt cross-lane violations, verify 403 |
| 3 | Rate limiting active | Send 101 messages/min, verify throttling |
| 4 | TLS enabled | Verify all endpoints use HTTPS |
| 5 | Message deduplication | Send duplicate message IDs, verify rejected |

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **In-memory queue lost on crash** | Medium | High | Document SQLite upgrade path for Sprint 4 |
| **Race conditions in delivery** | Low | Medium | Use atomic operations, add integration test |
| **Performance bottleneck** | Low | Medium | Load test with 1000 messages/sec baseline |
| **Lane mapping complexity grows** | Medium | Low | Use config file, document schema evolution |
| **Observability overhead** | Low | Low | Batch ledger writes, async logging |

---

## Dependencies

### Blocked By
- **DEC-001:** ✅ APPROVED (HTTP-based messaging API selected)

### Blocks
- **LAB-006:** Cross-agent handoff test (can use standardized relay)
- **LAB-011:** Multi-agent workflow orchestration
- **Sprint 3:** Multi-agent coordination experiments

### External Dependencies
- **OpenClaw HTTP capabilities:** ✅ Verified (LAB-005)
- **Express.js runtime:** ✅ Already in faintech-lab
- **SQLite (optional):** Deferred to Sprint 4

---

## Success Definition

### Minimum Viable Experiment
- All 7 test cases pass
- Delivery rate ≥95% (stretch goal: ≥99%)
- Security controls validated

### Production Readiness
- Documentation complete (protocol + integration guide)
- Agent integration checklist ≥80% complete
- Observability integration verified
- Performance benchmark documented

---

## Next Actions

| # | Action | Owner | Due |
|---|--------|-------|-----|
| 1 | Review and approve LAB-010 scope | cto | Mar 18 |
| 2 | Implement HTTP relay server | dev | Mar 20 |
| 3 | Execute test suite | qa | Mar 21 |
| 4 | Integrate with agent sessions | ciso | Mar 22 |
| 5 | Update LAB-006 test to use relay | research | Mar 22 |
| 6 | Document results and recommendations | ciso | Mar 23 |

---

**Proposed By:** CISO
**Date:** 2026-03-18
**Review Required:** CTO (technical feasibility), QA (test coverage), DevOps (infrastructure)
