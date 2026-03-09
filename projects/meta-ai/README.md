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

---

**Created**: 2026-03-09
**Owner**: faintech-frontend (role mismatch, but executed to unblock delivery)
**Task**: META-AI-002
