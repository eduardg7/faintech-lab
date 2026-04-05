#!/usr/bin/env python3
"""
Log Retention Script - DPIA Compliance (AC2)

Implements 30-day log retention policy per GDPR DPIA requirements.
Deletes log files older than 30 days to ensure data minimization.

Usage:
    python scripts/retention/cleanup_logs.py [--dry-run] [--verbose]

Owner: CTO
Created: 2026-04-03
Task: LAB-LEGAL-20260322-DPIA-PROD (AC2)
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple


def get_log_directories() -> List[Path]:
    """Get list of directories containing log files."""
    base_path = Path(__file__).parent.parent.parent
    return [
        base_path / "amc-backend" / "ops" / "logs",
        base_path / "logs",
    ]


def find_log_files(log_dirs: List[Path], days: int = 30) -> Tuple[List[Path], List[Path]]:
    """
    Find all log files and separate into keep/delete lists.

    Returns:
        Tuple of (keep_files, delete_files)
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_timestamp = cutoff_date.timestamp()

    keep_files = []
    delete_files = []

    for log_dir in log_dirs:
        if not log_dir.exists():
            continue

        for log_file in log_dir.glob("*.log"):
            # Get file modification time
            mtime = log_file.stat().st_mtime

            if mtime < cutoff_timestamp:
                delete_files.append(log_file)
            else:
                keep_files.append(log_file)

    return keep_files, delete_files


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def delete_log_files(files: List[Path], dry_run: bool = False) -> Tuple[int, int]:
    """
    Delete log files.

    Returns:
        Tuple of (deleted_count, total_size_bytes)
    """
    deleted_count = 0
    total_size = 0

    for log_file in files:
        file_size = log_file.stat().st_size
        total_size += file_size

        if dry_run:
            print(f"  [DRY RUN] Would delete: {log_file.name} ({format_size(file_size)})")
            deleted_count += 1
        else:
            try:
                log_file.unlink()
                print(f"  ✅ Deleted: {log_file.name} ({format_size(file_size)})")
                deleted_count += 1
            except Exception as e:
                print(f"  ❌ Failed to delete {log_file.name}: {e}")

    return deleted_count, total_size


def main():
    parser = argparse.ArgumentParser(
        description="Clean up log files older than retention period (DPIA compliance)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count log files to delete without actually deleting"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Retention period in days (default: 30)"
    )

    args = parser.parse_args()

    try:
        log_dirs = get_log_directories()

        if args.verbose:
            print(f"📁 Log directories:")
            for log_dir in log_dirs:
                exists = "✅" if log_dir.exists() else "❌"
                print(f"   {exists} {log_dir}")

        # Find log files
        keep_files, delete_files = find_log_files(log_dirs, args.days)

        print(f"\n📊 Log File Statistics:")
        print(f"   Total log files: {len(keep_files) + len(delete_files)}")
        print(f"   Files to keep: {len(keep_files)}")
        print(f"   Files to delete: {len(delete_files)} (older than {args.days} days)")

        if delete_files:
            # Calculate total size to be freed
            total_size = sum(f.stat().st_size for f in delete_files)
            print(f"   Size to be freed: {format_size(total_size)}")

            print(f"\n🧹 Cleaning up log files...")
            deleted_count, deleted_size = delete_log_files(delete_files, dry_run=args.dry_run)

            if not args.dry_run:
                print(f"\n✅ Cleanup complete:")
                print(f"   Deleted: {deleted_count} log files")
                print(f"   Freed: {format_size(deleted_size)}")
        else:
            print(f"\n✅ No log files older than {args.days} days. Nothing to clean up.")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
