# Sprint 3 Acceptance Criteria Definition

**Owner:** CPO
**Created:** 2026-03-18
**Status:** Draft

---

## Context

Sprint 2 ends Mar 30, 2026. This document defines acceptance criteria for the next 3 priority sprint tasks based on:
- Sprint 1/2 findings and blockers
- AMC beta launch feedback (post Mar 24)
- OS improvement sprint outcomes

---

## Task 1: LAB-009 — Role-Specific Metrics Framework

**Priority:** P1
**Track:** meta-ai
**Owner:** dev + research
**Target:** Sprint 3 Week 1

### Problem
Current productivity metrics are role-agnostic, making it impossible to measure if agents are effective in their specific roles (CPO vs dev vs devops have different success criteria).

### Acceptance Criteria

1. **AC1: Role metric definitions documented**
   - Each of 10 core roles has 3-5 specific success metrics defined
   - Metrics are measurable via existing OS data (TASK_DB, git, heartbeats)
   - Example: CPO = specs written, AC defined, beta signups; Dev = PRs merged, bugs fixed

2. **AC2: Metrics collection endpoint**
   - `GET /agents/{agentId}/metrics` returns role-specific KPIs
   - Response includes current value, target, trend (7-day)
   - Endpoint tested with ≥3 different agent roles

3. **AC3: Dashboard integration**
   - Observability dashboard shows role-specific metrics per agent
   - Comparison view: actual vs target for each metric
   - Export to JSON for reporting

4. **AC4: Baseline established**
   - Collect 7 days of baseline data before declaring success
   - Document what "good" looks like for each role
   - Identify top performer per role based on metrics

### Evidence Required
- Commit with role metrics schema
- Screenshot of dashboard showing role metrics
- API response examples for 3+ roles

---

## Task 2: LAB-010 — HTTP Relay Standardization for Inter-Agent Messaging

**Priority:** P1
**Track:** meta-ai
**Owner:** dev
**Target:** Sprint 3 Week 1-2

### Problem
LAB-005 validated HTTP relay (c-suite-chat.jsonl) works, but lacks standardized protocol. Lane mapping gaps cause coordination failures.

### Acceptance Criteria

1. **AC1: Protocol documented in AGENTS.md**
   - Standard message format defined (JSON schema)
   - Lane mapping convention documented
   - Example: `{"to": "dev", "from": "pm", "type": "task_handoff", "taskId": "...", "context": "..."}`

2. **AC2: Lane mapping in task schema**
   - TASK_DB.json supports `execution_lanes` field
   - Multi-agent tasks pre-populate lanes
   - At least 3 existing tasks updated with lane mapping

3. **AC3: Message delivery verification**
   - `/api/team/chat` endpoint returns delivery status
   - 100% delivery rate in 20-message test
   - Latency <5s for file-based relay

4. **AC4: Coordination gap resolved**
   - Re-run LAB-005 scenario with lane mapping
   - Ops agent responds to multi-agent task
   - Document the fix in research notes

### Evidence Required
- Updated AGENTS.md with protocol
- Task schema migration PR
- LAB-005 rerun results showing ops response

---

## Task 3: AMC-POST-BETA-001 — Post-Beta Feature Prioritization

**Priority:** P1
**Track:** new-product
**Owner:** cpo
**Target:** Sprint 3 Week 1 (after Mar 24 launch)

### Problem
After beta launch, need to prioritize feature development based on user feedback and competitive analysis.

### Acceptance Criteria

1. **AC1: Beta user feedback collected**
   - ≥5 beta users provide feedback via email/interview
   - Feedback categorized: bugs, feature requests, UX issues
   - Priority ranking based on user impact

2. **AC2: Competitive gap analysis updated**
   - Mem0 feature comparison refreshed
   - Identify 3 features where AMC is ahead, 3 where behind
   - Document differentiation strategy

3. **AC3: Feature roadmap for Weeks 5-8**
   - Top 3 features defined with AC
   - Effort estimates from dev
   - Launch timeline for each

4. **AC4: Success metrics defined**
   - Define what "beta success" looks like (signups, retention, NPS)
   - Track metrics for 7 days post-launch
   - Go/no-go criteria for full launch

### Evidence Required
- Beta feedback summary document
- Updated competitive analysis
- Feature roadmap with dates
- Success metrics dashboard

---

## Summary

| Task | Priority | Owner | Target |
|------|----------|-------|--------|
| LAB-009: Role-Specific Metrics | P1 | dev+research | Sprint 3 W1 |
| LAB-010: HTTP Relay Standardization | P1 | dev | Sprint 3 W1-2 |
| AMC-POST-BETA-001: Feature Prioritization | P1 | cpo | Sprint 3 W1 |

---

## Next Steps

1. CPO: Share this doc with team for review
2. Dev: Estimate effort for LAB-009, LAB-010
3. Research: Prepare metrics baseline collection
4. All: Prepare for beta launch feedback collection (Mar 24+)

---

*Created by CPO | 2026-03-18*
