#!/usr/bin/env bash
#
# log-action.sh - Simple wrapper for agents to log actions to execution ledger
#
# Usage:
#   log-action.sh --agent faintech-devops --task "META-AI-003" --action "task_started" --outcome "in_progress"
#   log-action.sh --agent faintech-qa --task "OS-123" --action "pr_created" --outcome "success" --evidence "https://github.com/..."
#
# This script provides deterministic, one-command logging for agent actions.
# No manual Python calls required - just bash.

set -euo pipefail

# Default ledger path (can be overridden with LEDGER_PATH env var)
LEDGER_PATH="${LEDGER_PATH:-/Users/eduardgridan/faintech-os/data/ops/EXECUTION_LEDGER.jsonl}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse arguments
AGENT_ID=""
TASK_ID=""
ACTION_TYPE=""
OUTCOME=""
EVIDENCE_PATH=""
TOKENS_USED=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --agent)
            AGENT_ID="$2"
            shift 2
            ;;
        --task)
            TASK_ID="$2"
            shift 2
            ;;
        --action)
            ACTION_TYPE="$2"
            shift 2
            ;;
        --outcome)
            OUTCOME="$2"
            shift 2
            ;;
        --evidence)
            EVIDENCE_PATH="$2"
            shift 2
            ;;
        --tokens)
            TOKENS_USED="$2"
            shift 2
            ;;
        --help)
            echo "Usage: log-action.sh --agent <agent_id> --task <task_id> --action <action> --outcome <outcome> [options]"
            echo ""
            echo "Required:"
            echo "  --agent     Agent ID (e.g., faintech-devops, faintech-qa)"
            echo "  --task      Task ID (e.g., META-AI-003)"
            echo "  --action    Action type: task_started, task_completed, pr_created, pr_merged, file_written, error"
            echo "  --outcome   Outcome: success, failure, in_progress"
            echo ""
            echo "Optional:"
            echo "  --evidence  Path to evidence file or PR URL"
            echo "  --tokens    Number of tokens used"
            echo ""
            echo "Environment:"
            echo "  LEDGER_PATH  Path to ledger file (default: $LEDGER_PATH)"
            echo ""
            echo "Examples:"
            echo "  log-action.sh --agent faintech-devops --task 'META-AI-003' --action task_started --outcome in_progress"
            echo "  log-action.sh --agent faintech-qa --task 'OS-123' --action pr_created --outcome success --evidence 'https://github.com/...'"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use --help for usage" >&2
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$AGENT_ID" ]]; then
    echo "Error: --agent is required" >&2
    exit 1
fi

if [[ -z "$TASK_ID" ]]; then
    echo "Error: --task is required" >&2
    exit 1
fi

if [[ -z "$ACTION_TYPE" ]]; then
    echo "Error: --action is required" >&2
    exit 1
fi

if [[ -z "$OUTCOME" ]]; then
    echo "Error: --outcome is required" >&2
    exit 1
fi

# Validate action types
VALID_ACTIONS=("task_started" "task_completed" "pr_created" "pr_merged" "file_written" "error")
if [[ ! " ${VALID_ACTIONS[@]} " =~ " ${ACTION_TYPE} " ]]; then
    echo "Error: Invalid action type '$ACTION_TYPE'. Must be one of: ${VALID_ACTIONS[*]}" >&2
    exit 1
fi

# Validate outcomes
VALID_OUTCOMES=("success" "failure" "in_progress")
if [[ ! " ${VALID_OUTCOMES[@]} " =~ " ${OUTCOME} " ]]; then
    echo "Error: Invalid outcome '$OUTCOME'. Must be one of: ${VALID_OUTCOMES[*]}" >&2
    exit 1
fi

# Build Python command to append to ledger
PYTHON_CMD="
import sys
sys.path.insert(0, '$SCRIPT_DIR/../src')
from observability.ledger import ExecutionLedger

ledger = ExecutionLedger(ledger_path='$LEDGER_PATH')
success = ledger.append(
    agent_id='$AGENT_ID',
    action_type='$ACTION_TYPE',
    task_id='$TASK_ID',
    outcome='$OUTCOME',
    evidence_path='${EVIDENCE_PATH:-None}',
    tokens_used=${TOKENS_USED:-None},
    metadata=None
)
print('OK' if success else 'FAILED')
"

# Execute and report result
RESULT=$(python3 -c "$PYTHON_CMD" 2>&1)

if [[ "$RESULT" == "OK" ]]; then
    echo "✓ Logged action: $AGENT_ID / $ACTION_TYPE / $TASK_ID / $OUTCOME"
    exit 0
else
    echo "✗ Failed to log action: $RESULT" >&2
    exit 1
fi
