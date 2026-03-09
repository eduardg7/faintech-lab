"""
Drift Detector - Identify agents with low completion rates

Flags agents whose completed_tasks rate < 0.3 over last 24h.
"""

from typing import List, Dict, Any
from .ledger import ExecutionLedger


class DriftDetector:
    """Detect agent drift based on completion rates"""

    def __init__(self, ledger: ExecutionLedger, threshold: float = 0.3, hours: int = 24):
        """
        Initialize drift detector.

        Args:
            ledger: ExecutionLedger instance
            threshold: Completion rate threshold (default 0.3)
            hours: Time window in hours (default 24)
        """
        self.ledger = ledger
        self.threshold = threshold
        self.hours = hours

    def detect_drift(self, agent_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Detect agents with drift (low completion rate).

        Args:
            agent_ids: List of agent IDs to check

        Returns:
            List of agents with drift, including stats
        """
        drifted_agents = []

        for agent_id in agent_ids:
            stats = self.ledger.get_agent_stats(agent_id, hours=self.hours)

            # Check if completion rate is below threshold
            if stats['task_started'] > 0 and stats['completion_rate'] < self.threshold:
                drifted_agents.append({
                    'agent_id': agent_id,
                    'completion_rate': stats['completion_rate'],
                    'threshold': self.threshold,
                    'task_started': stats['task_started'],
                    'task_completed': stats['task_completed'],
                    'task_failed': stats['task_failed'],
                    'hours': self.hours,
                    'status': 'drift_detected'
                })

        return drifted_agents

    def generate_report(self, agent_ids: List[str]) -> str:
        """
        Generate a human-readable drift report.

        Args:
            agent_ids: List of agent IDs to check

        Returns:
            Formatted report string
        """
        drifted = self.detect_drift(agent_ids)

        if not drifted:
            return f"No agent drift detected (threshold: {self.threshold}, window: {self.hours}h)"

        lines = [
            f"Agent Drift Report",
            f"Threshold: {self.threshold}",
            f"Time Window: {self.hours}h",
            f"Drifted Agents: {len(drifted)}",
            "",
            "-" * 80,
            ""
        ]

        for agent in drifted:
            lines.extend([
                f"Agent: {agent['agent_id']}",
                f"  Completion Rate: {agent['completion_rate']:.2%} (threshold: {agent['threshold']:.2%})",
                f"  Tasks Started: {agent['task_started']}",
                f"  Tasks Completed: {agent['task_completed']}",
                f"  Tasks Failed: {agent['task_failed']}",
                ""
            ])

        return "\n".join(lines)
