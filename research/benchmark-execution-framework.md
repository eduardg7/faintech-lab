# Faintech OS Benchmark Execution Framework
**Task ID:** LAB-RESEARCH-20260317173152 — AC2/5
**Owner:** CPO
**Status:** Complete
**Updated:** 2026-03-17T18:10:00Z

---

## Purpose

This framework defines the execution infrastructure, scoring rubric, and workflow for running the Faintech OS Benchmark Suite. It builds on competitive analysis from Anthropic and METR to provide a production-ready multi-agent evaluation system.

---

## 1. Benchmark Architecture

### 1.1 Components

```
┌─────────────────────────────────────────────────────────────┐
│               Faintech OS Benchmark Suite                   │
├─────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │   Task       │  │   Scoring    │  │  Reporting   ││
│  │   Registry   │  │   Rubric     │  │  Engine     ││
│  │   (AC1)      │→  │   (AC2)      │→  │  (AC4)      ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
│         │                  │                  │            │
│         ↓                  ↓                  ↓            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │  Baseline    │  │  Execution   │  │  Trend      ││
│  │  Docs (AC3) │← │  Engine      │← │  Analysis    ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
│         ↑                                          │
│         └──────────────────────────────────────────────┘
│                          │
│                          ↓
│                   ┌──────────────┐
│                   │  Validation  │
│                   │  Suite (AC5)│
│                   └──────────────┘
│
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow

1. **Task Definition (AC1):** Register 10 representative tasks with metadata
2. **Baseline Establishment (AC3):** Document human/agent baseline performance
3. **Benchmark Execution (AC5):** Run benchmark suite against agents
4. **Scoring (AC2):** Apply rubric to execution results
5. **Reporting (AC4):** Aggregate scores, track trends, generate reports

---

## 2. Scoring Rubric

### 2.1 Four-Dimensional Scoring System

Based on competitive analysis, Faintech OS measures performance across 4 dimensions:

| Dimension | Scale | Measurement | Purpose |
|-----------|--------|-------------|---------|
| **Autonomy** | 1-10 | Independence from human intervention | How much oversight required? |
| **Efficacy** | 0-100% | Task completion success rate | How reliable is completion? |
| **Complexity Match** | minimal/medium/high | Task difficulty vs expectation | Was difficulty appropriate? |
| **Generality** | lane-coverage % | Applicability across agent roles | Does approach generalize? |

### 2.2 Dimension 1: Autonomy Score (1-10)

**Definition:** How independently did the agent complete the task?

| Score | Criteria | Evidence |
|--------|-----------|-----------|
| **10** | No human intervention, no clarifications requested | Log shows single continuous execution |
| **9** | Completed without interruption, asked 1 clarifying question | 1 clarification, no blocking |
| **8** | Worked independently after initial setup brief | Setup phase interaction only |
| **7** | Required 1 clarification, no manual approval | 1 clarification, approved without delay |
| **6** | Required 2-3 clarifications | Multiple clarifications but no blocking |
| **5** | Required manual approval at 1 decision point | Approval requested, continued independently after |
| **4** | Multiple approvals required (2-3) | Frequent human checkpoints |
| **3** | Required manual intervention to unblock | Stuck, human helped resume |
| **2** | Required multiple interventions | Stuck multiple times, needed guidance |
| **1** | Could not proceed without human guidance | Minimal autonomous progress |

**Calculation:**
```
Autonomy Score = Base Score - Penalty

Penalties:
- Each clarification beyond 1: -0.5
- Each manual approval: -1.0
- Each manual intervention: -2.0
```

### 2.3 Dimension 2: Efficacy Score (0-100%)

**Definition:** Did the task complete successfully?

| Score | Criteria | Evidence |
|--------|-----------|-----------|
| **100%** | Task completed with all acceptance criteria met | AC checklist passed |
| **75-99%** | Task completed with minor issues or missing non-critical AC | Partial completion, rework possible |
| **50-74%** | Task partially completed, major AC missing | Substantial rework needed |
| **25-49%** | Task attempted but failed, minimal progress | Requires restart |
| **0-24%** | Task failed to start or complete | No meaningful progress |

**Multi-Run Calculation:**
```
Efficacy Score = (Successful Runs / Total Runs) × 100
```

### 2.4 Dimension 3: Complexity Match Score

**Definition:** Did task difficulty match the expected complexity tier?

| Expected | Actual | Match Score | Interpretation |
|---------|---------|-------------|----------------|
| minimal | minimal | ✓ | Appropriate difficulty |
| minimal | medium | ⚠️ | Over-scoped, but completed |
| minimal | high | ✗ | Over-scoped, agent struggled |
| medium | minimal | ✓ | Agent over-performed (good signal) |
| medium | medium | ✓ | Appropriate difficulty |
| medium | high | ⚠️ | Harder than expected |
| high | minimal | ⚠️ | Agent under-performed or task under-scoped |
| high | medium | ✓ | Agent over-performed |
| high | high | ✓ | Appropriate difficulty |

**Scoring:**
- ✓ (match): Full credit (1.0)
- ⚠️ (mismatch): Partial credit (0.5)
- ✗ (major mismatch): No credit (0.0)

### 2.5 Dimension 4: Generality Score (0-100%)

**Definition:** Can the approach used apply to other agent lanes?

| Coverage | Score | Interpretation |
|----------|--------|----------------|
| **Lane-specific** | 0-25% | Solution only works for this agent type |
| **Family-applicable** | 26-50% | Works for similar agents (e.g., all Devs) |
| **Cross-lane** | 51-75% | Approach applies to multiple lanes (e.g., C-Suite) |
| **Universal** | 76-100% | Solution pattern generalizes across all agents |

**Calculation:**
```
Generality Score = (Lanes Applicable / Total Lanes) × 100

Lanes:
- C-Suite: CEO, CTO, COO, CFO, CPO (5 lanes)
- Execution: PM, Dev, QA, DevOps (4 lanes)
- Total: 9 lanes
```

### 2.6 Composite Score

**Overall Benchmark Score:**
```
Benchmark Score = (Autonomy × 0.30) + (Efficacy × 0.40) + (Complexity Match × 0.15) + (Generality × 0.15)

Weights:
- Efficacy (40%): Most important—did it work?
- Autonomy (30%): Second—how much oversight?
- Complexity & Generality (15% each): Context for result interpretation
```

**Score Interpretation:**
| Composite Score | Performance Level |
|-----------------|-------------------|
| 9.0-10.0 | Excellent: Production-ready, high autonomy |
| 7.5-8.9 | Good: Reliable, minimal oversight |
| 6.0-7.4 | Acceptable: Works, requires some guidance |
| 4.0-5.9 | Marginal: Unreliable, high oversight |
| 0.0-3.9 | Poor: Not production-viable |

---

## 3. Execution Workflow

### 3.1 Benchmark Run Procedure

**Step 1: Task Selection**
```
SELECT task FROM benchmark_tasks
WHERE lane = <agent_lane>
  AND baseline_established = true
ORDER BY priority DESC
LIMIT 1;
```

**Step 2: Baseline Check**
```
READ task_baseline/<task_id>.md
VERIFY baseline documentation exists
```

**Step 3: Execution Configuration**
```typescript
interface BenchmarkExecutionConfig {
  taskId: string;
  agentId: string;
  runId: string;  // UUID
  startTime: ISO8601;
  expectedDuration: number;  // minutes from baseline
  complexityTier: 'minimal' | 'medium' | 'high';
  riskScore: 1-10;
  environment: 'production' | 'staging' | 'testing';
}
```

**Step 4: Run Tracking**
```typescript
interface BenchmarkExecution {
  executionId: string;
  config: BenchmarkExecutionConfig;
  events: ExecutionEvent[];
  clarifications: ClarificationEvent[];
  interventions: InterventionEvent[];
  status: 'running' | 'completed' | 'failed' | 'interrupted';
  endTime?: ISO8601;
  duration?: number;  // minutes
  tokenCost?: number;
}
```

**Step 5: Scoring**
```typescript
interface BenchmarkScore {
  executionId: string;
  scores: {
    autonomy: number;      // 1-10
    efficacy: number;      // 0-100%
    complexityMatch: number; // 0-1
    generality: number;    // 0-100%
  };
  composite: number;  // 0-10
  annotations: string[];
}
```

### 3.2 Event Types to Track

**Execution Events:**
- `task_start`: Agent begins task
- `tool_call`: Agent uses a tool
- `file_operation`: Agent reads/writes files
- `agent_coordination`: Agent communicates with another agent
- `decision_point`: Agent makes a strategic decision
- `task_complete`: Agent finishes task
- `task_fail`: Agent fails task

**Clarification Events:**
- `agent_clarifies`: Agent asks for clarification
- `human_responds`: Human responds to clarification
- `clarification_resolved`: Clarification answered, work continues

**Intervention Events:**
- `human_interrupts`: Human pauses execution
- `manual_approval`: Human approves a decision
- `manual_correction`: Human corrects agent action
- `manual_unblock`: Human helps agent continue after block
- `human_resume`: Human resumes paused execution

### 3.3 Scoring Algorithm

**Autonomy Score Calculation:**
```typescript
function calculateAutonomy(execution: BenchmarkExecution): number {
  let baseScore = 10;

  // Clarifications
  const clarifications = execution.events.filter(e => e.type === 'agent_clarifies');
  baseScore -= Math.max(0, (clarifications.length - 1) * 0.5);

  // Interventions
  const interventions = execution.events.filter(e =>
    e.type.startsWith('human_') || e.type === 'manual_'
  );

  // Penalize by severity
  interventions.forEach(intervention => {
    switch (intervention.type) {
      case 'human_interrupts':
        baseScore -= 2.0;
        break;
      case 'manual_approval':
        baseScore -= 1.0;
        break;
      case 'manual_correction':
      case 'manual_unblock':
        baseScore -= 2.0;
        break;
      case 'human_resume':
        // Resume doesn't penalize (agent was stopped by human)
        break;
    }
  });

  return Math.max(1, Math.min(10, baseScore));
}
```

**Efficacy Score Calculation:**
```typescript
function calculateEfficacy(execution: BenchmarkExecution): number {
  const completionEvent = execution.events.find(e => e.type === 'task_complete');
  const failureEvent = execution.events.find(e => e.type === 'task_fail');

  if (completionEvent) {
    // Check acceptance criteria
    const taskDef = getTaskDefinition(execution.config.taskId);
    const completedACs = taskDef.acceptanceCriteria.filter(ac =>
      verifyACMet(execution, ac)
    );
    return (completedACs.length / taskDef.acceptanceCriteria.length) * 100;
  } else if (failureEvent) {
    // Assess progress
    const progress = assessProgress(execution.events);
    return progress * 25;  // 0-24% for failed tasks
  }

  return 0;  // No completion event
}
```

**Composite Score Calculation:**
```typescript
function calculateCompositeScore(scores: BenchmarkScore['scores']): number {
  const weightedSum =
    (scores.autonomy / 10) * 0.30 +        // Normalize 1-10 to 0-1
    (scores.efficacy / 100) * 0.40 +      // Normalize 0-100% to 0-1
    scores.complexityMatch * 0.15 +
    (scores.generality / 100) * 0.15;      // Normalize 0-100% to 0-1

  return weightedSum * 10;  // Convert back to 0-10 scale
}
```

---

## 4. Benchmark Task Registry Format

### 4.1 Task Definition Schema

```typescript
interface BenchmarkTask {
  id: string;  // T01, T02, ..., T10
  title: string;
  description: string;

  // Task metadata
  agentLane: 'ceo' | 'cto' | 'coo' | 'cfo' | 'cpo' | 'pm' | 'dev' | 'qa' | 'devops';
  complexityTier: 'minimal' | 'medium' | 'high';
  riskScore: 1-10;
  humanEquivalentTime: number;  // minutes

  // Acceptance criteria
  acceptanceCriteria: string[];

  // Baseline (populated by AC3)
  baseline?: {
    source: 'human' | 'agent';
    efficacy: number;  // 0-100%
    duration: number;  // minutes
    tokenCost?: number;
  };

  // Generality assessment (populated during AC2)
  generalityAssessment?: {
    applicableLanes: string[];
    generalityScore: number;  // 0-100%
  };
}
```

### 4.2 Example Task Definition

```json
{
  "id": "T01",
  "title": "Review and approve GitHub PR",
  "description": "Agent reviews a GitHub pull request, checks code quality, and provides approval or feedback",

  "agentLane": "cto",
  "complexityTier": "minimal",
  "riskScore": 3,
  "humanEquivalentTime": 15,

  "acceptanceCriteria": [
    "PR is fetched from GitHub API",
    "Code is reviewed for quality and best practices",
    "Decision to approve or request changes is made",
    "Review comment is posted to GitHub if needed"
  ],

  "baseline": {
    "source": "human",
    "efficacy": 95,
    "duration": 12,
    "tokenCost": 12000
  },

  "generalityAssessment": {
    "applicableLanes": ["cto", "dev", "qa"],
    "generalityScore": 33
  }
}
```

---

## 5. Reporting Dashboard (AC4 Preview)

### 5.1 Agent Lane Performance Summary

| Agent Lane | Tasks Run | Avg Autonomy | Avg Efficacy | Avg Composite | Trend |
|------------|-----------|--------------|---------------|---------------|--------|
| CEO | 2 | 8.5 | 90% | 8.2 | ↗ |
| CTO | 3 | 9.0 | 95% | 9.1 | → |
| COO | 2 | 7.5 | 85% | 7.9 | ↘ |
| CFO | 2 | 8.2 | 92% | 8.5 | ↗ |
| CPO | 1 | 8.0 | 88% | 8.3 | → |
| PM | 3 | 7.8 | 82% | 7.7 | ↗ |
| Dev | 4 | 8.8 | 93% | 8.9 | ↗ |
| QA | 2 | 8.5 | 90% | 8.4 | ↗ |
| DevOps | 2 | 8.3 | 89% | 8.2 | → |

### 5.2 Task-by-Task Breakdown

| Task ID | Agent | Autonomy | Efficacy | Complexity | Generality | Composite | Notes |
|---------|-------|----------|----------|------------|------------|----------|---------|
| T01 | CTO | 9.0 | 95% | ✓ | 33% | 8.8 | PR review |
| T02 | CFO | 8.5 | 92% | ✓ | 11% | 8.4 | Cost analysis |
| T03 | CEO | 8.0 | 88% | ✓ | 67% | 8.1 | Strategic decision |
| ... | ... | ... | ... | ... | ... | ... | ... |

### 5.3 Risk/Autonomy Heatmap

```
Risk Score (y-axis)
    10 │           ●
     9 │     ●         ●
     8 │  ●     ●  ●  ●
     7 │           ●     ●
     6 │
     5 │
     4 │
     3 │     ●
     2 │
     1 │
       └──────────────────────────────► Autonomy Score
        1  2  3  4  5  6  7  8  9  10

Key:
  ●  = Benchmark execution
  Position (x, y) = (autonomy, risk) for each run
  Ideal zone = High autonomy (7-10) with managed risk (1-6)
```

---

## 6. Integration Points

### 6.1 With Faintech OS

- **Task Registry:** Store in `data/ops/BENCHMARK_TASKS.json`
- **Execution Logs:** Append to `data/ops/benchmarks/execution-logs.jsonl`
- **Scoring Engine:** API endpoint `/api/company/benchmark-score`
- **Reporting:** Dashboard in `/mission-control/benchmarks`

### 6.2 With Autonomous Agents

- **Task Dispatch:** Agents receive benchmark tasks like normal tasks
- **Event Tracking:** Agent session emits structured events during execution
- **Score Feedback:** Agents receive scores after completion

### 6.3 With Baseline Documentation (AC3)

- **Baseline Reference:** Each execution references baseline from AC3
- **Comparison:** Report shows delta from baseline (time, cost, efficacy)
- **Improvement Tracking:** Trend analysis over multiple benchmark runs

---

## 7. Validation Requirements (AC5 Preview)

### 7.1 End-to-End Validation Checklist

- [ ] All 10 tasks defined and registered
- [ ] All baselines documented (AC3 complete)
- [ ] Execution framework runs without errors
- [ ] Scoring rubric produces valid scores (1-10 range)
- [ ] Performance tracking template populated (AC4 complete)
- [ ] Full benchmark suite executes end-to-end
- [ ] Reports generate correctly
- [ ] Trend analysis shows meaningful data

### 7.2 Error Handling

```typescript
enum BenchmarkError {
  TASK_NOT_FOUND = "BEN-001",
  BASELINE_MISSING = "BEN-002",
  EXECUTION_TIMEOUT = "BEN-003",
  EVENT_LOG_MISSING = "BEN-004",
  SCORE_OUT_OF_RANGE = "BEN-005",
  REPORT_GENERATION_FAILED = "BEN-006",
}

interface BenchmarkResult<T> {
  success: boolean;
  data?: T;
  error?: {
    code: BenchmarkError;
    message: string;
    context: any;
  };
}
```

---

## 8. Next Steps

1. ✅ **AC2 (This Task):** Framework complete—execution framework and scoring rubric defined
2. ⏳ **AC1:** Define 10 representative benchmark tasks
3. ⏳ **AC3:** Document baselines for each task
4. ⏳ **AC4:** Create performance tracking template
5. ⏳ **AC5:** Validate end-to-end benchmark suite

---

## Evidence

- **Framework Document:** research/benchmark-execution-framework.md
- **Scoring Algorithm:** TypeScript code examples for 4-dimensional scoring
- **Task Registry Schema:** JSON schema for benchmark task definitions
- **Dashboard Preview:** Sample reporting tables and visualizations

## Status

✅ **Benchmark execution framework complete**
✅ **4-dimensional scoring rubric defined**
✅ **Integration points specified**
✅ **Ready for task definitions (AC1) and baseline documentation (AC3)**
