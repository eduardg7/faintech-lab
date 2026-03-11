/**
 * HTTP client for Agent Memory Cloud API.
 * @module client
 */

import { HttpClient } from './http-client.js';
import { MemoriesResource } from './resources/memories.js';
import { AgentsResource } from './resources/agents.js';
import { ProjectsResource } from './resources/projects.js';
import { SearchResource } from './resources/search.js';
import { AuthenticationError } from './exceptions.js';

/**
 * Configuration options for the MemoryClient.
 */
export interface MemoryClientConfig {
  /**
   * API key for authentication.
   * If not provided, reads from AGENT_MEMORY_API_KEY environment variable.
   */
  apiKey?: string;

  /**
   * Base URL for the API.
   * @default "https://api.faintech.dev/v1"
   */
  baseUrl?: string;

  /**
   * Request timeout in milliseconds.
   * @default 30000
   */
  timeout?: number;
}

/**
 * Client for Agent Memory Cloud API.
 *
 * @example
 * ```typescript
 * import { MemoryClient } from '@agentmemory/sdk';
 *
 * // Initialize with API key
 * const client = new MemoryClient({ apiKey: 'your-api-key' });
 *
 * // Or use environment variable
 * // export AGENT_MEMORY_API_KEY="your-api-key"
 * const client = new MemoryClient();
 *
 * // Create a memory
 * const memory = await client.memories.create({
 *   agentId: 'agent-001',
 *   memoryType: 'outcome',
 *   content: 'Task completed successfully',
 * });
 * ```
 */
export class MemoryClient {
  private readonly httpClient: HttpClient;
  private _memories?: MemoriesResource;
  private _agents?: AgentsResource;
  private _projects?: ProjectsResource;
  private _search?: SearchResource;

  /**
   * Initialize the MemoryClient.
   *
   * @param config - Configuration options
   * @throws {AuthenticationError} If API key is not provided and not in environment
   */
  constructor(config?: MemoryClientConfig) {
    const apiKey = config?.apiKey ?? (process.env as Record<string, string | undefined>)['AGENT_MEMORY_API_KEY'];
    if (!apiKey) {
      throw new AuthenticationError(
        'API key required. Pass apiKey in config or set AGENT_MEMORY_API_KEY environment variable.'
      );
    }

    this.httpClient = new HttpClient({
      apiKey,
      baseUrl: config?.baseUrl ?? 'https://api.faintech.dev/v1',
      timeout: config?.timeout ?? 30000,
    });
  }

  /**
   * Access memories resource.
   */
  get memories(): MemoriesResource {
    if (!this._memories) {
      this._memories = new MemoriesResource(this.httpClient);
    }
    return this._memories;
  }

  /**
   * Access agents resource.
   */
  get agents(): AgentsResource {
    if (!this._agents) {
      this._agents = new AgentsResource(this.httpClient);
    }
    return this._agents;
  }

  /**
   * Access projects resource.
   */
  get projects(): ProjectsResource {
    if (!this._projects) {
      this._projects = new ProjectsResource(this.httpClient);
    }
    return this._projects;
  }

  /**
   * Access search resource.
   */
  get search(): SearchResource {
    if (!this._search) {
      this._search = new SearchResource(this.httpClient);
    }
    return this._search;
  }
}
