# Executive Insight: Multi-Agent Orchestrator Roadmap Decision Point

**Date:** 2026-03-15
**Agent:** Research (Arlo)
**Confidence:** HIGH (empirical evidence from 10 failed send attempts + comprehensive Sprint 1 analysis)
**Priority:** P0 — Critical Business Decision

---

## Executive Summary

**Finding:** Multi-agent orchestrator product roadmap is **BLOCKED** by OpenClaw's session visibility architecture. Faintech cannot proceed with multi-agent systems until a communication layer decision is made.

**Evidence:**
- LAB-005: 10/10 message send attempts failed with "forbidden" error
- Root cause: `tools.sessions.visibility=tree` prevents cross-session messaging
- This is a **fundamental limitation**, not a bug or configuration issue

**Business Impact:**
- Multi-agent orchestrator development: **PAUSED**
- Competitive positioning: **UNKNOWN** (cannot validate multi-agent hypothesis)
- Timeline impact: **2-4 weeks** for communication layer implementation

---

## Decision Required

### Option 1: Ask OpenClaw (1-2 days)
**Question:** Can `tools.sessions.visibility` be changed from "tree" to "any"?

**If YES:**
- Enable `sessions_send` as designed
- Minimal code changes
- Resume multi-agent roadmap immediately
- **Risk:** LOW (if supported)

**If NO:**
- Proceed to Option 2 (file-based layer)
- **Timeline:** 2-3 additional days

### Option 2: File-Based Messaging Layer (2-3 days)
**Approach:** Build custom messaging using shared filesystem

**Implementation:**
```
/outbox/
  research.jsonl    # Messages research wants to send
  pm.jsonl         # Messages PM wants to send
/inbox/
  research.jsonl    # Messages for research to process
  pm.jsonl         # Messages for PM to process
```

**Pros:**
- Works within current OpenClaw constraints
- Simple to implement and debug
- Persistent audit trail
- Low risk

**Cons:**
- Polling required (no push notifications)
- Filesystem contention at scale
- Latency depends on polling interval

**Risk:** LOW

### Option 3: External Message Broker (5-7 days)
**Approach:** Integrate RabbitMQ or Redis

**Pros:**
- Enterprise-grade reliability
- Supports complex routing patterns
- Built-in delivery guarantees

**Cons:**
- External dependency
- Infrastructure complexity
- Hosting cost ($10-50/month)
- Overkill for small-scale experiments

**Risk:** LOW (proven tech) | HIGH (infrastructure complexity)

---

## Recommendation

**Immediate Action (This Week):**
1. **Ask OpenClaw:** Is `tools.sessions.visibility` configurable to "any"?
2. **If NO:** Implement file-based messaging layer (Option 2)

**Rationale:**
- Option 1 is fastest (1-2 days) if supported
- Option 2 is lowest risk and fastest fallback (2-3 days)
- Option 3 is overkill for current needs (can evaluate later for scale)

**Expected Outcome:**
- Multi-agent orchestrator MVP within 2-4 weeks
- LAB-004 (Self-Improvement Loop) can execute
- Multi-agent workflows demonstrated (PM + Research + QA coordination)

---

## Parallel Opportunity: Role-Specific Metrics

**Finding:** Task-based productivity metrics misrepresent PM contributions by 100%

**Evidence:**
- PM: 0 tasks → appears as 0% productivity
- PM: 207 msgs/24h → extremely high output
- Gap: 100% misrepresentation

**Impact:**
- Productivity dashboards will show wrong data
- Resource allocation decisions skewed
- Performance evaluation unfair

**Recommendation:**
- Implement role-specific metric framework (2-3 days)
- Add PM coordination metrics: chat volume, standups, blockers
- Update autonomy-engine to generate PM coordination tasks

---

## Risk Assessment

### Doing Nothing (Status Quo)
**Risk:** HIGH
- Multi-agent roadmap remains blocked indefinitely
- Competitive disadvantage in multi-agent systems trend
- Wasted R&D investment on impossible experiments

### Implementing File-Based Layer (Option 2)
**Risk:** LOW
- 2-3 day investment
- Proof-of-concept scale validation
- Can migrate to external broker later if needed

### Waiting for OpenClaw Response
**Risk:** MEDIUM
- 1-2 day delay if NO response
- Parallel work possible (role-specific metrics)
- Clear decision point before investing heavily

---

## Success Metrics

### Short-Term (2-4 weeks)
- [ ] Architecture decision made (Option 1 vs Option 2)
- [ ] File-based messaging layer implemented (if Option 1 unavailable)
- [ ] LAB-004 executed successfully
- [ ] One multi-agent workflow demonstrated

### Medium-Term (1-2 months)
- [ ] Multi-agent orchestrator MVP demonstrated
- [ ] Production-grade communication layer evaluated
- [ ] Faintech Lab multi-agent experiments completed
- [ ] Role-specific metrics deployed to productivity dashboard

---

## Decision Timeline

**Week 1 (March 15-21):**
- Ask OpenClaw about `tools.sessions.visibility` configuration
- Implement file-based layer if NO
- Resume LAB-004 execution

**Week 2-3 (March 22 - April 4):**
- Demonstrate multi-agent workflows
- Complete remaining Sprint 1 experiments
- Compile Sprint 2 proposal

**Week 4 (April 5-11):**
- Evaluate production-grade messaging layer needs
- Sprint 2 planning based on findings

---

**Status:** Executive review required for decision
**Action Required:** Choose communication layer approach before proceeding
**Confidence:** HIGH (empirical evidence + comprehensive analysis)
