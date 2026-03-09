# Learnings Log

## 2026-03-09 - Never Commit Secrets

### Context
Almost committed API key to repository.

### What Worked
1. **Pre-commit hook**: Detected secret before commit
2. **.gitignore**: Properly configured to exclude .env files

### Pattern for Future
Security checklist:
1. Never commit .env files
2. Use .gitignore for secrets
3. Use environment variables

### Root Cause
Forgot to check staged files before commit.

---

## 2026-03-09 - Validate Input Before Processing

### Context
Processing untrusted input caused security vulnerability.

### What Worked
1. **Input validation**: Sanitize all user input
2. **Security review**: Code review caught the issue

### Pattern for Future
Always validate and sanitize external input before processing.

### Root Cause
Trusted external data without validation.
