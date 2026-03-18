'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { healthScoreApi, mockHealthScoreData } from '@/lib/stats-api';
import HealthScoreDashboard from '@/components/dashboard/HealthScoreDashboard';
import { useEffect, useState } from 'react';

export default function HealthMonitoringPage() {
  const { isAuthenticated } = useAuth();
  const [useMockData, setUseMockData] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      window.location.href = '/';
    }
  }, [isAuthenticated]);

  // Mock beta user data for demo
  // In production, this would come from actual user analytics
  const mockBetaUsers = [
    {
      user_id: 'beta-user-001',
      sessions_per_week: 12,
      avg_session_duration_minutes: 45,
      messages_per_week: 85,
      agents_created: 5,
      agents_active_last_7d: 3,
      memories_stored: 42,
      projects_created: 2,
      search_queries_per_week: 25,
      in_app_rating: 4.5,
      nps_score: 9,
      daily_streak_days: 14,
      weekly_frequency: 0.95,
      device_consistency: 0.85,
    },
    {
      user_id: 'beta-user-002',
      sessions_per_week: 6,
      avg_session_duration_minutes: 25,
      messages_per_week: 30,
      agents_created: 2,
      agents_active_last_7d: 1,
      memories_stored: 15,
      projects_created: 1,
      search_queries_per_week: 8,
      in_app_rating: 4.0,
      nps_score: 7,
      daily_streak_days: 5,
      weekly_frequency: 0.7,
      device_consistency: 0.9,
    },
    {
      user_id: 'beta-user-003',
      sessions_per_week: 2,
      avg_session_duration_minutes: 10,
      messages_per_week: 5,
      agents_created: 1,
      agents_active_last_7d: 0,
      memories_stored: 3,
      projects_created: 0,
      search_queries_per_week: 2,
      in_app_rating: 3.0,
      nps_score: 5,
      daily_streak_days: 1,
      weekly_frequency: 0.3,
      device_consistency: 0.5,
    },
    {
      user_id: 'beta-user-004',
      sessions_per_week: 8,
      avg_session_duration_minutes: 35,
      messages_per_week: 50,
      agents_created: 3,
      agents_active_last_7d: 2,
      memories_stored: 28,
      projects_created: 1,
      search_queries_per_week: 15,
      in_app_rating: 4.2,
      nps_score: 8,
      daily_streak_days: 10,
      weekly_frequency: 0.85,
      device_consistency: 0.8,
    },
  ];

  const {
    data: healthData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ['health-scores'],
    queryFn: async () => {
      if (useMockData) return mockHealthScoreData;
      try {
        return await healthScoreApi.calculateBatchHealthScores(mockBetaUsers);
      } catch (err) {
        console.warn('Health Score API not available, using mock data');
        setUseMockData(true);
        return mockHealthScoreData;
      }
    },
    refetchInterval: 60000, // Refresh every minute
    refetchIntervalInBackground: true,
  });

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div
      className="min-h-screen bg-gray-50"
      role="main"
      id="main-content"
      aria-label="Health Monitoring Dashboard"
    >
      {/* Header */}
      <header className="bg-white border-b border-gray-200" role="banner">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Health Monitoring Dashboard
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                Beta user engagement and health score analytics
              </p>
            </div>
            <div className="flex items-center gap-4">
              <a
                href="/dashboard"
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary rounded transition-colors"
              >
                Agent Dashboard
              </a>
              <a
                href="/"
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary rounded transition-colors"
              >
                Memory List
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Live Update Indicator */}
        <div className="flex items-center gap-2 mb-6" role="status" aria-live="polite">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" aria-hidden="true" />
          <span className="text-xs text-gray-500">
            Live updates every 60 seconds
          </span>
          {useMockData && (
            <span className="text-xs text-orange-500 ml-2">
              (Using demo data)
            </span>
          )}
        </div>

        {/* Health Score Dashboard */}
        <div className="mb-6">
          <HealthScoreDashboard data={healthData || null} isLoading={isLoading} />
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">
              Scoring Formula
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Engagement</span>
                <span className="font-medium">40%</span>
              </div>
              <div className="flex justify-between">
                <span>Feature Adoption</span>
                <span className="font-medium">30%</span>
              </div>
              <div className="flex justify-between">
                <span>Feedback Sentiment</span>
                <span className="font-medium">20%</span>
              </div>
              <div className="flex justify-between">
                <span>Consistency</span>
                <span className="font-medium">10%</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">
              Tier Thresholds
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-green-500" />
                  Champion
                </span>
                <span className="font-medium">≥ 8.0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-blue-500" />
                  Healthy
                </span>
                <span className="font-medium">≥ 6.0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-yellow-500" />
                  At-Risk
                </span>
                <span className="font-medium">≥ 4.0</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-red-500" />
                  Critical
                </span>
                <span className="font-medium">&lt; 4.0</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">
              Actions
            </h3>
            <div className="space-y-2">
              <button
                className="w-full px-3 py-2 text-sm bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors"
                onClick={() => window.print()}
              >
                Export Report
              </button>
              <button
                className="w-full px-3 py-2 text-sm bg-yellow-50 text-yellow-700 rounded hover:bg-yellow-100 transition-colors"
                onClick={() => {
                  const atRisk = healthData?.results.filter(
                    (u) => u.health_tier === 'At-Risk' || u.health_tier === 'Critical'
                  );
                  alert(`${atRisk?.length || 0} users need attention`);
                }}
              >
                View At-Risk Users
              </button>
              <button
                className="w-full px-3 py-2 text-sm bg-green-50 text-green-700 rounded hover:bg-green-100 transition-colors"
                onClick={() => {
                  const champions = healthData?.results.filter(
                    (u) => u.health_tier === 'Champion'
                  );
                  alert(`${champions?.length || 0} champion users`);
                }}
              >
                View Champions
              </button>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-8" role="contentinfo">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-xs text-gray-500 text-center">
            Customer Health Monitoring Dashboard • Beta User Success Tracking
          </p>
        </div>
      </footer>
    </div>
  );
}
