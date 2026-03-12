'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { 
  statsApi, 
  mockMemoryStats, 
  mockAgentActivity, 
  mockProjectBreakdown 
} from '@/lib/stats-api';
import MemoryStatsChart from '@/components/dashboard/MemoryStatsChart';
import AgentActivityTimeline from '@/components/dashboard/AgentActivityTimeline';
import ProjectMemoryBreakdown from '@/components/dashboard/ProjectMemoryBreakdown';
import { useEffect, useState } from 'react';

export default function DashboardPage() {
  const { apiKey, logout, isAuthenticated } = useAuth();
  const [useMockData, setUseMockData] = useState(false);

  // Redirect to home if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      window.location.href = '/';
    }
  }, [isAuthenticated]);

  // Fetch memory stats with 30s polling
  const { 
    data: memoryStats, 
    isLoading: statsLoading, 
    error: statsError 
  } = useQuery({
    queryKey: ['memory-stats'],
    queryFn: async () => {
      if (useMockData) return mockMemoryStats;
      try {
        return await statsApi.getMemoryStats(apiKey!);
      } catch (error) {
        console.warn('Stats API not available, using mock data');
        setUseMockData(true);
        return mockMemoryStats;
      }
    },
    enabled: !!apiKey,
    refetchInterval: 30000, // Poll every 30 seconds
    refetchIntervalInBackground: true,
  });

  // Fetch agent activity with 30s polling
  const { 
    data: agentActivity, 
    isLoading: activityLoading 
  } = useQuery({
    queryKey: ['agent-activity'],
    queryFn: async () => {
      if (useMockData) return mockAgentActivity;
      try {
        return await statsApi.getAgentActivity(apiKey!, { days: 7, limit: 10 });
      } catch (error) {
        console.warn('Agent activity API not available, using mock data');
        return mockAgentActivity;
      }
    },
    enabled: !!apiKey,
    refetchInterval: 30000,
    refetchIntervalInBackground: true,
  });

  // Fetch project breakdown with 30s polling
  const { 
    data: projectBreakdown, 
    isLoading: projectsLoading 
  } = useQuery({
    queryKey: ['project-breakdown'],
    queryFn: async () => {
      if (useMockData) return mockProjectBreakdown;
      try {
        return await statsApi.getProjectBreakdown(apiKey!, { limit: 10 });
      } catch (error) {
        console.warn('Project breakdown API not available, using mock data');
        return mockProjectBreakdown;
      }
    },
    enabled: !!apiKey,
    refetchInterval: 30000,
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
      aria-label="Agent Memory Dashboard"
    >
      {/* Header */}
      <header 
        className="bg-white border-b border-gray-200"
        role="banner"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 
                className="text-2xl font-bold text-gray-900"
                id="dashboard-title"
              >
                Agent Dashboard
              </h1>
              <p className="text-sm text-gray-500 mt-1">
                Memory statistics and activity overview
              </p>
            </div>
            <div className="flex items-center gap-4">
              <a
                href="/"
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary rounded transition-colors"
                aria-label="View memory list"
              >
                Memory List
              </a>
              <button
                onClick={logout}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary rounded transition-colors"
                aria-label="Logout"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main 
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
        aria-labelledby="dashboard-title"
      >
        {/* Live Update Indicator */}
        <div 
          className="flex items-center gap-2 mb-6"
          role="status"
          aria-live="polite"
        >
          <div 
            className="w-2 h-2 bg-green-500 rounded-full animate-pulse"
            aria-hidden="true"
          />
          <span className="text-xs text-gray-500">
            Live updates every 30 seconds
          </span>
          {useMockData && (
            <span className="text-xs text-orange-500 ml-2">
              (Using demo data)
            </span>
          )}
        </div>

        {/* Stats Grid */}
        <div 
          className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6"
          role="list"
          aria-label="Dashboard statistics"
        >
          <div role="listitem">
            <MemoryStatsChart 
              stats={memoryStats || null} 
              isLoading={statsLoading} 
            />
          </div>
          <div role="listitem">
            <AgentActivityTimeline 
              agents={agentActivity?.agents || []}
              isLoading={activityLoading}
            />
          </div>
        </div>

        {/* Project Breakdown */}
        <div role="listitem">
          <ProjectMemoryBreakdown 
            projects={projectBreakdown?.projects || []}
            isLoading={projectsLoading}
          />
        </div>
      </main>

      {/* Footer */}
      <footer 
        className="bg-white border-t border-gray-200 mt-8"
        role="contentinfo"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-xs text-gray-500 text-center">
            Agent Memory Cloud Dashboard • Auto-refresh enabled
          </p>
        </div>
      </footer>
    </div>
  );
}
