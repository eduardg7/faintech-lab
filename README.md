# Faintech Lab

R&D workspace for Faintech Solutions SRL. Two active projects.

## Projects

### 1. meta-ai — Better Agents
**Goal:** Build reusable infrastructure that makes AI agents smarter, more autonomous, and more persistent.

Key bets:
- Persistent agent memory across sessions (file-based, structured, searchable)
- Self-improvement loops that actually update behavior (not just log it)
- Inter-agent communication protocols with delivery guarantees
- Agent observability: what is each agent doing, why, and did it work?

→ `projects/meta-ai/`

### 2. new-product — Customer Product
**Goal:** Build a new product for external customers, distinct from FainTrading.

Direction TBD by CPO. Starting point: identify a problem the meta-ai infrastructure naturally solves for non-technical teams.

→ `projects/new-product/`

## Working conventions

- Branch pattern: `lab/<project>/<task-slug>`
- One PR per bounded task slice
- Every merged PR updates the relevant `docs/` file
- Experiments that fail get documented in `docs/experiments/`

## Agent workspace

- TASK_DB: `/Users/eduardgridan/faintech-os/data/ops/TASK_DB.json`
- Project state: `/Users/eduardgridan/faintech-os/data/ops/FAINTECH_OS_STATE.json`
- Specs: `.specs/`
