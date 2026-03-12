'use client';

import { MemoryStats } from '@/lib/stats-api';

interface MemoryStatsChartProps {
  stats: MemoryStats | null;
  isLoading: boolean;
}

export default function MemoryStatsChart({ stats, isLoading }: MemoryStatsChartProps) {
  if (isLoading) {
    return (
      <div
        className="bg-white border border-gray-200 rounded-lg p-6"
        role="status"
        aria-live="polite"
        aria-label="Loading memory statistics"
      >
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-32 bg-gray-200 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
        <span className="sr-only">Loading memory statistics...</span>
      </div>
    );
  }

  if (!stats) {
    return (
      <div
        className="bg-white border border-gray-200 rounded-lg p-6"
        role="alert"
        aria-live="polite"
      >
        <p className="text-gray-500">Unable to load memory statistics.</p>
      </div>
    );
  }

  const maxCount = Math.max(...Object.values(stats.by_type));
  const typeColors: Record<string, string> = {
    outcome: 'bg-green-500',
    learning: 'bg-blue-500',
    preference: 'bg-purple-500',
    decision: 'bg-orange-500',
  };

  const typeLabels: Record<string, string> = {
    outcome: 'Outcomes',
    learning: 'Learnings',
    preference: 'Preferences',
    decision: 'Decisions',
  };

  return (
    <div
      className="bg-white border border-gray-200 rounded-lg p-6"
      role="region"
      aria-labelledby="memory-stats-title"
    >
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2
            id="memory-stats-title"
            className="text-lg font-semibold text-gray-900"
          >
            Memory Statistics
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Total: {stats.total_memories.toLocaleString()} memories
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Storage Used</p>
          <p className="text-lg font-semibold text-gray-900">
            {stats.storage_used_mb} MB
          </p>
        </div>
      </div>

      {/* Memory Type Distribution */}
      <div
        className="mb-6"
        role="img"
        aria-label={`Memory distribution: ${stats.by_type.outcome} outcomes, ${stats.by_type.learning} learnings, ${stats.by_type.preference} preferences, ${stats.by_type.decision} decisions`}
      >
        <h3 className="text-sm font-medium text-gray-700 mb-3">
          Distribution by Type
        </h3>
        <div className="space-y-3">
          {Object.entries(stats.by_type).map(([type, count]) => (
            <div key={type}>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-gray-600">
                  {typeLabels[type]}
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
                aria-label={`${typeLabels[type]}: ${count} out of ${maxCount}`}
              >
                <div
                  className={`${typeColors[type]} h-2 rounded-full transition-all duration-300`}
                  style={{ width: `${(count / maxCount) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Project Distribution */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">
          Top Projects
        </h3>
        <div
          className="space-y-2"
          role="list"
          aria-label="Memory distribution by project"
        >
          {stats.by_project.slice(0, 5).map((project) => (
            <div
              key={project.project_id}
              className="flex items-center justify-between"
              role="listitem"
            >
              <span className="text-sm text-gray-600 truncate">
                {project.project_id}
              </span>
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-900">
                  {project.count.toLocaleString()}
                </span>
                <span className="text-xs text-gray-400">
                  ({project.percentage}%)
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Average Importance */}
      <div className="mt-6 pt-4 border-t border-gray-100">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Avg Importance</span>
          <div
            className="flex items-center gap-2"
            role="meter"
            aria-valuenow={stats.avg_importance * 100}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`Average importance: ${Math.round(stats.avg_importance * 100)}%`}
          >
            <div className="w-24 bg-gray-200 rounded-full h-1.5">
              <div
                className="bg-amc-primary h-1.5 rounded-full"
                style={{ width: `${stats.avg_importance * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900">
              {Math.round(stats.avg_importance * 100)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
