"""Comprehensive tests for persistent agent memory library."""

import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

from src.memory import MemoryEntry, MemoryType, MemoryStore


class TestMemoryEntry:
    """Test MemoryEntry model."""
    
    def test_create_entry(self):
        """Test creating a basic memory entry."""
        entry = MemoryEntry(
            agent_id="test-agent",
            project_id="test-project",
            task_id="task-123",
            type=MemoryType.LEARNING,
            content="Learned something important",
            tags=["test", "example"]
        )
        
        assert entry.agent_id == "test-agent"
        assert entry.project_id == "test-project"
        assert entry.task_id == "task-123"
        assert entry.type == MemoryType.LEARNING
        assert entry.content == "Learned something important"
        assert entry.tags == ["test", "example"]
        assert entry.id  # Auto-generated UUID
        assert entry.timestamp  # Auto-generated timestamp
    
    def test_entry_serialization(self):
        """Test JSON serialization and deserialization."""
        entry = MemoryEntry(
            agent_id="test-agent",
            project_id="test-project",
            type=MemoryType.ERROR,
            content="Something went wrong",
            tags=["error", "test"]
        )
        
        json_str = entry.to_json()
        data = json.loads(json_str)
        
        assert data['agent_id'] == "test-agent"
        assert data['type'] == "error"
        
        # Deserialize
        restored = MemoryEntry.from_json(json_str)
        assert restored.agent_id == entry.agent_id
        assert restored.type == entry.type
        assert restored.content == entry.content
        assert restored.tags == entry.tags
    
    def test_all_memory_types(self):
        """Test all memory types are valid."""
        types = [MemoryType.LEARNING, MemoryType.ERROR, MemoryType.DECISION, 
                 MemoryType.PATTERN, MemoryType.FACT]
        
        for mem_type in types:
            entry = MemoryEntry(type=mem_type, content="test")
            assert entry.type == mem_type


class TestMemoryStore:
    """Test MemoryStore functionality."""
    
    @pytest.fixture
    def temp_store(self):
        """Create a temporary memory store for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield MemoryStore(base_path=Path(tmpdir))
    
    def test_write_entry(self, temp_store):
        """Test writing a memory entry."""
        entry = MemoryEntry(
            agent_id="agent-1",
            project_id="project-1",
            type=MemoryType.LEARNING,
            content="This is a test learning"
        )
        
        entry_id = temp_store.write(entry)
        
        # Verify file was created
        memory_file = temp_store.base_path / "agent-1" / f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
        assert memory_file.exists()
        
        # Verify content
        with open(memory_file, 'r') as f:
            line = f.readline()
            restored = MemoryEntry.from_json(line)
            assert restored.id == entry_id
            assert restored.content == "This is a test learning"
    
    def test_search_by_keyword(self, temp_store):
        """Test searching by keyword."""
        # Write multiple entries
        entries = [
            MemoryEntry(agent_id="agent-1", project_id="proj-1", 
                       type=MemoryType.LEARNING, content="Python is great"),
            MemoryEntry(agent_id="agent-1", project_id="proj-1",
                       type=MemoryType.ERROR, content="JavaScript error occurred"),
            MemoryEntry(agent_id="agent-2", project_id="proj-1",
                       type=MemoryType.FACT, content="Python was created in 1991"),
        ]
        
        for entry in entries:
            temp_store.write(entry)
        
        # Search for Python
        results = temp_store.search(query="Python")
        assert len(results) == 2
        assert all("Python" in r.content for r in results)
    
    def test_search_by_agent(self, temp_store):
        """Test filtering by agent ID."""
        # Write entries for different agents
        for i in range(3):
            entry = MemoryEntry(
                agent_id=f"agent-{i}",
                project_id="proj-1",
                type=MemoryType.LEARNING,
                content=f"Learning {i}"
            )
            temp_store.write(entry)
        
        # Search for specific agent
        results = temp_store.search(query="Learning", agent_id="agent-1")
        assert len(results) == 1
        assert results[0].agent_id == "agent-1"
    
    def test_search_by_type(self, temp_store):
        """Test filtering by entry type."""
        # Write different types
        for entry_type in [MemoryType.LEARNING, MemoryType.ERROR, MemoryType.DECISION]:
            entry = MemoryEntry(
                agent_id="agent-1",
                project_id="proj-1",
                type=entry_type,
                content=f"Content for {entry_type.value}"
            )
            temp_store.write(entry)
        
        # Search for errors only
        results = temp_store.search(query="Content", entry_type=MemoryType.ERROR)
        assert len(results) == 1
        assert results[0].type == MemoryType.ERROR
    
    def test_search_by_tags(self, temp_store):
        """Test filtering by tags (AND logic)."""
        entry1 = MemoryEntry(
            agent_id="agent-1", project_id="proj-1",
            type=MemoryType.LEARNING, content="Test 1",
            tags=["python", "testing"]
        )
        entry2 = MemoryEntry(
            agent_id="agent-1", project_id="proj-1",
            type=MemoryType.LEARNING, content="Test 2",
            tags=["python", "production"]
        )
        
        temp_store.write(entry1)
        temp_store.write(entry2)
        
        # Search with single tag
        results = temp_store.search(query="Test", tags=["python"])
        assert len(results) == 2
        
        # Search with multiple tags (AND logic)
        results = temp_store.search(query="Test", tags=["python", "testing"])
        assert len(results) == 1
        assert "testing" in results[0].tags
    
    def test_search_by_project_and_task(self, temp_store):
        """Test filtering by project and task."""
        entry = MemoryEntry(
            agent_id="agent-1",
            project_id="project-x",
            task_id="task-123",
            type=MemoryType.DECISION,
            content="Important decision"
        )
        temp_store.write(entry)
        
        # Filter by project
        results = temp_store.search(query="decision", project_id="project-x")
        assert len(results) == 1
        
        # Filter by task
        results = temp_store.search(query="decision", task_id="task-123")
        assert len(results) == 1
    
    def test_search_limit(self, temp_store):
        """Test result limiting."""
        # Write 20 entries
        for i in range(20):
            entry = MemoryEntry(
                agent_id="agent-1",
                project_id="proj-1",
                type=MemoryType.FACT,
                content=f"Fact number {i}"
            )
            temp_store.write(entry)
        
        # Search with limit
        results = temp_store.search(query="Fact", limit=5)
        assert len(results) == 5
        
        # Test max limit
        results = temp_store.search(query="Fact", limit=150)
        assert len(results) == 20  # Only 20 exist
    
    def test_search_recency_sorting(self, temp_store):
        """Test that results are sorted by recency."""
        import time
        
        # Write entries with slight time differences
        for i in range(3):
            entry = MemoryEntry(
                agent_id="agent-1",
                project_id="proj-1",
                type=MemoryType.LEARNING,
                content=f"Learning {i}"
            )
            temp_store.write(entry)
            if i < 2:
                time.sleep(0.01)  # Small delay to ensure different timestamps
        
        # Search and verify sorting
        results = temp_store.search(query="Learning", limit=10)
        assert len(results) == 3
        
        # Most recent should be first
        timestamps = [r.timestamp for r in results]
        assert timestamps == sorted(timestamps, reverse=True)
    
    def test_get_for_task(self, temp_store):
        """Test getting all entries for a task."""
        # Write entries for different tasks
        for task_id in ["task-1", "task-2"]:
            for i in range(3):
                entry = MemoryEntry(
                    agent_id="agent-1",
                    project_id="proj-1",
                    task_id=task_id,
                    type=MemoryType.LEARNING,
                    content=f"Learning for {task_id}"
                )
                temp_store.write(entry)
        
        # Get entries for specific task
        results = temp_store.get_for_task("proj-1", "task-1")
        assert len(results) == 3
        assert all(r.task_id == "task-1" for r in results)
    
    def test_get_recent_for_agent(self, temp_store):
        """Test getting recent entries for an agent."""
        # Write entries for multiple agents
        for agent_id in ["agent-1", "agent-2"]:
            for i in range(5):
                entry = MemoryEntry(
                    agent_id=agent_id,
                    project_id="proj-1",
                    type=MemoryType.FACT,
                    content=f"Fact for {agent_id}"
                )
                temp_store.write(entry)
        
        # Get recent for specific agent
        results = temp_store.get_recent_for_agent("agent-1", limit=3)
        assert len(results) == 3
        assert all(r.agent_id == "agent-1" for r in results)
    
    def test_compact_old_entries(self, temp_store):
        """Test compaction of old entries."""
        # Write entries with old timestamps (manipulating file names)
        old_date = (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d")
        old_file = temp_store.base_path / "agent-1" / f"{old_date}.jsonl"
        old_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(old_file, 'w') as f:
            for i in range(5):
                entry = MemoryEntry(
                    agent_id="agent-1",
                    project_id="proj-1",
                    type=MemoryType.LEARNING,
                    content=f"Old learning {i}"
                )
                f.write(entry.to_json() + '\n')
        
        # Run compaction
        result = temp_store.compact("agent-1", days_old=7)
        
        assert result['compacted'] == 5
        assert result['summaries_created'] > 0
        assert result['files_archived'] == 1
        
        # Verify old file was archived
        archive_dir = temp_store.base_path / "agent-1" / "archive"
        assert (archive_dir / f"{old_date}.jsonl").exists()
    
    def test_compact_no_old_entries(self, temp_store):
        """Test compaction when no old entries exist."""
        # Write recent entry
        entry = MemoryEntry(
            agent_id="agent-1",
            project_id="proj-1",
            type=MemoryType.LEARNING,
            content="Recent learning"
        )
        temp_store.write(entry)
        
        # Try to compact
        result = temp_store.compact("agent-1", days_old=7)
        
        assert result['compacted'] == 0
        assert "No entries old enough" in result['message']
    
    def test_compact_nonexistent_agent(self, temp_store):
        """Test compaction for agent with no memory."""
        result = temp_store.compact("nonexistent-agent")
        
        assert result['compacted'] == 0
        assert "No memory files found" in result['message']
    
    def test_malformed_entry_handling(self, temp_store):
        """Test that malformed entries are skipped during search."""
        # Write valid entry
        valid_entry = MemoryEntry(
            agent_id="agent-1",
            project_id="proj-1",
            type=MemoryType.FACT,
            content="Valid entry"
        )
        temp_store.write(valid_entry)
        
        # Write malformed entry directly to file
        memory_file = temp_store.base_path / "agent-1" / f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
        with open(memory_file, 'a') as f:
            f.write("invalid json\n")
            f.write('{"type": "invalid_type", "content": "test"}\n')
        
        # Search should still work
        results = temp_store.search(query="Valid")
        assert len(results) == 1
        assert results[0].content == "Valid entry"


class TestIntegration:
    """Integration tests for full workflow."""
    
    def test_full_workflow(self):
        """Test complete write -> search -> compact workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir))
            
            # Write multiple entries
            entries = [
                MemoryEntry(
                    agent_id="backend-agent",
                    project_id="faintech-os",
                    task_id="TASK-001",
                    type=MemoryType.LEARNING,
                    content="Learned to use pytest fixtures effectively",
                    tags=["testing", "python"]
                ),
                MemoryEntry(
                    agent_id="backend-agent",
                    project_id="faintech-os",
                    task_id="TASK-001",
                    type=MemoryType.ERROR,
                    content="Forgot to close file handle, caused resource leak",
                    tags=["bug", "python"]
                ),
                MemoryEntry(
                    agent_id="backend-agent",
                    project_id="faintech-os",
                    task_id="TASK-002",
                    type=MemoryType.DECISION,
                    content="Decided to use JSONL format for memory storage",
                    tags=["architecture"]
                ),
            ]
            
            for entry in entries:
                store.write(entry)
            
            # Search for task entries
            task_results = store.get_for_task("faintech-os", "TASK-001")
            assert len(task_results) == 2
            
            # Search by keyword
            pytest_results = store.search(query="pytest", agent_id="backend-agent")
            assert len(pytest_results) == 1
            assert "pytest" in pytest_results[0].content
            
            # Get recent for agent
            recent = store.get_recent_for_agent("backend-agent", limit=10)
            assert len(recent) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=src.memory', '--cov-report=term-missing'])
