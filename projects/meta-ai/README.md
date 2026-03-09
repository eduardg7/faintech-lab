# meta-ai

Infrastructure for better AI agents. Built at Faintech Lab.

## What we're building

### Phase 1 — Memory (current)
Agents lose context between sessions. We're building a persistent, structured memory layer:
- File-based storage (survives restarts, inspectable, version-controlled)
- Namespaced per agent + project
- Structured schema: `{task_id, agent_id, timestamp, type, content, tags}`
- Searchable by recency, relevance, and agent
- Auto-compaction: distill daily notes into long-term memory weekly

### Phase 2 — Self-improvement that sticks
Current self-improvement logs learnings but doesn't change behavior. We're building:
- Pattern detector: identifies repeated failures across agents
- Behavior updater: promotes patterns into AGENT.md, SOUL.md automatically
- Regression guard: verifies promoted behavior didn't break anything

### Phase 3 — Observability
Right now there's no way to know if an agent actually did what it said. We're building:
- Execution ledger: every agent action with timestamp, outcome, evidence
- Drift detector: flags when agent behavior diverges from its SOUL.md
- Cost attribution: tokens spent per task, per agent, per project

## Tech stack
- Python (core library, CLI)
- File-based storage (no external DB dependency)
- JSON schema for structured entries
- Optional: sqlite for search index

## Structure
```
src/
  memory/       # Memory read/write/search
  improvement/  # Pattern detection, behavior promotion
  observability/ # Execution ledger, drift detection
tests/
docs/
  experiments/  # Failed experiments documented here
  decisions/    # ADRs
```
