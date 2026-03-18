/**
 * Centralized Error Handling Utilities
 *
 * Provides custom error classes for consistent error handling across lib files.
 */

/** Base error class for lib operations */
export class LibError extends Error {
  constructor(message: string, public readonly code: string) {
    super(message);
    this.name = 'LibError';
  }
}

/** Error for file operations */
export class FileOperationError extends LibError {
  constructor(operation: string, path: string, cause?: Error) {
    super(`Failed to ${operation} file: ${path}${cause ? ` - ${cause.message}` : ''}`, 'FILE_OPERATION_ERROR');
    this.name = 'FileOperationError';
  }
}

/** Error for validation failures */
export class ValidationError extends LibError {
  constructor(message: string, public readonly field?: string) {
    super(message, 'VALIDATION_ERROR');
    this.name = 'ValidationError';
  }
}

/** Error for not found resources */
export class NotFoundError extends LibError {
  constructor(resource: string, identifier: string) {
    super(`${resource} not found: ${identifier}`, 'NOT_FOUND');
    this.name = 'NotFoundError';
  }
}

/**
 * Wrap async function with error handling
 */
export function withErrorHandling<T>(
  operation: () => Promise<T>,
  fallback: T,
  context?: string
): Promise<T> {
  return operation().catch((error) => {
    console.error(`Error${context ? ` in ${context}` : ''}:`, error);
    return fallback;
  });
}
