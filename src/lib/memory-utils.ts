/**
 * Global Memory Access Utility
 *
 * Enables cross-agent memory access for context sharing.
 *
 * Background (LAB-003 findings):
 * - memory_search tool is agent-scoped (only searches requesting agent's files)
 * - Cross-agent handoff failed at 41.7% accuracy vs 95-100% same-agent
 * - Solution: Direct file read utility that can access any agent's memory
 *
 * Usage:
 *   import { readGlobalMemory, searchGlobalMemory } from './memory-utils';
 *
 *   // Read specific agent's memory
 *   const pmMemory = await readGlobalMemory('pm');
 *
 *   // Search across all agents
 *   const results = await searchGlobalMemory('project decisions', { agentId: 'pm' });
 */

import * as fs from 'fs';
import * as path from 'path';

// Configuration
const AGENTS_BASE_PATH = path.join(process.env.HOME || '', '.openclaw', 'agents');
const MEMORY_FILE = 'MEMORY.md';
const DAILY_NOTES_DIR = 'memory';

export interface MemorySearchResult {
  agentId: string;
  filePath: string;
  snippet: string;
  lineStart: number;
  lineEnd: number;
  relevanceScore: number;
}

export interface MemoryReadResult {
  agentId: string;
  filePath: string;
  content: string;
  lastModified: string;
  exists: boolean;
}

export interface GlobalMemoryOptions {
  /** Specific agent to read/search. If omitted, searches all agents. */
  agentId?: string;
  /** Include daily notes in addition to MEMORY.md */
  includeDailyNotes?: boolean;
  /** Maximum results to return */
  limit?: number;
  /** Minimum relevance score (0-1) for search results */
  minScore?: number;
  /** Number of context lines around matches */
  contextLines?: number;
}

/**
 * Get the base path for an agent's memory files
 */
export function getAgentMemoryPath(agentId: string): string {
  return path.join(AGENTS_BASE_PATH, agentId);
}

/**
 * Check if an agent's memory directory exists
 */
export function agentMemoryExists(agentId: string): boolean {
  const agentPath = getAgentMemoryPath(agentId);
  return fs.existsSync(agentPath);
}

/**
 * List all available agents with memory
 */
export function listAvailableAgents(): string[] {
  if (!fs.existsSync(AGENTS_BASE_PATH)) {
    return [];
  }

  return fs.readdirSync(AGENTS_BASE_PATH)
    .filter(name => {
      const agentPath = path.join(AGENTS_BASE_PATH, name);
      return fs.statSync(agentPath).isDirectory();
    });
}

/**
 * Read an agent's MEMORY.md file
 */
export async function readGlobalMemory(
  agentId: string,
  options: GlobalMemoryOptions = {}
): Promise<MemoryReadResult> {
  const agentPath = getAgentMemoryPath(agentId);
  const memoryPath = path.join(agentPath, MEMORY_FILE);

  if (!fs.existsSync(memoryPath)) {
    return {
      agentId,
      filePath: memoryPath,
      content: '',
      lastModified: '',
      exists: false
    };
  }

  const stats = fs.statSync(memoryPath);
  const content = fs.readFileSync(memoryPath, 'utf-8');

  return {
    agentId,
    filePath: memoryPath,
    content,
    lastModified: stats.mtime.toISOString(),
    exists: true
  };
}

/**
 * Read an agent's daily notes
 */
export async function readDailyNotes(
  agentId: string,
  options: GlobalMemoryOptions = {}
): Promise<MemoryReadResult[]> {
  const agentPath = getAgentMemoryPath(agentId);
  const memoryDir = path.join(agentPath, DAILY_NOTES_DIR);

  if (!fs.existsSync(memoryDir)) {
    return [];
  }

  const files = fs.readdirSync(memoryDir)
    .filter(f => f.endsWith('.md'))
    .sort((a, b) => b.localeCompare(a)); // Most recent first

  const limit = options.limit || 7; // Default to last 7 days

  return files.slice(0, limit).map(file => {
    const filePath = path.join(memoryDir, file);
    const stats = fs.statSync(filePath);
    const content = fs.readFileSync(filePath, 'utf-8');

    return {
      agentId,
      filePath,
      content,
      lastModified: stats.mtime.toISOString(),
      exists: true
    };
  });
}

/**
 * Simple text-based search across agent memory
 *
 * For semantic search, consider integrating with a vector database
 * or using the memory_search tool within an agent's own session.
 */
export async function searchGlobalMemory(
  query: string,
  options: GlobalMemoryOptions = {}
): Promise<MemorySearchResult[]> {
  const results: MemorySearchResult[] = [];
  const agents = options.agentId
    ? [options.agentId]
    : listAvailableAgents();

  const queryLower = query.toLowerCase();
  const queryTerms = queryLower.split(/\s+/).filter(t => t.length > 2);
  const contextLines = options.contextLines || 3;
  const limit = options.limit || 10;
  const minScore = options.minScore || 0.1;

  for (const agentId of agents) {
    // Search MEMORY.md
    const memoryResult = await readGlobalMemory(agentId);
    if (memoryResult.exists) {
      const fileResults = searchInContent(
        memoryResult.content,
        memoryResult.filePath,
        agentId,
        queryTerms,
        contextLines
      );
      results.push(...fileResults);
    }

    // Search daily notes if requested
    if (options.includeDailyNotes) {
      const dailyNotes = await readDailyNotes(agentId, { limit: 7 });
      for (const note of dailyNotes) {
        const noteResults = searchInContent(
          note.content,
          note.filePath,
          agentId,
          queryTerms,
          contextLines
        );
        results.push(...noteResults);
      }
    }
  }

  // Sort by relevance score and filter by minimum
  return results
    .filter(r => r.relevanceScore >= minScore)
    .sort((a, b) => b.relevanceScore - a.relevanceScore)
    .slice(0, limit);
}

/**
 * Search within content and return scored results
 */
function searchInContent(
  content: string,
  filePath: string,
  agentId: string,
  queryTerms: string[],
  contextLines: number
): MemorySearchResult[] {
  const lines = content.split('\n');
  const results: MemorySearchResult[] = [];

  for (let i = 0; i < lines.length; i++) {
    const lineLower = lines[i].toLowerCase();

    // Count matching terms
    const matchCount = queryTerms.filter(term => lineLower.includes(term)).length;

    if (matchCount > 0) {
      // Calculate relevance score based on term matches
      const relevanceScore = matchCount / queryTerms.length;

      // Extract context
      const startLine = Math.max(0, i - contextLines);
      const endLine = Math.min(lines.length - 1, i + contextLines);
      const snippet = lines.slice(startLine, endLine + 1).join('\n');

      results.push({
        agentId,
        filePath,
        snippet,
        lineStart: startLine + 1, // 1-indexed
        lineEnd: endLine + 1,
        relevanceScore
      });
    }
  }

  return results;
}

/**
 * Read memory from multiple agents at once
 */
export async function readMultiAgentMemory(
  agentIds: string[],
  options: GlobalMemoryOptions = {}
): Promise<Map<string, MemoryReadResult>> {
  const results = new Map<string, MemoryReadResult>();

  for (const agentId of agentIds) {
    const memory = await readGlobalMemory(agentId, options);
    results.set(agentId, memory);
  }

  return results;
}

/**
 * Get a consolidated view of memory from key agents
 * Useful for cross-agent context transfer
 */
export async function getCrossAgentContext(
  query: string,
  options: GlobalMemoryOptions = {}
): Promise<{
  primaryResults: MemorySearchResult[];
  contextByAgent: Map<string, string>;
}> {
  // Search across agents
  const primaryResults = await searchGlobalMemory(query, {
    ...options,
    limit: options.limit || 5
  });

  // Get unique agents from results
  const agents = [...new Set(primaryResults.map(r => r.agentId))];

  // Read full memory from each relevant agent
  const contextByAgent = new Map<string, string>();
  for (const agentId of agents) {
    const memory = await readGlobalMemory(agentId);
    if (memory.exists) {
      // Include first 2000 characters as context
      contextByAgent.set(agentId, memory.content.slice(0, 2000));
    }
  }

  return {
    primaryResults,
    contextByAgent
  };
}

// Export types
export default {
  readGlobalMemory,
  searchGlobalMemory,
  readDailyNotes,
  listAvailableAgents,
  agentMemoryExists,
  readMultiAgentMemory,
  getCrossAgentContext
};
