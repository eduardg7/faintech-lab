# Multi-Agent Handoff Protocol Specification

**Version:** 1.0-draft
**Task:** LAB-004
**Author:** faintech-dev
**Created:** 2026-03-15
**Status:** Draft

---

## Overview

This specification defines a standardized JSON-based protocol for coordinating task handoffs between multiple AI agents in the Faintech OS ecosystem.

## Goals

1. **Reliability**: Ensure handoffs complete successfully with delivery guarantees
2. **Context preservation**: Transfer all necessary context to the receiving agent
3. **Auditability**: Track handoff history for debugging and improvement
4. **Cycling prevention**: Detect and prevent task cycling between agents

---

## Protocol Schema

### HandoffMessage

```json
{
  "protocol_version": "1.0",
  "message_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "handoff_type": "delegation|escalation|fallback|continuation",

  "task": {
    "task_id": "string",
    "project_id": "string",
    "title": "string",
    "status": "todo|in_progress|review|blocked",
    "acceptance_criteria": ["string"]
  },

  "from_agent": {
    "agent_id": "string",
    "role": "string",
    "session_id": "string",
    "reason": "string"
  },

  "to_agent": {
    "agent_id": "string",
    "role": "string",
    "expected_action": "string"
  },

  "context": {
    "summary": "string",
    "progress_percentage": 0-100,
    "blockers": ["string"],
    "decisions_made": ["string"],
    "artifacts": [
      {
        "type": "file|commit|pr|url",
        "path": "string",
        "description": "string"
      }
    ],
    "next_steps": ["string"]
  },

  "metadata": {
    "handoff_count": "integer",
    "previous_agents": ["string"],
    "cycling_risk": "low|medium|high",
    "priority": "P0|P1|P2|P3",
    "sla_deadline": "ISO-8601 or null"
  },

  "delivery": {
    "requires_acknowledgment": true,
    "ack_timeout_seconds": 300,
    "retry_policy": {
      "max_retries": 3,
      "backoff_seconds": 30
    }
  }
}
```

---

## Handoff Types

### 1. Delegation
Primary agent delegates work to a specialist agent.

```json
{
  "handoff_type": "delegation",
  "from_agent": {
    "reason": "Task requires backend expertise"
  }
}
```

### 2. Escalation
Agent escalates a blocker to a higher authority.

```json
{
  "handoff_type": "escalation",
  "from_agent": {
    "reason": "Decision requires CEO approval"
  },
  "context": {
    "blockers": ["Missing architectural decision on auth strategy"]
  }
}
```

### 3. Fallback
Agent cannot complete task, returns to pool or previous agent.

```json
{
  "handoff_type": "fallback",
  "from_agent": {
    "reason": "Environment setup failed after 3 attempts"
  }
}
```

### 4. Continuation
Agent passes work to continue in next session/shift.

```json
{
  "handoff_type": "continuation",
  "from_agent": {
    "reason": "Shift handoff - task in progress"
  }
}
```

---

## Cycling Detection

A task is flagged as **cycling** when:

1. `handoff_count` >= 3 for the same task_id
2. No new artifacts or progress between handoffs
3. Same agents repeatedly exchange the task

**Prevention mechanism:**

```json
{
  "metadata": {
    "cycling_risk": "high",
    "cycling_indicators": [
      "handoff_count > 3",
      "no_progress_delta",
      "repeated_agent_pair"
    ]
  }
}
```

When `cycling_risk: high`, the handoff is blocked and CEO is alerted.

---

## Delivery Guarantees

### Acknowledgment Flow

1. Sender creates HandoffMessage
2. Sender posts to `/api/team/handoff` endpoint
3. System validates message schema
4. System delivers to recipient agent
5. Recipient sends acknowledgment within `ack_timeout_seconds`
6. If no ack, retry according to `retry_policy`
7. After max retries, escalate to CEO

### Message States

```
pending → delivered → acknowledged → accepted
                    ↘ rejected
                    ↘ timed_out
```

---

## Implementation Checklist

- [ ] Create TypeScript types for HandoffMessage schema
- [ ] Implement `/api/team/handoff` endpoint
- [ ] Add handoff message queue with persistence
- [ ] Implement acknowledgment timeout handler
- [ ] Add cycling detection logic
- [ ] Create handoff history log
- [ ] Add metrics: latency, success rate, cycling incidents

---

## Example Handoff

```json
{
  "protocol_version": "1.0",
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-03-15T14:00:00Z",
  "handoff_type": "delegation",

  "task": {
    "task_id": "LAB-004",
    "project_id": "faintech-lab",
    "title": "Multi-Agent Coordination Protocol Prototype",
    "status": "in_progress",
    "acceptance_criteria": [
      "Define JSON-based handoff protocol specification",
      "Implement coordination prototype",
      "Test handoff scenarios"
    ]
  },

  "from_agent": {
    "agent_id": "faintech-cto",
    "role": "CTO",
    "session_id": "session-cto-001",
    "reason": "Implementation work delegated to Dev"
  },

  "to_agent": {
    "agent_id": "faintech-dev",
    "role": "Technical Lead",
    "expected_action": "Implement protocol specification and prototype"
  },

  "context": {
    "summary": "Protocol design complete, ready for implementation",
    "progress_percentage": 20,
    "blockers": [],
    "decisions_made": [
      "JSON-based format chosen",
      "Four handoff types defined"
    ],
    "artifacts": [
      {
        "type": "file",
        "path": "projects/meta-ai/docs/handoff-protocol-spec.md",
        "description": "Initial protocol specification"
      }
    ],
    "next_steps": [
      "Create TypeScript types",
      "Implement API endpoint",
      "Add test cases"
    ]
  },

  "metadata": {
    "handoff_count": 1,
    "previous_agents": ["faintech-pm"],
    "cycling_risk": "low",
    "priority": "P1",
    "sla_deadline": "2026-03-18T18:00:00Z"
  },

  "delivery": {
    "requires_acknowledgment": true,
    "ack_timeout_seconds": 300,
    "retry_policy": {
      "max_retries": 3,
      "backoff_seconds": 30
    }
  }
}
```

---

## Metrics & Observability

Track the following metrics:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Handoff latency (p95) | <5s | >10s |
| Acknowledgment rate | >95% | <90% |
| Cycling incidents | 0/week | >2/week |
| Handoff success rate | >90% | <85% |

---

## Next Steps

1. Review this specification with CTO
2. Implement TypeScript types
3. Build prototype in faintech-lab
4. Test with 2+ agents
5. Document edge cases

---

*This specification will be updated as we learn from implementation.*
