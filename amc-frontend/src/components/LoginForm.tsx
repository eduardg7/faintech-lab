'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';

export default function LoginForm() {
  const { setApiKey } = useAuth();
  const [key, setKey] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!key.trim()) {
      setError('Please enter your API key');
      return;
    }

    if (!key.startsWith('amc_live_')) {
      setError('Invalid API key format. Key should start with "amc_live_"');
      return;
    }

    setApiKey(key.trim());
    setError('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Agent Memory Cloud
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Enter your API key to access the dashboard
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="api-key" className="sr-only">
              API Key
            </label>
            <input
              id="api-key"
              name="api-key"
              type="password"
              autoComplete="off"
              required
              className="appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-amc-primary focus:border-amc-primary focus:z-10 sm:text-sm"
              placeholder="amc_live_xxxxxxxxxxxxxxxxxxxx"
              value={key}
              onChange={(e) => setKey(e.target.value)}
            />
          </div>

          {error && (
            <div className="text-red-600 text-sm text-center">{error}</div>
          )}

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-amc-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary"
            >
              Sign in
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
