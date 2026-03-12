/**
 * Agents resource for Agent Memory Cloud SDK.
 * @module resources/agents
 */

import type { HttpClient } from '../http-client.js';
import {
  type Agent,
  type AgentCreateParams,
  type AgentListParams,
  type PaginatedResponse,
  parsePaginatedResponse,
} from '../models.js';

/** Raw agent response from API */
interface AgentResponse {
  id: string;
  name: string;
  created_at: string;
  description?: string;
  metadata?: Record<string, unknown>;
}

/**
 * Resource for agent operations.
 */
export class AgentsResource {
  private readonly client: HttpClient;

  constructor(client: HttpClient) {
    this.client = client;
  }

  private parseAgent(data: AgentResponse): Agent {
    return {
      id: data.id,
      name: data.name,
      createdAt: data.created_at,
      description: data['description'],
      metadata: data['metadata'] ?? {},
    };
  }

  /**
   * Create a new agent.
   */
  async create(params: AgentCreateParams): Promise<Agent> {
    const payload: Record<string, unknown> = {
      name: params.name,
    };

    if (params.description !== undefined) {
      payload['description'] = params.description;
    }
    if (params.metadata !== undefined) {
      payload['metadata'] = params.metadata;
    }

    const data = await this.client.post<AgentResponse>('/agents', payload);
    return this.parseAgent(data);
  }

  /**
   * Get an agent by ID.
   */
  async get(agentId: string): Promise<Agent> {
    const data = await this.client.get<AgentResponse>(`/agents/${agentId}`);
    return this.parseAgent(data);
  }

  /**
   * List all agents.
   */
  async list(params?: AgentListParams): Promise<PaginatedResponse<Agent>> {
    const queryParams: Record<string, unknown> = {
      limit: params?.limit ?? 20,
      offset: params?.offset ?? 0,
    };

    const data = await this.client.get<{
      items: AgentResponse[];
      total: number;
      limit: number;
      offset: number;
    }>('/agents', queryParams);

    return parsePaginatedResponse(data, this.parseAgent);
  }
}
