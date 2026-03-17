import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

// Create shared axios instance for API calls
const apiClient = axios.create({
  baseURL: API_BASE_URL,
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

export interface MemoryStats {
  total_memories: number;
  by_type: {
    outcome: number;
    learning: number;
    preference: number;
    decision: number;
  };
  by_project: Array<{
    project_id: string;
    count: number;
    percentage: number;
  }>;
  storage_used_mb: number;
  avg_importance: number;
}

export interface AgentActivity {
  agent_id: string;
  memory_count: number;
  last_activity: string;
  activity_timeline: Array<{
    date: string;
    count: number;
  }>;
}

export interface AgentActivityResponse {
  agents: AgentActivity[];
  total: number;
  period_days: number;
}

export interface ProjectBreakdown {
  project_id: string;
  project_name: string;
  total_memories: number;
  by_type: {
    outcome: number;
    learning: number;
    preference: number;
    decision: number;
  };
  top_agents: Array<{
    agent_id: string;
    count: number;
  }>;
  growth_rate: number;
}

export interface ProjectBreakdownResponse {
  projects: ProjectBreakdown[];
  total: number;
}

interface RawMemory {
  id: string;
  workspace_id: string;
  agent_id: string;
  task_id: string | null;
  project_id: string | null;
  memory_type: 'outcome' | 'learning' | 'preference' | 'decision';
  importance: number;
  created_at: string;
  tags: string[];
  content: string;
  metadata: Record<string, unknown>;
  updated_at: string | null;
}

async function fetchAllMemories(token: string): Promise<RawMemory[]> {
  const pageSize = 100;
  let page = 1;
  let hasNext = true;
  const memories: RawMemory[] = [];

  while (hasNext) {
    const response = await apiClient.get('/memories', {
      params: { page, page_size: pageSize },
    });

    memories.push(...((response.data.memories || []) as RawMemory[]));
    hasNext = Boolean(response.data.has_next);
    page += 1;
  }

  return memories;
}

export const statsApi = {
  async getMemoryStats(token: string): Promise<MemoryStats> {
    const memories = await fetchAllMemories(token);

    const byType = { outcome: 0, learning: 0, preference: 0, decision: 0 };
    const byProjectMap: Record<string, number> = {};
    let importanceSum = 0;

    for (const memory of memories) {
      byType[memory.memory_type] += 1;
      if (memory.project_id) {
        byProjectMap[memory.project_id] = (byProjectMap[memory.project_id] || 0) + 1;
      }
      importanceSum += memory.importance || 0;
    }

    const total = memories.length;

    return {
      total_memories: total,
      by_type: byType,
      by_project: Object.entries(byProjectMap)
        .sort((a, b) => b[1] - a[1])
        .map(([project_id, count]) => ({
          project_id,
          count,
          percentage: total > 0 ? Math.round((count / total) * 1000) / 10 : 0,
        })),
      storage_used_mb: Math.round(total * 0.002 * 100) / 100,
      avg_importance: total > 0 ? Math.round((importanceSum / total) * 100) / 100 : 0,
    };
  },

  async getAgentActivity(token: string, params?: { days?: number; limit?: number }): Promise<AgentActivityResponse> {
    const days = params?.days || 7;
    const limit = params?.limit || 10;
    const memories = await fetchAllMemories(token);

    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);

    const recent = memories.filter((memory) => new Date(memory.created_at) >= cutoff);
    const byAgent: Record<string, { count: number; last: string; byDate: Record<string, number> }> = {};

    for (const memory of recent) {
      if (!byAgent[memory.agent_id]) {
        byAgent[memory.agent_id] = { count: 0, last: memory.created_at, byDate: {} };
      }

      byAgent[memory.agent_id].count += 1;
      if (memory.created_at > byAgent[memory.agent_id].last) {
        byAgent[memory.agent_id].last = memory.created_at;
      }

      const date = memory.created_at.split('T')[0];
      byAgent[memory.agent_id].byDate[date] = (byAgent[memory.agent_id].byDate[date] || 0) + 1;
    }

    const dates = Array.from({ length: days }, (_, index) => {
      const date = new Date();
      date.setDate(date.getDate() - (days - index - 1));
      return date.toISOString().split('T')[0];
    });

    const agents = Object.entries(byAgent)
      .sort((a, b) => b[1].count - a[1].count)
      .slice(0, limit)
      .map(([agent_id, data]) => ({
        agent_id,
        memory_count: data.count,
        last_activity: data.last,
        activity_timeline: dates.map((date) => ({
          date,
          count: data.byDate[date] || 0,
        })),
      }));

    return {
      agents,
      total: agents.length,
      period_days: days,
    };
  },

  async getProjectBreakdown(token: string, params?: { limit?: number }): Promise<ProjectBreakdownResponse> {
    const limit = params?.limit || 10;
    const memories = await fetchAllMemories(token);
    const byProject: Record<string, { byType: Record<string, number>; byAgent: Record<string, number> }> = {};

    for (const memory of memories) {
      if (!memory.project_id) {
        continue;
      }

      if (!byProject[memory.project_id]) {
        byProject[memory.project_id] = { byType: {}, byAgent: {} };
      }

      byProject[memory.project_id].byType[memory.memory_type] =
        (byProject[memory.project_id].byType[memory.memory_type] || 0) + 1;
      byProject[memory.project_id].byAgent[memory.agent_id] =
        (byProject[memory.project_id].byAgent[memory.agent_id] || 0) + 1;
    }

    const projects = Object.entries(byProject)
      .sort((a, b) => {
        const totalA = Object.values(a[1].byType).reduce((sum, value) => sum + value, 0);
        const totalB = Object.values(b[1].byType).reduce((sum, value) => sum + value, 0);
        return totalB - totalA;
      })
      .slice(0, limit)
      .map(([project_id, data]) => ({
        project_id,
        project_name: project_id,
        total_memories: Object.values(data.byType).reduce((sum, value) => sum + value, 0),
        by_type: {
          outcome: data.byType.outcome || 0,
          learning: data.byType.learning || 0,
          preference: data.byType.preference || 0,
          decision: data.byType.decision || 0,
        },
        top_agents: Object.entries(data.byAgent)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 3)
          .map(([agent_id, count]) => ({ agent_id, count })),
        growth_rate: 0,
      }));

    return {
      projects,
      total: projects.length,
    };
  },
};

export const mockMemoryStats: MemoryStats = {
  total_memories: 0,
  by_type: { outcome: 0, learning: 0, preference: 0, decision: 0 },
  by_project: [],
  storage_used_mb: 0,
  avg_importance: 0,
};

export const mockAgentActivity: AgentActivityResponse = {
  agents: [],
  total: 0,
  period_days: 7,
};

export const mockProjectBreakdown: ProjectBreakdownResponse = {
  projects: [],
  total: 0,
};

// Per-agent dashboard stats
export interface AgentDashboardStats {
  agent_id: string;
  total_memories: number;
  memories_this_week: number;
  pattern_count: number;
  storage_used_mb: number;
  by_type: {
    outcome: number;
    learning: number;
    preference: number;
    decision: number;
  };
  recent_activity: Array<{
    date: string;
    count: number;
  }>;
}

export const statsApi = {
  ...statsApi,

  async getAgentDashboardStats(token: string, agentId: string): Promise<AgentDashboardStats> {
    const memories = await fetchAllMemories(token);

    // Filter memories for this specific agent
    const agentMemories = memories.filter((m) => m.agent_id === agentId);
    const total = agentMemories.length;

    // Calculate memories this week
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    const memoriesThisWeek = agentMemories.filter(
      (m) => new Date(m.created_at) >= oneWeekAgo
    ).length;

    // Calculate by type
    const byType = { outcome: 0, learning: 0, preference: 0, decision: 0 };
    for (const memory of agentMemories) {
      byType[memory.memory_type] += 1;
    }

    // Calculate pattern count (unique tag combinations)
    const tagPatterns = new Set<string>();
    for (const memory of agentMemories) {
      if (memory.tags && memory.tags.length > 0) {
        tagPatterns.add(memory.tags.sort().join(','));
      }
    }
    const patternCount = tagPatterns.size;

    // Calculate recent activity (last 7 days)
    const activityMap: Record<string, number> = {};
    const dates = Array.from({ length: 7 }, (_, index) => {
      const date = new Date();
      date.setDate(date.getDate() - (6 - index));
      return date.toISOString().split('T')[0];
    });

    for (const date of dates) {
      activityMap[date] = 0;
    }

    for (const memory of agentMemories) {
      const date = memory.created_at.split('T')[0];
      if (activityMap[date] !== undefined) {
        activityMap[date] += 1;
      }
    }

    return {
      agent_id: agentId,
      total_memories: total,
      memories_this_week: memoriesThisWeek,
      pattern_count: patternCount,
      storage_used_mb: Math.round(total * 0.002 * 100) / 100,
      by_type: byType,
      recent_activity: dates.map((date) => ({
        date,
        count: activityMap[date] || 0,
      })),
    };
  },
};
