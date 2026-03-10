export interface Memory {
  id: string
  agent_id: string
  content: string
  metadata: Record<string, unknown>
  created_at: string
  updated_at: string
  importance_score: number
  access_count: number
}

export interface MemoryListParams {
  agent_id?: string
  limit?: number
  offset?: number
  sort_by?: 'created_at' | 'importance_score' | 'access_count'
  sort_order?: 'asc' | 'desc'
}

export interface MemoryListResponse {
  memories: Memory[]
  total: number
  limit: number
  offset: number
}

export interface SearchResult {
  memory: Memory
  highlight: string
  score: number
}

export interface SearchParams {
  query: string
  agent_id?: string
  limit?: number
}

export interface SearchResponse {
  results: SearchResult[]
  total: number
  query: string
}

export interface ApiKey {
  id: string
  name: string
  prefix: string
  created_at: string
  last_used_at: string | null
  expires_at: string | null
}

export interface CreateApiKeyRequest {
  name: string
  expires_in_days?: number
}

export interface CreateApiKeyResponse {
  api_key: ApiKey
  secret: string // Only shown once
}

export interface Analytics {
  total_memories: number
  memories_by_agent: Array<{
    agent_id: string
    count: number
  }>
  memories_by_day: Array<{
    date: string
    count: number
  }>
  top_agents: Array<{
    agent_id: string
    memory_count: number
    avg_importance: number
  }>
  growth_rate: number
}

export interface User {
  id: string
  email: string
  created_at: string
}
