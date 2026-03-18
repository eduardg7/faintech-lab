/**
 * Sprint State Validator
 *
 * Ensures SPRINT_STATE.json exists and is valid. Creates a default file if missing.
 * Run this on system startup to ensure data infrastructure is available.
 */

import * as fs from 'fs';
import * as path from 'path';

const SPRINT_STATE_PATH = '/Users/eduardgridan/faintech-lab/SPRINT_STATE.json';
const DEFAULT_SPRINT_STATE = {
  sprintId: 'sprint-unknown',
  status: 'initializing',
  title: 'Auto-generated sprint state',
  period: {
    startDate: new Date().toISOString().split('T')[0],
    endDate: null
  },
  experiments: [],
  findings: {
    sprint1Completed: false,
    keyBlockers: [],
    recommendations: []
  },
  metadata: {
    createdAt: new Date().toISOString(),
    lastUpdated: new Date().toISOString(),
    version: '1.0'
  }
};

interface SprintState {
  sprintId: string;
  status: string;
  title: string;
  period: {
    startDate: string;
    endDate: string | null;
  };
  experiments: Array<{
    id: string;
    title: string;
    status: string;
    track?: string;
  }>;
  findings: {
    sprint1Completed: boolean;
    keyBlockers: string[];
    recommendations: string[];
  };
  metadata: {
    createdAt: string;
    lastUpdated: string;
    version: string;
  };
}

/**
 * Check if SPRINT_STATE.json exists
 */
export function sprintStateExists(): boolean {
  try {
    return fs.existsSync(SPRINT_STATE_PATH);
  } catch (error) {
    console.error('Error checking SPRINT_STATE.json:', error);
    return false;
  }
}

/**
 * Read SPRINT_STATE.json
 */
export function readSprintState(): SprintState | null {
  try {
    const content = fs.readFileSync(SPRINT_STATE_PATH, 'utf-8');
    const state = JSON.parse(content) as SprintState;
    return state;
  } catch (error) {
    console.error('Error reading SPRINT_STATE.json:', error);
    return null;
  }
}

/**
 * Create default SPRINT_STATE.json
 */
export function createDefaultSprintState(): SprintState {
  try {
    fs.writeFileSync(
      SPRINT_STATE_PATH,
      JSON.stringify(DEFAULT_SPRINT_STATE, null, 2),
      'utf-8'
    );
    console.log('Created default SPRINT_STATE.json');
    return DEFAULT_SPRINT_STATE as SprintState;
  } catch (error) {
    console.error('Error creating SPRINT_STATE.json:', error);
    throw error;
  }
}

/**
 * Validate SPRINT_STATE.json structure
 */
export function validateSprintState(state: SprintState): boolean {
  const requiredFields = ['sprintId', 'status', 'title', 'period', 'experiments', 'findings', 'metadata'];
  const missingFields = requiredFields.filter(field => !(field in state));

  if (missingFields.length > 0) {
    console.warn(`Missing required fields: ${missingFields.join(', ')}`);
    return false;
  }

  // Validate period structure
  if (!state.period || !state.period.startDate) {
    console.warn('Invalid period structure');
    return false;
  }

  return true;
}

/**
 * Ensure SPRINT_STATE.json exists and is valid
 * Create default file if missing
 */
export function ensureSprintState(): SprintState {
  // Check if file exists
  if (!sprintStateExists()) {
    console.warn('SPRINT_STATE.json not found. Creating default...');
    return createDefaultSprintState();
  }

  // Try to read existing file
  const state = readSprintState();
  if (!state) {
    console.warn('SPRINT_STATE.json is invalid. Recreating...');
    return createDefaultSprintState();
  }

  // Validate structure
  if (!validateSprintState(state)) {
    console.warn('SPRINT_STATE.json structure is invalid. Recreating...');
    return createDefaultSprintState();
  }

  console.log('SPRINT_STATE.json is valid');
  return state;
}

/**
 * Update SPRINT_STATE.json
 */
export function updateSprintState(updates: Partial<SprintState>): SprintState {
  const state = ensureSprintState();

  const updatedState = {
    ...state,
    ...updates,
    metadata: {
      ...state.metadata,
      lastUpdated: new Date().toISOString()
    }
  };

  try {
    fs.writeFileSync(
      SPRINT_STATE_PATH,
      JSON.stringify(updatedState, null, 2),
      'utf-8'
    );
    console.log('Updated SPRINT_STATE.json');
    return updatedState;
  } catch (error) {
    console.error('Error updating SPRINT_STATE.json:', error);
    throw error;
  }
}

// CLI: Run validation on startup
if (require.main === module) {
  console.log('=== Sprint State Validator ===');
  ensureSprintState();
  console.log('=== Validation Complete ===');
}
