/**
 * HTTP client for Agent Memory Cloud API.
 * @module http-client
 */

import {
  AgentMemoryError,
  AuthenticationError,
  NotFoundError,
  RateLimitError,
  ValidationError,
} from './exceptions.js';

/**
 * Configuration options for HTTP client.
 */
export interface HttpClientConfig {
  /** API key for authentication */
  apiKey: string;
  /** Base URL for API */
  baseUrl: string;
  /** Request timeout in milliseconds */
  timeout: number;
}

/**
 * HTTP client for making API requests.
 */
export class HttpClient {
  private readonly apiKey: string;
  private readonly baseUrl: string;
  private readonly timeout: number;

  constructor(config: HttpClientConfig) {
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.timeout = config.timeout;
  }

  /**
   * Build request headers.
   */
  private buildHeaders(): Record<string, string> {
    return {
      'X-API-Key': this.apiKey,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    };
  }

  /**
   * Make HTTP request to API.
   * @throws {AuthenticationError} 401 response
   * @throws {NotFoundError} 404 response
   * @throws {RateLimitError} 429 response
   * @throws {ValidationError} 422 response
   * @throws {AgentMemoryError} Other errors
   */
  async request<T>(
    method: string,
    path: string,
    params?: Record<string, unknown>,
    json?: Record<string, unknown>
  ): Promise<T> {
    const url = new URL(`${this.baseUrl}/${path.replace(/^\//, '')}`);

    // Add query parameters
    if (params) {
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== null) {
          if (Array.isArray(value)) {
            url.searchParams.set(key, value.join(','));
          } else {
            url.searchParams.set(key, String(value));
          }
        }
      }
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const fetchOptions: RequestInit = {
        method,
        headers: this.buildHeaders(),
        signal: controller.signal,
      };

      if (json) {
        fetchOptions.body = JSON.stringify(json);
      }

      const response = await fetch(url.toString(), fetchOptions);

      clearTimeout(timeoutId);

      if (response.status === 401) {
        throw new AuthenticationError('Invalid API key', 401);
      }

      if (response.status === 404) {
        throw new NotFoundError(`Resource not found: ${path}`, 404);
      }

      if (response.status === 422) {
        const body = (await response.json()) as { detail?: string };
        throw new ValidationError(body.detail ?? 'Validation failed', 422);
      }

      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        throw new RateLimitError(
          'Rate limit exceeded',
          retryAfter ? parseInt(retryAfter, 10) : undefined,
          429
        );
      }

      if (response.status >= 400) {
        const text = await response.text();
        throw new AgentMemoryError(
          `API error: ${response.status} - ${text}`,
          response.status
        );
      }

      // Handle 204 No Content
      if (response.status === 204) {
        return undefined as T;
      }

      return (await response.json()) as T;
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof AgentMemoryError) {
        throw error;
      }

      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new AgentMemoryError('Request timeout', 408);
        }
        throw new AgentMemoryError(`Network error: ${error.message}`);
      }

      throw new AgentMemoryError('Unknown error');
    }
  }

  /**
   * GET request.
   */
  async get<T>(
    path: string,
    params?: Record<string, unknown>
  ): Promise<T> {
    return this.request<T>('GET', path, params);
  }

  /**
   * POST request.
   */
  async post<T>(
    path: string,
    json?: Record<string, unknown>
  ): Promise<T> {
    return this.request<T>('POST', path, undefined, json);
  }

  /**
   * PUT request.
   */
  async put<T>(
    path: string,
    json?: Record<string, unknown>
  ): Promise<T> {
    return this.request<T>('PUT', path, undefined, json);
  }

  /**
   * DELETE request.
   */
  async delete<T>(path: string): Promise<T> {
    return this.request<T>('DELETE', path);
  }
}
