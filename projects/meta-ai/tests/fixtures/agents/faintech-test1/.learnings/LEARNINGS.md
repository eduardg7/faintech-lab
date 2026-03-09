# Learnings Log

## 2026-03-09 - Always Check Git Status Before Commit

### Context
Committed wrong files due to not checking git status first.

### What Worked
1. **Pre-commit checklist**: Always run `git status` before `git add`
2. **Review staged changes**: Use `git diff --cached` to verify

### Pattern for Future
Before every commit:
1. Run `git status`
2. Review file list
3. Use `git add <specific-files>` not `git add .`

### Root Cause
Rushed commit without verification.

---

## 2026-03-09 - Test Before Push

### Context
Pushed code that failed tests locally.

### What Worked
1. **Local test run**: Always run tests before pushing
2. **CI verification**: Check CI passes after push

### Pattern for Future
Pre-push checklist:
1. Run test suite
2. Verify all pass
3. Then push

### Root Cause
Skipped local testing step.
