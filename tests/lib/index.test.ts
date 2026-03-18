/**
 * Integration tests for lib barrel exports
 */

import { describe, it, expect } from 'vitest';

describe('Lib Index Exports', () => {
  it('should export error classes', async () => {
    const { LibError, FileOperationError, ValidationError, NotFoundError, withErrorHandling } = await import('../../src/lib');
    expect(LibError).toBeDefined();
    expect(FileOperationError).toBeDefined();
    expect(ValidationError).toBeDefined();
    expect(NotFoundError).toBeDefined();
    expect(withErrorHandling).toBeDefined();
  });

  it('should export memory utilities', async () => {
    const { readGlobalMemory, searchGlobalMemory, getCrossAgentContext, listAvailableAgents } = await import('../../src/lib');
    expect(readGlobalMemory).toBeDefined();
    expect(searchGlobalMemory).toBeDefined();
    expect(getCrossAgentContext).toBeDefined();
    expect(listAvailableAgents).toBeDefined();
  });

  it('should export sprint state utilities', async () => {
    const { sprintStateExists, readSprintState, ensureSprintState, updateSprintState } = await import('../../src/lib');
    expect(sprintStateExists).toBeDefined();
    expect(readSprintState).toBeDefined();
    expect(ensureSprintState).toBeDefined();
    expect(updateSprintState).toBeDefined();
  });

  it('should export health score utilities', async () => {
    const { HealthScoreCalculator, calculateHealthScore, getHealthScoreCalculator } = await import('../../src/lib');
    expect(HealthScoreCalculator).toBeDefined();
    expect(calculateHealthScore).toBeDefined();
    expect(getHealthScoreCalculator).toBeDefined();
  });

  it('should export types', async () => {
    const mod = await import('../../src/lib');
    // Types are checked at compile time, just verify module loads
    expect(mod).toBeDefined();
  });
});
