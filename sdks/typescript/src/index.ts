/**
 * Agent Memory Cloud SDK for TypeScript.
 *
 * Persistent memory infrastructure for AI agent fleets.
 *
 * @packageDocumentation
 */

// Version
export const VERSION = '1.0.0';

// Client
export { MemoryClient, type MemoryClientConfig } from './client.js';

// Models
export {
  // Types
  type MemoryType,
  type Memory,
  type Agent,
  type Project,
  type SearchResult,
  type PaginatedResponse,
  // Parameter types
  type MemoryCreateParams,
  type MemoryListParams,
  type MemoryUpdateParams,
  type MemoryCompactParams,
  type MemoryCompactResult,
  type AgentCreateParams,
  type AgentListParams,
  type ProjectCreateParams,
  type ProjectListParams,
  type SearchKeywordParams,
  type SearchSemanticParams,
  type SearchResponse,
  // Constants
  MEMORY_TYPES,
  // Utility functions
  hasMore,
  // Parsers (for advanced use)
  parseMemory,
  parseAgent,
  parseProject,
  parseSearchResult,
  parsePaginatedResponse,
} from './models.js';

// Exceptions
export {
  AgentMemoryError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
  ValidationError,
} from './exceptions.js';

// Resources (for advanced use)
export { MemoriesResource } from './resources/memories.js';
export { AgentsResource } from './resources/agents.js';
export { ProjectsResource } from './resources/projects.js';
export { SearchResource } from './resources/search.js';
