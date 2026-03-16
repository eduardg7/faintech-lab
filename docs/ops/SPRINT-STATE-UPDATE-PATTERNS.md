# SPRINT_STATE.json Update Patterns and Dependencies

**Document Version:** 1.0
**Last Updated:** 2026-03-16
**Related Experiment:** LAB-008 (Data Infrastructure Validation)

---

## Overview

This document describes the update patterns, dependencies, and best practices for SPRINT_STATE.json. It provides guidance for agents and systems that need to read from or write to SPRINT_STATE.json.

**Location:** `/Users/eduardgridan/faintech-lab/SPRINT_STATE.json`
**Validator:** `/Users/eduardgridan/faintech-lab/src/lib/sprint-state-validator.ts`

---

## Table of Contents

1. [Update Patterns](#update-patterns)
2. [Dependencies](#dependencies)
3. [Common Update Scenarios](#common-update-scenarios)
4. [Helper Functions](#helper-functions)
5. [Best Practices](#best-practices)
6. [Error Handling](#error-handling)
7. [Schema Migration](#schema-migration)

---

## Update Patterns

### 1. Direct Update Pattern

Use `updateSprintState()` for direct field updates:

```typescript
import { updateSprintState } from './src/lib/sprint-state-validator';

// Update sprint status
updateSprintState({
  status: 'completed',
  title: 'Sprint 2 - Completed'
});

// Update experiment status
const currentState = ensureSprintState();
const experimentIndex = currentState.experiments.findIndex(e => e.id === 'LAB-006');
if (experimentIndex !== -1) {
  const updatedExperiments = [...currentState.experiments];
  updatedExperiments[experimentIndex] = {
    ...updatedExperiments[experimentIndex],
    status: 'done',
    progress: 'Validation complete with 85% accuracy'
  };
  updateSprintState({ experiments: updatedExperiments });
}
```

**Key Behavior:**
- Automatically updates `metadata.lastUpdated` timestamp
- Merges updates with existing state (partial update)
- Writes atomically to file
- Throws error on write failure

### 2. Array Update Pattern

For array fields (experiments, keyBlockers, recommendations), always read the current state first:

```typescript
// Add new experiment
const state = ensureSprintState();
const newExperiment = {
  id: 'LAB-009',
  title: 'New Experiment',
  status: 'todo',
  track: 'meta-ai'
};
updateSprintState({
  experiments: [...state.experiments, newExperiment]
});

// Add new blocker
const state = ensureSprintState();
updateSprintState({
  findings: {
    ...state.findings,
    keyBlockers: [...state.findings.keyBlockers, 'New blocker description']
  }
});
```

**Warning:** Never use spread operator on arrays without reading current state first, or you'll lose data.

### 3. Nested Field Update Pattern

For nested fields, preserve parent structure:

```typescript
// Update specific field in nested object
const state = ensureSprintState();
updateSprintState({
  findings: {
    ...state.findings,
    sprint1Completed: true,
    sprint2Started: true
  }
});

// Update period dates
const state = ensureSprintState();
updateSprintState({
  period: {
    ...state.period,
    endDate: '2026-03-30'
  }
});
```

### 4. Validation-First Pattern

Always validate state before reading:

```typescript
import { ensureSprintState, updateSprintState } from './src/lib/sprint-state-validator';

// Ensures file exists and is valid before proceeding
const state = ensureSprintState();

// Perform business logic
if (state.status === 'active') {
  updateSprintState({
    status: 'completed'
  });
}
```

**Benefits:**
- Auto-creates file if missing
- Auto-recreates if corrupted
- Guarantees valid structure

### 5. Batch Update Pattern

For multiple updates, use a single `updateSprintState()` call:

```typescript
// Good: Single batch update
updateSprintState({
  status: 'completed',
  findings: {
    ...state.findings,
    sprint2Completed: true
  },
  metadata: {
    ...state.metadata,
    completedAt: new Date().toISOString()
  }
});

// Avoid: Multiple separate writes
updateSprintState({ status: 'completed' });
updateSprintState({
  findings: {
    ...state.findings,
    sprint2Completed: true
  }
}); // Creates race condition potential
```

---

## Dependencies

### Systems that READ from SPRINT_STATE.json

| System | Usage | Frequency | Criticality |
|--------|-------|-----------|-------------|
| **Faintech Lab Experiments** | Read sprint context, experiment status | Per experiment run | HIGH |
| **LAB-006 (Global Memory)** | Read sprint ID for memory context | Per memory operation | HIGH |
| **LAB-007 (Observability)** | Read sprint metrics for dashboard | Real-time (every 5s) | MEDIUM |
| **Sprint Status Checks** | Verify sprint status before operations | On-demand | MEDIUM |
| **Report Generation** | Read findings and metrics | Per report | MEDIUM |

### Systems that WRITE to SPRINT_STATE.json

| System | Usage | Frequency | Criticality |
|--------|-------|-----------|-------------|
| **Agent Startup Scripts** | Call `ensureSprintState()` on init | Per agent start | HIGH |
| **Experiment Agents** | Update experiment status, progress | Per experiment phase | HIGH |
| **Sprint Management** | Update sprint status, period dates | Per sprint lifecycle | HIGH |
| **Findings Collector** | Add blockers, recommendations | Per experiment outcome | MEDIUM |
| **Scheduler** | Update sprint start/end dates | Per sprint boundary | MEDIUM |

### Critical Dependencies

1. **Path Hardcoded**: `/Users/eduardgridan/faintech-lab/SPRINT_STATE.json`
   - **Impact:** Single-environment limitation
   - **Mitigation:** Future support for `FAINTECH_LAB_STATE_PATH` env var

2. **File System**: Relies on local file system I/O
   - **Impact:** Requires write permissions
   - **Mitigation:** Check permissions on startup

3. **JSON Schema**: Version 1.0 schema expected
   - **Impact:** Breaking changes require migration
   - **Mitigation:** Version field for future migrations

---

## Common Update Scenarios

### Scenario 1: Starting a New Sprint

```typescript
import { updateSprintState, ensureSprintState } from './src/lib/sprint-state-validator';

// 1. Get current state
const currentState = ensureSprintState();

// 2. Update sprint info
updateSprintState({
  sprintId: 'sprint-3',
  status: 'active',
  title: 'Sprint 3 - Advanced Automation',
  period: {
    startDate: '2026-03-31',
    endDate: '2026-04-13'
  },
  experiments: [], // Clear experiments array
  findings: {
    sprint1Completed: true,
    sprint2Completed: true,
    keyBlockers: [],
    recommendations: []
  },
  metadata: {
    ...currentState.metadata,
    version: '1.0',
    sprintStartedAt: new Date().toISOString()
  }
});
```

### Scenario 2: Updating Experiment Status

```typescript
// Pattern: Experiment status update
const state = ensureSprintState();
const experimentId = 'LAB-006';
const newStatus = 'done';
const progress = 'Validation complete with 85% accuracy';

const updatedExperiments = state.experiments.map(exp =>
  exp.id === experimentId
    ? { ...exp, status: newStatus, progress }
    : exp
);

updateSprintState({ experiments: updatedExperiments });
```

### Scenario 3: Adding Key Blocker

```typescript
// Pattern: Add blocker to findings
const state = ensureSprintState();
const blocker = 'SPRINT_STATE.json missing → cannot evaluate sprint status';

updateSprintState({
  findings: {
    ...state.findings,
    keyBlockers: [...state.findings.keyBlockers, blocker]
  }
});
```

### Scenario 4: Removing Key Blocker

```typescript
// Pattern: Remove specific blocker
const state = ensureSprintState();
const blockerToRemove = 'SPRINT_STATE.json missing';

updateSprintState({
  findings: {
    ...state.findings,
    keyBlockers: state.findings.keyBlockers.filter(b => b !== blockerToRemove)
  }
});
```

### Scenario 5: Adding Recommendation

```typescript
// Pattern: Add recommendation
const state = ensureSprintState();
const recommendation = 'Implement role-specific metrics framework';

updateSprintState({
  findings: {
    ...state.findings,
    recommendations: [...state.findings.recommendations, recommendation]
  }
});
```

### Scenario 6: Completing Sprint

```typescript
// Pattern: Mark sprint as completed
const state = ensureSprintState();

updateSprintState({
  status: 'completed',
  period: {
    ...state.period,
    endDate: new Date().toISOString().split('T')[0]
  },
  metadata: {
    ...state.metadata,
    completedAt: new Date().toISOString()
  }
});
```

---

## Helper Functions

### Recommended Helper Functions

These functions are **recommended** for common operations but **not yet implemented**. Add them to `src/lib/sprint-state-validator.ts`:

#### 1. updateExperimentStatus()

```typescript
/**
 * Update experiment status and progress
 */
export function updateExperimentStatus(
  experimentId: string,
  status: 'todo' | 'in_progress' | 'done' | 'blocked',
  progress?: string
): SprintState {
  const state = ensureSprintState();
  const updatedExperiments = state.experiments.map(exp =>
    exp.id === experimentId
      ? { ...exp, status, ...(progress && { progress }) }
      : exp
  );

  return updateSprintState({ experiments: updatedExperiments });
}
```

**Usage:**
```typescript
updateExperimentStatus('LAB-006', 'done', 'Validation complete');
```

#### 2. addKeyBlocker()

```typescript
/**
 * Add a key blocker to findings
 */
export function addKeyBlocker(blocker: string): SprintState {
  const state = ensureSprintState();
  return updateSprintState({
    findings: {
      ...state.findings,
      keyBlockers: [...state.findings.keyBlockers, blocker]
    }
  });
}
```

**Usage:**
```typescript
addKeyBlocker('SPRINT_STATE.json missing → cannot evaluate sprint status');
```

#### 3. removeKeyBlocker()

```typescript
/**
 * Remove a key blocker from findings
 */
export function removeKeyBlocker(blocker: string): SprintState {
  const state = ensureSprintState();
  return updateSprintState({
    findings: {
      ...state.findings,
      keyBlockers: state.findings.keyBlockers.filter(b => b !== blocker)
    }
  });
}
```

**Usage:**
```typescript
removeKeyBlocker('SPRINT_STATE.json missing');
```

#### 4. addRecommendation()

```typescript
/**
 * Add a recommendation to findings
 */
export function addRecommendation(recommendation: string): SprintState {
  const state = ensureSprintState();
  return updateSprintState({
    findings: {
      ...state.findings,
      recommendations: [...state.findings.recommendations, recommendation]
    }
  });
}
```

**Usage:**
```typescript
addRecommendation('Implement role-specific metrics framework');
```

#### 5. addExperiment()

```typescript
/**
 * Add a new experiment to the sprint
 */
export function addExperiment(
  experiment: {
    id: string;
    title: string;
    status: 'todo' | 'in_progress' | 'done' | 'blocked';
    track?: string;
    description?: string;
    progress?: string;
  }
): SprintState {
  const state = ensureSprintState();
  return updateSprintState({
    experiments: [...state.experiments, experiment]
  });
}
```

**Usage:**
```typescript
addExperiment({
  id: 'LAB-009',
  title: 'New Experiment',
  status: 'todo',
  track: 'meta-ai',
  description: 'Test new feature'
});
```

---

## Best Practices

### 1. Always Call `ensureSprintState()` First

```typescript
// Good
const state = ensureSprintState();
updateSprintState({ status: 'completed' });

// Avoid (file might not exist or be corrupted)
updateSprintState({ status: 'completed' });
```

### 2. Use Batch Updates for Multiple Changes

```typescript
// Good: Single atomic update
updateSprintState({
  status: 'completed',
  findings: { ...state.findings, sprint2Completed: true }
});

// Avoid: Multiple writes (race condition risk)
updateSprintState({ status: 'completed' });
updateSprintState({
  findings: { ...state.findings, sprint2Completed: true }
});
```

### 3. Preserve Array Order

```typescript
// Good: Preserve order when modifying arrays
const updatedExperiments = state.experiments.map(exp =>
  exp.id === targetId ? { ...exp, status: 'done' } : exp
);

// Avoid: Filter+map (changes order)
const updatedExperiments = state.experiments
  .filter(exp => exp.id !== targetId)
  .concat([{ id: targetId, status: 'done' }]);
```

### 4. Update Metadata Last

```typescript
// Good: metadata updated automatically by updateSprintState()
updateSprintState({ status: 'completed' }); // lastUpdated auto-set

// Avoid: Manual metadata updates
updateSprintState({
  status: 'completed',
  metadata: {
    ...state.metadata,
    lastUpdated: new Date().toISOString() // Redundant
  }
});
```

### 5. Handle Errors Gracefully

```typescript
// Good: Error handling
try {
  updateSprintState({ status: 'completed' });
  console.log('State updated successfully');
} catch (error) {
  console.error('Failed to update state:', error);
  // Retry or fallback logic
}

// Avoid: No error handling
updateSprintState({ status: 'completed' }); // Throws if write fails
```

### 6. Validate Updates Before Writing

```typescript
// Good: Validate before update
if (newStatus === 'done' && !experimentOutcome) {
  console.warn('Cannot mark experiment as done without outcome');
  return;
}
updateSprintState({ experiments: updatedExperiments });

// Avoid: Write without validation
updateSprintState({ experiments: updatedExperiments });
```

---

## Error Handling

### Common Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| `ENOENT` | File path does not exist | Call `ensureSprintState()` first |
| `EACCES` | No write permissions | Check file permissions (chmod 600) |
| `JSON.parse` error | Corrupted JSON | Call `ensureSprintState()` to recreate |
| `Validation failed` | Missing required fields | Use `validateSprintState()` before update |

### Error Handling Pattern

```typescript
import { ensureSprintState, updateSprintState } from './src/lib/sprint-state-validator';

function safeUpdateSprintState(updates: Partial<SprintState>): boolean {
  try {
    const state = ensureSprintState();
    updateSprintState(updates);
    return true;
  } catch (error) {
    console.error('Failed to update SPRINT_STATE.json:', error);
    // Implement retry logic or fallback
    return false;
  }
}
```

### Recovery Pattern

```typescript
// Recover from corrupted state
try {
  const state = readSprintState();
  if (!validateSprintState(state)) {
    console.warn('State is invalid, recreating...');
    return createDefaultSprintState();
  }
  return state;
} catch (error) {
  console.error('Failed to read state:', error);
  return createDefaultSprintState();
}
```

---

## Schema Migration

### Current Schema: Version 1.0

```typescript
interface SprintState {
  sprintId: string;
  status: 'initializing' | 'active' | 'completed' | 'blocked';
  title: string;
  period: {
    startDate: string; // ISO date format
    endDate: string | null; // ISO date format or null
  };
  experiments: Array<{
    id: string;
    title: string;
    status: 'todo' | 'in_progress' | 'done' | 'blocked';
    track?: string;
    progress?: string;
  }>;
  findings: {
    sprint1Completed: boolean;
    sprint2Completed?: boolean; // Optional field
    sprint3Completed?: boolean; // Optional field
    keyBlockers: string[];
    recommendations: string[];
  };
  metadata: {
    createdAt: string; // ISO timestamp
    lastUpdated: string; // ISO timestamp
    version: '1.0'; // Schema version
    completedAt?: string; // Optional field
  };
}
```

### Future Schema Changes

#### Version 2.0 (Planned)

**New Fields:**
- `team`: Array of participant IDs
- `milestones`: Array of sprint milestones
- `metrics`: Object with sprint metrics

**Migration Strategy:**
```typescript
function migrateToV2(state: SprintStateV1): SprintStateV2 {
  return {
    ...state,
    team: [],
    milestones: [],
    metrics: {
      completionRate: 0,
      blockerCount: state.findings.keyBlockers.length
    },
    metadata: {
      ...state.metadata,
      version: '2.0',
      migratedAt: new Date().toISOString()
    }
  };
}
```

#### Version 3.0 (Planned)

**New Fields:**
- `sprintHistory`: Array of past sprint summaries
- `experimentDependencies`: Array of dependency relationships

**Migration Strategy:**
- Preserve existing data
- Add new fields with default values
- Update version number

### Migration Implementation Pattern

```typescript
function ensureSchemaVersion(targetVersion: string): SprintState {
  const state = ensureSprintState();

  if (state.metadata.version === targetVersion) {
    return state; // Already on target version
  }

  console.log(`Migrating from v${state.metadata.version} to v${targetVersion}`);

  // Apply migrations in order
  if (state.metadata.version === '1.0' && targetVersion === '2.0') {
    return migrateToV2(state);
  }

  if (state.metadata.version === '2.0' && targetVersion === '3.0') {
    return migrateToV3(state);
  }

  // Add more migration paths as needed
  throw new Error(`Unsupported migration path: ${state.metadata.version} -> ${targetVersion}`);
}
```

---

## Appendix: TypeScript Interface

```typescript
interface SprintState {
  sprintId: string;
  status: 'initializing' | 'active' | 'completed' | 'blocked';
  title: string;
  period: {
    startDate: string;
    endDate: string | null;
  };
  experiments: Array<{
    id: string;
    title: string;
    status: 'todo' | 'in_progress' | 'done' | 'blocked';
    track?: string;
    progress?: string;
    description?: string;
  }>;
  findings: {
    sprint1Completed: boolean;
    sprint2Completed?: boolean;
    sprint3Completed?: boolean;
    keyBlockers: string[];
    recommendations: string[];
  };
  metadata: {
    createdAt: string;
    lastUpdated: string;
    version: string;
    completedAt?: string;
    sprintStartedAt?: string;
  };
}
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-16 | Initial documentation created for AC4/5 of LAB-MMTI0R2X |

---

**Document Owner:** Assistant Agent
**Status:** ✅ Complete
**Related Tasks:** OS-20260316184642-33AC (AC4/5)
