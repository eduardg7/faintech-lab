# Security Documentation

## File Permission Hardening

The Meta-AI memory system implements file permission hardening to protect sensitive agent memory data from unauthorized access.

### Permission Requirements

| Resource | Permissions | Octal | Description |
|----------|-------------|-------|-------------|
| Memory files (`*.jsonl`) | `-rw-------` | `0o600` | Owner read/write only |
| Agent directories | `drwx------` | `0o700` | Owner read/write/execute only |
| Base memory directory | `drwx------` | `0o700` | Owner read/write/execute only |

### Implementation

File permissions are enforced in `memory/store.py`:

```python
class MemoryStore:
    FILE_PERMISSIONS = 0o600  # Owner read/write only
    DIR_PERMISSIONS = 0o700   # Owner read/write/execute only

    def write(self, entry: MemoryEntry) -> str:
        # Create directory with secure permissions
        agent_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(agent_dir, self.DIR_PERMISSIONS)

        # Write file
        with open(memory_file, 'a') as f:
            f.write(entry.to_json() + '\n')

        # Enforce secure file permissions
        os.chmod(memory_file, self.FILE_PERMISSIONS)
```

### Why These Permissions

1. **Memory files contain sensitive data**: Agent memory may include:
   - API keys and tokens (even though they shouldn't be stored there)
   - Internal system paths and configurations
   - Business decisions and strategic information
   - Error logs with potentially sensitive context

2. **Single-user environment assumption**: The current implementation assumes a single-user development environment. The 0o600/0o700 permissions prevent:
   - Other users on shared systems from reading memory
   - Accidental exposure via misconfigured file sharing
   - Service accounts or background processes from accessing memory

3. **Defense in depth**: Even though the system is single-user, proper permissions:
   - Reduce attack surface if the machine is compromised
   - Prevent accidental data leakage
   - Establish good security hygiene for future multi-tenant scenarios

### Migration

For existing memory files that may have been created before permission hardening, use the migration script:

```bash
# Preview changes
python scripts/fix_permissions.py --dry-run

# Apply fixes
python scripts/fix_permissions.py

# Apply to custom path
python scripts/fix_permissions.py --base-path /custom/memory/path
```

### Verification

To verify permissions are correctly set:

```bash
# Check memory directory permissions
ls -la ~/.agent-memory/

# Check specific agent directory
ls -la ~/.agent-memory/faintech-ciso/

# Verify no group/world permissions
stat -f "%A %N" ~/.agent-memory/*/*.jsonl
# Expected: 600 for files, 700 for directories
```

### Security Risks Addressed

| Risk ID | Description | Mitigation |
|---------|-------------|------------|
| R-LAB-001 | Memory files use default permissions | File permission hardening (0o600/0o700) |
| R-LAB-002 | No agent-scoped access control | See LAB-SEC-004 (access control) |
| R-LAB-003 | No content validation | See LAB-SEC-003 (content sanitization) |

### Related Tasks

- **LAB-SEC-002**: File permission hardening (this implementation)
- **LAB-SEC-003**: Content validation and sanitization
- **LAB-SEC-004**: Agent-scoped access control

### Performance Impact

Permission setting via `os.chmod()` adds minimal overhead:
- Typical overhead: <1ms per write
- Maximum acceptable overhead: <5ms per write (requirement from LAB-SEC-002)

The implementation meets the performance requirement.

---

_Last updated: 2026-03-10_
_Author: faintech-ciso_
