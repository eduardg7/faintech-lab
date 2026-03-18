/**
 * Tests for Sprint State Validator
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const TEST_DIR = path.join(os.tmpdir(), 'sprint-state-test-' + Date.now());
const TEST_SPRINT_STATE_PATH = path.join(TEST_DIR, 'SPRINT_STATE.json');

// Set environment variable before importing module
process.env.SPRINT_STATE_PATH = TEST_SPRINT_STATE_PATH;

// Import after setting env var
let validateSprintState: (state: any) => boolean;
let sprintStateExists: () => boolean;
let readSprintState: () => any;
let createDefaultSprintState: () => any;
let ensureSprintState: () => any;
let updateSprintState: (updates: any) => any;

beforeEach(async () => {
  vi.resetModules();

  // Create test directory
  if (!fs.existsSync(TEST_DIR)) {
    fs.mkdirSync(TEST_DIR, { recursive: true });
  }

  // Re-import module after reset
  const module = await import('../../src/lib/sprint-state-validator');
  validateSprintState = module.validateSprintState;
  sprintStateExists = module.sprintStateExists;
  readSprintState = module.readSprintState;
  createDefaultSprintState = module.createDefaultSprintState;
  ensureSprintState = module.ensureSprintState;
  updateSprintState = module.updateSprintState;
});

afterEach(() => {
  vi.clearAllMocks();

  // Cleanup test directory
  if (fs.existsSync(TEST_DIR)) {
    fs.rmSync(TEST_DIR, { recursive: true, force: true });
  }
});

describe('validateSprintState', () => {
  it('should return true for valid sprint state', () => {
    const validState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      period: {
        startDate: '2026-03-01',
        endDate: '2026-03-15'
      },
      experiments: [],
      findings: {
        sprint1Completed: false,
        keyBlockers: [],
        recommendations: []
      },
      metadata: {
        createdAt: '2026-03-01T00:00:00Z',
        lastUpdated: '2026-03-01T00:00:00Z',
        version: '1.0'
      }
    };

    expect(validateSprintState(validState)).toBe(true);
  });

  it('should return false when sprintId is missing', () => {
    const invalidState = {
      status: 'active',
      title: 'Test Sprint',
      period: { startDate: '2026-03-01' },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return false when status is missing', () => {
    const invalidState = {
      sprintId: 'sprint-1',
      title: 'Test Sprint',
      period: { startDate: '2026-03-01' },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return false when title is missing', () => {
    const invalidState = {
      sprintId: 'sprint-1',
      status: 'active',
      period: { startDate: '2026-03-01' },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return false when period is missing', () => {
    const invalidState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return false when period.startDate is missing', () => {
    const invalidState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      period: { endDate: '2026-03-15' },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return false when experiments is missing', () => {
    const invalidState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      period: { startDate: '2026-03-01' },
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return false when findings is missing', () => {
    const invalidState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      period: { startDate: '2026-03-01' },
      experiments: [],
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return false when metadata is missing', () => {
    const invalidState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      period: { startDate: '2026-03-01' },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] }
    };

    expect(validateSprintState(invalidState)).toBe(false);
  });

  it('should return true for state with experiments', () => {
    const validState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      period: { startDate: '2026-03-01' },
      experiments: [
        { id: 'exp-1', title: 'Test Experiment', status: 'running' }
      ],
      findings: {
        sprint1Completed: true,
        keyBlockers: ['blocker-1'],
        recommendations: ['rec-1']
      },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(validState)).toBe(true);
  });

  it('should return true for state with null endDate', () => {
    const validState = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test Sprint',
      period: { startDate: '2026-03-01', endDate: null },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };

    expect(validateSprintState(validState)).toBe(true);
  });
});

describe('sprintStateExists', () => {
  it('should return false when file does not exist', () => {
    expect(sprintStateExists()).toBe(false);
  });

  it('should return true when file exists', () => {
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, '{}', 'utf-8');
    expect(sprintStateExists()).toBe(true);
  });
});

describe('readSprintState', () => {
  it('should return null when file does not exist', () => {
    expect(readSprintState()).toBeNull();
  });

  it('should return parsed JSON when file exists', () => {
    const testData = {
      sprintId: 'sprint-1',
      status: 'active',
      title: 'Test',
      period: { startDate: '2026-03-01', endDate: null },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, JSON.stringify(testData), 'utf-8');

    const result = readSprintState();
    expect(result).not.toBeNull();
    expect(result?.sprintId).toBe('sprint-1');
    expect(result?.status).toBe('active');
  });

  it('should return null for invalid JSON', () => {
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, 'not valid json', 'utf-8');
    expect(readSprintState()).toBeNull();
  });
});

describe('createDefaultSprintState', () => {
  it('should create file with default values', () => {
    const result = createDefaultSprintState();

    expect(result).toBeDefined();
    expect(result.sprintId).toBe('sprint-unknown');
    expect(result.status).toBe('initializing');
    expect(fs.existsSync(TEST_SPRINT_STATE_PATH)).toBe(true);
  });

  it('should overwrite existing file', () => {
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, '{"sprintId": "old"}', 'utf-8');

    const result = createDefaultSprintState();
    expect(result.sprintId).toBe('sprint-unknown');
  });
});

describe('ensureSprintState', () => {
  it('should create default when file does not exist', () => {
    const result = ensureSprintState();
    expect(result.sprintId).toBe('sprint-unknown');
    expect(fs.existsSync(TEST_SPRINT_STATE_PATH)).toBe(true);
  });

  it('should return existing valid state', () => {
    const existingState = {
      sprintId: 'existing-sprint',
      status: 'active',
      title: 'Existing Sprint',
      period: { startDate: '2026-03-01', endDate: null },
      experiments: [],
      findings: { sprint1Completed: false, keyBlockers: [], recommendations: [] },
      metadata: { createdAt: '', lastUpdated: '', version: '1.0' }
    };
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, JSON.stringify(existingState), 'utf-8');

    const result = ensureSprintState();
    expect(result.sprintId).toBe('existing-sprint');
  });

  it('should recreate when file has invalid structure', () => {
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, '{"invalid": "structure"}', 'utf-8');

    const result = ensureSprintState();
    expect(result.sprintId).toBe('sprint-unknown');
  });

  it('should recreate when file has invalid JSON', () => {
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, 'not json', 'utf-8');

    const result = ensureSprintState();
    expect(result.sprintId).toBe('sprint-unknown');
  });
});

describe('updateSprintState', () => {
  it('should update sprint state with new values', () => {
    // First ensure state exists
    ensureSprintState();

    const result = updateSprintState({ status: 'completed', title: 'Updated Sprint' });

    expect(result.status).toBe('completed');
    expect(result.title).toBe('Updated Sprint');
    expect(result.metadata.lastUpdated).toBeDefined();
  });

  it('should preserve existing values not updated', () => {
    const existingState = {
      sprintId: 'preserve-test',
      status: 'active',
      title: 'Original Title',
      period: { startDate: '2026-03-01', endDate: null },
      experiments: [{ id: 'exp-1', title: 'Test', status: 'running' }],
      findings: { sprint1Completed: false, keyBlockers: ['blocker'], recommendations: [] },
      metadata: { createdAt: '2026-03-01', lastUpdated: '2026-03-01', version: '1.0' }
    };
    fs.writeFileSync(TEST_SPRINT_STATE_PATH, JSON.stringify(existingState), 'utf-8');

    const result = updateSprintState({ status: 'completed' });

    expect(result.sprintId).toBe('preserve-test');
    expect(result.title).toBe('Original Title');
    expect(result.experiments).toHaveLength(1);
    expect(result.status).toBe('completed');
  });

  it('should create default state if none exists', () => {
    const result = updateSprintState({ status: 'active' });

    expect(result).toBeDefined();
    expect(result.status).toBe('active');
  });
});
