#!/usr/bin/env python3
"""
Migration script to fix file permissions on existing agent memory files.

This script addresses security risk R-LAB-001 by ensuring:
- Memory files have 0o600 permissions (owner read/write only)
- Memory directories have 0o700 permissions (owner only)

Usage:
    python scripts/fix_permissions.py [--dry-run] [--base-path PATH]

Examples:
    # Preview changes without applying them
    python scripts/fix_permissions.py --dry-run

    # Apply permission fixes to default ~/.agent-memory
    python scripts/fix_permissions.py

    # Apply to custom path
    python scripts/fix_permissions.py --base-path /custom/memory/path
"""

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Tuple, List


# Security constants
FILE_PERMISSIONS = 0o600  # Owner read/write only
DIR_PERMISSIONS = 0o700  # Owner read/write/execute only


def check_current_permissions(path: Path) -> int:
    """Get current permission mode of a path."""
    return stat.S_IMODE(os.stat(path).st_mode)


def needs_fix(path: Path, expected_mode: int) -> bool:
    """Check if path needs permission fix."""
    current = check_current_permissions(path)
    return current != expected_mode


def fix_file_permissions(file_path: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Fix permissions on a single file.

    Returns:
        Tuple of (success, message)
    """
    try:
        current_mode = check_current_permissions(file_path)

        if current_mode == FILE_PERMISSIONS:
            return True, f"OK: {file_path} already has correct permissions {oct(FILE_PERMISSIONS)}"

        if dry_run:
            return True, f"WOULD FIX: {file_path} {oct(current_mode)} -> {oct(FILE_PERMISSIONS)}"

        os.chmod(file_path, FILE_PERMISSIONS)
        return True, f"FIXED: {file_path} {oct(current_mode)} -> {oct(FILE_PERMISSIONS)}"

    except Exception as e:
        return False, f"ERROR: {file_path} - {e}"


def fix_directory_permissions(dir_path: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Fix permissions on a single directory.

    Returns:
        Tuple of (success, message)
    """
    try:
        current_mode = check_current_permissions(dir_path)

        if current_mode == DIR_PERMISSIONS:
            return True, f"OK: {dir_path} already has correct permissions {oct(DIR_PERMISSIONS)}"

        if dry_run:
            return True, f"WOULD FIX: {dir_path} {oct(current_mode)} -> {oct(DIR_PERMISSIONS)}"

        os.chmod(dir_path, DIR_PERMISSIONS)
        return True, f"FIXED: {dir_path} {oct(current_mode)} -> {oct(DIR_PERMISSIONS)}"

    except Exception as e:
        return False, f"ERROR: {dir_path} - {e}"


def migrate_permissions(base_path: Path, dry_run: bool = False) -> dict:
    """
    Migrate all memory files and directories to secure permissions.

    Args:
        base_path: Base memory directory (e.g., ~/.agent-memory)
        dry_run: If True, only preview changes

    Returns:
        Dictionary with migration statistics
    """
    stats = {
        "files_checked": 0,
        "files_fixed": 0,
        "files_ok": 0,
        "files_error": 0,
        "dirs_checked": 0,
        "dirs_fixed": 0,
        "dirs_ok": 0,
        "dirs_error": 0,
        "messages": []
    }

    if not base_path.exists():
        stats["messages"].append(f"Base path does not exist: {base_path}")
        return stats

    # Fix base directory
    success, msg = fix_directory_permissions(base_path, dry_run)
    stats["messages"].append(msg)
    stats["dirs_checked"] += 1
    if success and "FIXED" in msg:
        stats["dirs_fixed"] += 1
    elif success and "OK" in msg:
        stats["dirs_ok"] += 1
    else:
        stats["dirs_error"] += 1

    # Iterate through agent directories
    for agent_dir in base_path.iterdir():
        if not agent_dir.is_dir():
            continue

        # Skip archive directories for now (they should still be secured)
        # but handle them as regular directories

        # Fix agent directory permissions
        success, msg = fix_directory_permissions(agent_dir, dry_run)
        stats["messages"].append(msg)
        stats["dirs_checked"] += 1
        if success and "FIXED" in msg:
            stats["dirs_fixed"] += 1
        elif success and "OK" in msg:
            stats["dirs_ok"] += 1
        else:
            stats["dirs_error"] += 1

        # Fix all memory files in the directory
        for memory_file in agent_dir.glob("*.jsonl"):
            success, msg = fix_file_permissions(memory_file, dry_run)
            stats["messages"].append(msg)
            stats["files_checked"] += 1
            if success and "FIXED" in msg:
                stats["files_fixed"] += 1
            elif success and "OK" in msg:
                stats["files_ok"] += 1
            else:
                stats["files_error"] += 1

        # Handle archive subdirectories
        archive_dir = agent_dir / "archive"
        if archive_dir.exists():
            success, msg = fix_directory_permissions(archive_dir, dry_run)
            stats["messages"].append(msg)
            stats["dirs_checked"] += 1
            if success and "FIXED" in msg:
                stats["dirs_fixed"] += 1
            elif success and "OK" in msg:
                stats["dirs_ok"] += 1
            else:
                stats["dirs_error"] += 1

            for archived_file in archive_dir.glob("*.jsonl"):
                success, msg = fix_file_permissions(archived_file, dry_run)
                stats["messages"].append(msg)
                stats["files_checked"] += 1
                if success and "FIXED" in msg:
                    stats["files_fixed"] += 1
                elif success and "OK" in msg:
                    stats["files_ok"] += 1
                else:
                    stats["files_error"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Fix file permissions on agent memory files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them"
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        default=Path.home() / ".agent-memory",
        help="Base memory directory (default: ~/.agent-memory)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only show summary, not individual files"
    )

    args = parser.parse_args()

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Migrating memory permissions...")
    print(f"Base path: {args.base_path}")
    print()

    stats = migrate_permissions(args.base_path, args.dry_run)

    if not args.quiet:
        print("\n".join(stats["messages"]))
        print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Directories checked: {stats['dirs_checked']}")
    print(f"  - Fixed: {stats['dirs_fixed']}")
    print(f"  - Already OK: {stats['dirs_ok']}")
    print(f"  - Errors: {stats['dirs_error']}")
    print()
    print(f"Files checked: {stats['files_checked']}")
    print(f"  - Fixed: {stats['files_fixed']}")
    print(f"  - Already OK: {stats['files_ok']}")
    print(f"  - Errors: {stats['files_error']}")
    print()

    if args.dry_run:
        print("DRY RUN COMPLETE - No changes were made")
        print("Run without --dry-run to apply changes")
    else:
        print("MIGRATION COMPLETE")

    # Exit with error if any failures
    if stats["files_error"] > 0 or stats["dirs_error"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
