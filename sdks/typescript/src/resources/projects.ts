/**
 * Projects resource for Agent Memory Cloud SDK.
 * @module resources/projects
 */

import type { HttpClient } from '../http-client.js';
import {
  type Project,
  type ProjectCreateParams,
  type ProjectListParams,
  type PaginatedResponse,
  parsePaginatedResponse,
} from '../models.js';

/** Raw project response from API */
interface ProjectResponse {
  id: string;
  name: string;
  created_at: string;
  description?: string;
  metadata?: Record<string, unknown>;
}

/**
 * Resource for project operations.
 */
export class ProjectsResource {
  private readonly client: HttpClient;

  constructor(client: HttpClient) {
    this.client = client;
  }

  private parseProject(data: ProjectResponse): Project {
    return {
      id: data.id,
      name: data.name,
      createdAt: data.created_at,
      description: data['description'],
      metadata: data['metadata'] ?? {},
    };
  }

  /**
   * Create a new project.
   */
  async create(params: ProjectCreateParams): Promise<Project> {
    const payload: Record<string, unknown> = {
      name: params.name,
    };

    if (params.description !== undefined) {
      payload['description'] = params.description;
    }
    if (params.metadata !== undefined) {
      payload['metadata'] = params.metadata;
    }

    const data = await this.client.post<ProjectResponse>('/projects', payload);
    return this.parseProject(data);
  }

  /**
   * Get a project by ID.
   */
  async get(projectId: string): Promise<Project> {
    const data = await this.client.get<ProjectResponse>(`/projects/${projectId}`);
    return this.parseProject(data);
  }

  /**
   * List all projects.
   */
  async list(params?: ProjectListParams): Promise<PaginatedResponse<Project>> {
    const queryParams: Record<string, unknown> = {
      limit: params?.limit ?? 20,
      offset: params?.offset ?? 0,
    };

    const data = await this.client.get<{
      items: ProjectResponse[];
      total: number;
      limit: number;
      offset: number;
    }>('/projects', queryParams);

    return parsePaginatedResponse(data, this.parseProject);
  }
}
