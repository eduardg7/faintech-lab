import axios from 'axios';
import axiosRetry from 'axios-retry';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

// Create axios instance for API calls with retry configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Add retry interceptor with exponential backoff
axiosRetry(apiClient, {
  retries: 3,
  retryDelay: (retryCount: number) => {
    // Exponential backoff: 1000ms, 2000ms, 4000ms
    return Math.min(1000 * Math.pow(2, retryCount), 10000);
  },
  retryCondition: (error: any) => {
    // Retry on: network errors, 5xx errors, timeouts
    return (
      !error.response ||
      (error.response?.status >= 500 && error.response?.status < 600) ||
      error.code === 'ECONNABORTED' ||
      error.code === 'ETIMEDOUT'
    );
  },
  onRetry: (retryCount: number, error: any, requestConfig: any) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`Retry attempt ${retryCount} for ${requestConfig.url}:`, error.message);
    }
  },
});

// Request interceptor to add auth header
apiClient.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('amc_access_token') : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('amc_refresh_token') : null;

        if (!refreshToken) {
          // No refresh token - logout
          if (typeof window !== 'undefined') {
            localStorage.removeItem('amc_access_token');
            localStorage.removeItem('amc_refresh_token');
            window.location.href = '/';
          }
          return Promise.reject(error);
        }

        // Try to refresh token
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token: newRefreshToken } = response.data;

        // Store new tokens
        if (typeof window !== 'undefined') {
          localStorage.setItem('amc_access_token', access_token);
          localStorage.setItem('amc_refresh_token', newRefreshToken);
        }

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed - logout
        if (typeof window !== 'undefined') {
          localStorage.removeItem('amc_access_token');
          localStorage.removeItem('amc_refresh_token');
          window.location.href = '/';
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

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

export interface CurrentUser {
  id: string;
  email: string;
  full_name?: string | null;
  workspace_id: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login_at?: string | null;
}

export interface ApiKeySummary {
  id: string;
  name: string;
  key_preview: string;
  is_active: boolean;
  created_at: string;
  last_used_at?: string | null;
  revoked_at?: string | null;
  expires_at?: string | null;
}

export interface ApiKeysResponse {
  api_keys: ApiKeySummary[];
  total: number;
}

// Auth headers are no longer needed - apiClient interceptor handles it
// Kept for backward compatibility with existing code
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
      date_from?: string;
      date_to?: string;
      limit?: number;
      offset?: number;
    }
  ): Promise<MemoriesResponse> {
    const pageSize = params?.limit ?? 20;
    const page = Math.floor((params?.offset ?? 0) / pageSize) + 1;

    const response = await apiClient.get('/memories', {
      params: {
        agent_id: params?.agent_id,
        project_id: params?.project_id,
        memory_type: params?.type,
        tag: params?.tags,
        since: params?.since || params?.date_from,
        until: params?.until || params?.date_to,
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
    const response = await apiClient.get('/search/keyword', {
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
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  async getCurrentUser(token: string): Promise<CurrentUser> {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  async listApiKeys(token: string): Promise<ApiKeysResponse> {
    const response = await apiClient.get('/api-keys');
    return response.data;
  },
};
