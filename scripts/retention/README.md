# Data Retention Scripts - DPIA Compliance

**Owner:** CTO
**Created:** 2026-04-03
**Task:** LAB-LEGAL-20260322-DPIA-PROD (AC2)
**Compliance:** GDPR Article 35 DPIA - Data Minimization

## Overview

This directory contains automated data retention scripts to comply with GDPR DPIA requirements for Faintech Lab's AMC (Agent Memory Cloud) product.

## Retention Policies

| Data Type | Retention Period | Script | Rationale |
|-----------|------------------|--------|-----------|
| **Memories** | 90 days | `cleanup_memories.py` | User memory data is transient; 90 days provides sufficient utility while minimizing data exposure |
| **Logs** | 30 days | `cleanup_logs.py` | Operational logs only needed for recent debugging; 30 days balances observability with data minimization |

## Scripts

### cleanup_memories.py

Deletes memories older than 90 days from the SQLite database.

**Usage:**
```bash
# Dry run (count only)
python3 scripts/retention/cleanup_memories.py --dry-run --verbose

# Execute cleanup
python3 scripts/retention/cleanup_memories.py --verbose

# Custom retention period
python3 scripts/retention/cleanup_memories.py --days 60
```

**Behavior:**
- Soft deletes memories (sets `deleted_at` timestamp)
- Only affects memories where `deleted_at IS NULL`
- Provides statistics before and after cleanup

### cleanup_logs.py

Deletes log files older than 30 days from filesystem.

**Usage:**
```bash
# Dry run (count only)
python3 scripts/retention/cleanup_logs.py --dry-run --verbose

# Execute cleanup
python3 scripts/retention/cleanup_logs.py --verbose

# Custom retention period
python3 scripts/retention/cleanup_logs.py --days 14
```

**Behavior:**
- Hard deletes log files (`.log` extension)
- Checks modification time (`mtime`)
- Shows total size freed

## Automated Execution

### Cron Setup (Recommended)

Add to crontab (`crontab -e`) for daily execution at 2:00 AM:

```bash
# Memory retention (90 days) - Daily at 2:00 AM
0 2 * * * cd /Users/eduardgridan/faintech-lab && /usr/bin/python3 scripts/retention/cleanup_memories.py --verbose >> /var/log/amc/retention_memories.log 2>&1

# Log retention (30 days) - Daily at 2:30 AM
30 2 * * * cd /Users/eduardgridan/faintech-lab && /usr/bin/python3 scripts/retention/cleanup_logs.py --verbose >> /var/log/amc/retention_logs.log 2>&1
```

### Manual Execution

For immediate cleanup:
```bash
cd /Users/eduardgridan/faintech-lab

# Cleanup memories
python3 scripts/retention/cleanup_memories.py --verbose

# Cleanup logs
python3 scripts/retention/cleanup_logs.py --verbose
```

## Testing

Both scripts support `--dry-run` mode to preview changes without executing:

```bash
# Test memory cleanup
python3 scripts/retention/cleanup_memories.py --dry-run --verbose

# Test log cleanup
python3 scripts/retention/cleanup_logs.py --dry-run --verbose
```

## Monitoring

After implementation, monitor:

1. **Database size:** Track `amc.db` growth over time
2. **Log directory size:** Check `/amc-backend/ops/logs/` size
3. **Retention execution:** Review cron logs for successful runs
4. **User impact:** Verify no legitimate data loss

## Compliance Evidence

### DPIA AC2 Requirements

✅ **Automated deletion implemented:**
- 90-day memory retention script created
- 30-day log retention script created
- Both scripts tested and verified
- Cron automation ready for deployment

### Documentation

- `TECH-ARCHITECTURE.md` - ADRs for retention decisions
- `TECH-DEBT.md` - Tracking implementation
- GDPR DPIA documentation - Compliance evidence

## Future Improvements

1. **Configurable retention:** Add config file for retention periods
2. **Email notifications:** Send alerts on cleanup completion
3. **Metrics tracking:** Log deletion statistics to monitoring
4. **Archive option:** Move old data to cold storage before deletion
5. **Multi-tenant support:** Per-workspace retention policies

## References

- GDPR Article 35 - Data Protection Impact Assessment
- GDPR Article 5(1)(c) - Data Minimization Principle
- `data/ops/TECH-ARCHITECTURE.md` - ADR-017 (Data Retention Policy)
- `~/.openclaw/agents/legal/docs/anspdcp-submission-draft.md` - DPIA submission

---

**Last Updated:** 2026-04-03
**Next Review:** 2026-06-03 (3 months post-implementation)
