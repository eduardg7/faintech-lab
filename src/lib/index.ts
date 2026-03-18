/**
 * Lib Module Exports (Barrel File)
 *
 * Centralized exports for all lib modules for cleaner imports.
 */

// Error utilities
export {
  LibError,
  FileOperationError,
  ValidationError,
  NotFoundError,
  withErrorHandling,
} from './errors';

// Memory utilities
export {
  readGlobalMemory,
  searchGlobalMemory,
  getCrossAgentContext,
  listAvailableAgents,
  agentMemoryExists,
  readDailyNotes,
  readMultiAgentMemory,
  getAgentMemoryPath,
  type MemoryReadResult,
  type MemorySearchResult,
  type GlobalMemoryOptions,
} from './memory-utils';

// Sprint state validator
export {
  sprintStateExists,
  readSprintState,
  createDefaultSprintState,
  validateSprintState,
  ensureSprintState,
  updateSprintState,
  type SprintState,
} from './sprint-state-validator';

// Analytics - Health Score Calculator
export {
  HealthScoreCalculator,
  calculateHealthScore,
  calculateHealthScores,
  getHealthScoreCalculator,
  configureHealthScoreCalculator,
  type UserActivityData,
  type HealthScoreBreakdown,
} from './analytics/health-score-calculator';
