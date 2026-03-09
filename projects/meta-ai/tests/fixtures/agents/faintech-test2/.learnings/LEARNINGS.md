# Learnings Log

## 2026-03-09 - Verify Branch Before Work

### Context
Started working on wrong branch, had to cherry-pick commits.

### What Worked
1. **Branch verification**: Always check current branch with `git branch`
2. **Worktree isolation**: Use worktrees to prevent confusion

### Pattern for Future
Before starting work:
1. Check current branch
2. Verify it's the correct task branch
3. Create new branch if needed

### Root Cause
Assumed branch without checking.

---

## 2026-03-09 - Run Tests Locally

### Context
CI failed due to tests that would have caught locally.

### What Worked
1. **Local test run**: Running `npm test` caught the issue
2. **Fast feedback**: Local testing is faster than waiting for CI

### Pattern for Future
Always run tests locally before pushing to save CI time.

### Root Cause
Relied solely on CI for testing.
