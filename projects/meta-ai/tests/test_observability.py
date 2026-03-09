#!/usr/bin/env python3
"""
Tests for Execution Ledger
"""

import pytest
import tempfile
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from observability.ledger import ExecutionLedger, LedgerEntry
from observability.drift_detector import DriftDetector


@pytest.fixture
def temp_ledger():
    """Create a temporary ledger file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_path = f.name
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_append_and_read(temp_ledger):
    """Test appending and reading entries"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    # Append entry
    success = ledger.append(
        agent_id='test-agent',
        action_type='task_started',
        task_id='TEST-001',
        outcome='in_progress'
    )
    assert success

    # Read back
    entries = ledger.read_entries(agent_id='test-agent')
    assert len(entries) == 1
    assert entries[0].agent_id == 'test-agent'
    assert entries[0].task_id == 'TEST-001'


def test_filter_by_agent(temp_ledger):
    """Test filtering by agent ID"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    # Add entries for multiple agents
    ledger.append(agent_id='agent-1', action_type='task_started', task_id='TASK-1', outcome='in_progress')
    ledger.append(agent_id='agent-2', action_type='task_started', task_id='TASK-2', outcome='in_progress')
    ledger.append(agent_id='agent-1', action_type='task_completed', task_id='TASK-1', outcome='success')

    # Filter by agent
    entries = ledger.read_entries(agent_id='agent-1')
    assert len(entries) == 2

    entries = ledger.read_entries(agent_id='agent-2')
    assert len(entries) == 1


def test_filter_by_action_type(temp_ledger):
    """Test filtering by action type"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    ledger.append(agent_id='agent', action_type='task_started', task_id='TASK-1', outcome='in_progress')
    ledger.append(agent_id='agent', action_type='task_completed', task_id='TASK-1', outcome='success')
    ledger.append(agent_id='agent', action_type='error', task_id='TASK-1', outcome='failure')

    entries = ledger.read_entries(action_type='error')
    assert len(entries) == 1
    assert entries[0].action_type == 'error'


def test_limit(temp_ledger):
    """Test limit parameter"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    # Add 10 entries
    for i in range(10):
        ledger.append(agent_id='agent', action_type='task_started', task_id=f'TASK-{i}', outcome='in_progress')

    # Limit to 5
    entries = ledger.read_entries(limit=5)
    assert len(entries) == 5


def test_invalid_action_type(temp_ledger):
    """Test that invalid action types raise errors"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    with pytest.raises(ValueError, match="Invalid action_type"):
        ledger.append(
            agent_id='agent',
            action_type='invalid_action',
            task_id='TASK-1',
            outcome='success'
        )


def test_invalid_outcome(temp_ledger):
    """Test that invalid outcomes raise errors"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    with pytest.raises(ValueError, match="Invalid outcome"):
        ledger.append(
            agent_id='agent',
            action_type='task_started',
            task_id='TASK-1',
            outcome='invalid_outcome'
        )


def test_agent_stats(temp_ledger):
    """Test agent statistics calculation"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    # Add some entries
    ledger.append(agent_id='agent', action_type='task_started', task_id='TASK-1', outcome='in_progress')
    ledger.append(agent_id='agent', action_type='task_completed', task_id='TASK-1', outcome='success')
    ledger.append(agent_id='agent', action_type='task_started', task_id='TASK-2', outcome='in_progress')
    ledger.append(agent_id='agent', action_type='task_completed', task_id='TASK-2', outcome='failure')

    stats = ledger.get_agent_stats('agent', hours=24)
    assert stats['task_started'] == 2
    assert stats['task_completed'] == 1
    assert stats['task_failed'] == 1
    assert stats['completion_rate'] == 0.5


def test_drift_detection(temp_ledger):
    """Test drift detector"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    # Agent with good completion rate (50%)
    ledger.append(agent_id='good-agent', action_type='task_started', task_id='TASK-1', outcome='in_progress')
    ledger.append(agent_id='good-agent', action_type='task_completed', task_id='TASK-1', outcome='success')
    ledger.append(agent_id='good-agent', action_type='task_started', task_id='TASK-2', outcome='in_progress')
    ledger.append(agent_id='good-agent', action_type='task_completed', task_id='TASK-2', outcome='failure')

    # Agent with poor completion rate (0%)
    ledger.append(agent_id='bad-agent', action_type='task_started', task_id='TASK-3', outcome='in_progress')
    ledger.append(agent_id='bad-agent', action_type='task_started', task_id='TASK-4', outcome='in_progress')
    ledger.append(agent_id='bad-agent', action_type='task_started', task_id='TASK-5', outcome='in_progress')

    detector = DriftDetector(ledger, threshold=0.3)
    drifted = detector.detect_drift(['good-agent', 'bad-agent'])

    assert len(drifted) == 1
    assert drifted[0]['agent_id'] == 'bad-agent'
    assert drifted[0]['completion_rate'] == 0.0


def test_atomic_writes(temp_ledger):
    """Test that concurrent writes don't corrupt the ledger"""
    import threading
    import time

    ledger = ExecutionLedger(ledger_path=temp_ledger)

    def write_entries(agent_id, count):
        for i in range(count):
            ledger.append(
                agent_id=agent_id,
                action_type='task_started',
                task_id=f'TASK-{agent_id}-{i}',
                outcome='in_progress'
            )

    # Create multiple threads writing concurrently
    threads = []
    for i in range(5):
        t = threading.Thread(target=write_entries, args=(f'agent-{i}', 10))
        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # Verify no corruption
    entries = ledger.read_entries()
    assert len(entries) == 50  # 5 agents * 10 entries each

    # Verify all entries are valid JSON
    for entry in entries:
        assert entry.agent_id is not None
        assert entry.task_id is not None


def test_evidence_and_metadata(temp_ledger):
    """Test optional evidence_path and metadata fields"""
    ledger = ExecutionLedger(ledger_path=temp_ledger)

    ledger.append(
        agent_id='agent',
        action_type='task_completed',
        task_id='TASK-1',
        outcome='success',
        evidence_path='/path/to/evidence.md',
        tokens_used=1234,
        metadata={'key': 'value', 'number': 42}
    )

    entries = ledger.read_entries(task_id='TASK-1')
    assert len(entries) == 1
    assert entries[0].evidence_path == '/path/to/evidence.md'
    assert entries[0].tokens_used == 1234
    assert entries[0].metadata == {'key': 'value', 'number': 42}


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
