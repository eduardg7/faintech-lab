'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { useEffect } from 'react';

interface APIKey {
  id: string;
  key_prefix: string;
  created_at: string;
  last_used_at: string | null;
}

export default function APIKeysPage() {
  const { accessToken, isAuthenticated } = useAuth();
  const queryClient = useQueryClient();
  const [newKey, setNewKey] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  // Redirect to home if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      window.location.href = '/';
    }
  }, [isAuthenticated]);

  // Fetch existing API keys
  const { data: keys, isLoading } = useQuery<APIKey[]>({
    queryKey: ['api-keys'],
    queryFn: async () => {
      const response = await fetch('/api/user/api-keys', {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      });
      if (!response.ok) throw new Error('Failed to fetch API keys');
      return response.json();
    },
    enabled: !!accessToken,
  });

  // Generate new API key mutation
  const generateMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch('/api/user/api-keys', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to generate API key');
      }
      return response.json();
    },
    onSuccess: (data) => {
      setNewKey(data.key);
      setCopied(false);
      queryClient.invalidateQueries({ queryKey: ['api-keys'] });
    },
  });

  // Revoke API key mutation
  const revokeMutation = useMutation({
    mutationFn: async (keyId: string) => {
      const response = await fetch(`/api/user/api-keys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
        },
      });
      if (!response.ok) throw new Error('Failed to revoke API key');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['api-keys'] });
    },
  });

  const copyToClipboard = async (text: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleRevoke = (keyId: string) => {
    if (window.confirm('Are you sure you want to revoke this API key? This action cannot be undone.')) {
      revokeMutation.mutate(keyId);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  const hasMaxKeys = keys && keys.length >= 5;

  return (
    <div
      className="min-h-screen bg-gray-50"
      role="main"
      id="main-content"
      aria-label="API Key Management"
    >
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <Link
                href="/dashboard"
                className="text-sm text-gray-500 hover:text-gray-700 mb-2 inline-block"
                aria-label="Back to Dashboard"
              >
                ← Back to Dashboard
              </Link>
              <h1 className="text-2xl font-bold text-gray-900">API Keys</h1>
              <p className="text-sm text-gray-600 mt-1">
                Manage API keys for programmatic access to your memory storage
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Generate New Key Section */}
        <section className="mb-8" aria-labelledby="generate-heading">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 id="generate-heading" className="text-lg font-semibold text-gray-900 mb-4">
              Generate New API Key
            </h2>

            {hasMaxKeys && (
              <div
                className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md"
                role="alert"
                aria-live="polite"
              >
                <p className="text-sm text-yellow-800">
                  ⚠️ You have reached the maximum limit of 5 API keys. Please revoke an existing key before generating a new one.
                </p>
              </div>
            )}

            {newKey ? (
              <div
                className="p-4 bg-green-50 border border-green-200 rounded-md"
                role="alert"
                aria-live="polite"
              >
                <h3 className="text-sm font-semibold text-green-900 mb-2">
                  ✅ API Key Generated Successfully
                </h3>
                <p className="text-xs text-green-800 mb-3">
                  <strong>Important:</strong> This key will only be shown once. Please copy it now and store it securely.
                </p>
                <div className="flex items-center gap-2 mb-3">
                  <code className="flex-1 p-2 bg-white border border-green-300 rounded font-mono text-sm">
                    {newKey}
                  </code>
                  <button
                    onClick={() => copyToClipboard(newKey)}
                    className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                    aria-label={copied ? 'Copied!' : 'Copy to clipboard'}
                  >
                    {copied ? '✓ Copied!' : 'Copy'}
                  </button>
                </div>
                <button
                  onClick={() => setNewKey(null)}
                  className="text-sm text-gray-600 hover:text-gray-800 underline"
                >
                  Generate another key
                </button>
              </div>
            ) : (
              <button
                onClick={() => generateMutation.mutate()}
                disabled={hasMaxKeys || generateMutation.isPending}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                aria-describedby={hasMaxKeys ? 'max-keys-warning' : undefined}
              >
                {generateMutation.isPending ? 'Generating...' : 'Generate New Key'}
              </button>
            )}

            {generateMutation.isError && (
              <p className="mt-2 text-sm text-red-600" role="alert">
                Error: {generateMutation.error?.message || 'Failed to generate key'}
              </p>
            )}
          </div>
        </section>

        {/* Existing Keys List */}
        <section aria-labelledby="existing-keys-heading">
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h2 id="existing-keys-heading" className="text-lg font-semibold text-gray-900">
                Your API Keys
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Only the last 4 characters are shown for security
              </p>
            </div>

            {isLoading ? (
              <div className="p-6 text-center text-gray-500">
                Loading API keys...
              </div>
            ) : keys && keys.length > 0 ? (
              <ul className="divide-y divide-gray-200" role="list">
                {keys.map((key) => (
                  <li key={key.id} className="p-6 hover:bg-gray-50 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3">
                          <code className="text-sm font-mono text-gray-900 bg-gray-100 px-2 py-1 rounded">
                            ••••••••••••••••••••••••••••••••{key.key_prefix}
                          </code>
                        </div>
                        <div className="mt-2 text-xs text-gray-500 space-y-1">
                          <p>Created: {new Date(key.created_at).toLocaleString()}</p>
                          {key.last_used_at && (
                            <p>Last used: {new Date(key.last_used_at).toLocaleString()}</p>
                          )}
                        </div>
                      </div>
                      <button
                        onClick={() => handleRevoke(key.id)}
                        disabled={revokeMutation.isPending}
                        className="ml-4 px-3 py-1.5 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded border border-red-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                        aria-label={`Revoke API key ending in ${key.key_prefix}`}
                      >
                        {revokeMutation.isPending ? 'Revoking...' : 'Revoke'}
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="p-6 text-center text-gray-500">
                No API keys yet. Generate your first key above.
              </div>
            )}
          </div>
        </section>

        {/* Usage Info */}
        <section className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">Using Your API Key</h3>
          <p className="text-xs text-blue-800 mb-3">
            Include your API key in the Authorization header when making requests:
          </p>
          <code className="block p-3 bg-white border border-blue-300 rounded text-xs">
            Authorization: Bearer YOUR_API_KEY
          </code>
        </section>
      </main>
    </div>
  );
}
