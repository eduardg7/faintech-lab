'use client';

import { HealthScoreBatchResponse } from '@/lib/stats-api';

interface HealthScoreDashboardProps {
  data: HealthScoreBatchResponse | null;
  isLoading: boolean;
}

const tierColors: Record<string, { bg: string; text: string; border: string }> = {
  Champion: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-300' },
  Healthy: { bg: 'bg-blue-100', text: 'text-blue-800', border: 'border-blue-300' },
  'At-Risk': { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-300' },
  Critical: { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-300' },
};

const scoreColor = (score: number): string => {
  if (score >= 8) return 'text-green-600';
  if (score >= 6) return 'text-blue-600';
  if (score >= 4) return 'text-yellow-600';
  return 'text-red-600';
};

export default function HealthScoreDashboard({ data, isLoading }: HealthScoreDashboardProps) {
  if (isLoading) {
    return (
      <div
        className="bg-white rounded-lg shadow p-6 animate-pulse"
        role="status"
        aria-label="Loading health scores"
      >
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4" />
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-16 bg-gray-200 rounded" />
          ))}
        </div>
      </div>
    );
  }

  if (!data || data.total_users === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Beta User Health Scores</h3>
        <p className="text-gray-500 text-sm">No user health data available</p>
      </div>
    );
  }

  const { tier_distribution } = data;

  return (
    <div
      className="bg-white rounded-lg shadow"
      role="region"
      aria-label="Beta User Health Monitoring"
    >
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Beta User Health Scores
            </h3>
            <p className="text-sm text-gray-500 mt-1">
              Monitor user engagement and identify at-risk accounts
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">
              {data.average_health_score.toFixed(1)}
            </div>
            <div className="text-xs text-gray-500">Avg Health Score</div>
          </div>
        </div>
      </div>

      {/* Tier Distribution Summary */}
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
        <div className="grid grid-cols-4 gap-4">
          {Object.entries(tier_distribution).map(([tier, count]) => {
            const colors = tierColors[tier];
            const percentage = data.total_users > 0
              ? Math.round((count / data.total_users) * 100)
              : 0;
            return (
              <div
                key={tier}
                className={`text-center p-3 rounded-lg ${colors.bg} ${colors.border} border`}
              >
                <div className={`text-2xl font-bold ${colors.text}`}>{count}</div>
                <div className={`text-xs ${colors.text}`}>{tier}</div>
                <div className="text-xs text-gray-500">{percentage}%</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* User List */}
      <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
        {data.results.map((user) => {
          const colors = tierColors[user.health_tier];
          return (
            <div
              key={user.user_id}
              className="px-6 py-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
                    <span className="text-sm font-medium text-gray-600">
                      {user.user_id.slice(0, 2).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">{user.user_id}</div>
                    <span
                      className={`inline-block px-2 py-0.5 text-xs rounded-full ${colors.bg} ${colors.text}`}
                    >
                      {user.health_tier}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-xl font-bold ${scoreColor(user.health_score)}`}>
                    {user.health_score.toFixed(1)}
                  </div>
                  <div className="text-xs text-gray-500">Health Score</div>
                </div>
              </div>

              {/* Component Breakdown */}
              <div className="mt-3 grid grid-cols-4 gap-2">
                {Object.entries(user.components).map(([component, value]) => (
                  <div key={component} className="text-center">
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${
                          value >= 8 ? 'bg-green-500' :
                          value >= 6 ? 'bg-blue-500' :
                          value >= 4 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${(value / 10) * 100}%` }}
                      />
                    </div>
                    <div className="text-xs text-gray-500 mt-1 capitalize">
                      {component.replace('_', ' ')}
                    </div>
                    <div className={`text-xs font-medium ${scoreColor(value)}`}>
                      {value.toFixed(1)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer */}
      <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 text-center">
        <span className="text-xs text-gray-500">
          {data.total_users} users • Formula: Engagement(40%) + Features(30%) + Feedback(20%) + Consistency(10%)
        </span>
      </div>
    </div>
  );
}
