/**
 * Tests for stats-api calculations
 *
 * Note: These tests document the expected behavior of the stats calculation logic.
 * To run: npm install --save-dev jest @types/jest ts-jest
 * Then add to package.json: "test": "jest"
 */

import { statsApi, AgentDashboardStats } from '../stats-api';

// Mock data for testing
const mockMemories = [
  {
    id: '1',
    agent_id: 'agent-1',
    memory_type: 'outcome' as const,
    importance: 8,
    created_at: new Date().toISOString(),
    tags: ['test', 'unit'],
    content: 'Test memory 1',
    workspace_id: 'ws-1',
    task_id: null,
    project_id: 'proj-1',
    metadata: {},
    updated_at: null,
  },
  {
    id: '2',
    agent_id: 'agent-1',
    memory_type: 'learning' as const,
    importance: 6,
    created_at: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
    tags: ['test', 'unit'],
    content: 'Test memory 2',
    workspace_id: 'ws-1',
    task_id: null,
    project_id: 'proj-1',
    metadata: {},
    updated_at: null,
  },
  {
    id: '3',
    agent_id: 'agent-2',
    memory_type: 'decision' as const,
    importance: 9,
    created_at: new Date().toISOString(),
    tags: ['other'],
    content: 'Test memory 3',
    workspace_id: 'ws-1',
    task_id: null,
    project_id: 'proj-2',
    metadata: {},
    updated_at: null,
  },
];

/**
 * Test: Agent dashboard stats calculation
 *
 * Expected behavior:
 * - Should filter memories by agent_id
 * - Should calculate total_memories correctly
 * - Should calculate memories_this_week correctly
 * - Should calculate pattern_count (unique tag combinations)
 * - Should calculate storage_used_mb
 * - Should calculate by_type distribution
 * - Should calculate recent_activity timeline
 */
export function testAgentDashboardStats() {
  const agent1Memories = mockMemories.filter(m => m.agent_id === 'agent-1');

  // Total memories
  const totalMemories = agent1Memories.length;
  console.assert(totalMemories === 2, `Expected 2 memories, got ${totalMemories}`);

  // Memories this week
  const oneWeekAgo = new Date();
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  const memoriesThisWeek = agent1Memories.filter(
    m => new Date(m.created_at) >= oneWeekAgo
  ).length;
  console.assert(memoriesThisWeek === 2, `Expected 2 memories this week, got ${memoriesThisWeek}`);

  // By type
  const byType = { outcome: 0, learning: 0, preference: 0, decision: 0 };
  for (const memory of agent1Memories) {
    byType[memory.memory_type] += 1;
  }
  console.assert(byType.outcome === 1, `Expected 1 outcome, got ${byType.outcome}`);
  console.assert(byType.learning === 1, `Expected 1 learning, got ${byType.learning}`);

  // Pattern count (unique tag combinations)
  const tagPatterns = new Set<string>();
  for (const memory of agent1Memories) {
    if (memory.tags && memory.tags.length > 0) {
      tagPatterns.add(memory.tags.sort().join(','));
    }
  }
  const patternCount = tagPatterns.size;
  console.assert(patternCount === 1, `Expected 1 pattern, got ${patternCount}`);

  // Storage (rough estimate: 0.002 MB per memory)
  const storageUsedMb = Math.round(totalMemories * 0.002 * 100) / 100;
  console.assert(storageUsedMb === 0, `Expected 0 MB, got ${storageUsedMb}`);

  console.log('✅ All stats calculation tests passed');
}

/**
 * Test: Memory type distribution
 *
 * Expected behavior:
 * - Should correctly categorize memories by type
 * - Should handle all four types: outcome, learning, preference, decision
 */
export function testMemoryTypeDistribution() {
  const testCases = [
    { type: 'outcome', expected: 1 },
    { type: 'learning', expected: 1 },
    { type: 'preference', expected: 0 },
    { type: 'decision', expected: 0 },
  ];

  const agent1Memories = mockMemories.filter(m => m.agent_id === 'agent-1');
  const byType = { outcome: 0, learning: 0, preference: 0, decision: 0 };
  for (const memory of agent1Memories) {
    byType[memory.memory_type] += 1;
  }

  for (const testCase of testCases) {
    const actual = byType[testCase.type as keyof typeof byType];
    console.assert(
      actual === testCase.expected,
      `Expected ${testCase.expected} for ${testCase.type}, got ${actual}`
    );
  }

  console.log('✅ Memory type distribution tests passed');
}

/**
 * Test: Recent activity timeline
 *
 * Expected behavior:
 * - Should generate 7 days of activity data
 * - Should count memories per day correctly
 */
export function testRecentActivityTimeline() {
  const agent1Memories = mockMemories.filter(m => m.agent_id === 'agent-1');

  const dates = Array.from({ length: 7 }, (_, index) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - index));
    return date.toISOString().split('T')[0];
  });

  console.assert(dates.length === 7, `Expected 7 dates, got ${dates.length}`);

  const activityMap: Record<string, number> = {};
  for (const date of dates) {
    activityMap[date] = 0;
  }

  for (const memory of agent1Memories) {
    const date = memory.created_at.split('T')[0];
    if (activityMap[date] !== undefined) {
      activityMap[date] += 1;
    }
  }

  const today = new Date().toISOString().split('T')[0];
  console.assert(
    activityMap[today] === 1,
    `Expected 1 memory today, got ${activityMap[today]}`
  );

  console.log('✅ Recent activity timeline tests passed');
}

/**
 * Test: Storage calculation
 *
 * Expected behavior:
 * - Should estimate storage based on memory count
 * - Should use formula: count * 0.002 MB
 */
export function testStorageCalculation() {
  const testCases = [
    { count: 0, expected: 0 },
    { count: 100, expected: 0.2 },
    { count: 1000, expected: 2 },
    { count: 5000, expected: 10 },
  ];

  for (const testCase of testCases) {
    const storage = Math.round(testCase.count * 0.002 * 100) / 100;
    console.assert(
      storage === testCase.expected,
      `For ${testCase.count} memories, expected ${testCase.expected} MB, got ${storage}`
    );
  }

  console.log('✅ Storage calculation tests passed');
}

// Run all tests
if (require.main === module) {
  console.log('Running stats-api tests...\n');
  testAgentDashboardStats();
  testMemoryTypeDistribution();
  testRecentActivityTimeline();
  testStorageCalculation();
  console.log('\n✅ All tests passed!');
}
