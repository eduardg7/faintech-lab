"""Memory store for persistent agent memory with file-based storage."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from collections import defaultdict
import re

from .models import MemoryEntry, MemoryType


class MemoryStore:
    """
    Persistent memory store for AI agents using file-based JSONL storage.
    
    Storage path: ~/.agent-memory/<agent_id>/<YYYY-MM-DD>.jsonl
    
    Features:
    - Write memory entries with structured schema
    - Search by keywords, recency, agent, type, tags
    - Auto-compaction of old entries into weekly summaries
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

    def write(self, entry: MemoryEntry) -> str:
        """
        Write a memory entry to persistent storage.

        Args:
            entry: MemoryEntry to persist

        Returns:
            Entry ID

        Performance:
            <100ms for append-only write

        Security:
            - Memory files created with 0o600 permissions (owner read/write only)
            - Directories created with 0o700 permissions (owner only)
        """
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
