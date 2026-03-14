# AMC Load-Test Runbook

## Purpose
Provide one reproducible entrypoint for AMC backend smoke/load validation so QA can run AC7 without rebuilding the harness each time.

## Files
- `load_tests/locustfile.py` — request mix and assertions
- `load_tests/.env.loadtest.example` — environment template
- `scripts/run-load-tests.sh` — smoke/full/custom runner

## Setup
1. Install test dependencies:
   ```bash
   pip install -r requirements-test.txt
   ```
2. Copy the environment file:
   ```bash
   cp load_tests/.env.loadtest.example load_tests/.env.loadtest
   ```
3. Adjust `AMC_LOADTEST_HOST` and `AMC_LOADTEST_API_KEY` for the target environment.

## Scenarios
### Smoke
```bash
./scripts/run-load-tests.sh smoke
```
Use before review/merge to confirm the harness and target are alive.

### Full
```bash
./scripts/run-load-tests.sh full
```
Use for AC7 validation or before beta release readiness sign-off.

### Custom
```bash
AMC_LOADTEST_USERS=25 AMC_LOADTEST_SPAWN_RATE=5 AMC_LOADTEST_DURATION=120s ./scripts/run-load-tests.sh custom
```
Use when QA wants a bounded repro for a suspected bottleneck.

## Expected thresholds
- smoke: target stays responsive, no immediate auth/config failures
- full: <1% errors, p99 <100ms target, throughput trend suitable for beta baseline

## Evidence to capture in TASK_DB
- exact command run
- target host
- HTML report path
- notable failures or bottlenecks
- follow-up owner (QA for validation, backend/devops if bottleneck appears)
