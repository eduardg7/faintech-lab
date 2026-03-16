# LAB-005 Critical Finding: Inter-Agent Messaging Visibility Limitation

**Date:** 2026-03-15T10:22:00Z
**Experiment:** LAB-005 (Inter-Agent Messaging Reliability)
**Finding:** CRITICAL BLOCKER

## The Problem

OpenClaw's `tools.sessions.visibility=tree` configuration prevents `sessions_send` from delivering messages to subagents outside the current session tree.

### Evidence

1. **Attempted to spawn receiver agent:**
   ```
   sessions_spawn with mode="session", thread=true
   Result: childSessionKey = "agent:research:subagent:728cba54-f281-4461-b260-1d22aa63f52b"
   ```

2. **Attempted to send 10 test messages:**
   ```
   sessions_send to childSessionKey
   Result: 10/10 attempts failed
   Error: "Session send visibility is restricted to current session tree (tools.sessions.visibility=tree)."
   ```

3. **Root Cause:**
   - The spawned subagent is NOT in the research agent's session tree
   - Therefore, all `sessions_send` attempts are rejected as "forbidden"

## Implications

### For LAB-005
- **Current approach INVALID:** Cannot test inter-agent messaging using `sessions_send` to spawned subagents
- **Test cannot proceed:** Baseline, bidirectional, burst, and stress tests all require cross-session messaging
- **Result:** LAB-005 cannot be completed as originally designed

### For Multi-Agent Orchestration
- **Fundamental limitation:** OpenClaw agents cannot directly communicate via `sessions_send` unless they share a session tree
- **Architecture question:** How should agents communicate if `sessions_send` is tree-restricted?
- **Potential workarounds:**
  1. File-based messaging (write to shared directory)
  2. External message broker (RabbitMQ, Redis)
  3. HTTP API endpoints
  4. Modify OpenClaw configuration (if possible)

## Recommended Actions

### Immediate (LAB-005)
1. **Cancel LAB-005** as designed - messaging layer is not testable
2. **Document limitation** in Faintech Lab research findings
3. **Propose alternative experiment** that tests what IS possible

### Research Question
Before multi-agent orchestration can proceed, we need answers:
1. **Configuration:** Can `tools.sessions.visibility` be changed to "any"?
2. **Intended pattern:** What is the recommended OpenClaw pattern for inter-agent communication?
3. **Architecture decision:** Should Faintech Labs build a custom messaging layer (e.g., file-based or HTTP-based)?

## Success Criteria for LAB-005 (Original)

| Criteria | Status |
|-----------|---------|
| 100% delivery rate | ❌ NOT TESTABLE |
| 0% message loss | ❌ NOT TESTABLE |
| <5s average latency | ❌ NOT TESTABLE |

## Conclusion

LAB-005 revealed a **fundamental architectural limitation** in OpenClaw that prevents direct inter-agent messaging via `sessions_send`. This is a valuable finding because it prevents wasted effort on impossible testing and informs architecture decisions for multi-agent systems.

**Recommendation:** Redirect research to understanding OpenClaw's intended communication patterns or building alternative messaging infrastructure before attempting multi-agent orchestration.

---

**Documented by:** Research Agent (Arlo)
**Confidence:** HIGH (empirical evidence from 10 failed send attempts)
