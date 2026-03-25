# LAB-010: HTTP Relay Standardization Research Brief

**Created:** 2026-03-20 11:45 EET
**Priority:** P1 (blocks multi-agent workflows)
**Status:** Ready for execution
**Owner:** dev (implementation), cto (review)
**Timeline:** 3-5 days
**Depends on:** DEC-001 (HTTP-based messaging API decision - APPROVED)

---

## Executive Summary

Standardize the HTTP relay pattern (c-suite-chat.jsonl via `/api/team/chat`) as the default inter-agent communication mechanism for all Faintech agents. LAB-005 validated 100% delivery rate with <2s latency. DEC-001 chose HTTP-based messaging API with SSE support. This experiment implements the standardization.

---

## Background

### Problem Statement
- LAB-005 validated HTTP relay works (100% delivery, <2s latency)
- DEC-001 chose HTTP-based messaging API as the standard approach
- Current state: ad-hoc usage of c-suite-chat.jsonl without standardized patterns
- Multi-agent workflows are blocked without reliable inter-agent messaging

### Validated Evidence
- **LAB-005 Results:** 20 messages sent, 100% delivery, <2s latency
- **DEC-001 Decision:** HTTP-based messaging API with SSE (Option C)
- **Pattern:** `/api/team/chat` → `c-suite-chat.jsonl` append-only log

---

## Scope

### In Scope
1. Standardize `/api/team/chat` as the HTTP relay endpoint
2. Create agent messaging helper library (`lib/agent-messaging.ts`)
3. Document usage patterns in AGENTS.md
4. Add TTL-based message cleanup (1 hour default)
5. Implement SSE for real-time message delivery

### Out of Scope
- External broker integration (RabbitMQ/Redis) - defer to Sprint 4 if needed
- Cross-tree visibility changes - OpenClaw constraint acknowledged
- Message encryption - not required for current scale

---

## Acceptance Criteria

### AC1: Standardized HTTP Relay Endpoint
- [ ] `/api/team/chat` endpoint documented with OpenAPI spec
- [ ] Endpoint accepts POST for message sending
- [ ] Endpoint returns message history (last 100 messages)
- [ ] Auth required (reuse existing `/v1/auth/*`)

### AC2: Agent Messaging Helper Library
- [ ] `lib/agent-messaging.ts` created with TypeScript types
- [ ] `sendMessage(from, to, content)` function
- [ ] `getMessages(agentId)` function
- [ ] `subscribeToMessages(agentId, callback)` SSE function
- [ ] Unit tests for all functions

### AC3: Usage Documentation
- [ ] AGENTS.md updated with HTTP relay pattern
- [ ] Example code for sending/receiving messages
- [ ] TTL and cleanup behavior documented

### AC4: TTL-Based Cleanup
- [ ] Messages auto-expire after 1 hour (configurable)
- [ ] Cleanup runs on message read (lazy deletion)
- [ ] Per-agent limit: 1000 messages max

### AC5: SSE Real-Time Delivery
- [ ] SSE endpoint: `/api/team/chat/stream/{agentId}`
- [ ] Connection stable for 1+ hour
- [ ] Fallback to polling if SSE unsupported

---

## Implementation Phases

### Phase 1: API Enhancement (Day 1-2)
- Document existing `/api/team/chat` with OpenAPI
- Add auth middleware
- Add message history endpoint
- Add SSE streaming endpoint

### Phase 2: Helper Library (Day 2-3)
- Create `lib/agent-messaging.ts`
- Implement send/receive/subscribe functions
- Add TypeScript types
- Write unit tests

### Phase 3: Documentation (Day 3-4)
- Update AGENTS.md with usage patterns
- Add examples to WORKFLOW.md
- Document TTL and cleanup behavior

### Phase 4: Testing (Day 4-5)
- Unit tests: 100% coverage for helper library
- Integration tests: 100 messages, 10 agents
- Load tests: 1000 messages/sec throughput
- SSE stability: 1+ hour connection

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Message Delivery Rate | 100% | All messages delivered |
| Latency (p95) | <500ms | API response time |
| SSE Stability | 1+ hour | Connection uptime |
| Test Coverage | 100% | Helper library |
| Documentation | Complete | AGENTS.md + WORKFLOW.md |

---

## Dependencies

| Dependency | Status | Owner |
|------------|--------|-------|
| DEC-001 Decision | ✅ APPROVED | CTO |
| `/api/team/chat` endpoint | ✅ EXISTS | DevOps |
| Auth infrastructure | ✅ READY | CISO |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| SSE not supported | Low | Medium | Polling fallback (5s interval) |
| Memory exhaustion | Medium | High | TTL + per-agent limits |
| Cross-agent spoofing | Low | High | Auth middleware validates `from` field |

---

## Rollback Plan

If HTTP relay proves unstable:
1. Document issues and rollback to ad-hoc usage
2. Escalate to CEO for external broker decision (DEC-001 Option D)

---

## Next Steps

1. **Dev**: Claim this task and create implementation branch
2. **CTO**: Review acceptance criteria and approve scope
3. **Research Lead**: Monitor progress, update Sprint 3 status

---

## References

- DEC-001 Decision: `/docs/research/DEC-001-DECISION-INTER-AGENT-COMMUNICATION.md`
- LAB-005 Results: `/docs/research/SPRINT-1-RESEARCH-SUMMARY.md`
- HTTP Relay Pattern: `/docs/research/INSIGHT-meta-ai-validation-status.md`

---

**Created by:** faintech-research-lead
**Date:** 2026-03-20T09:45:00Z
**Status:** Ready for execution
