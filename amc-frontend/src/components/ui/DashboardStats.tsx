'use client';

interface DashboardStatsProps {
  memoryCount: number;
  agentCount: number;
  lastActivity: string | null;
  isLoading?: boolean;
}

export default function DashboardStats({ 
  memoryCount, 
  agentCount, 
  lastActivity,
  isLoading = false 
}: DashboardStatsProps) {
  if (isLoading) {
    return (
      <div 
        className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6"
        role="status"
        aria-label="Loading dashboard statistics"
      >
        {[1, 2, 3].map((i) => (
          <div 
            key={i}
            className="bg-white border border-gray-200 rounded-lg p-4"
          >
            <div className="h-4 w-20 bg-gray-200 rounded animate-pulse mb-2"></div>
            <div className="h-8 w-16 bg-gray-200 rounded animate-pulse"></div>
          </div>
        ))}
        <span className="sr-only">Loading statistics...</span>
      </div>
    );
  }

  const formatLastActivity = (timestamp: string | null) => {
    if (!timestamp) return 'No activity yet';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins === 1 ? '' : 's'} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`;
    return date.toLocaleDateString();
  };

  return (
    <div 
      className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6"
      role="region"
      aria-label="Dashboard statistics"
    >
      {/* Memory Count */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500 mb-1">
              Total Memories
            </p>
            <p 
              className="text-2xl font-bold text-gray-900"
              aria-label={`${memoryCount} total memories`}
            >
              {memoryCount.toLocaleString()}
            </p>
          </div>
          <div 
            className="p-3 bg-blue-50 rounded-lg"
            aria-hidden="true"
          >
            <svg 
              className="w-6 h-6 text-blue-600" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Agent Count */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500 mb-1">
              Active Agents
            </p>
            <p 
              className="text-2xl font-bold text-gray-900"
              aria-label={`${agentCount} active agents`}
            >
              {agentCount.toLocaleString()}
            </p>
          </div>
          <div 
            className="p-3 bg-green-50 rounded-lg"
            aria-hidden="true"
          >
            <svg 
              className="w-6 h-6 text-green-600" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" 
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Last Activity */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500 mb-1">
              Last Activity
            </p>
            <p 
              className="text-lg font-semibold text-gray-900"
              aria-label={`Last activity: ${formatLastActivity(lastActivity)}`}
            >
              {formatLastActivity(lastActivity)}
            </p>
          </div>
          <div 
            className="p-3 bg-purple-50 rounded-lg"
            aria-hidden="true"
          >
            <svg 
              className="w-6 h-6 text-purple-600" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" 
              />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
