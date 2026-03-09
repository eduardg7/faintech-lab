#!/usr/bin/env python3
"""
CLI Viewer for Execution Ledger

Usage:
    python ledger_viewer.py --agent X --last 20
    python ledger_viewer.py --task META-AI-001
    python ledger_viewer.py --drift
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from observability.ledger import ExecutionLedger
from observability.drift_detector import DriftDetector


def format_entry(entry) -> str:
    """Format a ledger entry for display"""
    lines = [
        f"[{entry.at}] {entry.agent_id}",
        f"  Action: {entry.action_type}",
        f"  Task: {entry.task_id}",
        f"  Outcome: {entry.outcome}"
    ]

    if entry.evidence_path:
        lines.append(f"  Evidence: {entry.evidence_path}")
    if entry.tokens_used:
        lines.append(f"  Tokens: {entry.tokens_used}")
    if entry.metadata:
        lines.append(f"  Metadata: {entry.metadata}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='View execution ledger entries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View last 20 entries for an agent
  python ledger_viewer.py --agent faintech-devops --last 20

  # View all entries for a task
  python ledger_viewer.py --task META-AI-001

  # Check for agent drift
  python ledger_viewer.py --drift

  # View recent errors
  python ledger_viewer.py --action error --last 10
        """
    )

    parser.add_argument('--agent', help='Filter by agent ID')
    parser.add_argument('--task', help='Filter by task ID')
    parser.add_argument('--action', help='Filter by action type')
    parser.add_argument('--last', type=int, help='Limit to last N entries')
    parser.add_argument('--drift', action='store_true', help='Check for agent drift')
    parser.add_argument('--ledger', default='/Users/eduardgridan/faintech-os/data/ops/EXECUTION_LEDGER.jsonl',
                        help='Path to ledger file')

    args = parser.parse_args()

    ledger = ExecutionLedger(ledger_path=args.ledger)

    # Drift detection mode
    if args.drift:
        # Get unique agents from ledger
        entries = ledger.read_entries()
        agent_ids = list(set(e.agent_id for e in entries))

        if not agent_ids:
            print("No entries found in ledger")
            return

        detector = DriftDetector(ledger)
        report = detector.generate_report(agent_ids)
        print(report)
        return

    # Entry viewing mode
    entries = ledger.read_entries(
        agent_id=args.agent,
        task_id=args.task,
        action_type=args.action,
        limit=args.last
    )

    if not entries:
        print("No entries found matching criteria")
        return

    print(f"Found {len(entries)} entries:\n")
    print("=" * 80)
    for entry in entries:
        print(format_entry(entry))
        print("-" * 80)


if __name__ == '__main__':
    main()
