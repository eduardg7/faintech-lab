'use client';

import { AgentDashboardStats, Memory } from '@/lib/stats-api';

interface AgentDashboardViewProps {
  agentId: string;
  stats: AgentDashboardStats | null;
  recentMemories: Memory[];
  isLoading: boolean;
  error: string | null;
  onLogout: () => void;
}

export default function AgentDashboardView({
  agentId,
  stats,
  recentMemories,
  isLoading,
  error,
  onLogout,
}: AgentDashboardViewProps) {
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

  const formatTimestamp = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 60) {
      return `${diffMins}m ago`;
    } else if (diffHours < 24) {
      return `${diffHours}h ago`;
    } else if (diffDays < 7) {
      return `${diffDays}d ago`;
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div
            className="bg-red-50 border border-red-200 rounded-lg p-6 text-center"
            role="alert"
            aria-live="assertive"
          >
            <p className="text-red-700 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className="min-h-screen bg-gray-50"
      role="main"
      aria-label={`Agent Dashboard for ${agentId}`}
    >
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-gray-900">
                Agent Dashboard
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                <span className="sr-only">Agent ID: </span>
                <code className="bg-gray-100 px-2 py-0.5 rounded text-xs">
                  {agentId}
                </code>
              </p>
            </div>
            <div className="flex items-center gap-3">
              <span
                className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded"
                aria-label="Auto-refreshes every 30 seconds"
              >
                Auto-refresh: 30s
              </span>
              <button
                onClick={onLogout}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded transition-colors"
                aria-label="Logout"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {/* Stats Cards */}
        <section
          aria-labelledby="stats-heading"
          className="mb-8"
        >
          <h2 id="stats-heading" className="sr-only">Memory Statistics</h2>

          {isLoading && !stats ? (
            <div
              className="grid grid-cols-2 lg:grid-cols-4 gap-4"
              role="status"
              aria-live="polite"
              aria-label="Loading statistics"
            >
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6"
                >
                  <div className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-2/3 mb-3"></div>
                    <div className="h-8 bg-gray-200 rounded w-1/2"></div>
                  </div>
                </div>
              ))}
              <span className="sr-only">Loading statistics...</span>
            </div>
          ) : stats ? (
            <div
              className="grid grid-cols-2 lg:grid-cols-4 gap-4"
              role="list"
              aria-label="Memory statistics overview"
            >
              {/* Total Memories */}
              <div
                className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6 hover:shadow-sm transition-shadow"
                role="listitem"
              >
                <p className="text-xs sm:text-sm font-medium text-gray-500 uppercase tracking-wide">
                  Total Memories
                </p>
                <p
                  className="mt-2 text-2xl sm:text-3xl font-bold text-gray-900"
                  aria-label={`${stats.total_memories} total memories`}
                >
                  {stats.total_memories.toLocaleString()}
                </p>
              </div>

              {/* Memories This Week */}
              <div
                className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6 hover:shadow-sm transition-shadow"
                role="listitem"
              >
                <p className="text-xs sm:text-sm font-medium text-gray-500 uppercase tracking-wide">
                  This Week
                </p>
                <p
                  className="mt-2 text-2xl sm:text-3xl font-bold text-blue-600"
                  aria-label={`${stats.memories_this_week} memories created this week`}
                >
                  {stats.memories_this_week.toLocaleString()}
                </p>
              </div>

              {/* Pattern Count */}
              <div
                className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6 hover:shadow-sm transition-shadow"
                role="listitem"
              >
                <p className="text-xs sm:text-sm font-medium text-gray-500 uppercase tracking-wide">
                  Patterns
                </p>
                <p
                  className="mt-2 text-2xl sm:text-3xl font-bold text-purple-600"
                  aria-label={`${stats.pattern_count} unique tag patterns detected`}
                >
                  {stats.pattern_count.toLocaleString()}
                </p>
              </div>

              {/* Storage Used */}
              <div
                className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6 hover:shadow-sm transition-shadow"
                role="listitem"
              >
                <p className="text-xs sm:text-sm font-medium text-gray-500 uppercase tracking-wide">
                  Storage
                </p>
                <p
                  className="mt-2 text-2xl sm:text-3xl font-bold text-gray-900"
                  aria-label={`${stats.storage_used_mb} megabytes of storage used`}
                >
                  {stats.storage_used_mb}<span className="text-base sm:text-lg font-normal text-gray-500 ml-1">MB</span>
                </p>
              </div>
            </div>
          ) : null}
        </section>

        {/* Two Column Layout for Desktop */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Memory Type Distribution */}
          {stats && (
            <section
              aria-labelledby="distribution-heading"
              className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6"
            >
              <h2
                id="distribution-heading"
                className="text-base sm:text-lg font-semibold text-gray-900 mb-4"
              >
                Memory Distribution
              </h2>

              <div
                className="space-y-4"
                role="list"
                aria-label="Memory type distribution"
              >
                {Object.entries(stats.by_type).map(([type, count]) => {
                  const maxCount = Math.max(...Object.values(stats.by_type), 1);
                  const percentage = (count / maxCount) * 100;

                  return (
                    <div
                      key={type}
                      role="listitem"
                    >
                      <div className="flex justify-between items-center mb-1">
                        <span
                          className={`px-2 py-0.5 text-xs font-medium rounded capitalize ${getTypeColor(type)}`}
                        >
                          {type}
                        </span>
                        <span className="text-sm font-medium text-gray-900">
                          {count.toLocaleString()}
                        </span>
                      </div>
                      <div
                        className="w-full bg-gray-200 rounded-full h-2"
                        role="progressbar"
                        aria-valuenow={count}
                        aria-valuemin={0}
                        aria-valuemax={maxCount}
                        aria-label={`${type}: ${count} out of ${maxCount}`}
                      >
                        <div
                          className={`h-2 rounded-full transition-all duration-300 ${
                            type === 'outcome' ? 'bg-green-500' :
                            type === 'learning' ? 'bg-blue-500' :
                            type === 'preference' ? 'bg-purple-500' :
                            'bg-orange-500'
                          }`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>
          )}

          {/* Recent Memories */}
          <section
            aria-labelledby="recent-heading"
            className="bg-white border border-gray-200 rounded-lg p-4 sm:p-6"
          >
            <h2
              id="recent-heading"
              className="text-base sm:text-lg font-semibold text-gray-900 mb-4"
            >
              Recent Memories
            </h2>

            {isLoading && recentMemories.length === 0 ? (
              <div
                className="space-y-3"
                role="status"
                aria-live="polite"
                aria-label="Loading recent memories"
              >
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="animate-pulse"
                  >
                    <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded w-full"></div>
                  </div>
                ))}
                <span className="sr-only">Loading recent memories...</span>
              </div>
            ) : recentMemories.length > 0 ? (
              <div
                className="space-y-3 max-h-96 overflow-y-auto"
                role="list"
                aria-label="Recent memories list"
              >
                {recentMemories.slice(0, 10).map((memory) => (
                  <article
                    key={memory.id}
                    className="border-b border-gray-100 pb-3 last:border-0 last:pb-0"
                    role="listitem"
                  >
                    <div className="flex items-start justify-between gap-2 mb-1">
                      <span
                        className={`px-2 py-0.5 text-xs font-medium rounded ${getTypeColor(memory.type)}`}
                        aria-label={`Memory type: ${memory.type}`}
                      >
                        {memory.type}
                      </span>
                      <time
                        className="text-xs text-gray-400 shrink-0"
                        dateTime={memory.created_at}
                        title={new Date(memory.created_at).toLocaleString()}
                      >
                        {formatTimestamp(memory.created_at)}
                      </time>
                    </div>
                    <p className="text-sm text-gray-700 line-clamp-2">
                      {memory.content}
                    </p>
                    {memory.tags && memory.tags.length > 0 && (
                      <div
                        className="flex flex-wrap gap-1 mt-2"
                        role="list"
                        aria-label="Tags"
                      >
                        {memory.tags.slice(0, 3).map((tag) => (
                          <span
                            key={tag}
                            className="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                            role="listitem"
                          >
                            #{tag}
                          </span>
                        ))}
                        {memory.tags.length > 3 && (
                          <span className="text-xs text-gray-400">
                            +{memory.tags.length - 3} more
                          </span>
                        )}
                      </div>
                    )}
                  </article>
                ))}
              </div>
            ) : (
              <p
                className="text-sm text-gray-500 text-center py-8"
                role="status"
              >
                No recent memories for this agent.
              </p>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
