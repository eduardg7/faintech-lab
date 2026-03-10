"""Memory store for persistent agent memory with file-based storage."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from collections import defaultdict
import re
import html

from .models import MemoryEntry, MemoryType
from .secrets import scan_and_validate, SecurityError


# Content validation constants
MAX_CONTENT_SIZE = 10 * 1024  # 10KB per entry
MAX_SPECIAL_CHAR_RATIO = 0.3  # Max 30% special characters

# Malicious patterns to detect
DANGEROUS_PATTERNS = {
    'script_tags': re.compile(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.IGNORECASE | re.DOTALL),
    'sql_injection': re.compile(
        r'\b(union\s+select|select\s+.*\s+from|insert\s+into|delete\s+from|drop\s+table|'
        r'update\s+.*\s+set|exec\s*\(|execute\s*\()',
        re.IGNORECASE
    ),
    'command_injection': re.compile(
        r'(\||;|`|\$\(|\$\{|&&|\|\||>>|>|<)\s*('
        r'rm\s|wget\s|curl\s|bash\s|sh\s|python\s|perl\s|ruby\s|'
        r'eval\s|exec\s|system\s|passthru\s|shell_exec\s)',
        re.IGNORECASE
    ),
}


def validate_content(content: str, log_path: Optional[Path] = None) -> Tuple[bool, str, str]:
    """
    Validate memory entry content for security threats.
    
    Args:
        content: Content string to validate
        log_path: Optional path to validation log file
        
    Returns:
        Tuple of (is_valid, sanitized_content, rejection_reason)
        
    Validation checks:
        1. Content size limit (max 10KB)
        2. Script tag injection
        3. SQL injection attempts
        4. Command injection attempts
        5. Excessive special characters (DoS prevention)
    """
    # Check content size
    if len(content) > MAX_CONTENT_SIZE:
        reason = f"Content exceeds size limit ({len(content)} > {MAX_CONTENT_SIZE} bytes)"
        _log_rejection(content, reason, log_path)
        return False, "", reason
    
    # Check for script tags
    if DANGEROUS_PATTERNS['script_tags'].search(content):
        reason = "Content contains script tags"
        _log_rejection(content, reason, log_path)
        # Sanitize by escaping HTML
        sanitized = html.escape(content)
        return False, sanitized, reason
    
    # Check for SQL injection
    if DANGEROUS_PATTERNS['sql_injection'].search(content):
        reason = "Content contains potential SQL injection"
        _log_rejection(content, reason, log_path)
        return False, "", reason
    
    # Check for command injection
    if DANGEROUS_PATTERNS['command_injection'].search(content):
        reason = "Content contains potential command injection"
        _log_rejection(content, reason, log_path)
        return False, "", reason
    
    # Check for excessive special characters (DoS prevention)
    # Allow common safe characters: punctuation, quotes, JSON/URL chars
    safe_chars = set('.,!?;:\'"-()[]{}/@#$_+=~`| \n\t\r')
    special_char_count = sum(1 for c in content if not c.isalnum() and c not in safe_chars)
    if len(content) > 0 and (special_char_count / len(content)) > MAX_SPECIAL_CHAR_RATIO:
        reason = f"Content has excessive special characters ({special_char_count}/{len(content)})"
        _log_rejection(content, reason, log_path)
        return False, "", reason
    
    # Content is safe - sanitize HTML but allow through
    sanitized = html.escape(content) if '<' in content or '>' in content else content
    
    return True, sanitized, ""


def _log_rejection(content: str, reason: str, log_path: Optional[Path] = None) -> None:
    """
    Log rejected content to validation log file.
    
    Args:
        content: Rejected content
        reason: Rejection reason
        log_path: Path to log file (defaults to ~/.agent-memory/validation.log)
    """
    if log_path is None:
        log_path = Path.home() / ".agent-memory" / "validation.log"
    
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    log_entry = f"[{timestamp}] REJECTED: {reason}\n"
    log_entry += f"Content preview: {content[:200]}...\n\n"
    
    with open(log_path, 'a') as f:
        f.write(log_entry)


class MemoryStore:
    """
    Persistent memory store for AI agents using file-based JSONL storage.
    
    Storage path: ~/.agent-memory/<agent_id>/<YYYY-MM-DD>.jsonl
    
    Features:
    - Write memory entries with structured schema
    - Search by keywords, recency, agent, type, tags
    - Auto-compaction of old entries into weekly summaries
    - Content validation and secrets detection for security
    """
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize memory store.
        
        Args:
            base_path: Base directory for memory storage. Defaults to ~/.agent-memory
        """
        self.base_path = base_path or Path.home() / ".agent-memory"
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    # Security constants for file permission hardening
    FILE_PERMISSIONS = 0o600  # Owner read/write only
    DIR_PERMISSIONS = 0o700  # Owner read/write/execute only

    def write(self, entry: MemoryEntry, check_secrets: bool = True) -> str:
        """
        Write a memory entry to persistent storage.

        Args:
            entry: MemoryEntry to persist
            check_secrets: Whether to scan for secrets before writing (default: True)

        Returns:
            Entry ID

        Raises:
            ValueError: If content fails validation
            SecurityError: If secrets detected in content (when check_secrets=True)

        Performance:
            <100ms for append-only write (including secrets scan <10ms)

        Security:
            - Memory files created with 0o600 permissions (owner read/write only)
            - Directories created with 0o700 permissions (owner only)
            - Content validation prevents injection attacks
            - Secrets detection prevents accidental credential leakage
        """
        # Step 1: Validate content before writing (injection prevention)
        is_valid, sanitized_content, rejection_reason = validate_content(
            entry.content, 
            log_path=self.base_path / "validation.log"
        )
        
        if not is_valid:
            raise ValueError(f"Content validation failed: {rejection_reason}")
        
        # Use sanitized content
        entry.content = sanitized_content
        
        # Step 2: Security check - scan for secrets before writing
        if check_secrets:
            scan_and_validate(entry.content, agent_id=entry.agent_id)
            
            # Also check metadata for secrets
            if entry.metadata:
                import json as _json
                metadata_str = _json.dumps(entry.metadata)
                scan_and_validate(metadata_str, agent_id=entry.agent_id)

        # Get agent-specific directory
        agent_dir = self.base_path / entry.agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)

        # Enforce directory permissions (security hardening)
        os.chmod(agent_dir, self.DIR_PERMISSIONS)

        # Use daily JSONL file
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        memory_file = agent_dir / f"{date_str}.jsonl"

        # Append entry
        with open(memory_file, 'a') as f:
            f.write(entry.to_json() + '\n')

        # Enforce file permissions (security hardening)
        os.chmod(memory_file, self.FILE_PERMISSIONS)

        return entry.id
    
    def search(
        self,
        query: str,
        agent_id: Optional[str] = None,
        project_id: Optional[str] = None,
        task_id: Optional[str] = None,
        entry_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10,
        since: Optional[str] = None,
        until: Optional[str] = None
    ) -> List[MemoryEntry]:
        """
        Search memory entries by keywords and filters.
        
        Args:
            query: Search query (keyword matching in content)
            agent_id: Filter by agent ID
            project_id: Filter by project ID
            task_id: Filter by task ID
            entry_type: Filter by entry type
            tags: Filter by tags (AND logic)
            limit: Maximum number of results (default 10, max 100)
            since: ISO 8601 timestamp filter
            until: ISO 8601 timestamp filter
            
        Returns:
            List of matching MemoryEntry objects, sorted by recency
            
        Performance:
            <100ms for typical queries
        """
        limit = min(limit, 100)
        results = []
        
        # Determine which agent directories to search
        if agent_id:
            agent_dirs = [self.base_path / agent_id]
        else:
            agent_dirs = [d for d in self.base_path.iterdir() if d.is_dir()]
        
        # Search all relevant files
        for agent_dir in agent_dirs:
            if not agent_dir.exists():
                continue
                
            for jsonl_file in agent_dir.glob("*.jsonl"):
                # Date filter optimization
                file_date = jsonl_file.stem
                if since and file_date < since[:10]:
                    continue
                if until and file_date > until[:10]:
                    continue
                
                # Read and filter entries
                with open(jsonl_file, 'r') as f:
                    for line in f:
                        try:
                            entry = MemoryEntry.from_json(line.strip())
                            
                            # Apply filters
                            if project_id and entry.project_id != project_id:
                                continue
                            if task_id and entry.task_id != task_id:
                                continue
                            if entry_type and entry.type != entry_type:
                                continue
                            if tags and not all(tag in entry.tags for tag in tags):
                                continue
                            if since and entry.timestamp < since:
                                continue
                            if until and entry.timestamp > until:
                                continue
                            
                            # Keyword matching (case-insensitive)
                            if query.lower() in entry.content.lower():
                                results.append(entry)
                        except (json.JSONDecodeError, ValueError):
                            # Skip malformed entries
                            continue
        
        # Sort by timestamp (most recent first)
        results.sort(key=lambda e: e.timestamp, reverse=True)
        
        return results[:limit]
    
    def get_for_task(self, project_id: str, task_id: str, limit: int = 50) -> List[MemoryEntry]:
        """
        Get all memory entries for a specific task.
        
        Args:
            project_id: Project ID
            task_id: Task ID
            limit: Maximum results
            
        Returns:
            List of MemoryEntry objects for the task
        """
        return self.search(
            query="",
            project_id=project_id,
            task_id=task_id,
            limit=limit
        )
    
    def get_recent_for_agent(self, agent_id: str, limit: int = 10) -> List[MemoryEntry]:
        """
        Get recent memory entries for a specific agent.
        
        Args:
            agent_id: Agent ID
            limit: Maximum results
            
        Returns:
            List of recent MemoryEntry objects
        """
        return self.search(
            query="",
            agent_id=agent_id,
            limit=limit
        )
    
    def compact(self, agent_id: str, days_old: int = 7) -> Dict[str, Any]:
        """
        Compact old memory entries into weekly summaries.
        
        Args:
            agent_id: Agent ID to compact
            days_old: Age threshold in days (default 7)
            
        Returns:
            Summary statistics
            
        Process:
            1. Find all entries older than threshold
            2. Group by type and extract key insights
            3. Create summary entry
            4. Archive original files
        """
        threshold_date = datetime.utcnow() - timedelta(days=days_old)
        threshold_str = threshold_date.strftime("%Y-%m-%d")
        
        agent_dir = self.base_path / agent_id
        if not agent_dir.exists():
            return {"compacted": 0, "message": "No memory files found"}
        
        # Collect old entries
        old_entries_by_type = defaultdict(list)
        files_to_archive = []
        
        for jsonl_file in agent_dir.glob("*.jsonl"):
            if jsonl_file.stem < threshold_str:
                files_to_archive.append(jsonl_file)
                
                with open(jsonl_file, 'r') as f:
                    for line in f:
                        try:
                            entry = MemoryEntry.from_json(line.strip())
                            old_entries_by_type[entry.type.value].append(entry)
                        except (json.JSONDecodeError, ValueError):
                            continue
        
        if not old_entries_by_type:
            return {"compacted": 0, "message": "No entries old enough to compact"}
        
        # Create summary entries by type
        summaries_created = 0
        for entry_type, entries in old_entries_by_type.items():
            if not entries:
                continue
            
            # Extract key insights (simplified - just count and first 200 chars of each)
            summary_content = f"Weekly {entry_type} summary ({len(entries)} entries):\n"
            for entry in entries[:5]:  # Top 5 most recent
                summary_content += f"- {entry.content[:200]}\n"
            
            # Create summary entry
            summary_entry = MemoryEntry(
                agent_id=agent_id,
                project_id=entries[0].project_id if entries else "",
                type=MemoryType.PATTERN,
                content=summary_content,
                tags=[entry_type, "weekly-summary", "compacted"],
                metadata={
                    "compacted_count": len(entries),
                    "date_range": {
                        "start": min(e.timestamp for e in entries),
                        "end": max(e.timestamp for e in entries)
                    }
                }
            )
            
            self.write(summary_entry)
            summaries_created += 1
        
        # Archive old files (move to archive directory)
        archive_dir = agent_dir / "archive"
        archive_dir.mkdir(exist_ok=True)
        
        for jsonl_file in files_to_archive:
            archive_path = archive_dir / jsonl_file.name
            jsonl_file.rename(archive_path)
        
        total_entries = sum(len(entries) for entries in old_entries_by_type.values())
        
        return {
            "compacted": total_entries,
            "summaries_created": summaries_created,
            "files_archived": len(files_to_archive),
            "message": f"Compacted {total_entries} entries into {summaries_created} summaries"
        }
