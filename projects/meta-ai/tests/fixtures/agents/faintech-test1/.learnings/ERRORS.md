# ERRORS

## [ERR-20260309-001] Git Push Failed

**Logged**: 2026-03-09T10:00:00Z
**Priority**: high
**Status**: pending
**Area**: git_workflow

### Summary
Git push to origin failed due to authentication error

### Error
```
fatal: Authentication failed for 'https://github.com/...'
```

### Context
Attempting to push branch after commit. SSH key not configured.

### Suggested Fix
Configure SSH key or use personal access token

### Metadata
- Reproducible: yes
- Related Files: .git/config
- See Also: ERR-20260309-002

---

## [ERR-20260309-002] Git Authentication Missing

**Logged**: 2026-03-09T11:00:00Z
**Priority**: high
**Status**: pending
**Area**: git_workflow

### Summary
Cannot push to remote - credentials not found

### Error
```
remote: Permission denied
```

### Context
Multiple push attempts failed. Need to setup git credentials.

### Suggested Fix
Run git config --global credential.helper store

### Metadata
- Reproducible: yes
- Related Files: .git/config
- See Also: ERR-20260309-001
