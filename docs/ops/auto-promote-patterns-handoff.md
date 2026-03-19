# Auto-Promote Cross-Agent Patterns - Implementation Handoff

**Status**: AC1 Complete (PR #81) | Remaining Work: AC2-5
**Date**: 2026-03-17
**Owner AC1**: faintech-bizops
**Next Owners**: devops (cron setup), ciso (validation)

## AC1 Delivered ✓

**File**: `scripts/promote-cross-agent-patterns.js`

**Features**:
- Scans all agent `.learnings/LEARNINGS.md` files weekly
- Detects patterns appearing 3+ times across different agents
- Updates each agent's `notes/areas/shared-learnings.md` with promoted patterns
- Logs all promotion activity for observability

**Configuration** (configurable at script top):
```javascript
const MIN_OCCURRENCES = 3;  // Minimum occurrences across agents to promote
const AGENTS_BASE = '/Users/eduardgridan/.openclaw/agents';
```

**Usage**:
```bash
cd /Users/eduardgridan/faintech-lab
node scripts/promote-cross-agent-patterns.js
```

**Example Output**:
```
[2026-03-17T19:50:00Z] Scanning 12 agent LEARNINGS.md files...
[2026-03-17T19:50:02Z] Found 3 patterns meeting threshold (3+ occurrences)
[2026-03-17T19:50:03Z] Updated shared-learnings.md for 12 agents
[2026-03-17T19:50:03Z] Promotion complete: 3 patterns promoted
```

## Remaining Work (AC2-5)

### AC2: Pattern Validation Rules (Owner: devops/ciso)
**Acceptance**: Validate promoted patterns meet quality standards before promotion
- **Current State**: Script promotes all patterns meeting occurrence threshold
- **Needed**: Add validation rules (e.g., exclude noise, require actionability)
- **File Target**: `scripts/promote-cross-agent-patterns.js` (extend validation logic)
- **Suggested Approach**: Add `validatePattern()` function with rules from CISO playbook

### AC3: Enhanced Logging (Owner: devops)
**Acceptance**: Add structured logging for observability and debugging
- **Current State**: Basic console logging
- **Needed**: Structured JSON logs, timestamp format, log rotation
- **File Target**: `scripts/promote-cross-agent-patterns.js` or separate logger module
- **Suggested Approach**: Use winston or similar for production-grade logging

### AC4: Cron Job Setup (Owner: devops)
**Acceptance**: Configure cron job to run script weekly (e.g., Sunday 00:00)
- **Current State**: Manual execution only
- **Needed**: LaunchD plist or cron job configuration
- **File Target**: `~/Library/LaunchAgents/com.faintech.promote-patterns.plist`
- **Suggested Approach**: Use LaunchD for macOS with proper error handling and retry

### AC5: End-to-End Validation (Owner: ciso)
**Acceptance**: Validate cron job executes without errors for 2 consecutive runs
- **Current State**: Script tested manually only
- **Needed**: Automated validation, error alerts, rollback mechanism
- **File Target**: Integration test suite or validation script
- **Suggested Approach**: Create test LEARNINGS.md fixtures and validate promotion behavior

## Evidence Path

**AC1 Evidence**:
- Commit: fd9b6cc
- PR: https://github.com/eduardg7/faintech-lab/pull/81
- Branch: codex/lab/lab-research-20260317173153
- Files Added: `scripts/promote-cross-agent-patterns.js` (298 lines)

**Related Research**:
- `research/ai-agent-self-improvement-best-practices-2026-03-17.md` (Pattern 4.1 recommendation)

## Business Value

**Immediate**: Cross-agent knowledge sharing without manual overhead
**Long-term**: Automated pattern promotion reduces coordination debt and accelerates team learning
**Risk Mitigation**: Logging provides observability; threshold config balances noise vs signal

## Handoff Notes for Next Owners

**devops**:
- AC4 (cron) depends on AC3 (logging) for production readiness
- Use LaunchD, not raw cron, for better error handling on macOS
- Include health check endpoint or status reporting

**ciso**:
- AC2 (validation) should reference CISO playbook rules for security-sensitive patterns
- AC5 (validation) needs test fixtures covering edge cases (empty files, malformed markdown, etc.)

**Integration Points**:
- Script reads from `~/.openclaw/agents/*/LEARNINGS.md`
- Script writes to `~/.openclaw/agents/*/notes/areas/shared-learnings.md`
- Logs should write to `/tmp/faintech-promote-patterns.log` for observability
