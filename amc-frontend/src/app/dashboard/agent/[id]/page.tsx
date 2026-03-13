'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useQuery } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { statsApi, api, AgentDashboardStats } from '@/lib/stats-api';
import AgentDashboardView from '@/components/dashboard/AgentDashboardView';
import LoadingState from '@/components/ui/LoadingState';

interface PageProps {
  params: {
    id: string;
  };
}

export default function AgentDashboardPage({ params }: PageProps) {
  const { apiKey, logout, isAuthenticated } = useAuth();
  const router = useRouter();
  const agentId = params.id;

  // Redirect to home if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/');
    }
  }, [isAuthenticated, router]);

  // Fetch per-agent stats with 30s polling
  const {
    data: agentStats,
    isLoading: statsLoading,
    error: statsError,
  } = useQuery({
    queryKey: ['agent-stats', agentId],
    queryFn: async () => {
      return await statsApi.getAgentDashboardStats(apiKey!, agentId);
    },
    enabled: !!apiKey && !!agentId,
    refetchInterval: 30000, // Poll every 30 seconds
    refetchIntervalInBackground: true,
  });

  // Fetch recent memories for this agent with 30s polling
  const {
    data: recentMemories,
    isLoading: memoriesLoading,
  } = useQuery({
    queryKey: ['agent-memories', agentId],
    queryFn: async () => {
      const response = await api.getMemories(apiKey!, {
        agent_id: agentId,
        limit: 10,
      });
      return response.memories;
    },
    enabled: !!apiKey && !!agentId,
    refetchInterval: 30000,
    refetchIntervalInBackground: true,
  });

  if (!isAuthenticated) {
    return null;
  }

  if (statsLoading && !agentStats) {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoadingState />
      </div>
    );
  }

  return (
    <AgentDashboardView
      agentId={agentId}
      stats={agentStats || null}
      recentMemories={recentMemories || []}
      isLoading={statsLoading || memoriesLoading}
      error={statsError ? 'Failed to load agent statistics' : null}
      onLogout={logout}
    />
  );
}
