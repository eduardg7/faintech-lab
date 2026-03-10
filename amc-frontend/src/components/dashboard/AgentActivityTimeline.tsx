'use client';

import { AgentActivity } from '@/lib/stats-api';

interface AgentActivityTimelineProps {
  agents: AgentActivity[];
  isLoading: boolean;
}

export default function AgentActivityTimeline({ agents, isLoading }: AgentActivityTimelineProps) {
  if (isLoading) {
    return (
      <div 
        className="bg-white border border-gray-200 rounded-lg p-6"
        role="status"
        aria-live="polite"
        aria-label="Loading agent activity"
      >
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-48 bg-gray-200 rounded"></div>
        </div>
        <span className="sr-only">Loading agent activity timeline...</span>
      </div>
    );
  }

  if (!agents || agents.length === 0) {
    return (
      <div 
        className="bg-white border border-gray-200 rounded-lg p-6"
        role="alert"
        aria-live="polite"
      >
        <p className="text-gray-500">No agent activity data available.</p>
      </div>
    );
  }

  // Find max count for scaling
  const maxCount = Math.max(
    ...agents.flatMap((agent) => agent.activity_timeline.map((t) => t.count))
  );

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const formatTimeAgo = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    
    if (diffMins < 60) {
      return `${diffMins}m ago`;
    } else if (diffHours < 24) {
      return `${diffHours}h ago`;
    } else {
      const diffDays = Math.floor(diffHours / 24);
      return `${diffDays}d ago`;
    }
  };

  const getAgentColor = (index: number) => {
    const colors = [
      'bg-blue-500',
      'bg-green-500',
      'bg-purple-500',
      'bg-orange-500',
      'bg-pink-500',
      'bg-teal-500',
    ];
    return colors[index % colors.length];
  };

  return (
    <div 
      className="bg-white border border-gray-200 rounded-lg p-6"
      role="region"
      aria-labelledby="agent-activity-title"
    >
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 
            id="agent-activity-title"
            className="text-lg font-semibold text-gray-900"
          >
            Agent Activity Timeline
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Last 7 days activity
          </p>
        </div>
        <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
          Updates every 30s
        </span>
      </div>

      {/* Timeline Grid */}
      <div 
        className="mb-6"
        role="img"
        aria-label="Agent activity timeline visualization showing memory creation over the past 7 days"
      >
        {/* Date Labels */}
        <div className="flex justify-between text-xs text-gray-500 mb-2 pl-24">
          {agents[0]?.activity_timeline.map((t) => (
            <span key={t.date} className="w-8 text-center">
              {formatDate(t.date)}
            </span>
          ))}
        </div>

        {/* Agent Rows */}
        <div 
          className="space-y-3"
          role="list"
          aria-label="Agent activity breakdown"
        >
          {agents.map((agent, index) => (
            <div 
              key={agent.agent_id}
              className="flex items-center gap-3"
              role="listitem"
            >
              {/* Agent Label */}
              <div className="w-24 flex items-center gap-2">
                <div 
                  className={`w-2 h-2 rounded-full ${getAgentColor(index)}`}
                  aria-hidden="true"
                />
                <span className="text-xs text-gray-700 truncate">
                  {agent.agent_id.replace('faintech-', '')}
                </span>
              </div>

              {/* Timeline Bars */}
              <div 
                className="flex-1 flex items-end gap-1 h-8"
                role="img"
                aria-label={`${agent.agent_id}: ${agent.activity_timeline.map(t => `${t.count} on ${t.date}`).join(', ')}`}
              >
                {agent.activity_timeline.map((t, i) => (
                  <div 
                    key={`${t.date}-${i}`}
                    className="flex-1 flex items-end justify-center"
                  >
                    <div
                      className={`w-full max-w-[24px] ${getAgentColor(index)} rounded-t transition-all duration-300`}
                      style={{ 
                        height: `${Math.max(4, (t.count / maxCount) * 100)}%`,
                        minHeight: '4px'
                      }}
                      title={`${t.count} memories on ${formatDate(t.date)}`}
                    />
                  </div>
                ))}
              </div>

              {/* Total Count */}
              <span className="text-xs font-medium text-gray-600 w-12 text-right">
                {agent.memory_count}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div 
        className="flex flex-wrap gap-3 pt-4 border-t border-gray-100"
        role="list"
        aria-label="Agent legend"
      >
        {agents.map((agent, index) => (
          <div 
            key={agent.agent_id}
            className="flex items-center gap-2"
            role="listitem"
          >
            <div 
              className={`w-2 h-2 rounded-full ${getAgentColor(index)}`}
              aria-hidden="true"
            />
            <span className="text-xs text-gray-600">
              {agent.agent_id}
            </span>
            <span className="text-xs text-gray-400">
              • {formatTimeAgo(agent.last_activity)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
