import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { fetchApiKeys, createApiKey, revokeApiKey } from '../api/realApi'
import { format } from 'date-fns'
import clsx from 'clsx'

export default function Settings() {
  const queryClient = useQueryClient()
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newKeyName, setNewKeyName] = useState('')
  const [newKeySecret, setNewKeySecret] = useState<string | null>(null)
  const [expiresInDays, setExpiresInDays] = useState<number | undefined>(undefined)

  const { data: apiKeys, isLoading } = useQuery({
    queryKey: ['apiKeys'],
    queryFn: fetchApiKeys,
  })

  const createMutation = useMutation({
    mutationFn: () => createApiKey(newKeyName, expiresInDays),
    onSuccess: (data) => {
      setNewKeySecret(data.secret)
      queryClient.invalidateQueries({ queryKey: ['apiKeys'] })
    },
  })

  const revokeMutation = useMutation({
    mutationFn: revokeApiKey,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['apiKeys'] })
    },
  })

  const handleCreateKey = () => {
    if (newKeyName.trim()) {
      createMutation.mutate()
    }
  }

  const handleCloseModal = () => {
    setShowCreateModal(false)
    setNewKeyName('')
    setNewKeySecret(null)
    setExpiresInDays(undefined)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="text-dark-400 mt-1">Manage your API keys and account settings</p>
      </div>

      {/* API Keys Section */}
      <div className="bg-dark-900 rounded-xl border border-dark-800">
        <div className="p-6 border-b border-dark-800 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white">API Keys</h2>
            <p className="text-dark-400 text-sm mt-1">Manage API keys for accessing the memory service</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <span>➕</span>
            Create Key
          </button>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-500"></div>
          </div>
        ) : apiKeys && apiKeys.length > 0 ? (
          <div className="divide-y divide-dark-800">
            {apiKeys.map(key => (
              <div key={key.id} className="p-4 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <span className="font-medium text-white">{key.name}</span>
                    {key.expires_at && (
                      <span className="text-xs text-yellow-400 bg-yellow-400/10 px-2 py-0.5 rounded">
                        Expires {format(new Date(key.expires_at), 'MMM dd, yyyy')}
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-dark-500 mt-1 font-mono">{key.prefix}</div>
                  <div className="text-xs text-dark-600 mt-1">
                    Created {format(new Date(key.created_at), 'MMM dd, yyyy')}
                    {key.last_used_at && (
                      <> · Last used {format(new Date(key.last_used_at), 'MMM dd, yyyy')}</>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => revokeMutation.mutate(key.id)}
                  disabled={revokeMutation.isPending}
                  className="px-3 py-1.5 text-red-400 hover:bg-red-400/10 rounded-lg transition-colors text-sm"
                >
                  Revoke
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-8 text-center text-dark-500">
            No API keys yet. Create one to get started.
          </div>
        )}
      </div>

      {/* Usage Stats */}
      <div className="bg-dark-900 rounded-xl p-6 border border-dark-800">
        <h2 className="text-lg font-semibold text-white mb-4">Usage This Month</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-dark-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-white">1,234</div>
            <div className="text-dark-400 text-sm">Memory Writes</div>
          </div>
          <div className="bg-dark-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-white">5,678</div>
            <div className="text-dark-400 text-sm">Memory Reads</div>
          </div>
          <div className="bg-dark-800 rounded-lg p-4">
            <div className="text-2xl font-bold text-white">432</div>
            <div className="text-dark-400 text-sm">Search Queries</div>
          </div>
        </div>
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-dark-900 rounded-xl p-6 w-full max-w-md border border-dark-800">
            {newKeySecret ? (
              <>
                <h3 className="text-lg font-semibold text-white mb-4">API Key Created</h3>
                <p className="text-dark-400 text-sm mb-4">
                  Copy this key now. You won't be able to see it again.
                </p>
                <div className="bg-dark-800 rounded-lg p-4 mb-4 overflow-x-auto">
                  <code className="text-green-400 text-sm break-all">{newKeySecret}</code>
                </div>
                <button
                  onClick={handleCloseModal}
                  className="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Done
                </button>
              </>
            ) : (
              <>
                <h3 className="text-lg font-semibold text-white mb-4">Create API Key</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-dark-400 text-sm mb-2">Key Name</label>
                    <input
                      type="text"
                      value={newKeyName}
                      onChange={(e) => setNewKeyName(e.target.value)}
                      placeholder="e.g., Production Key"
                      className="w-full px-4 py-2 bg-dark-800 border border-dark-700 rounded-lg text-white placeholder-dark-500 focus:outline-none focus:border-primary-500"
                    />
                  </div>
                  <div>
                    <label className="block text-dark-400 text-sm mb-2">Expiration (optional)</label>
                    <select
                      value={expiresInDays ?? ''}
                      onChange={(e) => setExpiresInDays(e.target.value ? Number(e.target.value) : undefined)}
                      className="w-full px-4 py-2 bg-dark-800 border border-dark-700 rounded-lg text-white focus:outline-none focus:border-primary-500"
                    >
                      <option value="">Never</option>
                      <option value="30">30 days</option>
                      <option value="90">90 days</option>
                      <option value="365">1 year</option>
                    </select>
                  </div>
                </div>
                <div className="flex gap-3 mt-6">
                  <button
                    onClick={handleCloseModal}
                    className="flex-1 py-2 bg-dark-800 text-dark-300 rounded-lg hover:bg-dark-700 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleCreateKey}
                    disabled={!newKeyName.trim() || createMutation.isPending}
                    className="flex-1 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
                  >
                    Create
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
