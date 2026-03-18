/**
 * Tests for Error Handling Utilities
 */

import { describe, it, expect } from 'vitest';
import { LibError, FileOperationError, ValidationError, NotFoundError, withErrorHandling } from '../../src/lib/errors';

describe('LibError', () => {
  it('should create error with message and code', () => {
    const error = new LibError('Test error', 'TEST_CODE');
    expect(error.message).toBe('Test error');
    expect(error.code).toBe('TEST_CODE');
    expect(error.name).toBe('LibError');
  });
});

describe('FileOperationError', () => {
  it('should create error for file operation', () => {
    const error = new FileOperationError('read', '/path/to/file');
    expect(error.message).toBe('Failed to read file: /path/to/file');
    expect(error.code).toBe('FILE_OPERATION_ERROR');
  });

  it('should include cause message when provided', () => {
    const cause = new Error('Permission denied');
    const error = new FileOperationError('write', '/path/to/file', cause);
    expect(error.message).toContain('Permission denied');
  });
});

describe('ValidationError', () => {
  it('should create validation error', () => {
    const error = new ValidationError('Invalid value');
    expect(error.message).toBe('Invalid value');
    expect(error.code).toBe('VALIDATION_ERROR');
  });

  it('should include field name when provided', () => {
    const error = new ValidationError('Required', 'email');
    expect(error.field).toBe('email');
  });
});

describe('NotFoundError', () => {
  it('should create not found error', () => {
    const error = new NotFoundError('User', 'user-123');
    expect(error.message).toBe('User not found: user-123');
    expect(error.code).toBe('NOT_FOUND');
  });
});

describe('withErrorHandling', () => {
  it('should return result on success', async () => {
    const result = await withErrorHandling(
      async () => 'success',
      'fallback'
    );
    expect(result).toBe('success');
  });

  it('should return fallback on error', async () => {
    const result = await withErrorHandling(
      async () => { throw new Error('Failed'); },
      'fallback'
    );
    expect(result).toBe('fallback');
  });

  it('should log error with context', async () => {
    const logs: string[] = [];
    const originalError = console.error;
    console.error = (...args) => logs.push(args.join(' '));

    await withErrorHandling(
      async () => { throw new Error('Test'); },
      null,
      'testContext'
    );

    console.error = originalError;
    expect(logs.some(l => l.includes('testContext'))).toBe(true);
  });
});
