# Productivity Metrics Dashboard - Views Specification

**Task:** OS-20260317152756-F644 (AC2/4 of LAB-RESEARCH-001)
**Author:** Faintech Dev
**Date:** 2026-03-17
**Project:** Faintech Labs

## Overview

This document defines the three core dashboard views for the productivity metrics dashboard. These views provide visibility into task cycling patterns, agent performance, and task lifecycle across all active projects (faintech-lab, faintech-os, faintrading).

**Data Sources:**
- `TASK_DB.json` - primary task metadata and activity logs
- Agent sessions from `FAINTECH_OS_STATE.json`
- Git evidence from task metadata (`git_noop`, `commit_sha`, `pr_url`)
- Worktrees and PR state from `metadata` blocks

---

## View 1: Project Summary Dashboard

**Purpose:** High-level overview of project health and productivity at the project level.

**Layout:**
- Grid layout with cards per active project
- Each card shows aggregate metrics
- Click-through to project detail view

**Metrics per Project Card:**

1. **Task Throughput**
   - Tasks completed in last 24h / 7d / 30d
   - Color-coded: Green (>5/day), Yellow (2-5/day), Red (<2/day)

2. **Git Evidence Health**
   - `% tasks with git_noop=false` (real code changes)
   - Recent commit SHAs (last 5)
   - Open PR count
   - Color-coded: Green (>80% evidence), Yellow (50-80%), Red (<50%)

3. **Cycling Alert**
   - Tasks with `noop_release_count >= 2`
   - Count of cycling-blocked tasks
   - Color-coded: Green (0), Yellow (1-3), Red (>3)

4. **Queue Health**
   - Tasks in each status: backlog, todo, in_progress, review, done
   - Average age by status
   - Stale task count (>3h without progress)

5. **Agent Coverage**
   - Agents with active leases
   - Agent throughput ranking (tasks completed/shift)
   - Total tokens burned per project

**Interactions:**
- Filter by time range: 24h, 7d, 30d
- Sort by: throughput, git health, cycling, stale
- Export to CSV/JSON

**Data Source Queries:**
```javascript
// Project-level aggregation
db.tasks.filter(t => t.project_id === project).reduce({
  completed: count(t.status === 'done'),
  git_evidence_rate: avg(t.git_noop === false),
  cycling_blocked: count(t.git_noop_release_count >= 2),
  stale_tasks: count(taskAge(t) > 3h && !hasRecentActivity(t))
})
```

---

## View 2: Agent Performance Ranking

**Purpose:** Identify top performers and underperforming agents across all projects.

**Layout:**
- Table view with sortable columns
- Heatmap coloring for key metrics
- Agent detail modal on click

**Columns:**

1. **Agent Identity**
   - Agent ID
   - Primary project allocation
   - Role (dev, qa, pm, etc.)
   - Avatar (from AGENT.md)

2. **Task Execution**
   - Tasks completed (total, 7d, 24h)
   - Tasks created
   - Completion rate: completed / assigned
   - Color-coded: Green (>70%), Yellow (40-70%), Red (<40%)

3. **Evidence Quality**
   - % tasks with git evidence
   - % tasks with non-code evidence (docs, specs, logs)
   - Evidence diversity score: types(t.evidence) / max_types
   - Average evidence items per task

4. **Cycle Discipline**
   - Cycling incidents: count(`noop_release_count >= 2`)
   - Avg noop release count per task
   - Cycling rate: cycling_incidents / total_tasks
   - Color-coded: Green (<5%), Yellow (5-15%), Red (>15%)

5. **Response Latency**
   - Avg time from assignment -> in_progress
   - Avg time from assignment -> first evidence
   - Avg time from in_progress -> review
   - SLA breach count: time > 2h without progress

6. **Cost Efficiency**
   - Total tokens burned
   - Tokens per completed task
   - Tokens per git_noop task (waste)
   - Cost ranking: low / medium / high

**Sorting Options:**
- Default: by completion rate (descending)
- Alt: by git evidence rate, cycling rate, cost efficiency, response latency

**Performance Tiers (Badges):**
- **Gold Star:** Completion >80%, git_evidence >80%, cycling <5%
- **Silver Star:** Completion >60%, git_evidence >60%, cycling <10%
- **Bronze Star:** Completion >40%, git_evidence >40%, cycling <20%
- **At Risk:** Below Bronze Star thresholds

**Data Source Queries:**
```javascript
// Agent-level aggregation
agents.map(agent => ({
  agent_id: agent.id,
  primary_project: getPrimaryAllocation(agent.id),
  completed_tasks: db.tasks.filter(t => t.owner === agent.id && t.status === 'done'),
  git_evidence_rate: db.tasks.filter(t => t.owner === agent.id && t.git_noop === false).length / total_tasks,
  cycling_rate: db.tasks.filter(t => t.owner === agent.id && t.noop_release_count >= 2).length / total_tasks,
  avg_latency: avg(timeToFirstEvidence(agent.tasks)),
  tokens_per_task: agent.totalTokens / completed_tasks
})).sort(by_completion_rate)
```

---

## View 3: Task Lifecycle Visualization

**Purpose:** Visualize task flow, identify bottlenecks, and surface process gaps.

**Layout:**
- Sankey diagram or flow chart
- Left-to-right flow: backlog → todo → in_progress → review → done
- Pipeline thickness = task volume
- Node size = avg duration

**Flow Elements:**

1. **Status Transitions**
   - Edges between status nodes
   - Edge thickness = transition frequency
   - Edge color = avg transition time
   - Hover: show transition list with task IDs

2. **Duration Bubbles**
   - At each status node: show avg duration, max duration
   - Bubble size = avg task age
   - Color = health: Green (<1h), Yellow (1-3h), Red (>3h)
   - Hover: show task distribution breakdown

3. **Bottleneck Indicators**
   - **Stuck nodes:** avg duration > threshold (configurable, default 2h)
   - **Dead-end paths:** transitions with 0 downstream moves
   - **Orphaned tasks:** tasks without recent heartbeat (>4h)
   - **Cycling loops:** back-and-forth transitions (e.g., in_progress → todo → in_progress)

4. **Success Funnel**
   - Conversion rate at each transition:
     - backlog → todo: % promoted from backlog
     - todo → in_progress: % started execution
     - in_progress → review: % submitted for review
     - review → done: % merged/approved
   - Overall funnel efficiency: done / created
   - Color-coded: Green (>80% conversion), Yellow (50-80%), Red (<50%)

**Interactivity:**
- Click node: filter task table to tasks in that status
- Click edge: show transition details (task IDs, times, blockers)
- Time range filter: show flow for 24h, 7d, 30d
- Play/pause animation: watch task flow over time

**Data Source Queries:**
```javascript
// Flow aggregation
const flow = {
  nodes: ['backlog', 'todo', 'in_progress', 'review', 'done'],
  edges: [
    {from: 'backlog', to: 'todo', count: count(transitions('backlog', 'todo'))},
    {from: 'todo', to: 'in_progress', count: count(transitions('todo', 'in_progress'))},
    {from: 'in_progress', to: 'review', count: count(transitions('in_progress', 'review'))},
    {from: 'review', to: 'done', count: count(transitions('review', 'done'))},
    {from: 'review', to: 'todo', count: count(transitions('review', 'todo'))}, // rejections
    {from: 'in_progress', to: 'todo', count: count(transitions('in_progress', 'todo'))}, // cycling
  ],
  node_metrics: nodes.map(node => ({
    node,
    avg_duration: avgDuration(node),
    task_count: count(t.status === node),
    conversion_rate: downstreamTasks / upstreamTasks
  }))
}
```

---

## Refresh Frequency & Accuracy Requirements

**Data Refresh:**
- Real-time: WebSocket or 30s polling for heartbeat updates
- Batch refresh: Every 5 minutes for task state, git evidence, agent sessions
- Cache: 1-minute TTL for dashboard widgets, 5-minute TTL for detail views

**Accuracy Validation:**
- **Task count match:** Dashboard total tasks = TASK_DB total tasks
- **Git evidence sync:** Dashboard commit SHAs = GitHub API commit list (last 100)
- **Agent session sync:** Dashboard active agents = FAINTECH_OS_STATE agentSessions
- **Latency < 2s:** All dashboard views render within 2 seconds

**Alerting:**
- Trigger alert when data sync fails > 5 minutes
- Trigger alert when git evidence mismatch > 10%
- Trigger alert when task count drift > 5%

---

## Implementation Priority

**Phase 1 (MVP - Week 6):**
1. Project Summary Dashboard (basic metrics)
2. Agent Performance Ranking (table view)
3. Data refresh pipeline (polling TASK_DB)

**Phase 2 (Enhanced - Week 7):**
1. Task Lifecycle Visualization (Sankey flow)
2. Agent detail modal
3. Export functionality

**Phase 3 (Advanced - Week 8):**
1. Real-time WebSocket updates
2. Configurable time ranges
3. Performance trend lines (historical comparison)

---

## Acceptance Criteria Checklist

- [x] View 1 defined: Project Summary with 5 metric categories
- [x] View 2 defined: Agent Performance Ranking with sortable table
- [x] View 3 defined: Task Lifecycle Visualization with flow diagram
- [x] Data sources specified for all views (TASK_DB, OS_STATE, git metadata)
- [x] Refresh frequency defined (real-time + batch)
- [x] Accuracy validation criteria specified (<2s render, <5% drift)
- [x] Implementation prioritized into 3 phases

**Status:** ✅ Complete - Ready for review by cto
