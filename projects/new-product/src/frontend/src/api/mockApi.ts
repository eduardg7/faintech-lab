// Mock data for development - will be replaced with actual API calls

import type { Memory, MemoryListResponse, SearchResponse, Analytics, ApiKey, CreateApiKeyResponse } from '../types'

const mockAgents = [
  'faintech-ceo',
  'faintech-cto',
  'faintech-cpo',
  'faintech-frontend',
  'faintech-backend',
  'faintech-devops',
  'faintech-qa',
]

const generateMockMemory = (id: number): Memory => ({
  id: `mem-${id.toString().padStart(4, '0')}`,
  agent_id: mockAgents[Math.floor(Math.random() * mockAgents.length)],
  content: `This is a sample memory entry #${id}. It contains information about the agent's learnings, decisions, and context. The content can be quite long and detailed, representing the kind of information an AI agent might want to persist for future reference.`,
  metadata: {
    source: ['conversation', 'task', 'learning', 'correction'][Math.floor(Math.random() * 4)],
    tags: ['important', 'technical', 'business', 'process'].slice(0, Math.floor(Math.random() * 4) + 1),
  },
  created_at: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
  updated_at: new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000).toISOString(),
  importance_score: Math.random() * 100,
  access_count: Math.floor(Math.random() * 50),
})

const mockMemories: Memory[] = Array.from({ length: 150 }, (_, i) => generateMockMemory(i + 1))

export async function fetchMemories(params: {
  agent_id?: string
  limit?: number
  offset?: number
}): Promise<MemoryListResponse> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))

  let filtered = [...mockMemories]
  
  if (params.agent_id) {
    filtered = filtered.filter(m => m.agent_id === params.agent_id)
  }

  const limit = params.limit ?? 20
  const offset = params.offset ?? 0

  return {
    memories: filtered.slice(offset, offset + limit),
    total: filtered.length,
    limit,
    offset,
  }
}

export async function searchMemories(query: string, params?: { agent_id?: string; limit?: number }): Promise<SearchResponse> {
  await new Promise(resolve => setTimeout(resolve, 200))

  const results = mockMemories
    .filter(m => {
      const matchesQuery = m.content.toLowerCase().includes(query.toLowerCase()) ||
        m.agent_id.toLowerCase().includes(query.toLowerCase())
      const matchesAgent = !params?.agent_id || m.agent_id === params.agent_id
      return matchesQuery && matchesAgent
    })
    .slice(0, params?.limit ?? 10)
    .map(memory => ({
      memory,
      highlight: memory.content.replace(
        new RegExp(`(${query})`, 'gi'),
        '<mark class="bg-yellow-500/30 text-yellow-200">$1</mark>'
      ),
      score: Math.random() * 100,
    }))

  return {
    results,
    total: results.length,
    query,
  }
}

export async function fetchAnalytics(): Promise<Analytics> {
  await new Promise(resolve => setTimeout(resolve, 400))

  const memoriesByAgent = mockAgents.map(agent_id => ({
    agent_id,
    count: mockMemories.filter(m => m.agent_id === agent_id).length,
  }))

  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const date = new Date()
    date.setDate(date.getDate() - (6 - i))
    return date.toISOString().split('T')[0]
  })

  const memoriesByDay = last7Days.map(date => ({
    date,
    count: Math.floor(Math.random() * 30) + 5,
  }))

  const topAgents = mockAgents
    .map(agent_id => {
      const agentMemories = mockMemories.filter(m => m.agent_id === agent_id)
      return {
        agent_id,
        memory_count: agentMemories.length,
        avg_importance: agentMemories.reduce((sum, m) => sum + m.importance_score, 0) / agentMemories.length || 0,
      }
    })
    .sort((a, b) => b.memory_count - a.memory_count)
    .slice(0, 5)

  return {
    total_memories: mockMemories.length,
    memories_by_agent: memoriesByAgent,
    memories_by_day: memoriesByDay,
    top_agents: topAgents,
    growth_rate: 12.5,
  }
}

export async function fetchApiKeys(): Promise<ApiKey[]> {
  await new Promise(resolve => setTimeout(resolve, 200))

  return [
    {
      id: 'key-001',
      name: 'Production Key',
      prefix: 'amc_prod_****',
      created_at: '2026-03-01T10:00:00Z',
      last_used_at: '2026-03-10T06:30:00Z',
      expires_at: null,
    },
    {
      id: 'key-002',
      name: 'Development Key',
      prefix: 'amc_dev_****',
      created_at: '2026-03-05T14:30:00Z',
      last_used_at: '2026-03-09T18:45:00Z',
      expires_at: '2026-06-05T14:30:00Z',
    },
  ]
}

export async function createApiKey(name: string, expiresInDays?: number): Promise<CreateApiKeyResponse> {
  await new Promise(resolve => setTimeout(resolve, 300))

  const secret = `amc_${name.toLowerCase().replace(/\s+/g, '_')}_${Math.random().toString(36).substring(2, 15)}`

  return {
    api_key: {
      id: `key-${Date.now()}`,
      name,
      prefix: `${secret.substring(0, 12)}****`,
      created_at: new Date().toISOString(),
      last_used_at: null,
      expires_at: expiresInDays ? new Date(Date.now() + expiresInDays * 24 * 60 * 60 * 1000).toISOString() : null,
    },
    secret,
  }
}

export async function revokeApiKey(id: string): Promise<void> {
  await new Promise(resolve => setTimeout(resolve, 200))
  console.log('Revoking key:', id)
}
