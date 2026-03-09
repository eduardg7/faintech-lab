#!/usr/bin/env python3
"""CLI tool for agent memory operations."""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from .models import MemoryEntry, MemoryType
from .store import MemoryStore


def cmd_write(args):
    """Write a memory entry."""
    store = MemoryStore()
    
    entry = MemoryEntry(
        agent_id=args.agent_id,
        project_id=args.project_id,
        task_id=args.task_id,
        type=MemoryType(args.type),
        content=args.content,
        tags=args.tags.split(',') if args.tags else []
    )
    
    entry_id = store.write(entry)
    print(f"Written memory entry: {entry_id}")


def cmd_search(args):
    """Search memory entries."""
    store = MemoryStore()
    
    results = store.search(
        query=args.query,
        agent_id=args.agent_id,
        project_id=args.project_id,
        task_id=args.task_id,
        entry_type=MemoryType(args.type) if args.type else None,
        tags=args.tags.split(',') if args.tags else [],
        limit=args.limit
    )
    
    if not results:
        print("No results found.")
        return
    
    print(f"Found {len(results)} entries:\n")
    for entry in results:
        print(f"[{entry.timestamp}] {entry.type.value}: {entry.content[:100]}")
        if entry.tags:
            print(f"  Tags: {', '.join(entry.tags)}")
        print()


def cmd_compact(args):
    """Compact old memory entries."""
    store = MemoryStore()
    
    result = store.compact(args.agent_id, days_old=args.days)
    
    print(f"Compaction complete:")
    print(f"  Entries compacted: {result['compacted']}")
    print(f"  Summaries created: {result['summaries_created']}")
    print(f"  Files archived: {result['files_archived']}")
    print(f"  Message: {result['message']}")


def main():
    parser = argparse.ArgumentParser(
        description='Agent Memory CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Write command
    write_parser = subparsers.add_parser('write', help='Write a memory entry')
    write_parser.add_argument('--agent-id', required=True, help='Agent ID')
    write_parser.add_argument('--project-id', required=True, help='Project ID')
    write_parser.add_argument('--task-id', help='Task ID')
    write_parser.add_argument('--type', required=True, 
                             choices=[t.value for t in MemoryType],
                             help='Entry type')
    write_parser.add_argument('--content', required=True, help='Memory content')
    write_parser.add_argument('--tags', help='Comma-separated tags')
    write_parser.set_defaults(func=cmd_write)
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search memory entries')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--agent-id', help='Filter by agent ID')
    search_parser.add_argument('--project-id', help='Filter by project ID')
    search_parser.add_argument('--task-id', help='Filter by task ID')
    search_parser.add_argument('--type', choices=[t.value for t in MemoryType],
                              help='Filter by entry type')
    search_parser.add_argument('--tags', help='Comma-separated tags')
    search_parser.add_argument('--limit', type=int, default=10,
                              help='Maximum results (default: 10)')
    search_parser.set_defaults(func=cmd_search)
    
    # Compact command
    compact_parser = subparsers.add_parser('compact', help='Compact old entries')
    compact_parser.add_argument('--agent-id', required=True, help='Agent ID')
    compact_parser.add_argument('--days', type=int, default=7,
                               help='Age threshold in days (default: 7)')
    compact_parser.set_defaults(func=cmd_compact)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
