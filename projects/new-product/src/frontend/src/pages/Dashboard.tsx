import { useQuery } from '@tanstack/react-query'
import { fetchAnalytics } from '../api/mockApi'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { format, parseISO } from 'date-fns'

export default function Dashboard() {
  const { data: analytics, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: fetchAnalytics,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  if (!analytics) {
    return <div className="text-dark-400">Failed to load analytics</div>
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-dark-400 mt-1">Overview of your Agent Memory Cloud</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Memories"
          value={analytics.total_memories.toLocaleString()}
          icon="📝"
          iconLabel="Notes"
          trend={`+${analytics.growth_rate}%`}
          trendLabel="this week"
        />
        <StatCard
          title="Active Agents"
          value={analytics.top_agents.length.toString()}
          icon="🤖"
          iconLabel="Robot"
          trend=""
          trendLabel=""
        />
        <StatCard
          title="Growth Rate"
          value={`${analytics.growth_rate}%`}
          icon="📈"
          iconLabel="Chart trending up"
          trend="+2.3%"
          trendLabel="vs last week"
        />
        <StatCard
          title="Avg Importance"
          value={`${Math.round(analytics.top_agents.reduce((sum, a) => sum + a.avg_importance, 0) / analytics.top_agents.length)}%`}
          icon="⭐"
          iconLabel="Star"
          trend=""
          trendLabel=""
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Memory Growth Chart */}
        <div className="bg-dark-900 rounded-xl p-6 border border-dark-800">
          <h2 className="text-lg font-semibold text-white mb-4">Memory Growth (Last 7 Days)</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={analytics.memories_by_day}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis 
                  dataKey="date" 
                  stroke="#64748b"
                  tickFormatter={(value) => format(parseISO(value), 'MMM dd')}
                />
                <YAxis stroke="#64748b" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1e293b', 
                    border: '1px solid #334155',
                    borderRadius: '8px',
                    color: '#f1f5f9'
                  }}
                  labelFormatter={(value) => format(parseISO(value as string), 'MMMM dd, yyyy')}
                />
                <Area 
                  type="monotone" 
                  dataKey="count" 
                  stroke="#0ea5e9" 
                  fillOpacity={1} 
                  fill="url(#colorCount)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Agents Chart */}
        <div className="bg-dark-900 rounded-xl p-6 border border-dark-800">
          <h2 className="text-lg font-semibold text-white mb-4">Top Agents by Memory Count</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analytics.top_agents} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis type="number" stroke="#64748b" />
                <YAxis dataKey="agent_id" type="category" stroke="#64748b" width={120} tick={{ fontSize: 12 }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1e293b', 
                    border: '1px solid #334155',
                    borderRadius: '8px',
                    color: '#f1f5f9'
                  }}
                />
                <Bar dataKey="memory_count" fill="#0ea5e9" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Top Agents Table */}
      <div className="bg-dark-900 rounded-xl p-6 border border-dark-800">
        <h2 className="text-lg font-semibold text-white mb-4">Agent Leaderboard</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left text-dark-400 border-b border-dark-800">
                <th className="pb-3 font-medium">Agent</th>
                <th className="pb-3 font-medium">Memories</th>
                <th className="pb-3 font-medium">Avg Importance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-800">
              {analytics.top_agents.map((agent, index) => (
                <tr key={agent.agent_id} className="text-dark-200">
                  <td className="py-3 flex items-center gap-3">
                    <span className="text-lg" role="img" aria-label={index === 0 ? 'Gold medal, first place' : index === 1 ? 'Silver medal, second place' : index === 2 ? 'Bronze medal, third place' : 'Agent'}>
                      {index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🤖'}
                    </span>
                    <span className="font-medium">{agent.agent_id}</span>
                  </td>
                  <td className="py-3">{agent.memory_count}</td>
                  <td className="py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-dark-800 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-primary-500 rounded-full"
                          style={{ width: `${agent.avg_importance}%` }}
                          role="progressbar"
                          aria-valuenow={agent.avg_importance}
                          aria-valuemin={0}
                          aria-valuemax={100}
                          aria-label={`${agent.avg_importance}% average importance`}
                        />
                      </div>
                      <span className="text-sm text-dark-400">{Math.round(agent.avg_importance)}%</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, icon, iconLabel, trend, trendLabel }: {
  title: string
  value: string
  icon: string
  iconLabel: string
  trend: string
  trendLabel: string
}) {
  return (
    <div className="bg-dark-900 rounded-xl p-6 border border-dark-800">
      <div className="flex items-center justify-between mb-4">
        <span className="text-2xl" role="img" aria-label={iconLabel}>{icon}</span>
        {trend && (
          <span className="text-sm text-green-400 bg-green-400/10 px-2 py-1 rounded" aria-label={`Trend: ${trend}`}>
            {trend}
          </span>
        )}
      </div>
      <div className="text-3xl font-bold text-white mb-1">{value}</div>
      <div className="text-dark-400 text-sm">{title}</div>
      {trendLabel && (
        <div className="text-dark-500 text-xs mt-1">{trendLabel}</div>
      )}
    </div>
  )
}
