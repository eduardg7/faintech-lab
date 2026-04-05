#!/usr/bin/env python3
"""
Memory Retention Script - DPIA Compliance (AC2)

Implements 90-day memory retention policy per GDPR DPIA requirements.
Deletes memories older than 90 days to ensure data minimization.

Usage:
    python scripts/retention/cleanup_memories.py [--dry-run] [--verbose]

Owner: CTO
Created: 2026-04-03
Task: LAB-LEGAL-20260322-DPIA-PROD (AC2)
"""

import argparse
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple


def get_database_path() -> Path:
    """Get the path to the AMC database."""
    # Try multiple possible locations
    possible_paths = [
        Path(__file__).parent.parent.parent / "amc-backend" / "amc.db",
        Path(__file__).parent.parent.parent / "amc.db",
        Path(__file__).parent.parent.parent / "projects" / "new-product" / "amc.db",
    ]

    for db_path in possible_paths:
        if db_path.exists():
            return db_path

    raise FileNotFoundError(f"Database not found. Tried: {possible_paths}")


def count_old_memories(conn: sqlite3.Connection, days: int = 90) -> Tuple[int, int]:
    """
    Count memories older than the retention period.

    Returns:
        Tuple of (total_memories, old_memories_count)
    """
    cursor = conn.cursor()

    # Count total memories
    cursor.execute("SELECT COUNT(*) FROM memories WHERE deleted_at IS NULL")
    total = cursor.fetchone()[0]

    # Count old memories (older than retention period, not deleted)
    cutoff_date = datetime.now() - timedelta(days=days)
    cursor.execute(
        "SELECT COUNT(*) FROM memories WHERE created_at < ? AND deleted_at IS NULL",
        (cutoff_date.isoformat(),)
    )
    old_count = cursor.fetchone()[0]

    return total, old_count


def delete_old_memories(conn: sqlite3.Connection, days: int = 90, dry_run: bool = False) -> int:
    """
    Delete memories older than the retention period.

    Args:
        conn: Database connection
        days: Retention period in days (default: 90)
        dry_run: If True, only count without deleting

    Returns:
        Number of memories deleted
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    cutoff_iso = cutoff_date.isoformat()

    cursor = conn.cursor()

    if dry_run:
        # Count only
        cursor.execute(
            "SELECT COUNT(*) FROM memories WHERE created_at < ? AND deleted_at IS NULL",
            (cutoff_iso,)
        )
        count = cursor.fetchone()[0]
        print(f"[DRY RUN] Would delete {count} memories older than {days} days (created before {cutoff_iso})")
        return count
    else:
        # Soft delete (set deleted_at timestamp)
        cursor.execute(
            "UPDATE memories SET deleted_at = ? WHERE created_at < ? AND deleted_at IS NULL",
            (datetime.now().isoformat(), cutoff_iso)
        )
        deleted = cursor.rowcount
        conn.commit()
        print(f"✅ Deleted {deleted} memories older than {days} days (created before {cutoff_iso})")
        return deleted


def main():
    parser = argparse.ArgumentParser(
        description="Clean up memories older than retention period (DPIA compliance)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count memories to delete without actually deleting"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Retention period in days (default: 90)"
    )

    args = parser.parse_args()

    try:
        db_path = get_database_path()
        if args.verbose:
            print(f"📁 Database: {db_path}")

        conn = sqlite3.connect(str(db_path))

        # Show stats
        total, old_count = count_old_memories(conn, args.days)
        print(f"\n📊 Memory Statistics:")
        print(f"   Total memories: {total}")
        print(f"   Memories older than {args.days} days: {old_count}")

        if old_count == 0:
            print(f"\n✅ No memories older than {args.days} days. Nothing to clean up.")
            return 0

        # Delete old memories
        print(f"\n🧹 Cleaning up memories...")
        deleted = delete_old_memories(conn, args.days, dry_run=args.dry_run)

        if not args.dry_run:
            # Verify
            total_after, old_after = count_old_memories(conn, args.days)
            print(f"\n✅ Cleanup complete:")
            print(f"   Deleted: {deleted} memories")
            print(f"   Remaining: {total_after} memories")
            print(f"   Older than {args.days} days: {old_after}")

        conn.close()
        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
