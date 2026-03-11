'use client';

import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import { useState } from 'react';

function looksLikeJwt(value: string) {
  return value.split('.').length === 3;
}

export default function LoginForm() {
  const { setApiKey } = useAuth();
  const [token, setToken] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const trimmedToken = token.trim();

    if (!trimmedToken) {
      setError('Please enter your JWT access token');
      return;
    }

    if (!looksLikeJwt(trimmedToken)) {
      setError('Invalid token format. Paste the JWT access token returned by /v1/auth/login.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError('');
      await api.validateToken(trimmedToken);
      setApiKey(trimmedToken);
    } catch {
      setError('Token validation failed. Make sure the backend is running and the token is still valid.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Agent Memory Cloud
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Paste the JWT access token from the backend login response to access the dashboard
          </p>
          <p className="mt-1 text-center text-xs text-gray-400">
            Get a token via <code className="bg-gray-100 px-1 rounded">POST /v1/auth/login</code>
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit} noValidate>
          <div>
            <label htmlFor="jwt-token" className="block text-sm font-medium text-gray-700 mb-1">
              JWT Access Token
            </label>
            <textarea
              id="jwt-token"
              name="jwt-token"
              autoComplete="off"
              required
              aria-required="true"
              aria-describedby={error ? 'jwt-token-error' : 'jwt-token-help'}
              rows={4}
              className="appearance-none rounded relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-amc-primary focus:border-amc-primary focus:z-10 sm:text-sm font-mono text-xs"
              placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
              value={token}
              onChange={(e) => setToken(e.target.value)}
            />
            <p id="jwt-token-help" className="mt-2 text-xs text-gray-500">
              Expected format: Bearer token returned by POST /v1/auth/login or /v1/auth/register.
            </p>
          </div>

          {error && (
            <div
              id="jwt-token-error"
              className="text-red-600 text-sm text-center"
              role="alert"
              aria-live="polite"
            >
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isSubmitting}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-amc-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amc-primary disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Validating token...' : 'Sign in with JWT'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
