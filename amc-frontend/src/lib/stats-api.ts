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

interface RawMemory {
  id: string;
  workspace_id: string;
  agent_id: string;
  task_id: string | null;
  project_id: string;
  memory_type: string;
  importance: number;
  created_at: string;
  tags: string[];
  content: string;
  metadata: Record<string, unknown>;
  updated_at: string | null;
}

// Fetch all memories and aggregate client-side (backend has no /stats/* endpoints)
async function fetchAllMemories(apiKey: string): Promise<RawMemory[]> {
  const response = await axios.get(`${API_BASE_URL}/memories`, {
    headers: { Authorization: `Bearer ${apiKey}` },
    params: { page_size: 500 },
  });
  return (response.data.memories || []) as RawMemory[];
}

export const statsApi = {
  async getMemoryStats(apiKey: string): Promise<MemoryStats> {
    const memories = await fetchAllMemories(apiKey);

    const by_type = { outcome: 0, learning: 0, preference: 0, decision: 0 };
    const by_project_map: Record<string, number> = {};
    let importance_sum = 0;

    for (const m of memories) {
      if (m.memory_type in by_type) by_type[m.memory_type as keyof typeof by_type]++;
      by_project_map[m.project_id] = (by_project_map[m.project_id] || 0) + 1;
      importance_sum += m.importance || 0;
    }

    const total = memories.length;
    const by_project = Object.entries(by_project_map).map(([project_id, count]) => ({
      project_id,
      count,
      percentage: total > 0 ? Math.round((count / total) * 1000) / 10 : 0,
    }));

    return {
      total_memories: total,
      by_type,
      by_project,
      storage_used_mb: Math.round(total * 0.002 * 100) / 100,
      avg_importance: total > 0 ? Math.round((importance_sum / total) * 100) / 100 : 0,
    };
  },

  async getAgentActivity(
    apiKey: string,
    params?: { days?: number; limit?: number }
  ): Promise<AgentActivityResponse> {
    const days = params?.days || 7;
    const limit = params?.limit || 10;
    const memories = await fetchAllMemories(apiKey);

    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);
    const recent = memories.filter(m => new Date(m.created_at) >= cutoff);

    const by_agent: Record<string, { count: number; last: string; by_date: Record<string, number> }> = {};
    for (const m of recent) {
      if (!by_agent[m.agent_id]) {
        by_agent[m.agent_id] = { count: 0, last: m.created_at, by_date: {} };
      }
      by_agent[m.agent_id].count++;
      if (m.created_at > by_agent[m.agent_id].last) {
        by_agent[m.agent_id].last = m.created_at;
      }
      const date = m.created_at.split('T')[0];
      by_agent[m.agent_id].by_date[date] = (by_agent[m.agent_id].by_date[date] || 0) + 1;
    }

    const dates: string[] = [];
    for (let i = days - 1; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      dates.push(d.toISOString().split('T')[0]);
    }

    const agents: AgentActivity[] = Object.entries(by_agent)
      .sort((a, b) => b[1].count - a[1].count)
      .slice(0, limit)
      .map(([agent_id, data]) => ({
        agent_id,
        memory_count: data.count,
        last_activity: data.last,
        activity_timeline: dates.map(date => ({
          date,
          count: data.by_date[date] || 0,
        })),
      }));

    return { agents, total: agents.length, period_days: days };
  },

  async getProjectBreakdown(
    apiKey: string,
    params?: { limit?: number }
  ): Promise<ProjectBreakdownResponse> {
    const limit = params?.limit || 10;
    const memories = await fetchAllMemories(apiKey);

    const by_project: Record<string, { by_type: Record<string, number>; by_agent: Record<string, number> }> = {};

    for (const m of memories) {
      if (!by_project[m.project_id]) {
        by_project[m.project_id] = { by_type: {}, by_agent: {} };
      }
      by_project[m.project_id].by_type[m.memory_type] = (by_project[m.project_id].by_type[m.memory_type] || 0) + 1;
      by_project[m.project_id].by_agent[m.agent_id] = (by_project[m.project_id].by_agent[m.agent_id] || 0) + 1;
    }

    const projects: ProjectBreakdown[] = Object.entries(by_project)
      .sort((a, b) => {
        const totalA = Object.values(a[1].by_type).reduce((s, v) => s + v, 0);
        const totalB = Object.values(b[1].by_type).reduce((s, v) => s + v, 0);
        return totalB - totalA;
      })
      .slice(0, limit)
      .map(([project_id, data]) => {
        const total = Object.values(data.by_type).reduce((s, v) => s + v, 0);
        const top_agents = Object.entries(data.by_agent)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 3)
          .map(([agent_id, count]) => ({ agent_id, count }));
        return {
          project_id,
          project_name: project_id,
          total_memories: total,
          by_type: {
            outcome: data.by_type['outcome'] || 0,
            learning: data.by_type['learning'] || 0,
            preference: data.by_type['preference'] || 0,
            decision: data.by_type['decision'] || 0,
          },
          top_agents,
          growth_rate: 0,
        };
      });

    return { projects, total: projects.length };
  },
};

// Empty mock data (fallback when no memories exist yet)
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
