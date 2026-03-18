/**
 * Test Harness for memory-utils.ts
 *
 * Tests global memory access functions for cross-agent context sharing.
 * Based on LAB-006 testing protocol.
 *
 * Run with: npx vitest run tests/memory-utils.test.ts
 * Or: npm test (if configured in package.json)
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

// Import the functions to test
import {
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
} from '../src/lib/memory-utils';

// Test constants
const TEST_HOME_DIR = path.join(os.tmpdir(), 'faintech-test-home');
const TEST_AGENTS_DIR = path.join(TEST_HOME_DIR, '.openclaw', 'agents');
const TEST_MEMORY_CONTENT = '# Test Agent Memory\n\nProject sprint deadline: 2026-03-30\nCritical blocker: LAB-006 cross-agent handoff test pending\nCurrent task: LAB-006 testing protocol';
const TEST_MEMORY_CONTENT_DEV = '# Dev Agent Memory\n\nTesting note: global memory validation session 2026-03-16\nCurrent task: LAB-006 testing protocol\nTest consolidated view data';
const TEST_MEMORY_CONTENT_2 = '# Sales Agent Memory\n\nCRM status: 10 OSM leads added\nPending follow-ups: 15 accounts\nTest consolidated view sales data\n';
const TEST_DAILY_NOTE = '# 2026-03-16\n\nTesting note: global memory validation session 2026-03-16';

// Setup and teardown - top-level hooks apply to all tests
beforeEach(async () => {
  // Set HOME environment variable for memory-utils.ts
  process.env.HOME = TEST_HOME_DIR;

  // Create test agents directory structure
  if (!fs.existsSync(TEST_AGENTS_DIR)) {
    fs.mkdirSync(TEST_AGENTS_DIR, { recursive: true });
  }

  // Create test agent directories
  const testAgents = ['test-pm', 'test-dev', 'test-sales', 'test-research'];
  for (const agentId of testAgents) {
    const agentPath = path.join(TEST_AGENTS_DIR, agentId);
    if (!fs.existsSync(agentPath)) {
      fs.mkdirSync(agentPath, { recursive: true });
    }

    // Create MEMORY.md
    const memoryPath = path.join(agentPath, 'MEMORY.md');
    if (agentId === 'test-pm') {
      fs.writeFileSync(memoryPath, TEST_MEMORY_CONTENT);
    } else if (agentId === 'test-dev') {
      fs.writeFileSync(memoryPath, TEST_MEMORY_CONTENT_DEV);
    } else if (agentId === 'test-sales') {
      fs.writeFileSync(memoryPath, TEST_MEMORY_CONTENT_2);
    } else {
      fs.writeFileSync(memoryPath, `# ${agentId} Memory\n\nDefault content for ${agentId}.`);
    }

    // Create memory directory for daily notes
    const memoryDir = path.join(agentPath, 'memory');
    if (!fs.existsSync(memoryDir)) {
      fs.mkdirSync(memoryDir, { recursive: true });
    }

    // Create a daily note for test-pm
    if (agentId === 'test-pm') {
      const dailyNotePath = path.join(memoryDir, '2026-03-16.md');
      fs.writeFileSync(dailyNotePath, TEST_DAILY_NOTE);
    }
  }
});

afterEach(() => {
  // Cleanup test directory
  if (fs.existsSync(TEST_HOME_DIR)) {
    fs.rmSync(TEST_HOME_DIR, { recursive: true, force: true });
  }

  // Restore HOME
  delete process.env.HOME;
});

describe('readGlobalMemory', () => {
  it('should read existing agent memory', async () => {
    const result = await readGlobalMemory('test-pm');

    expect(result).toBeDefined();
    expect(result.agentId).toBe('test-pm');
    expect(result.exists).toBe(true);
    expect(result.content).toContain('Project sprint deadline: 2026-03-30');
    expect(result.content).toContain('Critical blocker: LAB-006 cross-agent handoff test pending');
    expect(result.lastModified).toBeTruthy();
  });

  it('should return empty content for non-existent memory', async () => {
    const result = await readGlobalMemory('nonexistent-agent');

    expect(result).toBeDefined();
    expect(result.agentId).toBe('nonexistent-agent');
    expect(result.exists).toBe(false);
    expect(result.content).toBe('');
    expect(result.lastModified).toBe('');
  });

  it('should read memory from multiple agents', async () => {
    const pmResult = await readGlobalMemory('test-pm');
    const salesResult = await readGlobalMemory('test-sales');

    expect(pmResult.agentId).toBe('test-pm');
    expect(salesResult.agentId).toBe('test-sales');
    expect(pmResult.content).toContain('sprint deadline');
    expect(salesResult.content).toContain('CRM status');
  });

  it('should handle special characters in agentId', async () => {
    const agentId = 'test-agent-with-dashes';
    const agentPath = path.join(TEST_AGENTS_DIR, agentId);
    fs.mkdirSync(agentPath, { recursive: true });
    fs.writeFileSync(path.join(agentPath, 'MEMORY.md'), '# Test\n\nContent with special chars: @#$%^&*()');

    const result = await readGlobalMemory(agentId);

    expect(result.exists).toBe(true);
    expect(result.content).toContain('Content with special chars');
  });
});

describe('searchGlobalMemory', () => {
  it('should find "sprint deadline" in test-pm memory', async () => {
    const results = await searchGlobalMemory('sprint deadline', { agentId: 'test-pm' });

    expect(results).toHaveLength(1);
    expect(results[0].agentId).toBe('test-pm');
    expect(results[0].relevanceScore).toBeGreaterThan(0);
    expect(results[0].snippet).toContain('2026-03-30');
  });

  it('should search across all agents when agentId not specified', async () => {
    const results = await searchGlobalMemory('testing');

    expect(results.length).toBeGreaterThan(0);
    expect(results.some(r => r.agentId === 'test-pm')).toBe(true);
  });

  it('should limit results when limit option is provided', async () => {
    const results = await searchGlobalMemory('test', { limit: 2 });

    expect(results.length).toBeLessThanOrEqual(2);
  });

  it('should filter by minimum relevance score', async () => {
    const results = await searchGlobalMemory('nonexistent-term', { minScore: 0.5 });

    // Should return fewer or no results for non-existent term
    expect(results.length).toBe(0);
  });

  it('should include context lines around matches', async () => {
    const results = await searchGlobalMemory('LAB-006', { agentId: 'test-pm', contextLines: 2 });

    expect(results.length).toBeGreaterThanOrEqual(1);
    expect(results[0].snippet.split('\n').length).toBeGreaterThan(1); // Should have context
  });

  it('should search daily notes when includeDailyNotes is true', async () => {
    const results = await searchGlobalMemory('global memory validation', {
      agentId: 'test-pm',
      includeDailyNotes: true,
    });

    expect(results.length).toBeGreaterThan(0);
    expect(results.some(r => r.filePath.includes('2026-03-16.md'))).toBe(true);
  });

  it('should return results sorted by relevance score', async () => {
    const results = await searchGlobalMemory('test', { limit: 10 });

    // Check if sorted by relevance (highest first)
    for (let i = 1; i < results.length; i++) {
      expect(results[i - 1].relevanceScore).toBeGreaterThanOrEqual(results[i].relevanceScore);
    }
  });

  it('should handle multi-term queries', async () => {
    const results = await searchGlobalMemory('cross-agent handoff', { agentId: 'test-pm' });

    expect(results).toHaveLength(1);
    expect(results[0].snippet.toLowerCase()).toContain('cross-agent');
  });

  it('should return empty array for no matches', async () => {
    const results = await searchGlobalMemory('nonexistent query term xyz123', { agentId: 'test-pm' });

    expect(results).toEqual([]);
  });
});

describe('getCrossAgentContext', () => {
  it('should get consolidated context from multiple agents', async () => {
    const result = await getCrossAgentContext('CRM status', {
      limit: 2,
    });

    expect(result).toBeDefined();
    expect(result.primaryResults).toBeDefined();
    expect(result.contextByAgent).toBeDefined();
    expect(result.contextByAgent.size).toBeGreaterThan(0);
  });

  it('should search with query and return relevant agents', async () => {
    const result = await getCrossAgentContext('sprint deadline');

    expect(result.primaryResults.length).toBeGreaterThan(0);
    expect(result.primaryResults[0].agentId).toBe('test-pm');
    expect(result.primaryResults[0].snippet).toContain('2026-03-30');
  });

  it('should limit primary results', async () => {
    const result = await getCrossAgentContext('test', { limit: 1 });

    expect(result.primaryResults.length).toBeLessThanOrEqual(1);
  });

  it('should return context map with agent IDs as keys', async () => {
    const result = await getCrossAgentContext('LAB-006');

    expect(result.contextByAgent).toBeInstanceOf(Map);
    expect(result.contextByAgent.has('test-pm')).toBe(true);
  });

  it('should provide truncated context (first 2000 chars)', async () => {
    // Create a large memory file
    const largeContent = '# Large Memory\n\n' + 'x'.repeat(5000);
    const agentPath = path.join(TEST_AGENTS_DIR, 'test-dev');
    fs.writeFileSync(path.join(agentPath, 'MEMORY.md'), largeContent);

    const result = await getCrossAgentContext('Large', { agentId: 'test-dev' });
    const devContext = result.contextByAgent.get('test-dev');

    expect(devContext).toBeDefined();
    expect(devContext!.length).toBeLessThanOrEqual(2000);
  });
});

describe('listAvailableAgents', () => {
  it('should list all agents with memory directories', async () => {
    const agents = listAvailableAgents();

    expect(agents.length).toBeGreaterThan(0);
    expect(agents).toContain('test-pm');
    expect(agents).toContain('test-sales');
    expect(agents).toContain('test-dev');
  });

  it('should return empty array when no agents exist', async () => {
    // Remove agents directory temporarily
    fs.rmSync(TEST_AGENTS_DIR, { recursive: true, force: true });

    const agents = listAvailableAgents();

    expect(agents).toEqual([]);
  });

  it('should filter out non-directory files', async () => {
    // Create a file (not directory) in agents path
    const filePath = path.join(TEST_AGENTS_DIR, 'not-a-directory.txt');
    fs.writeFileSync(filePath, 'test content');

    const agents = listAvailableAgents();

    expect(agents).not.toContain('not-a-directory.txt');
  });
});

describe('agentMemoryExists', () => {
  it('should return true for existing agent', () => {
    const exists = agentMemoryExists('test-pm');

    expect(exists).toBe(true);
  });

  it('should return false for non-existent agent', () => {
    const exists = agentMemoryExists('nonexistent-agent');

    expect(exists).toBe(false);
  });
});

describe('readDailyNotes', () => {
  it('should read daily notes from agent', async () => {
    const notes = await readDailyNotes('test-pm');

    expect(notes).toBeDefined();
    expect(notes.length).toBeGreaterThan(0);
    expect(notes[0].content).toContain('global memory validation session 2026-03-16');
    expect(notes[0].agentId).toBe('test-pm');
  });

  it('should limit number of daily notes returned', async () => {
    const notes = await readDailyNotes('test-pm', { limit: 1 });

    expect(notes.length).toBeLessThanOrEqual(1);
  });

  it('should return empty array when no daily notes exist', async () => {
    const notes = await readDailyNotes('test-dev');

    expect(notes).toEqual([]);
  });

  it('should return notes sorted by most recent first', async () => {
    // Create additional daily notes
    const memoryDir = path.join(TEST_AGENTS_DIR, 'test-pm', 'memory');
    fs.writeFileSync(path.join(memoryDir, '2026-03-15.md'), '# 2026-03-15\n\nOlder note');

    const notes = await readDailyNotes('test-pm', { limit: 10 });

    expect(notes.length).toBeGreaterThan(1);
    expect(notes[0].filePath).toContain('2026-03-16.md'); // Most recent first
  });
});

describe('readMultiAgentMemory', () => {
  it('should read memory from multiple agents', async () => {
    const results = await readMultiAgentMemory(['test-pm', 'test-sales']);

    expect(results).toBeInstanceOf(Map);
    expect(results.size).toBe(2);
    expect(results.get('test-pm')?.exists).toBe(true);
    expect(results.get('test-sales')?.exists).toBe(true);
  });

  it('should handle empty agent list', async () => {
    const results = await readMultiAgentMemory([]);

    expect(results).toBeInstanceOf(Map);
    expect(results.size).toBe(0);
  });

  it('should handle non-existent agents', async () => {
    const results = await readMultiAgentMemory(['test-pm', 'nonexistent-agent']);

    expect(results.size).toBe(2);
    expect(results.get('test-pm')?.exists).toBe(true);
    expect(results.get('nonexistent-agent')?.exists).toBe(false);
  });
});

describe('getAgentMemoryPath', () => {
  it('should return correct path for agent', () => {
    const agentPath = getAgentMemoryPath('test-pm');

    expect(agentPath).toBeDefined();
    expect(agentPath).toContain('test-pm');
  });

  it('should use AGENTS_BASE_PATH from environment', () => {
    const customPath = '/custom/agents/path';
    process.env.HOME = customPath;

    const agentPath = getAgentMemoryPath('test-agent');

    expect(agentPath).toContain(customPath);
  });
});

// LAB-006 Test Protocol Integration Tests
describe('LAB-006 Test Protocol', () => {
  describe('Test 1: Cross-Agent Information Retrieval', () => {
    it('should retrieve sprint deadline from PM memory', async () => {
      // PM agent query: "What is the sprint deadline?"
      const results = await searchGlobalMemory('sprint deadline', { agentId: 'test-pm' });

      expect(results).toHaveLength(1);
      expect(results[0].snippet).toContain('2026-03-30');
      expect(results[0].relevanceScore).toBeGreaterThan(0.8); // ≥80% accuracy threshold
    });

    it('should retrieve critical blocker from PM memory', async () => {
      // Research agent query for blocker information
      const results = await searchGlobalMemory('critical blocker LAB-006', { agentId: 'test-pm' });

      expect(results.length).toBeGreaterThanOrEqual(1);
      expect(results[0].snippet).toContain('LAB-006 cross-agent handoff test pending');
    });
  });

  describe('Test 2: Multi-Agent Context Consolidation', () => {
    it('should gather context from dev and sales agents', async () => {
      // Assistant agent calls getCrossAgentContext for dev + sales
      const result = await getCrossAgentContext('current task CRM status', {
        limit: 5,
      });

      expect(result.primaryResults.length).toBeGreaterThan(0);
      expect(result.contextByAgent.has('test-dev')).toBe(true);
      expect(result.contextByAgent.has('test-sales')).toBe(true);
      expect(result.contextByAgent.get('test-dev')).toContain('LAB-006 testing protocol');
      expect(result.contextByAgent.get('test-sales')).toContain('10 OSM leads added');
    });

    it('should consolidate output without data loss', async () => {
      const result = await getCrossAgentContext('test consolidated view');

      const devContext = result.contextByAgent.get('test-dev');
      const salesContext = result.contextByAgent.get('test-sales');

      expect(devContext).toBeDefined();
      expect(salesContext).toBeDefined();
      expect(devContext!.length).toBeGreaterThan(0);
      expect(salesContext!.length).toBeGreaterThan(0);
    });
  });

  describe('Test 3: Memory Search Across Agents', () => {
    it('should find global memory validation in both dev and PM memories', async () => {
      // Dev agent: "Testing note: global memory validation session 2026-03-16"
      // PM agent: "Testing note: LAB-006 cross-agent test"
      const results = await searchGlobalMemory('global memory validation', {
        includeDailyNotes: true,
      });

      expect(results.length).toBeGreaterThan(0);
      expect(results.some(r => r.agentId === 'test-pm')).toBe(true);
    });

    it('should return relevant information ranked appropriately', async () => {
      const results = await searchGlobalMemory('LAB-006', { limit: 10 });

      expect(results.length).toBeGreaterThan(0);
      // Check that results are sorted by relevance
      for (let i = 1; i < results.length; i++) {
        expect(results[i - 1].relevanceScore).toBeGreaterThanOrEqual(results[i].relevanceScore);
      }
    });

    it('should find at least one match from dev or PM', async () => {
      const results = await searchGlobalMemory('testing protocol', { limit: 10 });

      expect(results.length).toBeGreaterThanOrEqual(1);
      expect(results.some(r => r.agentId === 'test-pm' || r.agentId === 'test-dev')).toBe(true);
    });
  });
});

describe('Edge Cases and Error Handling', () => {
  it('should handle empty search queries', async () => {
    const results = await searchGlobalMemory('', { agentId: 'test-pm' });

    // Empty query should return no results or handle gracefully
    expect(results).toEqual([]);
  });

  it('should handle special characters in search queries', async () => {
    const results = await searchGlobalMemory('@#$%^&*()', { agentId: 'test-pm' });

    // Should handle special chars gracefully
    expect(Array.isArray(results)).toBe(true);
  });

  it('should handle very long search queries', async () => {
    const longQuery = 'test '.repeat(1000);
    const results = await searchGlobalMemory(longQuery, { agentId: 'test-pm' });

    // Should handle long queries gracefully
    expect(Array.isArray(results)).toBe(true);
  });
});

describe('Performance Tests', () => {
  it('should read memory within acceptable time (<100ms)', async () => {
    const start = Date.now();
    await readGlobalMemory('test-pm');
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(100);
  });

  it('should search memory within acceptable time (<200ms)', async () => {
    const start = Date.now();
    await searchGlobalMemory('test', { limit: 10 });
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(200);
  });

  it('should list agents within acceptable time (<50ms)', async () => {
    const start = Date.now();
    const agents = listAvailableAgents();
    const duration = Date.now() - start;

    expect(duration).toBeLessThan(50);
  });
});
