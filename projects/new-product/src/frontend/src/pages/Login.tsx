import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Login() {
  const [apiKey, setApiKey] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!apiKey.trim()) {
      setError('Please enter an API key')
      return
    }

    const success = await login(apiKey.trim())
    if (success) {
      navigate('/')
    } else {
      setError('Invalid API key')
    }
  }

  return (
    <div className="min-h-screen bg-dark-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🧠</div>
          <h1 className="text-3xl font-bold text-white">Agent Memory Cloud</h1>
          <p className="text-dark-400 mt-2">Sign in with your API key</p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="bg-dark-900 rounded-xl p-6 border border-dark-800">
          <div className="space-y-4">
            <div>
              <label htmlFor="apiKey" className="block text-dark-400 text-sm mb-2">
                API Key
              </label>
              <input
                id="apiKey"
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter your API key"
                className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-white placeholder-dark-500 focus:outline-none focus:border-primary-500 transition-colors"
              />
            </div>

            {error && (
              <div className="text-red-400 text-sm bg-red-400/10 px-3 py-2 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
            >
              Sign In
            </button>
          </div>

          <div className="mt-6 pt-6 border-t border-dark-800">
            <p className="text-dark-500 text-sm text-center">
              Don't have an API key?{' '}
              <a href="#" className="text-primary-400 hover:text-primary-300">
                Contact us
              </a>
            </p>
          </div>
        </form>

        {/* Demo hint */}
        <div className="mt-4 text-center">
          <p className="text-dark-600 text-xs">
            Demo mode: Enter any non-empty string to login
          </p>
        </div>
      </div>
    </div>
  )
}
