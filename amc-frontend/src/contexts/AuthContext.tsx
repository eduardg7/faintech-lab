'use client';

import { useState, useEffect, createContext, useContext, ReactNode, useCallback } from 'react';

interface AuthContextType {
  accessToken: string | null;
  refreshToken: string | null;
  setAuth: (accessToken: string, refreshToken: string) => void;
  isAuthenticated: boolean;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [accessToken, setAccessTokenState] = useState<string | null>(null);
  const [refreshToken, setRefreshTokenState] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load both tokens from localStorage on mount
    const storedAccess = localStorage.getItem('amc_access_token');
    const storedRefresh = localStorage.getItem('amc_refresh_token');
    if (storedAccess) {
      setAccessTokenState(storedAccess);
    }
    if (storedRefresh) {
      setRefreshTokenState(storedRefresh);
    }
    setIsLoading(false);
  }, []);

  const setAuth = useCallback((accessTokenValue: string, refreshTokenValue: string) => {
    setAccessTokenState(accessTokenValue);
    setRefreshTokenState(refreshTokenValue);
    localStorage.setItem('amc_access_token', accessTokenValue);
    localStorage.setItem('amc_refresh_token', refreshTokenValue);
  }, []);

  const logout = useCallback(() => {
    setAccessTokenState(null);
    setRefreshTokenState(null);
    localStorage.removeItem('amc_access_token');
    localStorage.removeItem('amc_refresh_token');
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amc-primary"></div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ accessToken, refreshToken, setAuth, isAuthenticated: !!accessToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
