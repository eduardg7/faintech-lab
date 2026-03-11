/**
 * Custom exceptions for Agent Memory Cloud SDK.
 * @module exceptions
 */

/**
 * Base exception for all SDK errors.
 */
export class AgentMemoryError extends Error {
  /** HTTP status code if available */
  public readonly statusCode: number | undefined;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = 'AgentMemoryError';
    this.statusCode = statusCode;
    Object.setPrototypeOf(this, AgentMemoryError.prototype);
  }
}

/**
 * Raised when authentication fails (401).
 */
export class AuthenticationError extends AgentMemoryError {
  constructor(message: string, statusCode?: number) {
    super(message, statusCode);
    this.name = 'AuthenticationError';
    Object.setPrototypeOf(this, AuthenticationError.prototype);
  }
}

/**
 * Raised when rate limit is exceeded (429).
 */
export class RateLimitError extends AgentMemoryError {
  /** Seconds to wait before retrying */
  public readonly retryAfter: number | undefined;

  constructor(message: string, retryAfter: number | undefined, statusCode?: number) {
    super(message, statusCode ?? 429);
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter;
    Object.setPrototypeOf(this, RateLimitError.prototype);
  }
}

/**
 * Raised when a resource is not found (404).
 */
export class NotFoundError extends AgentMemoryError {
  constructor(message: string, statusCode?: number) {
    super(message, statusCode);
    this.name = 'NotFoundError';
    Object.setPrototypeOf(this, NotFoundError.prototype);
  }
}

/**
 * Raised when request validation fails (422).
 */
export class ValidationError extends AgentMemoryError {
  constructor(message: string, statusCode?: number) {
    super(message, statusCode);
    this.name = 'ValidationError';
    Object.setPrototypeOf(this, ValidationError.prototype);
  }
}
