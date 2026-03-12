/**
 * Data models for Agent Memory Cloud SDK.
 * @module models
 */

/**
 * Type of memory entry.
 */
export type MemoryType = 'outcome' | 'learning' | 'preference' | 'decision';

/**
 * All supported memory types as an array.
 */
export const MEMORY_TYPES: readonly MemoryType[] = [
  'outcome',
  'learning',
  'preference',
  'decision',
] as const;

/**
 * Represents a memory entry.
 */
export interface Memory {
  /** Unique identifier */
  readonly id: string;
  /** ID of the agent that created this memory */
  readonly agentId: string;
  /** Type of memory */
  readonly memoryType: MemoryType;
  /** Memory content text */
  readonly content: string;
  /** Creation timestamp (ISO 8601) */
  readonly createdAt: string;
  /** Optional workspace ID */
  readonly workspaceId: string | undefined;
  /** Optional project ID */
  readonly projectId: string | undefined;
  /** Tags associated with this memory */
  readonly tags: readonly string[];
  /** Additional metadata */
  readonly metadata: Record<string, unknown>;
  /** Vector embedding (if available) */
  readonly embedding: readonly number[] | undefined;
  /** Last update timestamp (ISO 8601) */
  readonly updatedAt: string | undefined;
  /** Confidence score (0.0-1.0) */
  readonly confidence: number | undefined;
}

/**
 * Represents an AI agent that owns memories.
 */
export interface Agent {
  /** Unique identifier */
  readonly id: string;
  /** Agent name */
  readonly name: string;
  /** Creation timestamp (ISO 8601) */
  readonly createdAt: string;
  /** Optional description */
  readonly description: string | undefined;
  /** Additional metadata */
  readonly metadata: Record<string, unknown>;
}

/**
 * Represents a project for organizing memories.
 */
export interface Project {
  /** Unique identifier */
  readonly id: string;
  /** Project name */
  readonly name: string;
  /** Creation timestamp (ISO 8601) */
  readonly createdAt: string;
  /** Optional description */
  readonly description: string | undefined;
  /** Additional metadata */
  readonly metadata: Record<string, unknown>;
}

/**
 * Represents a search result with relevance score.
 */
export interface SearchResult {
  /** The memory that matched the search */
  readonly memory: Memory;
  /** Relevance score (0.0-1.0) */
  readonly score: number;
}

/**
 * Generic paginated response.
 */
export interface PaginatedResponse<T> {
  /** Items on this page */
  readonly items: readonly T[];
  /** Total number of items */
  readonly total: number;
  /** Max items per page */
  readonly limit: number;
  /** Current offset */
  readonly offset: number;
}

/**
 * Check if there are more results.
 */
export function hasMore<T>(response: PaginatedResponse<T>): boolean {
  return response.offset + response.items.length < response.total;
}

// ============= API Response Types (raw from server) =============

/** Raw memory response from API */
interface MemoryResponse {
  id: string;
  agent_id: string;
  memory_type: string;
  content: string;
  created_at: string;
  workspace_id?: string;
  project_id?: string;
  tags?: string[];
  metadata?: Record<string, unknown>;
  embedding?: number[];
  updated_at?: string;
  confidence?: number;
}

/** Raw agent response from API */
interface AgentResponse {
  id: string;
  name: string;
  created_at: string;
  description?: string;
  metadata?: Record<string, unknown>;
}

/** Raw project response from API */
interface ProjectResponse {
  id: string;
  name: string;
  created_at: string;
  description?: string;
  metadata?: Record<string, unknown>;
}

/** Raw search result response from API */
interface SearchResultResponse {
  memory: MemoryResponse;
  score: number;
}

/** Raw paginated response from API */
interface PaginatedResponseRaw<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

// ============= Parsers =============

/**
 * Parse a memory response from the API.
 */
export function parseMemory(data: MemoryResponse): Memory {
  return {
    id: data.id,
    agentId: data.agent_id,
    memoryType: data.memory_type as MemoryType,
    content: data.content,
    createdAt: data.created_at,
    workspaceId: data.workspace_id,
    projectId: data.project_id,
    tags: data.tags ?? [],
    metadata: data.metadata ?? {},
    embedding: data.embedding,
    updatedAt: data.updated_at,
    confidence: data.confidence,
  };
}

/**
 * Parse an agent response from the API.
 */
export function parseAgent(data: AgentResponse): Agent {
  return {
    id: data.id,
    name: data.name,
    createdAt: data.created_at,
    description: data.description,
    metadata: data.metadata ?? {},
  };
}

/**
 * Parse a project response from the API.
 */
export function parseProject(data: ProjectResponse): Project {
  return {
    id: data.id,
    name: data.name,
    createdAt: data.created_at,
    description: data.description,
    metadata: data.metadata ?? {},
  };
}

/**
 * Parse a search result response from the API.
 */
export function parseSearchResult(data: SearchResultResponse): SearchResult {
  return {
    memory: parseMemory(data.memory),
    score: data.score,
  };
}

/**
 * Parse a paginated response from the API.
 */
export function parsePaginatedResponse<T, R>(
  data: PaginatedResponseRaw<T>,
  itemParser: (item: T) => R
): PaginatedResponse<R> {
  return {
    items: data.items.map(itemParser),
    total: data.total,
    limit: data.limit,
    offset: data.offset,
  };
}

// ============= Request Parameter Types =============

/** Parameters for creating a memory */
export interface MemoryCreateParams {
  /** ID of the agent creating the memory */
  agentId: string;
  /** Type of memory */
  memoryType: MemoryType;
  /** Memory content text */
  content: string;
  /** Optional workspace ID */
  workspaceId?: string;
  /** Optional project ID */
  projectId?: string;
  /** Optional tags */
  tags?: readonly string[];
  /** Optional metadata */
  metadata?: Record<string, unknown>;
  /** Optional confidence score (0.0-1.0) */
  confidence?: number;
}

/** Parameters for listing memories */
export interface MemoryListParams {
  /** Filter by agent ID */
  agentId?: string;
  /** Filter by project ID */
  projectId?: string;
  /** Filter by memory type */
  memoryType?: MemoryType;
  /** Filter by tags (AND logic) */
  tags?: readonly string[];
  /** Max results per page (1-100) */
  limit?: number;
  /** Pagination offset */
  offset?: number;
}

/** Parameters for updating a memory */
export interface MemoryUpdateParams {
  /** Memory UUID */
  memoryId: string;
  /** New content */
  content?: string;
  /** New tags */
  tags?: readonly string[];
  /** New metadata */
  metadata?: Record<string, unknown>;
  /** New confidence score */
  confidence?: number;
}

/** Parameters for compacting memories */
export interface MemoryCompactParams {
  /** Agent ID to compact memories for */
  agentId: string;
  /** Optional project ID filter */
  projectId?: string;
  /** Only compact memories older than this many days */
  maxAgeDays?: number;
}

/** Result of memory compaction */
export interface MemoryCompactResult {
  /** Number of memories processed */
  memoriesProcessed: number;
  /** Number of summary memories created */
  memoriesCreated: number;
  /** Number of memories archived */
  memoriesArchived: number;
}

/** Parameters for creating an agent */
export interface AgentCreateParams {
  /** Agent name */
  name: string;
  /** Optional description */
  description?: string;
  /** Optional metadata */
  metadata?: Record<string, unknown>;
}

/** Parameters for listing agents */
export interface AgentListParams {
  /** Max results per page */
  limit?: number;
  /** Pagination offset */
  offset?: number;
}

/** Parameters for creating a project */
export interface ProjectCreateParams {
  /** Project name */
  name: string;
  /** Optional description */
  description?: string;
  /** Optional metadata */
  metadata?: Record<string, unknown>;
}

/** Parameters for listing projects */
export interface ProjectListParams {
  /** Max results per page */
  limit?: number;
  /** Pagination offset */
  offset?: number;
}

/** Parameters for keyword search */
export interface SearchKeywordParams {
  /** Search query string */
  query: string;
  /** Filter by agent ID */
  agentId?: string;
  /** Filter by project ID */
  projectId?: string;
  /** Filter by tags */
  tags?: readonly string[];
  /** Max results */
  limit?: number;
}

/** Parameters for semantic search */
export interface SearchSemanticParams {
  /** Natural language query */
  query: string;
  /** Filter by agent ID */
  agentId?: string;
  /** Filter by project ID */
  projectId?: string;
  /** Filter by tags */
  tags?: readonly string[];
  /** Max results */
  limit?: number;
}

/** Search response wrapper */
export interface SearchResponse {
  /** Search results */
  results: readonly SearchResult[];
}
