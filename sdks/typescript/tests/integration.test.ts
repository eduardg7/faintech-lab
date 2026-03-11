/**
 * Integration tests for Agent Memory Cloud TypeScript SDK.
 *
 * These tests require a running backend server.
 * Run with: npm test
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { MemoryClient } from '../src/client.js';
import {
  MemoryType,
  parseMemory,
  parseAgent,
  parseProject,
  parseSearchResult,
  parsePaginatedResponse,
  Memory,
  Agent,
  Project,
  SearchResult,
  PaginatedResponse,
  hasMore,
} from '../src/models.js';

// Mock fetch for testing
const mockFetch = vi.fn();
global.fetch = mockFetch as any;

describe('MemoryClient', () => {
  let client: MemoryClient;

  beforeEach(() => {
    process.env['AGENT_MEMORY_API_KEY'] = 'test-api-key-12345';
    mockFetch.mockClear();
    client = new MemoryClient();
  });

  afterEach(() => {
    delete process.env['AGENT_MEMORY_API_KEY'];
  });

  describe('initialization', () => {
    it('should initialize with API key from parameter', () => {
      const clientWithKey = new MemoryClient({ apiKey: 'explicit-key' });
      expect(clientWithKey).toBeDefined();
    });

    it('should initialize with API key from environment variable', () => {
      expect(client).toBeDefined();
    });

    it('should use custom base URL', () => {
      const customClient = new MemoryClient({
        baseUrl: 'http://localhost:8000/api/v1',
      });
      expect(customClient).toBeDefined();
    });

    it('should use custom timeout', () => {
      const customClient = new MemoryClient({ timeout: 60000 });
      expect(customClient).toBeDefined();
    });

    it('should throw error when API key is missing', () => {
      delete process.env['AGENT_MEMORY_API_KEY'];
      expect(() => new MemoryClient()).toThrow('API key required');
    });

    it('should expose memories resource', () => {
      expect(client.memories).toBeDefined();
    });

    it('should expose agents resource', () => {
      expect(client.agents).toBeDefined();
    });

    it('should expose projects resource', () => {
      expect(client.projects).toBeDefined();
    });

    it('should expose search resource', () => {
      expect(client.search).toBeDefined();
    });
  });
});

describe('Memory models', () => {
  describe('parseMemory', () => {
    it('should parse memory from API response', () => {
      const data = {
        id: 'mem-001',
        agent_id: 'agent-001',
        memory_type: 'outcome' as MemoryType,
        content: 'Task completed successfully',
        created_at: '2026-03-11T10:00:00Z',
        updated_at: '2026-03-11T10:00:00Z',
        tags: ['deployment', 'success'],
        metadata: { env: 'production' },
        confidence: 0.95,
        project_id: 'proj-001',
        workspace_id: 'ws-001',
      };

      const memory = parseMemory(data);

      expect(memory.id).toBe('mem-001');
      expect(memory.agentId).toBe('agent-001');
      expect(memory.memoryType).toBe('outcome');
      expect(memory.content).toBe('Task completed successfully');
      expect(memory.createdAt).toBe('2026-03-11T10:00:00Z');
      expect(memory.updatedAt).toBe('2026-03-11T10:00:00Z');
      expect(memory.tags).toEqual(['deployment', 'success']);
      expect(memory.metadata).toEqual({ env: 'production' });
      expect(memory.confidence).toBe(0.95);
      expect(memory.projectId).toBe('proj-001');
      expect(memory.workspaceId).toBe('ws-001');
    });

    it('should handle missing optional fields', () => {
      const data = {
        id: 'mem-001',
        agent_id: 'agent-001',
        memory_type: 'outcome' as MemoryType,
        content: 'Task completed',
        created_at: '2026-03-11T10:00:00Z',
      };

      const memory = parseMemory(data);

      expect(memory.tags).toEqual([]);
      expect(memory.metadata).toEqual({});
      expect(memory.confidence).toBeUndefined();
      expect(memory.projectId).toBeUndefined();
      expect(memory.workspaceId).toBeUndefined();
      expect(memory.updatedAt).toBeUndefined();
      expect(memory.embedding).toBeUndefined();
    });
  });

  describe('parseAgent', () => {
    it('should parse agent from API response', () => {
      const data = {
        id: 'agent-001',
        name: 'Test Agent',
        description: 'Test agent description',
        created_at: '2026-03-11T09:00:00Z',
        metadata: { version: '1.0' },
      };

      const agent = parseAgent(data);

      expect(agent.id).toBe('agent-001');
      expect(agent.name).toBe('Test Agent');
      expect(agent.description).toBe('Test agent description');
      expect(agent.createdAt).toBe('2026-03-11T09:00:00Z');
      expect(agent.metadata).toEqual({ version: '1.0' });
    });

    it('should handle missing optional fields', () => {
      const data = {
        id: 'agent-001',
        name: 'Test Agent',
        created_at: '2026-03-11T09:00:00Z',
      };

      const agent = parseAgent(data);

      expect(agent.description).toBeUndefined();
      expect(agent.metadata).toEqual({});
    });
  });

  describe('parseProject', () => {
    it('should parse project from API response', () => {
      const data = {
        id: 'proj-001',
        name: 'Test Project',
        description: 'Test project description',
        created_at: '2026-03-11T08:00:00Z',
        metadata: { team: 'engineering' },
      };

      const project = parseProject(data);

      expect(project.id).toBe('proj-001');
      expect(project.name).toBe('Test Project');
      expect(project.description).toBe('Test project description');
      expect(project.createdAt).toBe('2026-03-11T08:00:00Z');
      expect(project.metadata).toEqual({ team: 'engineering' });
    });

    it('should handle missing optional fields', () => {
      const data = {
        id: 'proj-001',
        name: 'Test Project',
        created_at: '2026-03-11T08:00:00Z',
      };

      const project = parseProject(data);

      expect(project.description).toBeUndefined();
      expect(project.metadata).toEqual({});
    });
  });

  describe('parseSearchResult', () => {
    it('should parse search result from API response', () => {
      const data = {
        memory: {
          id: 'mem-001',
          agent_id: 'agent-001',
          memory_type: 'outcome' as MemoryType,
          content: 'Task completed',
          created_at: '2026-03-11T10:00:00Z',
        },
        score: 0.95,
      };

      const result = parseSearchResult(data);

      expect(result.score).toBe(0.95);
      expect(result.memory.id).toBe('mem-001');
      expect(result.memory.agentId).toBe('agent-001');
    });
  });

  describe('parsePaginatedResponse', () => {
    it('should parse paginated response', () => {
      const data = {
        items: [
          { id: 'mem-001', agent_id: 'agent-001', memory_type: 'outcome' as MemoryType, content: 'Test', created_at: '2026-03-11T10:00:00Z' },
        ],
        total: 100,
        limit: 20,
        offset: 0,
      };

      const response = parsePaginatedResponse(data, parseMemory);

      expect(response.items).toHaveLength(1);
      expect(response.items[0].id).toBe('mem-001');
      expect(response.total).toBe(100);
      expect(response.limit).toBe(20);
      expect(response.offset).toBe(0);
    });
  });

  describe('hasMore', () => {
    it('should return true when there are more results', () => {
      const response: PaginatedResponse<Memory> = {
        items: [{ id: 'mem-001', agentId: 'agent-001', memoryType: 'outcome', content: 'Test', createdAt: '2026-03-11T10:00:00Z' }],
        total: 100,
        limit: 20,
        offset: 0,
      };

      expect(hasMore(response)).toBe(true);
    });

    it('should return false when there are no more results', () => {
      const response: PaginatedResponse<Memory> = {
        items: [{ id: 'mem-001', agentId: 'agent-001', memoryType: 'outcome', content: 'Test', createdAt: '2026-03-11T10:00:00Z' }],
        total: 1,
        limit: 20,
        offset: 0,
      };

      expect(hasMore(response)).toBe(false);
    });
  });
});

describe('MemoryType', () => {
  it('should support all memory types', () => {
    const types: MemoryType[] = ['outcome', 'learning', 'preference', 'decision'];

    types.forEach(type => {
      expect(type).toMatch(/^(outcome|learning|preference|decision)$/);
    });
  });
});

describe('Error handling', () => {
  it('should handle 401 authentication errors', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
      json: async () => ({ detail: 'Invalid API key' }),
    } as Response);

    try {
      await client.memories.list();
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error.message).toContain('Invalid API key');
      expect(error.status_code).toBe(401);
    }
  });

  it('should handle 404 not found errors', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ detail: 'Resource not found' }),
    } as Response);

    try {
      await client.memories.get('nonexistent-id');
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error.message).toContain('Resource not found');
      expect(error.status_code).toBe(404);
    }
  });

  it('should handle 422 validation errors', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: 'Invalid memory type' }),
    } as Response);

    try {
      await client.memories.create({
        agentId: 'agent-001',
        memoryType: 'invalid' as any,
        content: 'test',
      });
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error.message).toContain('Invalid memory type');
      expect(error.status_code).toBe(422);
    }
  });

  it('should handle 429 rate limit errors', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 429,
      headers: new Headers({ 'Retry-After': '60' }),
      json: async () => ({ detail: 'Rate limit exceeded' }),
    } as Response);

    try {
      await client.memories.list();
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error.message).toContain('Rate limit exceeded');
      expect(error.retry_after).toBe(60);
      expect(error.status_code).toBe(429);
    }
  });

  it('should handle 500 server errors', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      text: async () => 'Internal server error',
    } as Response);

    try {
      await client.memories.list();
      expect.fail('Should have thrown an error');
    } catch (error: any) {
      expect(error.message).toContain('API error: 500');
      expect(error.status_code).toBe(500);
    }
  });
});
