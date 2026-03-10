import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface AuthContextType {
  isAuthenticated: boolean
  isLoading: boolean
  apiKey: string | null
  login: (key: string) => Promise<boolean>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

const STORAGE_KEY = 'amc_api_key'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [apiKey, setApiKey] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for stored API key on mount
    const storedKey = localStorage.getItem(STORAGE_KEY)
    if (storedKey) {
      setApiKey(storedKey)
    }
    setIsLoading(false)
  }, [])

  const login = async (key: string): Promise<boolean> => {
    // In production, validate the key with the backend
    // For now, we'll accept any non-empty key
    if (key.trim().length > 0) {
      localStorage.setItem(STORAGE_KEY, key)
      setApiKey(key)
      return true
    }
    return false
  }

  const logout = () => {
    localStorage.removeItem(STORAGE_KEY)
    setApiKey(null)
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated: !!apiKey, isLoading, apiKey, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
