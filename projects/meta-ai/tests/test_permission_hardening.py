"""Tests for file permission hardening in MemoryStore."""

import os
import stat
import sys
import tempfile
from pathlib import Path
from datetime import datetime

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from memory.store import MemoryStore
from memory.models import MemoryEntry, MemoryType


class TestPermissionHardening:
    """Verify that memory files and directories have secure permissions."""

    @pytest.fixture
    def temp_store(self, tmp_path):
        """Create a MemoryStore with a temporary base path."""
        return MemoryStore(base_path=tmp_path / "test-memory")

    def test_file_permissions_on_write(self, temp_store):
        """Verify that memory files are created with 0o600 permissions."""
        entry = MemoryEntry(
            agent_id="test-agent",
            project_id="test-project",
            type=MemoryType.DECISION,
            content="Test content for permission check"
        )

        temp_store.write(entry)

        # Find the created file
        agent_dir = temp_store.base_path / "test-agent"
        memory_files = list(agent_dir.glob("*.jsonl"))
        assert len(memory_files) == 1, "Expected one memory file to be created"

        # Verify file permissions
        file_stat = os.stat(memory_files[0])
        file_mode = stat.S_IMODE(file_stat.st_mode)
        expected_mode = 0o600

        assert file_mode == expected_mode, (
            f"File permissions should be 0o600 (owner read/write only), "
            f"got {oct(file_mode)}"
        )

    def test_directory_permissions_on_create(self, temp_store):
        """Verify that agent directories are created with 0o700 permissions."""
        entry = MemoryEntry(
            agent_id="new-agent",
            project_id="test-project",
            type=MemoryType.DECISION,
            content="Test content for directory permission check"
        )

        temp_store.write(entry)

        # Check directory permissions
        agent_dir = temp_store.base_path / "new-agent"
        assert agent_dir.exists(), "Agent directory should exist"

        dir_stat = os.stat(agent_dir)
        dir_mode = stat.S_IMODE(dir_stat.st_mode)
        expected_mode = 0o700

        assert dir_mode == expected_mode, (
            f"Directory permissions should be 0o700 (owner only), "
            f"got {oct(dir_mode)}"
        )

    def test_base_directory_exists_with_permissions(self, temp_store):
        """Verify that base memory directory has restricted permissions."""
        base_dir = temp_store.base_path

        # Base directory should exist after store creation
        assert base_dir.exists(), "Base memory directory should exist"

        # Check base directory permissions (should be 0o700 or more restrictive)
        dir_stat = os.stat(base_dir)
        dir_mode = stat.S_IMODE(dir_stat.st_mode)

        # Base dir should be owner-only (0o700) or at least not world-writable
        assert not (dir_mode & stat.S_IWOTH), (
            f"Base directory should not be world-writable, got {oct(dir_mode)}"
        )

    def test_multiple_writes_maintain_permissions(self, temp_store):
        """Verify that permissions are maintained across multiple writes."""
        agent_id = "multi-write-agent"

        for i in range(3):
            entry = MemoryEntry(
                agent_id=agent_id,
                project_id="test-project",
                type=MemoryType.LEARNING,
                content=f"Entry {i}"
            )
            temp_store.write(entry)

        # Check file permissions after multiple writes
        agent_dir = temp_store.base_path / agent_id
        memory_files = list(agent_dir.glob("*.jsonl"))

        for memory_file in memory_files:
            file_stat = os.stat(memory_file)
            file_mode = stat.S_IMODE(file_stat.st_mode)
            assert file_mode == 0o600, (
                f"File {memory_file} should have 0o600 permissions, "
                f"got {oct(file_mode)}"
            )

    def test_file_permissions_preserved_on_existing_file(self, temp_store):
        """Verify permissions are set correctly even when appending to existing file."""
        agent_id = "existing-file-agent"

        # First write
        entry1 = MemoryEntry(
            agent_id=agent_id,
            project_id="test-project",
            type=MemoryType.DECISION,
            content="First entry"
        )
        temp_store.write(entry1)

        # Second write to same file
        entry2 = MemoryEntry(
            agent_id=agent_id,
            project_id="test-project",
            type=MemoryType.DECISION,
            content="Second entry"
        )
        temp_store.write(entry2)

        # Verify file permissions
        agent_dir = temp_store.base_path / agent_id
        memory_file = list(agent_dir.glob("*.jsonl"))[0]

        file_stat = os.stat(memory_file)
        file_mode = stat.S_IMODE(file_stat.st_mode)
        assert file_mode == 0o600, (
            f"File should maintain 0o600 permissions after append, "
            f"got {oct(file_mode)}"
        )

    def test_no_group_or_world_access_on_files(self, temp_store):
        """Verify no group or world permissions on memory files."""
        entry = MemoryEntry(
            agent_id="secure-agent",
            project_id="test-project",
            type=MemoryType.ERROR,
            content="Sensitive error information"
        )
        temp_store.write(entry)

        agent_dir = temp_store.base_path / "secure-agent"
        memory_file = list(agent_dir.glob("*.jsonl"))[0]

        file_stat = os.stat(memory_file)
        file_mode = stat.S_IMODE(file_stat.st_mode)

        # No group permissions
        assert not (file_mode & stat.S_IRGRP), "File should not be group-readable"
        assert not (file_mode & stat.S_IWGRP), "File should not be group-writable"
        assert not (file_mode & stat.S_IXGRP), "File should not be group-executable"

        # No world permissions
        assert not (file_mode & stat.S_IROTH), "File should not be world-readable"
        assert not (file_mode & stat.S_IWOTH), "File should not be world-writable"
        assert not (file_mode & stat.S_IXOTH), "File should not be world-executable"

    def test_no_group_or_world_access_on_directories(self, temp_store):
        """Verify no group or world permissions on agent directories."""
        entry = MemoryEntry(
            agent_id="secure-dir-agent",
            project_id="test-project",
            type=MemoryType.PATTERN,
            content="Pattern data"
        )
        temp_store.write(entry)

        agent_dir = temp_store.base_path / "secure-dir-agent"
        dir_stat = os.stat(agent_dir)
        dir_mode = stat.S_IMODE(dir_stat.st_mode)

        # No group permissions
        assert not (dir_mode & stat.S_IRGRP), "Directory should not be group-readable"
        assert not (dir_mode & stat.S_IWGRP), "Directory should not be group-writable"
        assert not (dir_mode & stat.S_IXGRP), "Directory should not be group-executable"

        # No world permissions
        assert not (dir_mode & stat.S_IROTH), "Directory should not be world-readable"
        assert not (dir_mode & stat.S_IWOTH), "Directory should not be world-writable"
        assert not (dir_mode & stat.S_IXOTH), "Directory should not be world-executable"


class TestPermissionConstants:
    """Verify permission constants are correctly defined."""

    def test_file_permission_constant(self):
        """Verify FILE_PERMISSIONS is 0o600."""
        assert MemoryStore.FILE_PERMISSIONS == 0o600, (
            "FILE_PERMISSIONS should be 0o600 (owner read/write only)"
        )

    def test_directory_permission_constant(self):
        """Verify DIR_PERMISSIONS is 0o700."""
        assert MemoryStore.DIR_PERMISSIONS == 0o700, (
            "DIR_PERMISSIONS should be 0o700 (owner read/write/execute only)"
        )
