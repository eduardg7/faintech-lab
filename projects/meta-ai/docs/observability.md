# Agent Observability

## Overview

The execution ledger provides a centralized, atomic log of all agent actions across Faintech projects. This enables:
- Auditing agent behavior
- Detecting drift (low completion rates)
- Tracking token usage
- Verifying task execution

## Architecture

### Ledger Location
- **Path**: `/Users/eduardgridan/faintech-os/data/ops/EXECUTION_LEDGER.jsonl`
- **Format**: JSONL (JSON Lines) - one entry per line
- **Writes**: Atomic with file locking to prevent concurrent corruption

### Entry Schema

Each ledger entry contains:
```json
{
  "at": "2026-03-09T21:10:00Z",
  "agent_id": "faintech-devops",
  "action_type": "task_started",
  "task_id": "META-AI-003",
  "outcome": "in_progress",
  "evidence_path": "/path/to/evidence.md",
  "tokens_used": 1234,
  "metadata": {"key": "value"}
}
```

### Action Types
- `task_started` - Agent began work on a task
- `task_completed` - Agent finished a task (success or failure)
- `pr_created` - Pull request created
- `pr_merged` - Pull request merged
- `file_written` - File created/modified
- `error` - Error occurred

### Outcomes
- `success` - Action completed successfully
- `failure` - Action failed
- `in_progress` - Action is ongoing

## Usage

### Writing to the Ledger

```python
from observability import ExecutionLedger

ledger = ExecutionLedger()

# Log task start
ledger.append(
    agent_id='faintech-devops',
    action_type='task_started',
    task_id='META-AI-003',
    outcome='in_progress',
    evidence_path='/path/to/session-state.md'
)

# Log task completion
ledger.append(
    agent_id='faintech-devops',
    action_type='task_completed',
    task_id='META-AI-003',
    outcome='success',
    tokens_used=5000
)
```

### Reading the Ledger

#### CLI Viewer

```bash
# View last 20 entries for an agent
python projects/meta-ai/src/observability/ledger_viewer.py --agent faintech-devops --last 20

# View all entries for a task
python projects/meta-ai/src/observability/ledger_viewer.py --task META-AI-001

# View recent errors
python projects/meta-ai/src/observability/ledger_viewer.py --action error --last 10

# Check for agent drift
python projects/meta-ai/src/observability/ledger_viewer.py --drift
```

#### Programmatic Access

```python
from observability import ExecutionLedger

ledger = ExecutionLedger()

# Get entries for an agent
entries = ledger.read_entries(agent_id='faintech-devops', limit=20)

# Get stats for an agent
stats = ledger.get_agent_stats('faintech-devops', hours=24)
print(f"Completion rate: {stats['completion_rate']:.2%}")
```

### Drift Detection

The drift detector flags agents with completion rates below a threshold (default: 30%) over a time window (default: 24h).

```python
from observability import ExecutionLedger, DriftDetector

ledger = ExecutionLedger()
detector = DriftDetector(ledger, threshold=0.3, hours=24)

# Check specific agents
drifted = detector.detect_drift(['faintech-devops', 'faintech-qa'])

# Generate report
report = detector.generate_report(['faintech-devops', 'faintech-qa'])
print(report)
```

## Integration with Existing Systems

### health-check.log
The ledger complements (not replaces) the existing health-check.log:
- **health-check.log**: System-level health and cron job status
- **EXECUTION_LEDGER.jsonl**: Agent-level action tracking

Both files should be monitored for complete observability.

### TASK_DB.json
The ledger integrates with TASK_DB.json:
- When an agent starts a task: write `task_started` to ledger
- When an agent completes a task: write `task_completed` to ledger + update TASK_DB
- Evidence paths in ledger should point to actual files

## Best Practices

### For Agents
1. **Log task boundaries**: Always log `task_started` and `task_completed`
2. **Include evidence**: Provide paths to evidence files (SESSION-STATE.md, etc.)
3. **Track tokens**: Report token usage when available
4. **Be specific**: Use metadata for additional context

### For Operators
1. **Monitor drift**: Run drift detection daily
2. **Review low performers**: Investigate agents with <30% completion rate
3. **Check evidence**: Verify evidence paths exist and contain real work
4. **Correlate with TASK_DB**: Cross-reference ledger entries with task status

## Testing

Run tests with:
```bash
cd /Users/eduardgridan/faintech-lab/projects/meta-ai
python -m pytest tests/test_observability.py -v
```

## Troubleshooting

### Ledger file corrupted
- The ledger uses atomic writes with file locking
- If corruption occurs, check for processes holding locks: `lsof /Users/eduardgridan/faintech-os/data/ops/EXECUTION_LEDGER.jsonl`
- Backup and recreate if needed

### Drift detector false positives
- Adjust threshold: `DriftDetector(ledger, threshold=0.2)`
- Adjust time window: `DriftDetector(ledger, hours=48)`
- Consider task complexity: some tasks legitimately take longer

### Missing entries
- Check file permissions on ledger path
- Verify agent is calling `ledger.append()`
- Look for exceptions in agent logs
