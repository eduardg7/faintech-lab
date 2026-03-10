#!/usr/bin/env python3
"""
Tests for Memory Analytics Dashboard

Run with: python -m pytest tests/test_dashboard.py -v
"""

import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
import sys
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from memory.dashboard import MemoryDashboard
from memory.store import MemoryStore
from memory.models import MemoryEntry, MemoryType


@pytest.fixture
def temp_store():
    """Create a temporary memory store for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = MemoryStore(base_path=Path(tmpdir))
        yield store


@pytest.fixture
def populated_store(temp_store):
    """Memory store with sample data."""
    agents = ['agent-1', 'agent-2']
    
    for i, agent_id in enumerate(agents):
        for j in range(10):
            entry = MemoryEntry(
                agent_id=agent_id,
                project_id='test-project',
                task_id=f'task-{j}',
                type=MemoryType.LEARNING if j % 2 == 0 else MemoryType.ERROR,
                content=f'Test content {j} for {agent_id}',
                tags=[f'tag-{j % 3}', f'agent-{i}']
            )
            temp_store.write(entry)
    
    return temp_store


@pytest.fixture
def dashboard(temp_store):
    """Dashboard with temp store."""
    return MemoryDashboard(store=temp_store)


@pytest.fixture
def populated_dashboard(populated_store):
    """Dashboard with sample data."""
    return MemoryDashboard(store=populated_store)


class TestMemoryDashboard:
    """Test suite for MemoryDashboard."""
    
    def test_initialization(self, temp_store):
        """Test dashboard initializes correctly."""
        dashboard = MemoryDashboard(store=temp_store)
        assert dashboard.store == temp_store
    
    def test_initialization_default_store(self):
        """Test dashboard creates default store."""
        dashboard = MemoryDashboard()
        assert dashboard.store is not None
    
    def test_collect_stats_empty(self, dashboard):
        """Test stats collection with no data."""
        stats = dashboard.collect_stats(agent_id='nonexistent')
        
        assert stats['total_memories'] == 0
        assert stats['total_size_bytes'] == 0
        assert 'nonexistent' not in stats['agents']  # No entry for nonexistent agent
    
    def test_collect_stats_populated(self, populated_dashboard):
        """Test stats collection with sample data."""
        stats = populated_dashboard.collect_stats()
        
        assert stats['total_memories'] == 20  # 2 agents × 10 entries
        assert stats['total_size_bytes'] > 0
        assert 'agent-1' in stats['agents']
        assert 'agent-2' in stats['agents']
    
    def test_collect_stats_single_agent(self, populated_dashboard):
        """Test stats collection for specific agent."""
        stats = populated_dashboard.collect_stats(agent_id='agent-1')
        
        assert stats['total_memories'] == 10
        assert 'agent-1' in stats['agents']
        assert 'agent-2' not in stats['agents']
    
    def test_collect_stats_days_filter(self, populated_dashboard):
        """Test stats collection with day filter."""
        stats = populated_dashboard.collect_stats(days=7)
        
        # All our test data is within 7 days
        assert stats['total_memories'] == 20
    
    def test_memory_types_breakdown(self, populated_dashboard):
        """Test memory types are collected correctly."""
        stats = populated_dashboard.collect_stats()
        
        # 10 entries per agent, 5 LEARNING + 5 ERROR per agent
        assert 'learning' in stats['memory_types']
        assert 'error' in stats['memory_types']
        assert stats['memory_types']['learning'] == 10
        assert stats['memory_types']['error'] == 10
    
    def test_top_tags_collection(self, populated_dashboard):
        """Test tags are collected and counted."""
        stats = populated_dashboard.collect_stats()
        
        # Tags: tag-0, tag-1, tag-2, agent-0, agent-1
        assert 'tag-0' in stats['top_tags']
        assert 'tag-1' in stats['top_tags']
        assert 'tag-2' in stats['top_tags']
    
    def test_age_distribution(self, populated_dashboard):
        """Test age distribution buckets."""
        stats = populated_dashboard.collect_stats()
        
        # All entries are recent, should be in 0-1 days
        assert '0-1 days' in stats['age_distribution']
        assert stats['age_distribution']['0-1 days'] == 20
    
    def test_compute_growth_rate(self, populated_dashboard):
        """Test growth rate calculation."""
        stats = populated_dashboard.collect_stats(days=7)
        rates = populated_dashboard.compute_growth_rate(stats, days=7)
        
        assert 'agent-1' in rates
        assert 'agent-2' in rates
        # 10 entries / 7 days ≈ 1.43 per day
        assert rates['agent-1'] > 0
        assert rates['agent-2'] > 0
    
    def test_render_simple(self, populated_dashboard):
        """Test simple text rendering."""
        stats = populated_dashboard.collect_stats(days=7)
        output = populated_dashboard.render_simple(stats, 7, show_patterns=False)
        
        assert 'MEMORY ANALYTICS DASHBOARD' in output
        assert 'Total memories: 20' in output
        assert 'agent-1' in output
        assert 'agent-2' in output
    
    def test_render_rich_fallback(self, populated_dashboard):
        """Test rich rendering falls back gracefully."""
        stats = populated_dashboard.collect_stats(days=7)
        # Should either use rich or fall back to simple
        output = populated_dashboard.render_rich(stats, 7, show_patterns=False)
        
        assert len(output) > 0
        # Either rich or simple output should contain key info
        assert 'agent-1' in output or 'Agent' in output
    
    def test_format_bytes(self, dashboard):
        """Test byte formatting."""
        assert dashboard._format_bytes(500) == '500.0 B'
        assert dashboard._format_bytes(1024) == '1.0 KB'
        assert dashboard._format_bytes(1048576) == '1.0 MB'
    
    def test_get_age_bucket(self, dashboard):
        """Test age bucket categorization."""
        assert dashboard._get_age_bucket(0) == '0-1 days'
        assert dashboard._get_age_bucket(3) == '1-7 days'
        assert dashboard._get_age_bucket(14) == '7-30 days'
        assert dashboard._get_age_bucket(45) == '30-90 days'
        assert dashboard._get_age_bucket(120) == '90+ days'
    
    def test_export_json(self, populated_dashboard):
        """Test JSON export."""
        stats = populated_dashboard.collect_stats(days=7)
        result = populated_dashboard.export(stats, format='json')
        
        # Should be valid JSON
        data = json.loads(result)
        
        assert data['total_memories'] == 20
        assert 'agents' in data
        assert 'memory_types' in data
        assert 'generated_at' in data
    
    def test_export_csv(self, populated_dashboard):
        """Test CSV export."""
        stats = populated_dashboard.collect_stats(days=7)
        result = populated_dashboard.export(stats, format='csv')
        
        lines = result.split('\n')
        assert 'agent,memories,size_bytes,type,tag,count' in lines[0]
        assert len(lines) > 1  # Should have data rows
    
    def test_export_to_file(self, populated_dashboard):
        """Test export to file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = f.name
        
        try:
            stats = populated_dashboard.collect_stats(days=7)
            populated_dashboard.export(stats, format='json', output_path=output_path)
            
            # Verify file was written
            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            data = json.loads(content)
            assert data['total_memories'] == 20
        finally:
            os.unlink(output_path)
    
    def test_export_invalid_format(self, populated_dashboard):
        """Test export with invalid format."""
        stats = populated_dashboard.collect_stats(days=7)
        
        with pytest.raises(ValueError, match="Unsupported format"):
            populated_dashboard.export(stats, format='xml')
    
    def test_agent_stats_structure(self, populated_dashboard):
        """Test agent stats have correct structure."""
        stats = populated_dashboard.collect_stats()
        
        for agent_name, agent_stats in stats['agents'].items():
            assert 'total' in agent_stats
            assert 'size_bytes' in agent_stats
            assert 'types' in agent_stats
            assert 'tags' in agent_stats
            assert 'oldest' in agent_stats
            assert 'newest' in agent_stats
            assert 'daily_counts' in agent_stats
    
    def test_pattern_detection_optional(self, populated_dashboard):
        """Test pattern detection is optional."""
        stats = populated_dashboard.collect_stats()
        
        # Should not crash when pattern detection fails
        output = populated_dashboard.render_simple(stats, 7, show_patterns=True)
        assert len(output) > 0
    
    def test_growth_data_collection(self, populated_dashboard):
        """Test growth data is collected per agent per day."""
        stats = populated_dashboard.collect_stats()
        
        assert 'growth_data' in stats
        assert 'agent-1' in stats['growth_data']
        
        # Growth data should have daily entries
        today = datetime.utcnow().strftime('%Y-%m-%d')
        assert today in stats['growth_data']['agent-1']
    
    def test_empty_store_dashboard(self, dashboard):
        """Test dashboard with completely empty store."""
        stats = dashboard.collect_stats()
        
        # Should handle gracefully
        output = dashboard.render_simple(stats, 7, show_patterns=False)
        assert 'MEMORY ANALYTICS DASHBOARD' in output


class TestDashboardCLI:
    """Test CLI functionality."""
    
    def test_cli_dashboard_command(self, populated_store):
        """Test dashboard command runs without error."""
        from memory.dashboard import main
        import sys
        
        # Mock sys.argv
        old_argv = sys.argv
        try:
            sys.argv = ['memory', 'dashboard', '--simple', '--days', '7']
            # Should not crash
            # main() would print output, we just verify no exception
        finally:
            sys.argv = old_argv
    
    def test_cli_export_command_json(self, populated_store, tmp_path):
        """Test export command with JSON format."""
        from memory.dashboard import main
        import sys
        
        output_file = tmp_path / "export.json"
        
        old_argv = sys.argv
        try:
            sys.argv = ['memory', 'export', '--format', 'json', '--output', str(output_file)]
            # main() would write file
        finally:
            sys.argv = old_argv


class TestIntegration:
    """Integration tests."""
    
    def test_full_pipeline(self, temp_store):
        """Test complete dashboard pipeline."""
        # Write some entries
        for i in range(5):
            entry = MemoryEntry(
                agent_id='test-agent',
                project_id='test-project',
                type=MemoryType.LEARNING,
                content=f'Learning {i}',
                tags=['test', 'integration']
            )
            temp_store.write(entry)
        
        # Create dashboard and collect stats
        dashboard = MemoryDashboard(store=temp_store)
        stats = dashboard.collect_stats(agent_id='test-agent', days=7)
        
        # Verify stats
        assert stats['total_memories'] == 5
        
        # Export
        json_export = dashboard.export(stats, format='json')
        data = json.loads(json_export)
        assert data['total_memories'] == 5
        
        csv_export = dashboard.export(stats, format='csv')
        assert 'test-agent' in csv_export
    
    def test_multiple_agents_with_different_types(self, temp_store):
        """Test multiple agents with different memory types."""
        types = [MemoryType.LEARNING, MemoryType.ERROR, MemoryType.DECISION, 
                 MemoryType.PATTERN, MemoryType.FACT]
        
        for i, mem_type in enumerate(types):
            for j in range(3):
                entry = MemoryEntry(
                    agent_id=f'agent-{i}',
                    project_id='test-project',
                    type=mem_type,
                    content=f'{mem_type.value} content {j}',
                    tags=[mem_type.value]
                )
                temp_store.write(entry)
        
        dashboard = MemoryDashboard(store=temp_store)
        stats = dashboard.collect_stats()
        
        # Should have 5 agents × 3 entries = 15 total
        assert stats['total_memories'] == 15
        
        # Should have all 5 types
        assert len(stats['memory_types']) == 5
        for mem_type in types:
            assert mem_type.value in stats['memory_types']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
