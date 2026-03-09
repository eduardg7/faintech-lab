"""
Execution Ledger - Atomic append-only log for agent actions

Provides thread-safe, atomic writes to prevent corruption from concurrent agents.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any
import fcntl
from dataclasses import dataclass, asdict


@dataclass
class LedgerEntry:
    """Single execution ledger entry"""
    at: str  # ISO timestamp
    agent_id: str
    action_type: str  # task_started, task_completed, pr_created, pr_merged, file_written, error
    task_id: str
    outcome: str  # success, failure, in_progress
    evidence_path: Optional[str]
    tokens_used: Optional[int]
    metadata: Optional[Dict[str, Any]] = None

    def to_jsonl(self) -> str:
        """Convert to JSONL format"""
        return json.dumps(asdict(self))


class ExecutionLedger:
    """Thread-safe execution ledger with atomic writes"""

    ACTION_TYPES = {
        'task_started',
        'task_completed',
        'pr_created',
        'pr_merged',
        'file_written',
        'error'
    }

    OUTCOMES = {
        'success',
        'failure',
        'in_progress'
    }

    def __init__(self, ledger_path: str = '/Users/eduardgridan/faintech-os/data/ops/EXECUTION_LEDGER.jsonl'):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.touch()

    def append(
        self,
        agent_id: str,
        action_type: str,
        task_id: str,
        outcome: str,
        evidence_path: Optional[str] = None,
        tokens_used: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Atomically append an entry to the ledger.

        Uses file locking to prevent concurrent write corruption.

        Args:
            agent_id: Agent performing the action
            action_type: Type of action (task_started, task_completed, etc.)
            task_id: Task ID this action relates to
            outcome: Result (success, failure, in_progress)
            evidence_path: Path to evidence file (optional)
            tokens_used: Token count for this action (optional)
            metadata: Additional context (optional)

        Returns:
            True if write succeeded, False otherwise
        """
        # Validate inputs
        if action_type not in self.ACTION_TYPES:
            raise ValueError(f"Invalid action_type: {action_type}. Must be one of {self.ACTION_TYPES}")
        if outcome not in self.OUTCOMES:
            raise ValueError(f"Invalid outcome: {outcome}. Must be one of {self.OUTCOMES}")

        entry = LedgerEntry(
            at=datetime.now(timezone.utc).isoformat(),
            agent_id=agent_id,
            action_type=action_type,
            task_id=task_id,
            outcome=outcome,
            evidence_path=evidence_path,
            tokens_used=tokens_used,
            metadata=metadata
        )

        # Atomic write with file locking
        try:
            with open(self.ledger_path, 'a') as f:
                # Acquire exclusive lock
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    f.write(entry.to_jsonl() + '\n')
                    f.flush()
                    os.fsync(f.fileno())  # Ensure write to disk
                finally:
                    # Release lock
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return True
        except Exception as e:
            print(f"Error writing to ledger: {e}")
            return False

    def read_entries(
        self,
        agent_id: Optional[str] = None,
        action_type: Optional[str] = None,
        task_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> list[LedgerEntry]:
        """
        Read entries from the ledger with optional filtering.

        Args:
            agent_id: Filter by agent ID
            action_type: Filter by action type
            task_id: Filter by task ID
            limit: Maximum number of entries to return

        Returns:
            List of matching LedgerEntry objects
        """
        entries = []
        try:
            with open(self.ledger_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    data = json.loads(line)
                    entry = LedgerEntry(**data)

                    # Apply filters
                    if agent_id and entry.agent_id != agent_id:
                        continue
                    if action_type and entry.action_type != action_type:
                        continue
                    if task_id and entry.task_id != task_id:
                        continue

                    entries.append(entry)

                    if limit and len(entries) >= limit:
                        break
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error reading ledger: {e}")

        return entries

    def get_agent_stats(self, agent_id: str, hours: int = 24) -> Dict[str, Any]:
        """
        Get statistics for an agent over the last N hours.

        Args:
            agent_id: Agent to analyze
            hours: Time window in hours

        Returns:
            Dictionary with stats including completion rate
        """
        from datetime import timedelta

        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        entries = self.read_entries(agent_id=agent_id)

        # Filter to time window
        recent_entries = []
        for entry in entries:
            entry_time = datetime.fromisoformat(entry.at.replace('Z', '+00:00'))
            if entry_time >= cutoff:
                recent_entries.append(entry)

        # Calculate stats
        total_actions = len(recent_entries)
        task_started = sum(1 for e in recent_entries if e.action_type == 'task_started')
        task_completed = sum(1 for e in recent_entries if e.action_type == 'task_completed' and e.outcome == 'success')
        task_failed = sum(1 for e in recent_entries if e.action_type == 'task_completed' and e.outcome == 'failure')

        completion_rate = (task_completed / task_started) if task_started > 0 else 0.0

        return {
            'agent_id': agent_id,
            'hours': hours,
            'total_actions': total_actions,
            'task_started': task_started,
            'task_completed': task_completed,
            'task_failed': task_failed,
            'completion_rate': completion_rate
        }
