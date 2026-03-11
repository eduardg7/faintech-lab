import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

export interface Memory {
  id: string;
  workspace_id?: string;
  agent_id: string;
  task_id?: string | null;
  project_id: string | null;
  type: 'outcome' | 'learning' | 'preference' | 'decision';
  content: string;
  tags: string[];
  metadata?: Record<string, unknown>;
  importance: number;
  created_at: string;
  updated_at?: string | null;
}

interface BackendMemory {
  id: string;
  workspace_id?: string;
  agent_id: string;
  task_id?: string | null;
  project_id: string | null;
  memory_type: 'outcome' | 'learning' | 'preference' | 'decision';
  content: string;
  tags: string[];
  metadata?: Record<string, unknown>;
  importance: number;
  created_at: string;
  updated_at?: string | null;
}

export interface MemoriesResponse {
  memories: Memory[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

export interface SearchResponse {
  results: Array<{
    memory: Memory;
    score: number;
  }>;
  total: number;
}

const authHeaders = (token: string) => ({
  Authorization: `Bearer ${token}`,
});

const mapMemory = (memory: BackendMemory): Memory => ({
  id: memory.id,
  workspace_id: memory.workspace_id,
  agent_id: memory.agent_id,
  task_id: memory.task_id,
  project_id: memory.project_id,
  type: memory.memory_type,
  content: memory.content,
  tags: memory.tags,
  metadata: memory.metadata,
  importance: memory.importance,
  created_at: memory.created_at,
  updated_at: memory.updated_at,
});

export const api = {
  async getMemories(
    token: string,
    params?: {
      agent_id?: string;
      project_id?: string;
      type?: string;
      tags?: string;
      since?: string;
      until?: string;
      limit?: number;
      offset?: number;
    }
  ): Promise<MemoriesResponse> {
    const pageSize = params?.limit ?? 20;
    const page = Math.floor((params?.offset ?? 0) / pageSize) + 1;

    const response = await axios.get(`${API_BASE_URL}/memories`, {
      headers: authHeaders(token),
      params: {
        agent_id: params?.agent_id,
        project_id: params?.project_id,
        memory_type: params?.type,
        tag: params?.tags,
        page,
        page_size: pageSize,
      },
    });

    return {
      memories: response.data.memories.map(mapMemory),
      total: response.data.total,
      limit: response.data.page_size,
      offset: (response.data.page - 1) * response.data.page_size,
      has_more: response.data.has_next,
    };
  },

  async searchMemories(
    token: string,
    query: string,
    params?: {
      agent_id?: string;
      type?: string;
      limit?: number;
    }
  ): Promise<SearchResponse> {
    const response = await axios.get(`${API_BASE_URL}/search/keyword`, {
      headers: authHeaders(token),
      params: {
        q: query,
        agent_id: params?.agent_id,
        page: 1,
        page_size: params?.limit ?? 20,
      },
    });

    return {
      results: response.data.results.map((result: BackendMemory & { relevance_score: number }) => ({
        memory: mapMemory(result),
        score: result.relevance_score,
      })),
      total: response.data.total,
    };
  },

  async validateToken(token: string) {
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: authHeaders(token),
    });
    return response.data;
  },
};
