import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

export interface Memory {
  id: string;
  workspace_id: string;
  agent_id: string;
  task_id: string | null;
  project_id: string;
  memory_type: 'outcome' | 'learning' | 'preference' | 'decision';
  content: string;
  tags: string[];
  metadata: Record<string, unknown>;
  importance: number;
  created_at: string;
  updated_at: string | null;
}

export interface MemoriesResponse {
  memories: Memory[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
}

export interface SearchResponse {
  results: Array<{
    memory: Memory;
    score: number;
  }>;
  total: number;
}

export const api = {
  async getMemories(
    apiKey: string,
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
    const response = await axios.get(`${API_BASE_URL}/memories`, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
      params,
    });
    return response.data;
  },

  async searchMemories(
    apiKey: string,
    query: string,
    params?: {
      agent_id?: string;
      type?: string;
      limit?: number;
    }
  ): Promise<SearchResponse> {
    const response = await axios.get(`${API_BASE_URL}/search/keyword`, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
      params: {
        q: query,
        ...params,
      },
    });
    return response.data;
  },
};
