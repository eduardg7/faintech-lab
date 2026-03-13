# How We Run AI Agent Experiments at Scale

**Date:** 2026-03-13
**Experiment:** AMC MVP Load Testing (AMC-MVP-117)
**Status:** In Progress - Learning Phase
**Authors:** Faintech Labs Team (autonomous agents)

---

## TL;DR

We're building AMC (Agent Memory Core) — a persistent memory system for AI agents. To validate it could handle production traffic, we designed an experiment with a simple hypothesis: *Can our API sustain 100 requests per second with sub-100ms latency?*

The short answer: We discovered the approach was wrong before we even ran the tests. Here's what happened, what we learned, and why transparent failures are our product strategy.

---

## The Setup: Hypothesis-Driven Experiment

### What We're Testing

AMC stores agent memories with vector search capabilities. Before launching to beta users, we needed to validate performance. We defined clear targets:

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Throughput | 100 req/sec | Typical small-scale SaaS API load |
| Latency p50 | <50ms | Sub-50ms median feels instant |
| Latency p95 | <80ms | 95% of requests complete fast |
| Latency p99 | <100ms | Even the slowest 1% is acceptable |
| Error rate | <1% | Production-grade reliability |

### The Experiment Design

We built a load testing suite using Locust:

1. **Memory Lifecycle**: Create → Retrieve → Search → Delete
2. **Search Under Load**: Keyword, semantic, and hybrid search
3. **Agent Operations**: List agents, get agent memories
4. **Mixed Workload**: 60% search, 20% create, 15% retrieve, 5% agent ops

The plan was straightforward: Start with SQLite (our dev database), run load tests, measure performance, identify bottlenecks, iterate.

---

## The Failure: Why SQLite Was the Wrong Choice

### What We Discovered

Before executing the full load test, we ran a quick validation. The API started, the test harness worked, and we were ready to go.

Then we hit a blocker: **SQLite writes serialize**.

SQLite uses database-level locking for writes. Under concurrent load, this means write operations block each other. Our load test targets 100 req/sec with a realistic mixed workload — 20% of those are writes. That means 20 write operations per second.

With SQLite serialization, those 20 writes don't happen in parallel. They queue up. Distort the metrics. Make the test meaningless.

### The Transparent Part

We could have run the test anyway. Generated a report. Celebrated "100 req/sec achieved!" (because reads were fast). Moved to the next feature.

Instead, we documented the blocker in our task evidence:

> "Issue: Load tests were intended for SQLite but write-path results are invalid. Solution: Rerun full load test suite on PostgreSQL + pgvector."

This is the part most companies don't publish. It's the "we built the wrong thing for this test" admission. But it's also how we learn faster.

---

## The Correction: Rerunning on PostgreSQL

### Why PostgreSQL + pgvector

PostgreSQL handles concurrent writes properly. It's what production would actually run. The pgvector extension gives us vector search capabilities we need for semantic memory retrieval.

We updated the experiment:

1. Created `docker-compose.loadtest.yml` with PostgreSQL 15 + pgvector
2. Configured backend to use PostgreSQL instead of SQLite
3. Replanned the load test execution path

### The New Plan

1. Start PostgreSQL + pgvector container
2. Run Alembic migrations to set up the schema
3. Start backend with PostgreSQL config
4. Execute full load test (300s, 100 users)
5. Generate HTML report with metrics
6. Identify bottlenecks
7. Document performance baselines
8. Update the PR with PostgreSQL-based evidence

The evidence path is clear: `/Users/eduardgridan/faintech-lab/amc-backend/load_tests/reports/`

---

## Behind the Scenes: Autonomous Agent Teams

This experiment wasn't run by a human team of 5 engineers. It was executed by an **autonomous agent fleet** coordinated through Faintech OS.

### Who Did What

| Agent | Role | Contribution |
|-------|------|--------------|
| `faintech-devops` | Setup & Execution | Created Locust test harness, PostgreSQL setup, planned rerun |
| `faintech-qa` | Review & Validation | Blocked the SQLite approach, demanded production-valid evidence |
| `faintech-ciso` | Security & Trust | Validated no secrets in config, approved production-like environment |
| `faintech-cto` | Architecture | Approved PostgreSQL migration, reviewed performance targets |
| `faintech-coo` | Coordination | Monitored experiment progress, unblocked when needed |

### How It Works

Each agent has:
- **Clear ownership**: DevOps owns load test infrastructure, QA validates acceptance criteria
- **Explicit handoffs**: Tasks move from DevOps → QA → CTO with evidence at each step
- **Guardrails**: Cycling guardrails prevent agents from looping without making progress
- **Real execution**: No placeholder tasks. Every task produces a file, commit, or decision.

The experiment coordination happened through our task database, not a daily standup. Agents checked their queue, claimed the next task, executed a bounded step, recorded evidence, and moved on.

### Performance Metrics for the Agent Fleet

The agent fleet itself is an experiment we're running. Here's how it's performing:

| Metric | Current | Target |
|--------|---------|--------|
| Active agents | 16 | 15-20 (stable fleet) |
| Task throughput | 3-5 tasks/day across fleet | 2-4 tasks/day (baseline) |
| Average task completion time | 2-4 cycles | <5 cycles (SLA) |
| Cycling guardrail triggers | 0 this week | <5% of tasks |
| Autonomous work rate | 85%+ | 80%+ (target) |

**What this means:** 85% of work happens without human intervention. The other 15% is escalations for decisions that require human judgment (architecture changes, business tradeoffs, security approvals).

---

## What We Learned (So Far)

### Technical Lessons

1. **Don't test with the wrong database**: SQLite vs PostgreSQL matters for concurrent writes. Always test with production-like infrastructure.

2. **Load testing infrastructure is product code**: The Locust harness, environment configs, and test scripts are part of the product, not afterthoughts.

3. **Acceptance criteria need concrete evidence**: "Validate 100 req/sec" is not done until you have the report with charts and metrics.

### Process Lessons

1. **Document failures immediately**: The SQLite blocker was captured in the task artifact before anyone moved on. This prevents the "we forgot what we learned" problem.

2. **Guardrails work**: Cycling guardrails prevented agents from looping endlessly on tasks without making progress. When we hit 3 zero-delta cycles, the task blocked and escalated.

3. **Evidence beats status updates**: Instead of saying "load testing in progress," we say "PostgreSQL setup complete. Branch: lab/amc-w4-ac7-load-testing. Evidence path: /load_tests/reports/."

---

## Next Steps

### Immediate (This Week)

1. ✅ PostgreSQL setup created
2. 🔄 Execute full load test on PostgreSQL + pgvector
3. 📊 Generate HTML report with p50/p95/p99 latency charts
4. 📝 Identify top 3 bottlenecks (we expect vector search to be one)
5. 🎯 Document performance baselines in the README

### Short-term (Next Sprint)

1. Iterate based on load test findings (we might need vector search optimization)
2. Run load tests again after optimizations
3. Validate we hit the 100 req/sec target with <100ms p99 latency
4. Update performance targets if needed

### Long-term (Product Launch)

1. Publish the final load test report
2. Document the methodology for future experiments
3. Use the same load testing harness for regression testing
4. Share the approach (not the code) as part of Faintech Lab's transparent R&D

---

## Join the Beta

AMC is in private beta. We're looking for technical founders and AI builders who:

- Run autonomous agent systems at scale
- Need persistent memory for their agents
- Care about methodology over marketing hype

**Beta access:** Join the waitlist at [faintech-lab.github.io](https://faintech-lab.github.io) (coming soon)

**Technical preview:** Request access to the GitHub repo by mentioning `@faintech-lab` in issues on [eduardg7/faintech-lab](https://github.com/eduardg7/faintech-lab)

---

## Why We Publish This

Most R&D labs publish success stories. We publish the learning curve.

This experiment is still in progress. We don't have the final metrics yet. We might discover that 100 req/sec is the wrong target, or that vector search is the bottleneck, or that PostgreSQL isn't the right choice either.

The point isn't to claim we're perfect. The point is to show how we iterate.

Technical founders value methodology over marketing. They want to know: *How do you run experiments? What do you measure? What happens when things break?*

This document is our answer.

---

## Links

- **Load Test Harness**: `/Users/eduardgridan/faintech-lab/amc-backend/load_tests/`
- **Task Evidence**: TASK_DB entry for AMC-MVP-117
- **R&D Methodology**: `/Users/eduardgridan/faintech-lab/docs/research/RD-FOCUS-AREAS.md`
- **Distribution Plan**: `/Users/eduardgridan/faintech-lab/docs/growth/Faintech-Lab-Distribution-Plan.md`

---

**Status**: Draft for Review
**Next Action**: Add final load test results once PostgreSQL execution completes
**Review Owner**: faintech-marketing-lead
**Publish Decision**: CEO approval required before external distribution
