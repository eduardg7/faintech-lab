/**
 * Search resource for Agent Memory Cloud SDK.
 * @module resources/search
 */

import type { HttpClient } from '../http-client.js';
import {
  type SearchResult,
  type SearchKeywordParams,
  type SearchSemanticParams,
} from '../models.js';

/** Raw search result response from API */
interface SearchResultResponse {
  memory: {
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
  };
  score: number;
}

/** Raw search response from API */
interface SearchResponseRaw {
  results: SearchResultResponse[];
}

/**
 * Resource for search operations.
 */
export class SearchResource {
  private readonly client: HttpClient;

  constructor(client: HttpClient) {
    this.client = client;
  }

  private parseMemory(data: SearchResultResponse['memory']): SearchResult['memory'] {
    return {
      id: data.id,
      agentId: data.agent_id,
      memoryType: data.memory_type as 'outcome' | 'learning' | 'preference' | 'decision',
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

  private parseSearchResult(data: SearchResultResponse): SearchResult {
    return {
      memory: this.parseMemory(data.memory),
      score: data.score,
    };
  }

  /**
   * Keyword search across memories.
   *
   * @example
   * ```typescript
   * const results = await client.search.keyword({
   *   query: 'redis caching',
   *   limit: 5,
   * });
   * for (const result of results) {
   *   console.log(`Score: ${result.score}`);
   *   console.log(`Content: ${result.memory.content}`);
   * }
   * ```
   */
  async keyword(params: SearchKeywordParams): Promise<readonly SearchResult[]> {
    const queryParams: Record<string, unknown> = {
      query: params.query,
      limit: params.limit ?? 10,
    };

    if (params.agentId !== undefined) {
      queryParams['agent_id'] = params.agentId;
    }
    if (params.projectId !== undefined) {
      queryParams['project_id'] = params.projectId;
    }
    if (params.tags !== undefined && params.tags.length > 0) {
      queryParams['tags'] = [...params.tags];
    }

    const data = await this.client.get<SearchResponseRaw>(
      '/search/keyword',
      queryParams
    );

    return data.results.map((result) => this.parseSearchResult(result));
  }

  /**
   * Semantic search using natural language queries.
   *
   * Uses vector embeddings to find conceptually similar memories,
   * not just keyword matches.
   *
   * @example
   * ```typescript
   * const results = await client.search.semantic({
   *   query: 'How did we improve performance?',
   *   limit: 5,
   * });
   * ```
   */
  async semantic(params: SearchSemanticParams): Promise<readonly SearchResult[]> {
    const queryParams: Record<string, unknown> = {
      query: params.query,
      limit: params.limit ?? 5,
    };

    if (params.agentId !== undefined) {
      queryParams['agent_id'] = params.agentId;
    }
    if (params.projectId !== undefined) {
      queryParams['project_id'] = params.projectId;
    }
    if (params.tags !== undefined && params.tags.length > 0) {
      queryParams['tags'] = [...params.tags];
    }

    const data = await this.client.get<SearchResponseRaw>(
      '/search/semantic',
      queryParams
    );

    return data.results.map((result) => this.parseSearchResult(result));
  }
}
