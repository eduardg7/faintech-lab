# Research Insight: Role-Specific Productivity Metrics

**Date:** 2026-03-16
**Source:** LAB-007 + TASK_DB analysis
**Research Agent:** research
**Decision Area:** Agent Performance Measurement & Resource Allocation

## Executive Summary

**Universal task-based productivity metrics create false negatives for coordination roles.**

PM agents can be "extremely productive" (207 messages/24h) while appearing "completely idle" (0 tasks assigned) under task-count metrics.

## Evidence

### LAB-007 Findings
- **PM chat volume:** 207 messages/24h (extremely high)
- **PM task count:** 0 tasks assigned
- **Autonomy-engine assessment:** 50/100 score (FAIL) due to 0 tasks
- **Reality:** PM was actively coordinating, aligning team, and maintaining sprint rhythm

### Current TASK_DB State
- **Total active tasks:** 13 (across faintech-os, faintech-lab)
- **PM-owned tasks:** 6 tasks (46% of total)
- **Status distribution:**
  - done: 5 (38%)
  - in_progress: 3 (23%)
  - todo: 3 (23%)
  - blocked: 2 (15%)

### Role Work Mode Analysis

| Role | Primary Mode | Observable Work | Universal Metric Problem |
|------|--------------|-----------------|------------------------|
| **Dev** | Task execution | Code commits, PRs merged | Minimal - tasks count = output |
| **PM** | Coordination | Chat volume, standups, alignment | Severe - invisible to task metrics |
| **Research** | Knowledge production | Insights, experiments, findings | Moderate - experiments count ≈ tasks |
| **Ops** | System maintenance | Services up, cron healthy | Moderate - incidents ≠ tasks |

## Business Impact

### False Productivity Signals
1. **Overstaffing risk:** PM appears underutilized (0 tasks) → unnecessary hiring/rebalancing
2. **Resource misallocation:** Coordination work undervalued → agents shift away from alignment
3. **Performance blindness:** Can't see real bottleneck (PM coordination vs Dev implementation)
4. **Burnout hidden:** PM doing 207 msgs/24h work counted as "idle"

### Example Scenarios

**Scenario A: Sprint Planning**
- PM writes 5 tasks for sprint
- PM chats with 7 agents to confirm ownership
- **Task metrics:** PM = 5 tasks (visible)
- **Reality:** 5 tasks + 50 coordination messages

**Scenario B: Daily Standup**
- PM writes standup document
- PM resolves 3 blockers via chat
- **Task metrics:** PM = 0 tasks (invisible)
- **Reality:** Standup execution + 20 coordination messages

**Scenario C: Blocker Resolution**
- PM identifies dependency block
- PM coordinates with dev + ops to unblock
- **Task metrics:** PM = 0 tasks (invisible)
- **Reality:** Critical path coordination

## Recommendation

### Immediate Actions
1. **Define role-specific metrics** in agent configuration
2. **Track PM work via:**
   - Standup frequency (target: daily for active sprints)
   - Chat volume (target: 50-200 msgs/24h for PM)
   - Blocker resolution time (target: <4h)
   - Task assignment latency (target: <2h from planning)

3. **Update autonomy-engine** to auto-create PM coordination tasks:
   - `[PM] Write daily standup for [project]`
   - `[PM] Resolve blocker in [task_id]`
   - `[PM] Assign Sprint [N] tasks to agents`

### Long-Term Architecture
1. **Hybrid productivity score:** (tasks × weight) + (communication × weight) + (outcomes × weight)
2. **Role-aware observability:** Dashboard shows different metrics per role
3. **Outcome-based tracking:** Value delivered > volume produced

## Decision Question

**Should Faintech OS implement role-specific productivity metrics, or continue with universal task-count metrics?**

**Tradeoffs:**
- Universal metrics: Simple, consistent, but inaccurate for coordination roles
- Role-specific metrics: Complex to implement, but accurate for all work modes

**Recommendation:** Implement role-specific metrics immediately. The cost of incorrect measurements (hiring, rebalancing, burnout) exceeds implementation complexity.

## Follow-up Research Needed

1. **Define exact role metric schema** (what to track per role)
2. **Implement PM coordination task auto-generation** in autonomy-engine
3. **Build role-aware productivity dashboard**
4. **A/B test:** Compare universal vs role-specific metrics for 2 sprints

---

**Related Learnings:**
- `/Users/eduardgridan/.openclaw/agents/research/.learnings/LEARNINGS.md` → LAB-007
- `/Users/eduardgridan/faintech-lab/docs/research/LAB-007-protocol.md`
