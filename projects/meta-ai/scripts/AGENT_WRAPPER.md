# Agent Execution Wrapper

Automatic execution logging wrapper for Faintech agents that invokes `log-action.sh` at key agent lifecycle points without requiring manual calls.

## Purpose

The execution ledger (META-AI-003) provides `log-action.sh` for manual logging, but agents often forget to call it. This wrapper automates the pattern:

- **Start:** Automatically logs `task_started` before executing a command
- **Completion:** Automatically logs `task_completed` when the command succeeds
- **Error:** Automatically logs `error` when the command fails (non-zero exit code)

## Usage

### Start Mode (Wrap Command Execution)

Log `task_started`, execute command, then log `task_completed` or `error` based on result:

```bash
# Explicit flags
agent-wrapper.sh --agent faintech-dev --task META-AI-004 -- python script.py

# Environment variables
AGENT_ID=faintech-dev TASK_ID=META-AI-004 agent-wrapper.sh -- python script.py

# Multi-word command
agent-wrapper.sh --agent faintech-qa --task OS-123 -- python -m pytest tests/test_feature.py
```

### End Mode (Manual Logging)

Log completion or error after custom logic:

```bash
# Log success manually
agent-wrapper.sh --agent faintech-dev --task META-AI-004 --success

# Log error manually
agent-wrapper.sh --agent faintech-dev --task META-AI-004 --error --message "Timed out after 30s"

# Log error with detailed message
agent-wrapper.sh --agent faintech-dev --task META-AI-004 --error --message "API rate limit exceeded (429)"
```

## Arguments

| Flag | Required | Description |
|-------|----------|-------------|
| `--agent <id>` | Yes¹ | Agent ID (e.g., `faintech-dev`, `faintech-qa`, `faintech-pm`) |
| `--task <id>` | Yes¹ | Task ID (e.g., `META-AI-004`, `OS-123`) |
| `--start` | No² | Start mode: execute command and auto-log completion/error |
| `--success` | No² | End mode: log `task_completed` |
| `--error` | No² | End mode: log `error` |
| `--message <text>` | No | Error message (only with `--error`) |
| `--` | No² | Delimiter; everything after this is the command to execute |

¹ Either flag or environment variable (`AGENT_ID`, `TASK_ID`)

² If no mode is specified and a command is provided, defaults to `--start`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_ID` | Agent identifier (alternative to `--agent`) |
| `TASK_ID` | Task identifier (alternative to `--task`) |
| `LEDGER_PATH` | Path to execution ledger (inherited from `log-action.sh`) |

## Logging Behavior

### Automatic (Start Mode)

```bash
agent-wrapper.sh --agent faintech-dev --task META-AI-004 -- python script.py
```

This sequence executes:

1. **Log `task_started`** with outcome `in_progress`
2. **Execute** `python script.py`
3. **If exit code = 0:** Log `task_completed` with outcome `success`
4. **If exit code ≠ 0:** Log `error` with outcome `failure`

The wrapper preserves the original exit code from the wrapped command.

### Manual (End Mode)

```bash
# After custom logic succeeds
agent-wrapper.sh --agent faintech-dev --task META-AI-004 --success

# After custom logic fails
agent-wrapper.sh --agent faintech-dev --task META-AI-004 --error --message "Database connection failed"
```

## Integration Examples

### Cron Jobs

Wrap cron commands to automatically log execution:

```bash
# In crontab
0 */2 * * * * agent-wrapper.sh --agent faintech-pm --task planning-cron -- /path/to/planning-script.sh
```

### Long-Running Processes

Wrap initialization and termination:

```bash
# Start
agent-wrapper.sh --agent faintech-dev --task LONG-OP-001 -- python long_process.py &
PID=$!

# ... later, monitor and log manually if needed
if ! kill -0 $PID 2>/dev/null; then
    agent-wrapper.sh --agent faintech-dev --task LONG-OP-001 --error --message "Process died"
fi
```

### Test Suites

Wrap test execution:

```bash
agent-wrapper.sh --agent faintech-qa --task OS-123 -- python -m pytest tests/
```

This logs start and completion (success if all tests pass, error if any fail).

## Examples

### Example 1: Simple Command

```bash
$ agent-wrapper.sh --agent faintech-dev --task META-AI-004 -- echo "Hello World"
→ Starting task: META-AI-004 (agent: faintech-dev)
✓ Logged action: faintech-dev / task_started / META-AI-004 / in_progress
Hello World
✓ Task completed: META-AI-004
✓ Logged action: faintech-dev / task_completed / META-AI-004 / success
```

### Example 2: Command That Fails

```bash
$ agent-wrapper.sh --agent faintech-dev --task META-AI-004 -- python missing_script.py
→ Starting task: META-AI-004 (agent: faintech-dev)
✓ Logged action: faintech-dev / task_started / META-AI-004 / in_progress
python: can't open file 'missing_script.py'
✗ Task failed: META-AI-004 (exit code: 2)
✓ Logged action: faintech-dev / error / META-AI-004 / failure
```

### Example 3: Manual Error Logging

```bash
$ agent-wrapper.sh --agent faintech-dev --task META-AI-004 --error --message "API rate limit"
✗ Logging error for task: META-AI-004
  Error message: API rate limit
✓ Logged action: faintech-dev / error / META-AI-004 / failure
```

## Error Handling

The wrapper distinguishes between:

1. **Wrapper errors:** Invalid arguments, missing flags → exits with code 1, **no log entry**
2. **Command errors:** Wrapped command fails → logs `error` entry, exits with command's exit code
3. **Logging failures:** If `log-action.sh` fails, wrapper continues (warning printed) but returns the command's exit code

## See Also

- `log-action.sh` - Manual logging script this wrapper automates
- `projects/meta-ai/src/observability/ledger.py` - ExecutionLedger Python implementation
- META-AI-003 - Execution ledger implementation
- META-AI-004 - This wrapper (auto-execution logging)
