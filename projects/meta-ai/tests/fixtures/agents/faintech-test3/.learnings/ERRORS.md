# ERRORS

## [ERR-20260309-004] Security Issue Detected

**Logged**: 2026-03-09T13:00:00Z
**Priority**: critical
**Status**: pending
**Area**: security

### Summary
API key exposed in git commit

### Error
```
Secret detected in commit history
```

### Context
Accidentally committed .env file with API key.

### Suggested Fix
Use git filter-branch to remove from history, rotate key immediately

### Metadata
- Reproducible: no
- Related Files: .env
- See Also: security best practices

---

## [ERR-20260309-005] Permission Denied

**Logged**: 2026-03-09T14:00:00Z
**Priority**: high
**Status**: pending
**Area**: security

### Summary
Cannot access secure resource without proper auth

### Error
```
403 Forbidden - Insufficient permissions
```

### Context
Tried to access production resource with dev credentials.

### Suggested Fix
Verify credentials and permissions before access attempt

### Metadata
- Reproducible: yes
- Related Files: config/auth
