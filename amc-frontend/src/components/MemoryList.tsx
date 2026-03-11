'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { api, Memory } from '@/lib/api';
import { useState } from 'react';
import ErrorState from './ui/ErrorState';
import LoadingState from './ui/LoadingState';
import EmptyState from './ui/EmptyState';

export default function MemoryList() {
  const { apiKey, logout } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState<string>('');
  const [selectedAgent, setSelectedAgent] = useState<string>('');

  // Fetch memories
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['memories', selectedType, selectedAgent],
    queryFn: () =>
      api.getMemories(apiKey!, {
        type: selectedType || undefined,
        agent_id: selectedAgent || undefined,
        limit: 50,
      }),
    enabled: !!apiKey,
  });

  // Search memories
  const { data: searchData, refetch: refetchSearch } = useQuery({
    queryKey: ['search', searchQuery],
    queryFn: () =>
      api.searchMemories(apiKey!, searchQuery, {
        type: selectedType || undefined,
        agent_id: selectedAgent || undefined,
      }),
    enabled: !!apiKey && searchQuery.length > 0,
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery) {
      refetchSearch();
    } else {
      refetch();
    }
  };

  const memories = searchQuery ? searchData?.results.map((r) => r.memory) : data?.memories;
  const hasActiveFilters = searchQuery || selectedType || selectedAgent;

  const clearFilters = () => {
    setSelectedType('');
    setSelectedAgent('');
    setSearchQuery('');
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'outcome':
        return 'bg-green-100 text-green-800';
      case 'learning':
        return 'bg-blue-100 text-blue-800';
      case 'preference':
        return 'bg-purple-100 text-purple-800';
      case 'decision':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Memory Dashboard</h1>
          <button
            onClick={logout}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary rounded"
            aria-label="Logout"
          >
            Logout
          </button>
        </div>
        <ErrorState 
          message="We couldn't load your memories. Please check your connection and try again."
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  return (
    <div 
      className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
      id="main-content"
      role="main"
      aria-label="Memory Dashboard"
    >
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Memory Dashboard</h1>
        <button
          onClick={logout}
          className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary rounded transition-colors"
          aria-label="Logout"
        >
          Logout
        </button>
      </div>

      {/* Search and Filters */}
      <div className="mb-6 space-y-4">
        <form onSubmit={handleSearch} className="flex gap-2">
          <label htmlFor="search-input" className="sr-only">
            Search memories
          </label>
          <input
            id="search-input"
            type="text"
            placeholder="Search memories..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amc-primary focus:border-transparent"
            aria-label="Search memories"
          />
          <button
            type="submit"
            className="px-6 py-2 bg-amc-primary text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary transition-colors"
            aria-label="Submit search"
          >
            Search
          </button>
        </form>

        <div className="flex flex-wrap gap-2">
          <label htmlFor="type-filter" className="sr-only">
            Filter by memory type
          </label>
          <select
            id="type-filter"
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amc-primary focus:outline-none"
            aria-label="Filter by type"
          >
            <option value="">All Types</option>
            <option value="outcome">Outcome</option>
            <option value="learning">Learning</option>
            <option value="preference">Preference</option>
            <option value="decision">Decision</option>
          </select>

          <label htmlFor="agent-filter" className="sr-only">
            Filter by agent ID
          </label>
          <input
            id="agent-filter"
            type="text"
            placeholder="Filter by agent ID"
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amc-primary focus:outline-none"
            aria-label="Filter by agent ID"
          />

          <button
            onClick={clearFilters}
            className="px-4 py-2 text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary rounded transition-colors"
            aria-label="Clear all filters"
          >
            Clear filters
          </button>
        </div>
      </div>

      {/* Memory List */}
      {memories && memories.length > 0 ? (
        <div className="space-y-4" role="list" aria-label="Memory list">
          {memories.map((memory) => (
            <article
              key={memory.id}
              className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              role="listitem"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded ${getTypeColor(
                      memory.type
                    )}`}
                    aria-label={`Memory type: ${memory.type}`}
                  >
                    {memory.type}
                  </span>
                  <span className="text-xs text-gray-500" aria-label={`Agent ID: ${memory.agent_id}`}>
                    {memory.agent_id}
                  </span>
                </div>
                <time 
                  className="text-xs text-gray-400"
                  dateTime={memory.created_at}
                  aria-label={`Created at ${new Date(memory.created_at).toLocaleString()}`}
                >
                  {new Date(memory.created_at).toLocaleString()}
                </time>
              </div>
              <p className="text-gray-700 mb-2">{memory.content}</p>
              {memory.tags && memory.tags.length > 0 && (
                <div className="flex flex-wrap gap-1" role="list" aria-label="Tags">
                  {memory.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded"
                      role="listitem"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}
            </article>
          ))}
        </div>
      ) : (
        <EmptyState 
          hasFilters={!!hasActiveFilters}
          onClearFilters={clearFilters}
        />
      )}
    </div>
  );
}
