/**
 * Memories resource for Agent Memory Cloud SDK.
 * @module resources/memories
 */

import type { HttpClient } from '../http-client.js';
import {
  type Memory,
  type MemoryType,
  type MemoryCreateParams,
  type MemoryListParams,
  type MemoryUpdateParams,
  type MemoryCompactParams,
  type MemoryCompactResult,
  type PaginatedResponse,
  parsePaginatedResponse,
} from '../models.js';

/** Raw memory response from API */
interface MemoryResponse {
  id: string;
  agent_id: string;
  memory_type: string;
  content: string;
  created_at: string;
  workspace_id?: string;
  project_id?: string;
  tags?: string[];
  metadata?: Record<string, unknown>;
  embedding?: number[];
  updated_at?: string;
  confidence?: number;
}

/** Raw compact result from API */
interface CompactResultResponse {
  memories_processed: number;
  memories_created: number;
  memories_archived: number;
}

/**
 * Resource for memory operations.
 */
export class MemoriesResource {
  private readonly client: HttpClient;

  constructor(client: HttpClient) {
    this.client = client;
  }

  private parseMemory(data: MemoryResponse): Memory {
    return {
      id: data.id,
      agentId: data.agent_id,
      memoryType: data.memory_type as MemoryType,
      content: data.content,
      createdAt: data.created_at,
      workspaceId: data['workspace_id'],
      projectId: data['project_id'],
      tags: data['tags'] ?? [],
      metadata: data['metadata'] ?? {},
      embedding: data['embedding'],
      updatedAt: data['updated_at'],
      confidence: data['confidence'],
    };
  }

  /**
   * Create a new memory.
   *
   * @example
   * ```typescript
   * const memory = await client.memories.create({
   *   agentId: 'agent-001',
   *   memoryType: 'outcome',
   *   content: 'Task completed successfully',
   *   tags: ['deployment', 'success'],
   * });
   * ```
   */
  async create(params: MemoryCreateParams): Promise<Memory> {
    const payload: Record<string, unknown> = {
      agent_id: params.agentId,
      memory_type: params.memoryType,
      content: params.content,
    };

    if (params.workspaceId !== undefined) {
      payload['workspace_id'] = params.workspaceId;
    }
    if (params.projectId !== undefined) {
      payload['project_id'] = params.projectId;
    }
    if (params.tags !== undefined) {
      payload['tags'] = [...params.tags];
    }
    if (params.metadata !== undefined) {
      payload['metadata'] = params.metadata;
    }
    if (params.confidence !== undefined) {
      payload['confidence'] = params.confidence;
    }

    const data = await this.client.post<MemoryResponse>('/memories', payload);
    return this.parseMemory(data);
  }

  /**
   * Get a memory by ID.
   *
   * @throws {NotFoundError} If memory doesn't exist.
   */
  async get(memoryId: string): Promise<Memory> {
    const data = await this.client.get<MemoryResponse>(`/memories/${memoryId}`);
    return this.parseMemory(data);
  }

  /**
   * List memories with optional filters.
   */
  async list(params?: MemoryListParams): Promise<PaginatedResponse<Memory>> {
    const queryParams: Record<string, unknown> = {
      limit: params?.limit ?? 20,
      offset: params?.offset ?? 0,
    };

    if (params?.agentId !== undefined) {
      queryParams['agent_id'] = params.agentId;
    }
    if (params?.projectId !== undefined) {
      queryParams['project_id'] = params.projectId;
    }
    if (params?.memoryType !== undefined) {
      queryParams['memory_type'] = params.memoryType;
    }
    if (params?.tags !== undefined && params.tags.length > 0) {
      queryParams['tags'] = [...params.tags];
    }

    const data = await this.client.get<{
      items: MemoryResponse[];
      total: number;
      limit: number;
      offset: number;
    }>('/memories', queryParams);

    return parsePaginatedResponse(data, this.parseMemory);
  }

  /**
   * Update a memory.
   */
  async update(params: MemoryUpdateParams): Promise<Memory> {
    const payload: Record<string, unknown> = {};

    if (params.content !== undefined) {
      payload['content'] = params.content;
    }
    if (params.tags !== undefined) {
      payload['tags'] = [...params.tags];
    }
    if (params.metadata !== undefined) {
      payload['metadata'] = params.metadata;
    }
    if (params.confidence !== undefined) {
      payload['confidence'] = params.confidence;
    }

    const data = await this.client.put<MemoryResponse>(
      `/memories/${params.memoryId}`,
      payload
    );
    return this.parseMemory(data);
  }

  /**
   * Delete a memory.
   *
   * @throws {NotFoundError} If memory doesn't exist.
   */
  async delete(memoryId: string): Promise<void> {
    await this.client.delete(`/memories/${memoryId}`);
  }

  /**
   * Compact memories for an agent.
   *
   * Consolidates and summarizes old memories to reduce storage and improve
   * retrieval performance.
   *
   * @example
   * ```typescript
   * const result = await client.memories.compact({
   *   agentId: 'agent-001',
   *   maxAgeDays: 30,
   * });
   * console.log(`Processed ${result.memoriesProcessed} memories`);
   * ```
   */
  async compact(params: MemoryCompactParams): Promise<MemoryCompactResult> {
    const payload: Record<string, unknown> = {
      agent_id: params.agentId,
    };

    if (params.projectId !== undefined) {
      payload['project_id'] = params.projectId;
    }
    if (params.maxAgeDays !== undefined) {
      payload['max_age_days'] = params.maxAgeDays;
    }

    const data = await this.client.post<CompactResultResponse>(
      '/memories/compact',
      payload
    );

    return {
      memoriesProcessed: data.memories_processed,
      memoriesCreated: data.memories_created,
      memoriesArchived: data.memories_archived,
    };
  }
}
