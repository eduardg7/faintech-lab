# LAB-006: Global Memory Access Pattern Validation

**Experiment ID**: LAB-006
**Purpose**: Test standardized global memory access pattern for cross-agent context transfer
**Status**: IN PROGRESS
**Agent**: dev
**Date Started**: 2026-03-16T19:29:00Z

---

## Background

From LAB-003 findings:
- `memory_search` tool is **agent-scoped** (only searches requesting agent's files)
- Cross-agent handoff failed at **41.7% accuracy** vs **95-100% same-agent**
- Root cause: dev agent could not access pm agent's MEMORY.md

## Hypothesis

Standardized global memory access enables cross-agent context transfer with ≥80% accuracy.

## Solution

Created `/Users/eduardgridan/faintech-lab/src/lib/memory-utils.ts` - a global memory utility that:
1. Accepts `targetAgent` parameter to specify which agent's memory to read
2. Reads directly from global memory paths (`~/.openclaw/agents/{agentId}/MEMORY.md`)
3. Provides text-based search across all agents' memory

## API

### Read Global Memory
```typescript
import { readGlobalMemory } from './memory-utils';

// Read pm agent's memory
const pmMemory = await readGlobalMemory('pm');
console.log(pmMemory.content);
```

### Search Global Memory
```typescript
import { searchGlobalMemory } from './memory-utils';

// Search across all agents
const results = await searchGlobalMemory('project decisions', {
  limit: 10,
  minScore: 0.3
});

// Search specific agent
const pmResults = await searchGlobalMemory('project decisions', {
  agentId: 'pm'
});
```

### Get Cross-Agent Context
```typescript
import { getCrossAgentContext } from './memory-utils';

// Get consolidated context from relevant agents
const { primaryResults, contextByAgent } = await getCrossAgentContext(
  'project decisions',
  { limit: 5 }
);
```

## Functions

| Function | Description |
|----------|-------------|
| `readGlobalMemory(agentId)` | Read an agent's MEMORY.md |
| `readDailyNotes(agentId, limit?)` | Read an agent's daily notes |
| `searchGlobalMemory(query, options)` | Search across agent memory |
| `listAvailableAgents()` | List all agents with memory |
| `agentMemoryExists(agentId)` | Check if agent has memory |
| `readMultiAgentMemory(agentIds)` | Read from multiple agents |
| `getCrossAgentContext(query, options)` | Get consolidated context |

## Options

```typescript
interface GlobalMemoryOptions {
  agentId?: string;        // Specific agent (omit for all)
  includeDailyNotes?: boolean;  // Include daily notes (default: false)
  limit?: number;          // Max results (default: 10)
  minScore?: number;       // Min relevance 0-1 (default: 0.1)
  contextLines?: number;   // Context lines around matches (default: 3)
}
```

## Acceptance Criteria Progress

| # | Criteria | Status | Notes |
|---|----------|--------|-------|
| 1 | Global memory utility function implemented in memory-utils.ts | ✅ DONE | 8240 bytes, 7 exported functions |
| 2 | Cross-agent handoff test achieves ≥80% accuracy | ⏳ PENDING | Needs test execution |
| 3 | Documentation explains how to use global memory access pattern | ✅ DONE | This document |
| 4 | Test results documented in LAB-006-results.md | ⏳ PENDING | This document, awaiting test results |

## Next Steps

1. Execute cross-agent handoff test using the new utility
2. Compare accuracy to LAB-003 baseline (41.7%)
3. Document final results

---

**Created**: 2026-03-16T19:29:00Z
**Agent**: dev
