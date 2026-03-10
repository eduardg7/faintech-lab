# Meta-AI: Self-Improvement Pattern Detector

Part of Faintech Lab's meta-ai experiments for autonomous agent improvement.

## Overview

The Pattern Detector analyzes agent learning and error logs to identify recurring patterns that should be promoted to system-wide rules. It reads ERRORS.md and LEARNINGS.md files from all agents, clusters similar entries, and outputs promotion candidates.

## Components

### 1. Pattern Detector (`src/improvement/pattern_detector.py`)

Main script that:
- Scans all agent `.learnings` directories
- Parses ERRORS.md and LEARNINGS.md files
- Clusters entries by keyword similarity
- Identifies recurring patterns across multiple agents
- Outputs promotion candidates with suggested rules

### 2. Tests (`tests/test_pattern_detector.py`)

Comprehensive test suite with:
- Unit tests for keyword extraction, categorization, similarity
- Integration tests with fixture data
- 16 test cases covering all major functionality

## Usage

```bash
# Basic usage (default threshold: 3)
python src/improvement/pattern_detector.py --output promotion_candidates.json

# Custom threshold
python src/improvement/pattern_detector.py --threshold 2 --output results.json

# Verbose output
python src/improvement/pattern_detector.py --threshold 3 --output results.json --verbose

# Custom agents directory
python src/improvement/pattern_detector.py --agents-dir /path/to/agents --output results.json
```

## Output Format

```json
{
  "metadata": {
    "scan_timestamp": "2026-03-09T21:18:00Z",
    "agents_directory": "~/.openclaw/agents",
    "total_entries_scanned": 42,
    "total_patterns_found": 15,
    "promotion_threshold": 3,
    "total_promotion_candidates": 5
  },
  "promotion_candidates": [
    {
      "pattern": "git_push_authentication",
      "frequency": 5,
      "affected_agents": ["faintech-dev", "faintech-qa", "faintech-devops"],
      "num_agents": 3,
      "suggested_rule": "When encountering git_push_authentication, check logs and escalate after 2 failed attempts",
      "priority": "HIGH",
      "sample_entries": [...],
      "detected_at": "2026-03-09T21:18:00Z"
    }
  ]
}
```

## Priority Levels

- **HIGH**: 3+ occurrences across 2+ agents (requires immediate attention)
- **MEDIUM**: 3+ occurrences in 1 agent (worth investigating)
- **LOW**: 2 occurrences (potential pattern, monitor)

## Algorithm

1. **Scan**: Read all ERRORS.md and LEARNINGS.md from `~/.openclaw/agents/*/`
2. **Parse**: Extract entries with title, content, metadata
3. **Categorize**: Classify by type (error, correction, security, etc.)
4. **Extract Keywords**: Remove stop words, keep meaningful terms
5. **Cluster**: Group entries by keyword similarity (Jaccard index > 0.5)
6. **Filter**: Keep only patterns meeting threshold
7. **Prioritize**: Assign priority based on frequency and agent count
8. **Suggest Rules**: Generate actionable rules for each pattern

## Testing

```bash
# Run all tests
python -m pytest tests/test_pattern_detector.py -v

# Run with coverage
python -m pytest tests/test_pattern_detector.py --cov=src/improvement

# Run specific test
python -m pytest tests/test_pattern_detector.py::TestPatternDetector::test_detect_git_pattern -v
```

## Test Coverage

- Keyword extraction and stop word filtering
- Entry categorization by type
- Jaccard similarity computation
- Markdown parsing
- File scanning across agents
- Pattern clustering
- Priority assignment
- Output format validation
- Edge cases (empty directories, missing files)

## Integration with Faintech OS

This tool is part of the META-AI-002 task in Faintech Lab. It supports the self-improvement loop by:

1. Detecting recurring mistakes across agents
2. Identifying knowledge gaps that need documentation
3. Finding process failures that need automation
4. Suggesting system-wide rule improvements

## Future Enhancements

- Semantic similarity using embeddings (beyond keyword matching)
- Automatic promotion to AGENT.md when patterns reach critical mass
- Historical trend tracking (are patterns increasing/decreasing?)
- Integration with task assignment (avoid assigning to agents with related errors)

## Related

- META-AI-001: Agent Memory System (persistent memory for agents)
- META-AI-003: Execution Ledger (track agent decisions and outcomes)

## Security

### Secrets Detection

The Memory System includes automatic secrets detection to prevent accidental credential leakage.

**Protected Patterns:**
- OpenAI API keys (`sk-...`)
- Generic API keys (`api_key`, `apikey`, `x-api-key`)
- Bearer tokens and JWTs
- OAuth tokens
- Passwords
- AWS Access Keys (`AKIA...`)
- AWS Secret Access Keys
- Private keys (PEM format)
- Database URLs with credentials

**How It Works:**
1. Every memory write is scanned for secrets before persistence
2. If secrets detected, write is blocked with `SecurityError`
3. Blocked attempts are logged to `~/.agent-memory/security.log`
4. Performance impact: <5ms for typical content (keyword pre-filtering optimization)

**Allowlist (Safe Patterns):**
- `test_api_key`, `test_token`, `test_password` (test fixtures)
- `example`, `sample`, `dummy`, `placeholder` (example values)
- `xxx`, `redacted`, `[REDACTED]` (redacted placeholders)

**Usage:**
```python
from src.memory.secrets import check_content_safe, SecurityError

try:
    check_content_safe(content, agent_id="my-agent")
    # Safe to write
except SecurityError as e:
    print(f"Blocked: {e.message}")
    for secret in e.detected_secrets:
        print(f"  - {secret.secret_type.value}: {secret.masked_preview}")
```

**Disabling for Testing:**
```python
# In MemoryStore.write()
store.write(entry, check_secrets=False)  # Skip secrets check
```

### File Permissions

Memory files are created with restricted permissions:
- Files: `0o600` (owner read/write only)
- Directories: `0o700` (owner only)

### Incident Response

See `INCIDENT-RESPONSE-RUNBOOK.md` for security incident procedures.

---

**Created**: 2026-03-09
**Last Updated**: 2026-03-10
**Owner**: faintech-ciso
**Task**: META-AI-002
