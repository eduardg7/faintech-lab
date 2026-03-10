#!/usr/bin/env bash
#
# agent-wrapper.sh - Automatic execution logging wrapper for agents
#
# Usage (start mode - logs task_started then executes command):
#   agent-wrapper.sh --agent <agent_id> --task <task_id> -- <command>
#
# Usage (end mode - logs task_completed or error):
#   agent-wrapper.sh --agent <agent_id> --task <task_id> --success
#   agent-wrapper.sh --agent <agent_id> --task <task_id> --error [--message "error text"]
#
# This wrapper automates logging at agent lifecycle points without requiring
# manual calls to log-action.sh. It detects success/failure automatically
# when wrapping command execution.
#
# Environment:
#   AGENT_ID   Can be set as env var instead of --agent flag
#   TASK_ID    Can be set as env var instead of --task flag

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_ACTION="$SCRIPT_DIR/log-action.sh"

# Parse mode and required arguments
MODE=""
AGENT_ID="${AGENT_ID:-}"
TASK_ID="${TASK_ID:-}"
ERROR_MSG=""
COMMAND=()

# Parse arguments
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
        --start)
            MODE="start"
            shift
            ;;
        --success)
            MODE="success"
            shift
            ;;
        --error)
            MODE="error"
            ERROR_MSG="${2:-}"
            [[ -n "$ERROR_MSG" ]] && shift || shift
            ;;
        --message)
            ERROR_MSG="$2"
            shift 2
            ;;
        --help)
            echo "agent-wrapper.sh - Automatic execution logging wrapper for agents"
            echo ""
            echo "Usage:"
            echo "  # Start mode: log task_started then execute command"
            echo "  agent-wrapper.sh --agent <id> --task <id> -- <command>"
            echo ""
            echo "  # End mode: log task_completed or error"
            echo "  agent-wrapper.sh --agent <id> --task <id> --success"
            echo "  agent-wrapper.sh --agent <id> --task <id> --error [--message \"msg\"]"
            echo ""
            echo "Environment variables (alternatives to flags):"
            echo "  AGENT_ID   Agent identifier (e.g., faintech-dev, faintech-qa)"
            echo "  TASK_ID    Task identifier (e.g., META-AI-004)"
            echo ""
            echo "Examples:"
            echo "  # Wrap a Python script execution"
            echo "  agent-wrapper.sh --agent faintech-dev --task META-AI-004 -- python script.py"
            echo ""
            echo "  # Wrap with environment variables"
            echo "  AGENT_ID=faintech-dev TASK_ID=META-AI-004 agent-wrapper.sh -- python script.py"
            echo ""
            echo "  # Manually log success after custom logic"
            echo "  agent-wrapper.sh --agent faintech-dev --task META-AI-004 --success"
            echo ""
            echo "  # Manually log error"
            echo "  agent-wrapper.sh --agent faintech-dev --task META-AI-004 --error --message \"Timed out\""
            exit 0
            ;;
        --)
            shift
            COMMAND=("$@")
            break
            ;;
        *)
            # If mode is start and we encounter non-flag, treat as command
            if [[ "$MODE" == "start" ]]; then
                COMMAND+=("$1")
                shift
            else
                echo "Unknown option: $1" >&2
                echo "Use --help for usage" >&2
                exit 1
            fi
            ;;
    esac
done

# Validate required arguments
if [[ -z "$AGENT_ID" ]]; then
    echo "Error: --agent (or AGENT_ID env var) is required" >&2
    exit 1
fi

if [[ -z "$TASK_ID" ]]; then
    echo "Error: --task (or TASK_ID env var) is required" >&2
    exit 1
fi

if [[ -z "$MODE" ]]; then
    # Default to start mode if no mode specified and command provided
    if [[ ${#COMMAND[@]} -gt 0 ]]; then
        MODE="start"
    else
        echo "Error: Must specify mode (--start, --success, --error) or provide a command" >&2
        exit 1
    fi
fi

# Execute based on mode
case $MODE in
    start)
        # Log task_started, then execute command, then log completion or error
        echo "→ Starting task: $TASK_ID (agent: $AGENT_ID)"
        "$LOG_ACTION" --agent "$AGENT_ID" --task "$TASK_ID" --action "task_started" --outcome "in_progress" || {
            echo "Warning: Failed to log task_started" >&2
        }

        # Execute the command
        EXIT_CODE=0
        if [[ ${#COMMAND[@]} -gt 0 ]]; then
            "${COMMAND[@]}" || EXIT_CODE=$?
        fi

        # Log completion or error based on exit code
        if [[ $EXIT_CODE -eq 0 ]]; then
            echo "✓ Task completed: $TASK_ID"
            "$LOG_ACTION" --agent "$AGENT_ID" --task "$TASK_ID" --action "task_completed" --outcome "success" || {
                echo "Warning: Failed to log task_completed" >&2
            }
            exit 0
        else
            echo "✗ Task failed: $TASK_ID (exit code: $EXIT_CODE)"
            "$LOG_ACTION" --agent "$AGENT_ID" --task "$TASK_ID" --action "error" --outcome "failure" || {
                echo "Warning: Failed to log error" >&2
            }
            exit $EXIT_CODE
        fi
        ;;

    success)
        # Log task_completed manually
        echo "✓ Logging task completion: $TASK_ID"
        "$LOG_ACTION" --agent "$AGENT_ID" --task "$TASK_ID" --action "task_completed" --outcome "success"
        exit 0
        ;;

    error)
        # Log error manually
        echo "✗ Logging error for task: $TASK_ID"
        if [[ -n "$ERROR_MSG" ]]; then
            echo "  Error message: $ERROR_MSG"
        fi
        "$LOG_ACTION" --agent "$AGENT_ID" --task "$TASK_ID" --action "error" --outcome "failure" --evidence "$ERROR_MSG"
        exit 1
        ;;

    *)
        echo "Error: Unknown mode: $MODE" >&2
        exit 1
        ;;
esac
