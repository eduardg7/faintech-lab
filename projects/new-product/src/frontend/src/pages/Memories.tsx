import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { fetchMemories } from '../api/mockApi'
import { format } from 'date-fns'
import clsx from 'clsx'

const AGENTS = [
  'all',
  'faintech-ceo',
  'faintech-cto',
  'faintech-cpo',
  'faintech-frontend',
  'faintech-backend',
  'faintech-devops',
  'faintech-qa',
]

export default function Memories() {
  const [selectedAgent, setSelectedAgent] = useState('all')
  const [page, setPage] = useState(0)
  const limit = 20

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['memories', selectedAgent, page],
    queryFn: () => fetchMemories({
      agent_id: selectedAgent === 'all' ? undefined : selectedAgent,
      limit,
      offset: page * limit,
    }),
  })

  const handleAgentChange = (agent: string) => {
    setSelectedAgent(agent)
    setPage(0)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">Memories</h1>
          <p className="text-dark-400 mt-1">Browse and manage agent memories</p>
        </div>
        <button
          onClick={() => refetch()}
          className="flex items-center gap-2 px-4 py-2 bg-dark-800 text-dark-200 rounded-lg hover:bg-dark-700 transition-colors"
        >
          <span>🔄</span>
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="bg-dark-900 rounded-xl p-4 border border-dark-800">
        <div className="flex flex-wrap gap-2">
          {AGENTS.map(agent => (
            <button
              key={agent}
              onClick={() => handleAgentChange(agent)}
              className={clsx(
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                selectedAgent === agent
                  ? 'bg-primary-600 text-white'
                  : 'bg-dark-800 text-dark-300 hover:bg-dark-700 hover:text-white'
              )}
            >
              {agent === 'all' ? 'All Agents' : agent}
            </button>
          ))}
        </div>
      </div>

      {/* Memory List */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
        </div>
      ) : data ? (
        <div className="space-y-4">
          {/* Results count */}
          <div className="text-dark-400 text-sm">
            Showing {data.memories.length} of {data.total} memories
          </div>

          {/* Memory cards */}
          <div className="space-y-3">
            {data.memories.map(memory => (
              <MemoryCard key={memory.id} memory={memory} />
            ))}
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between pt-4">
            <button
              onClick={() => setPage(p => Math.max(0, p - 1))}
              disabled={page === 0}
              className="px-4 py-2 bg-dark-800 text-dark-200 rounded-lg hover:bg-dark-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="text-dark-400">
              Page {page + 1} of {Math.ceil(data.total / limit)}
            </span>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={(page + 1) * limit >= data.total}
              className="px-4 py-2 bg-dark-800 text-dark-200 rounded-lg hover:bg-dark-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      ) : (
        <div className="text-dark-400">Failed to load memories</div>
      )}
    </div>
  )
}

function MemoryCard({ memory }: { memory: import('../types').Memory }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="bg-dark-900 rounded-xl p-5 border border-dark-800 hover:border-dark-700 transition-colors">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {/* Agent and date */}
          <div className="flex items-center gap-3 mb-2">
            <span className="text-sm font-medium text-primary-400 bg-primary-400/10 px-2 py-1 rounded">
              {memory.agent_id}
            </span>
            <span className="text-xs text-dark-500">
              {format(new Date(memory.created_at), 'MMM dd, yyyy HH:mm')}
            </span>
          </div>

          {/* Content */}
          <p className={clsx(
            'text-dark-200 leading-relaxed',
            !expanded && 'line-clamp-2'
          )}>
            {memory.content}
          </p>

          {/* Expand button */}
          {memory.content.length > 150 && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="text-primary-400 text-sm mt-2 hover:text-primary-300"
            >
              {expanded ? 'Show less' : 'Show more'}
            </button>
          )}

          {/* Metadata */}
          <div className="flex items-center gap-4 mt-3 text-xs text-dark-500">
            <span>Importance: {Math.round(memory.importance_score)}%</span>
            <span>Accessed: {memory.access_count}x</span>
            {memory.metadata.tags && (
              <div className="flex gap-1">
                {(memory.metadata.tags as string[]).map(tag => (
                  <span key={tag} className="bg-dark-800 px-2 py-0.5 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
