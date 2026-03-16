# Memory Utils Test Harness

## Overview

This test harness validates the global memory access functions for cross-agent context sharing, as part of LAB-006 experiment.

**Functions Tested:**
- `readGlobalMemory()` - Read agent's MEMORY.md
- `searchGlobalMemory()` - Search across agent memory
- `getCrossAgentContext()` - Get consolidated context
- `listAvailableAgents()` - List agents with memory files
- `agentMemoryExists()` - Check if agent memory exists
- `readDailyNotes()` - Read agent's daily notes
- `readMultiAgentMemory()` - Read memory from multiple agents
- `getAgentMemoryPath()` - Get agent memory directory path

## Installation

```bash
npm install
```

## Running Tests

### Run all tests:
```bash
npm test
```

### Run tests in watch mode:
```bash
npm run test:watch
```

### Run tests with coverage:
```bash
npm run test:coverage
```

### Type checking:
```bash
npm run typecheck
```

## Test Structure

### Unit Tests
- `readGlobalMemory` - Tests for reading agent memory files
- `searchGlobalMemory` - Tests for searching memory content
- `getCrossAgentContext` - Tests for multi-agent context consolidation
- `listAvailableAgents` - Tests for agent discovery
- `agentMemoryExists` - Tests for agent existence checks
- `readDailyNotes` - Tests for daily notes reading
- `readMultiAgentMemory` - Tests for batch memory reading

### LAB-006 Protocol Tests
Tests aligned with LAB-006 testing protocol:

1. **Test 1: Cross-Agent Information Retrieval**
   - Verifies research agent retrieves context from PM agent's memory
   - Validates sprint deadline retrieval
   - Validates critical blocker retrieval

2. **Test 2: Multi-Agent Context Consolidation**
   - Verifies assistant agent gathers context from multiple agents
   - Tests dev + sales agent context gathering
   - Validates no data loss or corruption

3. **Test 3: Memory Search Across Agents**
   - Verifies searchGlobalMemory finds information across multiple agent memories
   - Tests search ranking and relevance scoring
   - Validates at least one match from relevant agents

### Edge Case Tests
- Empty memory files
- Malformed memory files
- Empty search queries
- Special characters in queries
- Long search queries
- Non-ASCII characters in memory content

### Performance Tests
- Memory read performance (<100ms)
- Search performance (<200ms)
- Agent listing performance (<50ms)

## Test Data

Tests use temporary agent directories in `/tmp/faintech-test-agents/` with the following structure:

```
/tmp/faintech-test-agents/
├── test-pm/
│   ├── MEMORY.md          # Contains sprint deadline and blocker info
│   └── memory/
│       └── 2026-03-16.md  # Daily note
├── test-sales/
│   └── MEMORY.md          # Contains CRM status
├── test-dev/
│   └── MEMORY.md          # Contains current task info
└── test-research/
    └── MEMORY.md          # Default content
```

## Success Criteria

LAB-006 success requires ≥80% pass rate across all tests:

- Cross-agent information retrieval works reliably
- Global memory functions perform as specified
- Search returns relevant, ranked results
- No data loss or corruption in context consolidation
- Performance thresholds met

## Coverage

Run `npm run test:coverage` to generate coverage reports:

- Terminal coverage summary
- JSON coverage report (`coverage/coverage-final.json`)
- HTML coverage report (`coverage/index.html`)

## CI/CD Integration

Add to your CI pipeline:

```yaml
- name: Run tests
  run: npm test

- name: Generate coverage
  run: npm run test:coverage

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/coverage-final.json
```

## Troubleshooting

### Tests fail with "Cannot find module"
Ensure dependencies are installed:
```bash
npm install
```

### TypeScript errors
Run type check to see all errors:
```bash
npm run typecheck
```

### Tests timeout
Increase timeout in vitest.config.ts:
```ts
export default defineConfig({
  test: {
    testTimeout: 10000, // 10 seconds
  },
});
```

## Contributing

When adding new tests:
1. Add test function to appropriate describe block
2. Follow naming convention: `should <expected behavior>`
3. Include setup and teardown if needed
4. Add relevant test data in beforeEach/afterEach
5. Update this README with new test descriptions

## Related Documentation

- [LAB-006 Testing Protocol](../docs/research/LAB-006-testing-protocol.md)
- [Memory Utils Implementation](../src/lib/memory-utils.ts)
- [LAB-SCOPE.md](../LAB-SCOPE.md)

---

**Created:** 2026-03-16
**Owner:** dev agent (testing lane)
**Experiment:** LAB-006 (Global Memory Access Pattern Validation)
