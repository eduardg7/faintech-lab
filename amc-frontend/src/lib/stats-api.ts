import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

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

export const statsApi = {
  async getMemoryStats(apiKey: string): Promise<MemoryStats> {
    const response = await axios.get(`${API_BASE_URL}/stats/memories`, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
    });
    return response.data;
  },

  async getAgentActivity(
    apiKey: string,
    params?: { days?: number; limit?: number }
  ): Promise<AgentActivityResponse> {
    const response = await axios.get(`${API_BASE_URL}/stats/agents`, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
      params: {
        days: params?.days || 7,
        limit: params?.limit || 10,
      },
    });
    return response.data;
  },

  async getProjectBreakdown(
    apiKey: string,
    params?: { limit?: number }
  ): Promise<ProjectBreakdownResponse> {
    const response = await axios.get(`${API_BASE_URL}/stats/projects`, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
      params: {
        limit: params?.limit || 10,
      },
    });
    return response.data;
  },
};

// Mock data for development when API is not available
export const mockMemoryStats: MemoryStats = {
  total_memories: 1247,
  by_type: {
    outcome: 423,
    learning: 398,
    preference: 256,
    decision: 170,
  },
  by_project: [
    { project_id: 'faintech-os', count: 512, percentage: 41.1 },
    { project_id: 'faintech-lab', count: 389, percentage: 31.2 },
    { project_id: 'faintrading', count: 212, percentage: 17.0 },
    { project_id: 'amc-mvp', count: 134, percentage: 10.7 },
  ],
  storage_used_mb: 24.8,
  avg_importance: 0.72,
};

export const mockAgentActivity: AgentActivityResponse = {
  agents: [
    {
      agent_id: 'faintech-ceo',
      memory_count: 187,
      last_activity: '2026-03-10T22:15:00Z',
      activity_timeline: [
        { date: '2026-03-04', count: 12 },
        { date: '2026-03-05', count: 18 },
        { date: '2026-03-06', count: 24 },
        { date: '2026-03-07', count: 31 },
        { date: '2026-03-08', count: 28 },
        { date: '2026-03-09', count: 42 },
        { date: '2026-03-10', count: 32 },
      ],
    },
    {
      agent_id: 'faintech-cto',
      memory_count: 156,
      last_activity: '2026-03-10T22:20:00Z',
      activity_timeline: [
        { date: '2026-03-04', count: 8 },
        { date: '2026-03-05', count: 15 },
        { date: '2026-03-06', count: 22 },
        { date: '2026-03-07', count: 28 },
        { date: '2026-03-08', count: 31 },
        { date: '2026-03-09', count: 29 },
        { date: '2026-03-10', count: 23 },
      ],
    },
    {
      agent_id: 'faintech-frontend',
      memory_count: 98,
      last_activity: '2026-03-10T22:25:00Z',
      activity_timeline: [
        { date: '2026-03-04', count: 5 },
        { date: '2026-03-05', count: 9 },
        { date: '2026-03-06', count: 14 },
        { date: '2026-03-07', count: 18 },
        { date: '2026-03-08', count: 21 },
        { date: '2026-03-09', count: 17 },
        { date: '2026-03-10', count: 14 },
      ],
    },
    {
      agent_id: 'faintech-backend',
      memory_count: 142,
      last_activity: '2026-03-10T22:10:00Z',
      activity_timeline: [
        { date: '2026-03-04', count: 11 },
        { date: '2026-03-05', count: 16 },
        { date: '2026-03-06', count: 23 },
        { date: '2026-03-07', count: 26 },
        { date: '2026-03-08', count: 28 },
        { date: '2026-03-09', count: 22 },
        { date: '2026-03-10', count: 16 },
      ],
    },
  ],
  total: 4,
  period_days: 7,
};

export const mockProjectBreakdown: ProjectBreakdownResponse = {
  projects: [
    {
      project_id: 'faintech-os',
      project_name: 'Faintech OS',
      total_memories: 512,
      by_type: { outcome: 178, learning: 156, preference: 98, decision: 80 },
      top_agents: [
        { agent_id: 'faintech-ceo', count: 89 },
        { agent_id: 'faintech-cto', count: 67 },
        { agent_id: 'faintech-coo', count: 54 },
      ],
      growth_rate: 12.5,
    },
    {
      project_id: 'faintech-lab',
      project_name: 'Faintech Labs',
      total_memories: 389,
      by_type: { outcome: 134, learning: 118, preference: 78, decision: 59 },
      top_agents: [
        { agent_id: 'faintech-cto', count: 72 },
        { agent_id: 'faintech-backend', count: 58 },
        { agent_id: 'faintech-frontend', count: 45 },
      ],
      growth_rate: 18.2,
    },
    {
      project_id: 'faintrading',
      project_name: 'FainTrading',
      total_memories: 212,
      by_type: { outcome: 72, learning: 68, preference: 42, decision: 30 },
      top_agents: [
        { agent_id: 'faintech-ceo', count: 45 },
        { agent_id: 'faintech-cto', count: 38 },
        { agent_id: 'faintech-backend', count: 32 },
      ],
      growth_rate: 8.7,
    },
  ],
  total: 3,
};
