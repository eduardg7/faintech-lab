'use client';

import { ProjectBreakdown } from '@/lib/stats-api';

interface ProjectMemoryBreakdownProps {
  projects: ProjectBreakdown[];
  isLoading: boolean;
}

export default function ProjectMemoryBreakdown({ projects, isLoading }: ProjectMemoryBreakdownProps) {
  if (isLoading) {
    return (
      <div
        className="bg-white border border-gray-200 rounded-lg p-6"
        role="status"
        aria-live="polite"
        aria-label="Loading project breakdown"
      >
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="space-y-4">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
        <span className="sr-only">Loading project memory breakdown...</span>
      </div>
    );
  }

  if (!projects || projects.length === 0) {
    return (
      <div
        className="bg-white border border-gray-200 rounded-lg p-6"
        role="alert"
        aria-live="polite"
      >
        <p className="text-gray-500">No project data available.</p>
      </div>
    );
  }

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

  const getGrowthColor = (rate: number) => {
    if (rate >= 15) return 'text-green-600';
    if (rate >= 5) return 'text-blue-600';
    if (rate >= 0) return 'text-gray-600';
    return 'text-red-600';
  };

  const getGrowthIcon = (rate: number) => {
    if (rate >= 5) return '↑';
    if (rate >= 0) return '→';
    return '↓';
  };

  return (
    <div
      className="bg-white border border-gray-200 rounded-lg p-6"
      role="region"
      aria-labelledby="project-breakdown-title"
    >
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2
            id="project-breakdown-title"
            className="text-lg font-semibold text-gray-900"
          >
            Project Memory Breakdown
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Memory distribution across projects
          </p>
        </div>
      </div>

      {/* Type Legend */}
      <div
        className="flex flex-wrap gap-4 mb-4 pb-4 border-b border-gray-100"
        role="list"
        aria-label="Memory type legend"
      >
        {Object.entries(typeLabels).map(([type, label]) => (
          <div
            key={type}
            className="flex items-center gap-2"
            role="listitem"
          >
            <div
              className={`w-3 h-3 rounded ${typeColors[type]}`}
              aria-hidden="true"
            />
            <span className="text-xs text-gray-600">{label}</span>
          </div>
        ))}
      </div>

      {/* Project Cards */}
      <div
        className="space-y-4"
        role="list"
        aria-label="Project memory breakdown"
      >
        {projects.map((project) => {
          const total = project.total_memories;
          const maxType = Math.max(...Object.values(project.by_type));

          return (
            <article
              key={project.project_id}
              className="border border-gray-100 rounded-lg p-4 hover:border-gray-200 transition-colors"
              role="listitem"
              aria-labelledby={`project-${project.project_id}-title`}
            >
              {/* Project Header */}
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3
                    id={`project-${project.project_id}-title`}
                    className="font-medium text-gray-900"
                  >
                    {project.project_name}
                  </h3>
                  <p className="text-xs text-gray-500">
                    {project.project_id}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-gray-900">
                    {total.toLocaleString()}
                  </p>
                  <p
                    className={`text-xs font-medium ${getGrowthColor(project.growth_rate)}`}
                    aria-label={`Growth rate: ${project.growth_rate}% per week`}
                  >
                    {getGrowthIcon(project.growth_rate)} {project.growth_rate}%/wk
                  </p>
                </div>
              </div>

              {/* Type Distribution */}
              <div
                className="mb-3"
                role="img"
                aria-label={`Memory distribution for ${project.project_name}: ${project.by_type.outcome} outcomes, ${project.by_type.learning} learnings, ${project.by_type.preference} preferences, ${project.by_type.decision} decisions`}
              >
                <div className="flex h-2 rounded-full overflow-hidden bg-gray-100">
                  {Object.entries(project.by_type).map(([type, count]) => (
                    <div
                      key={type}
                      className={`${typeColors[type]} transition-all duration-300`}
                      style={{
                        width: `${(count / total) * 100}%`,
                      }}
                      title={`${typeLabels[type]}: ${count}`}
                    />
                  ))}
                </div>
                <div className="flex justify-between mt-1">
                  {Object.entries(project.by_type).map(([type, count]) => (
                    <span
                      key={type}
                      className="text-xs text-gray-500"
                    >
                      {count}
                    </span>
                  ))}
                </div>
              </div>

              {/* Top Agents */}
              <div>
                <p className="text-xs text-gray-500 mb-2">Top Contributors</p>
                <div
                  className="flex flex-wrap gap-2"
                  role="list"
                  aria-label="Top contributing agents"
                >
                  {project.top_agents.slice(0, 3).map((agent) => (
                    <div
                      key={agent.agent_id}
                      className="flex items-center gap-1 bg-gray-50 px-2 py-1 rounded text-xs"
                      role="listitem"
                    >
                      <span className="text-gray-700">
                        {agent.agent_id.replace('faintech-', '')}
                      </span>
                      <span className="text-gray-400">•</span>
                      <span className="font-medium text-gray-900">
                        {agent.count}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </div>
  );
}
