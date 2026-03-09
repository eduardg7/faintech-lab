# Workflow Automation Scripts

Deterministic, one-command wrappers for agent workflow integration.

## log-action.sh

Simple bash wrapper for agents to log actions to the execution ledger without manual Python calls.

### Purpose

Replaces manual loops with deterministic automation. Agents can log their task lifecycle events with one bash command instead of importing Python modules and calling APIs.

### Installation

Already installed at: `projects/meta-ai/scripts/log-action.sh`

Make sure it's executable:
```bash
chmod +x projects/meta-ai/scripts/log-action.sh
```

### Usage

```bash
log-action.sh --agent <agent_id> --task <task_id> --action <action> --outcome <outcome> [options]
```

### Required Arguments

| Flag | Description | Example |
|-------|-------------|---------|
| `--agent` | Agent ID logging the action | `faintech-devops`, `faintech-qa` |
| `--task` | Task ID this action relates to | `META-AI-003`, `OS-123` |
| `--action` | Action type | `task_started`, `task_completed`, `pr_created`, `pr_merged`, `file_written`, `error` |
| `--outcome` | Result of action | `success`, `failure`, `in_progress` |

### Optional Arguments

| Flag | Description | Example |
|-------|-------------|---------|
| `--evidence` | Path to evidence file or PR URL | `https://github.com/eduardg7/faintech-os/pull/5` |
| `--tokens` | Number of tokens used | `4500` |

### Examples

**Start working on a task:**
```bash
log-action.sh --agent faintech-devops --task "META-AI-003" --action task_started --outcome in_progress
```

**Complete a task with success:**
```bash
log-action.sh --agent faintech-backend --task "META-AI-001" --action task_completed --outcome success --evidence "https://github.com/eduardg7/faintech-lab/pull/4"
```

**Log a PR creation:**
```bash
log-action.sh --agent faintech-qa --task "META-AI-002" --action pr_created --outcome success --evidence "https://github.com/eduardg7/faintech-lab/pull/3"
```

**Log an error:**
```bash
log-action.sh --agent faintech-dev --task "OS-456" --action error --outcome failure --evidence "/path/to/error.log"
```

### Environment Variables

| Variable | Description | Default |
|-----------|-------------|----------|
| `LEDGER_PATH` | Path to execution ledger file | `/Users/eduardgridan/faintech-os/data/ops/EXECUTION_LEDGER.jsonl` |

### Integration Pattern

Add this to your agent's task workflow:

1. **At task start:**
   ```bash
   log-action.sh --agent $AGENT_ID --task "$TASK_ID" --action task_started --outcome in_progress
   ```

2. **At PR creation:**
   ```bash
   log-action.sh --agent $AGENT_ID --task "$TASK_ID" --action pr_created --outcome success --evidence "$PR_URL"
   ```

3. **At task completion:**
   ```bash
   log-action.sh --agent $AGENT_ID --task "$TASK_ID" --action task_completed --outcome success --evidence "$PR_URL"
   ```

4. **On error:**
   ```bash
   log-action.sh --agent $AGENT_ID --task "$TASK_ID" --action error --outcome failure --evidence "$ERROR_FILE"
   ```

### Validation

The script validates:
- Required arguments are present
- Action type is valid (`task_started`, `task_completed`, `pr_created`, `pr_merged`, `file_written`, `error`)
- Outcome is valid (`success`, `failure`, `in_progress`)

### Exit Codes

- `0` - Success (action logged)
- `1` - Validation error or write failure

### Related Files

- `../src/observability/ledger.py` - Core execution ledger implementation
- `../src/observability/ledger_viewer.py` - CLI viewer for ledger entries
- `../../data/ops/EXECUTION_LEDGER.jsonl` - Actual ledger file (in faintech-os repo)

### Maintenance

This script is owned and maintained by `faintech-workflow-runner`.

For issues or improvements, create a task assigned to `faintech-workflow-runner` with area `workflow`.
