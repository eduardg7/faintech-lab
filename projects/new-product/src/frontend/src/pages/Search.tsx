import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { searchMemories } from '../api/mockApi'
import clsx from 'clsx'

export default function Search() {
  const [query, setQuery] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedAgent, setSelectedAgent] = useState('all')

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['search', searchTerm, selectedAgent],
    queryFn: () => searchMemories(searchTerm, {
      agent_id: selectedAgent === 'all' ? undefined : selectedAgent,
      limit: 20,
    }),
    enabled: searchTerm.length > 0,
  })

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      setSearchTerm(query.trim())
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Search</h1>
        <p className="text-dark-400 mt-1">Search through all agent memories</p>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="space-y-4">
        <div className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search memories..."
              className="w-full px-4 py-3 bg-dark-900 border border-dark-800 rounded-xl text-white placeholder-dark-500 focus:outline-none focus:border-primary-500 transition-colors"
              aria-label="Search memories"
            />
          </div>
          <button
            type="submit"
            disabled={!query.trim()}
            className="px-6 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Search"
          >
            Search
          </button>
        </div>

        {/* Agent filter */}
        <div className="flex flex-wrap gap-2">
          {['all', 'faintech-ceo', 'faintech-cto', 'faintech-frontend', 'faintech-backend'].map(agent => (
            <button
              key={agent}
              type="button"
              onClick={() => setSelectedAgent(agent)}
              className={clsx(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                selectedAgent === agent
                  ? 'bg-dark-800 text-white'
                  : 'text-dark-400 hover:text-white hover:bg-dark-800/50'
              )}
              aria-pressed={selectedAgent === agent}
            >
              {agent === 'all' ? 'All Agents' : agent}
            </button>
          ))}
        </div>
      </form>

      {/* Results */}
      {searchTerm && (
        <div className="space-y-4">
          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
            </div>
          ) : data ? (
            <>
              <div className="text-dark-400 text-sm">
                Found {data.total} results for "{data.query}"
              </div>

              {data.results.length > 0 ? (
                <div className="space-y-3">
                  {data.results.map((result, index) => (
                    <div
                      key={`${result.memory.id}-${index}`}
                      className="bg-dark-900 rounded-xl p-5 border border-dark-800 hover:border-dark-700 transition-colors"
                    >
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-sm font-medium text-primary-400 bg-primary-400/10 px-2 py-1 rounded">
                          {result.memory.agent_id}
                        </span>
                        <span className="text-xs text-dark-500">
                          Score: {Math.round(result.score)}%
                        </span>
                      </div>
                      <p 
                        className="text-dark-200 leading-relaxed"
                        dangerouslySetInnerHTML={{ __html: result.highlight }}
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12 text-dark-500">
                  No results found. Try a different search term.
                </div>
              )}
            </>
          ) : (
            <div className="text-dark-400">Search failed</div>
          )}
        </div>
      )}

      {/* Empty state */}
      {!searchTerm && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4" role="img" aria-label="Magnifying glass">🔍</div>
          <p className="text-dark-400 text-lg">Enter a search term to find memories</p>
          <p className="text-dark-500 text-sm mt-2">Search across all agents or filter by specific agent</p>
        </div>
      )}
    </div>
  )
}
