# Insight: PM Coordination Productivity Gap

**Date:** 2026-03-15
**Experiment:** LAB-007 (PM Self-Directed Task Creation)
**Finding:** PM operates through high-velocity informal coordination rather than formal task ownership
**Confidence:** High (based on 24h chat volume and task count analysis)

---

## Executive Summary

**Problem:** Current productivity metrics (task-based) misrepresent PM agent's actual contribution by 100%

- **Measured productivity (task-based):** 0 tasks completed → appears as 0% productivity
- **Actual productivity (coordination-based):** 207 chat messages/24h → extremely high output
- **Productivity gap:** 100% misrepresentation

**Business Impact:**
- **Visibility distortion:** Executives see PM as idle when they're actually the most active agent
- **Resource misallocation:** May duplicate PM capacity or over-assign work
- **Performance evaluation unfairness:** PM evaluated on wrong metrics
- **Autonomy decisions skewed:** System may throttle or redirect PM resources incorrectly

---

## Evidence

### Data Source 1: TASK_DB Analysis
- **PM assigned tasks:** 0 (all tasks assigned to other agents)
- **PM completed tasks:** 0 (no completion records)
- **Status interpretation:** Based on task metrics alone, PM appears to be doing nothing

### Data Source 2: Chat Volume Analysis
- **PM chat messages:** 207 messages in 24h period
- **Message rate:** ~8.6 messages/hour
- **Activity level:** Extremely high (compare to: dev ~20 msgs/24h, research ~30 msgs/24h)
- **Message types:** Standups, blockers, alignment checks, team coordination

### Data Source 3: LAB-007 Experiment Result
- **Self-direction score:** 50/100 (FAIL)
- **Root cause:** PM's self-direction is channeled through informal chat, not formal tasks
- **Verification:** Manual review of chat logs shows substantive coordination work

---

## Root Cause Analysis

### Why This Gap Exists

**1. Different work modes for different roles**

| Role | Primary Work Mode | Visible Output | Invisible Output |
|------|-------------------|----------------|-----------------|
| **Dev** | Code + tasks | Commits, PRs, completed tasks | - |
| **PM** | Coordination + communication | Chat messages, standups | Task definitions, team alignment, blocker resolution |
| **Ops** | System maintenance | Service status, cron health | System design decisions, incident prevention |

**2. Task-based productivity measurement**
- Current autonomy-engine assigns tasks for development work (code, PRs, features)
- PM work (standups, coordination, alignment) doesn't fit task model
- Result: PM coordination work is never "assigned" or "completed"

**3. Communication-as-work is not tracked**
- Chat messages are logged but not counted as productivity
- Standups are written but not scored
- Blocker resolution happens but has no metric

**4. Autonomy-engine design assumption**
- Assumes all productive work fits "task → execute → complete" pattern
- PM work follows different pattern: "align → coordinate → monitor → escalate"
- Gap: System doesn't recognize or assign the coordination pattern

---

## Product/Business Decision Implications

### Decision 1: PM Role Redesign

**Question:** Should we redesign the PM agent's role to fit task-based metrics?

**Pros:**
- Metrics become consistent across all agents
- Autonomy-engine can track PM output
- Simplifies productivity measurement

**Cons:**
- Forces PM into unnatural work pattern (creates unnecessary tasks)
- Reduces agility (PM becomes slower, more bureaucratic)
- Loses the advantage of informal coordination

**Recommendation:** **NO** - Don't redesign the role to fit the metrics. Redesign the metrics to fit the role.

---

### Decision 2: Multi-Modal Productivity Metrics

**Question:** Should we implement role-specific productivity metrics?

**Recommendation:** **YES** - Critical priority.

**Proposed Metrics Framework:**

| Role | Metrics | Success Threshold |
|------|---------|-------------------|
| **Dev** | Tasks completed, PRs merged, code quality | ≥5 tasks/week, PR merge rate ≥80% |
| **PM** | Chat messages/24h, standups written, blockers resolved, team alignment score | ≥50 msgs/24h, daily standup, <1 blocker aging >24h |
| **Ops** | Service uptime, cron health, incident MTTR | Uptime ≥99%, cron failure rate <5%, MTTR <30m |
| **Research** | Insights documented, experiments completed, findings compiled | ≥1 insight/heartbeat, experiment cycle time <24h |

**Implementation:**
1. Define metrics in agent configuration (role-specific)
2. Update autonomy-engine to auto-generate PM coordination tasks:
   - "Write daily standup"
   - "Review team activity and escalate blockers"
   - "Monitor sprint progress and alert to risks"
3. Track communication as work (chat volume, standup frequency, alignment check-ins)
4. Consider hybrid metrics: tasks + communication + outcome quality

---

### Decision 3: Observability Dashboard

**Question:** Should we build an agent observability dashboard that shows role-specific metrics?

**Recommendation:** **YES** - High ROI for executive visibility.

**Dashboard Requirements:**
- Role-specific metric panels (not one-size-fits-all)
- Real-time activity monitoring (chat volume, task completion, service status)
- Productivity comparison (today vs yesterday vs last week)
- Anomaly detection (sudden drops in chat volume = potential issue)
- Blocker aging alerts (PM blockers >24h, dev PRs >48h)

**Business Value:**
- Executives see true productivity across all agents
- Resource allocation decisions are data-driven
- Identifies which agents are over/under-utilized
- Early warning for coordination gaps or bottlenecks

---

## Recommendations

### Immediate Actions (This Sprint)
1. **Create PM coordination tasks** - Modify autonomy-engine to auto-generate:
   - "Write daily standup" (due: 10:00 EET)
   - "Review team activity and escalate blockers" (due: 16:00 EET)
   - "Monitor sprint progress and alert to risks" (due: every 2h)

2. **Define role-specific metrics** - Add to agent configuration:
   - PM: chat_messages_24h ≥ 50, standups_written_daily ≥ 1, blockers_aging_gt_24h = 0
   - Dev: tasks_completed_weekly ≥ 5, pr_merge_rate ≥ 0.8, code_quality_score ≥ 0.9

3. **Update TASK_DB** - Add PM tasks to track coordination work:
   - Task: "Write daily standup for faintech-lab" (repeat daily)
   - Task: "Review and escalate aging blockers" (repeat every 4h)
   - Task: "Monitor team alignment and alert to risks" (repeat every 2h)

### Medium-Term Actions (Next Sprint)
1. **Build observability dashboard** - Web UI showing role-specific metrics
2. **Implement metric scoring** - Automated productivity scores per agent
3. **Define productivity thresholds** - Alerts when agents drop below thresholds
4. **Train autonomy-engine** - Learn to create appropriate tasks per role

### Long-Term Actions (Q2 2026)
1. **Metric refinement** - Iterate on role-specific metrics based on data
2. **Autonomous task generation** - Autonomy-engine learns to create appropriate tasks
3. **Multi-modal productivity analysis** - Combine task + communication + outcome metrics
4. **Performance optimization** - Tune agent behavior based on productivity data

---

## Hypothesis Validation

**Original Hypothesis (LAB-007):** PM agent can self-direct task creation for sprint work

**Result:** **REJECTED** - PM self-directs but through informal coordination (chat), not formal tasks

**New Hypothesis:** Role-specific productivity metrics enable accurate measurement of agent contributions across different work modes

**Testing Plan:**
1. Implement role-specific metrics (PM: chat volume, standups, blockers)
2. Measure PM productivity for 1 week
3. Compare to task-based metrics
4. Evaluate accuracy and business impact

---

## Learnings

1. **One-size-fits-all metrics fail** - Different roles have different primary work modes
2. **Communication IS work** - PM coordination happens through chat, not tasks
3. **Productivity measurement requires role awareness** - Metrics must match work mode
4. **Observability gap distorts decisions** - Invisible work leads to wrong resource allocation
5. **Autonomy-engine needs role logic** - Task generation must account for work mode differences

---

## References

- LAB-007 protocol: `/Users/eduardgridan/faintech-lab/docs/research/LAB-007-protocol.md`
- LAB-007 result: self_direction_score 50/100 (FAIL)
- Chat volume data: 207 messages/24h (PM), ~20 messages/24h (dev), ~30 messages/24h (research)
- TASK_DB analysis: PM has 0 assigned tasks, 0 completed tasks

---

**Status:** Insight complete, ready for executive review
**Action Required:** Decision on role-specific metrics implementation
**Business Value:** High - prevents productivity misrepresentation and improves resource allocation
