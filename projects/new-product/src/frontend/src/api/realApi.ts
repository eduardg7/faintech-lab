// Real API client for Agent Memory Cloud

import type { ApiKey, CreateApiKeyResponse } from '../types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

// Helper function to get API key from storage
function getApiKey(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('api_key')
}

// Helper function for API requests
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const apiKey = getApiKey()

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(apiKey && { 'X-API-Key': apiKey }),
    ...options.headers,
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `API Error: ${response.status}`)
  }

  return response.json()
}

// API Key Management
export async function fetchApiKeys(): Promise<ApiKey[]> {
  const response = await apiRequest<ApiKey[]>('/keys')
  return response
}

export async function createApiKey(
  name: string,
  expiresInDays?: number
): Promise<CreateApiKeyResponse> {
  const response = await apiRequest<CreateApiKeyResponse>('/keys', {
    method: 'POST',
    body: JSON.stringify({
      name,
      expires_in_days: expiresInDays,
    }),
  })
  return response
}

export async function revokeApiKey(id: string): Promise<void> {
  await apiRequest(`/keys/${id}`, {
    method: 'DELETE',
  })
}

// Export other API functions as needed
export { apiRequest }
