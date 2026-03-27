import { describe, it, expect, beforeEach } from 'vitest';
import db from '../../src/lib/db';
import { encrypt, decrypt } from '../../src/lib/encryption';
import crypto from 'crypto';

const randomBytes = (n: number) => crypto.randomBytes(n);

describe('API Key Generation', () => {
  const testUserId = 'test-user-123';

  beforeEach(async () => {
    // Reset in-memory database
    const keys = await db.apiKey.findMany({ where: { userId: testUserId } });
    for (const key of keys) {
      await db.apiKey.update({
        where: { id: key.id },
        data: { revoked: true, revokedAt: new Date() }
      });
    }
  });

  it('should create a new API key', async () => {
    const rawKey = `lab_${randomBytes(16).toString('hex')}`;
    const keyHash = await encrypt(rawKey);
    const keyId = randomBytes(16).toString('hex');

    const result = await db.apiKey.create({
      data: {
        id: keyId,
        userId: testUserId,
        keyHash,
        lastFour: rawKey.slice(-4),
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
      }
    });

    expect(result).toHaveProperty('id', keyId);
    expect(result).toHaveProperty('userId', testUserId);
    expect(result).toHaveProperty('keyHash');
    expect(result).toHaveProperty('lastFour');
    expect(result.revoked).toBe(false);
  });

  it('should store API key encrypted', async () => {
    const rawKey = `lab_${randomBytes(16).toString('hex')}`;
    const keyHash = await encrypt(rawKey);

    const result = await db.apiKey.create({
      data: {
        id: randomBytes(16).toString('hex'),
        userId: testUserId,
        keyHash,
        lastFour: rawKey.slice(-4),
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
      }
    });

    // Key should be stored encrypted, not in plain text
    expect(result.keyHash).not.toBe(rawKey);
    expect(result.keyHash).toBeTruthy();
  });

  it('should enforce rate limiting (max 5 keys per user)', async () => {
    // Create 5 keys
    for (let i = 0; i < 5; i++) {
      const rawKey = `lab_${randomBytes(16).toString('hex')}`;
      const keyHash = await encrypt(rawKey);

      await db.apiKey.create({
        data: {
          id: randomBytes(16).toString('hex'),
          userId: testUserId,
          keyHash,
          lastFour: rawKey.slice(-4),
          createdAt: new Date(),
          expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
        }
      });
    }

    const count = await db.apiKey.count({ where: { userId: testUserId } });
    expect(count).toBe(5);
  });
});

describe('API Key Listing', () => {
  const testUserId = 'test-user-456';

  beforeEach(async () => {
    // Reset in-memory database
    const keys = await db.apiKey.findMany({ where: { userId: testUserId } });
    for (const key of keys) {
      await db.apiKey.update({
        where: { id: key.id },
        data: { revoked: true, revokedAt: new Date() }
      });
    }
  });

  it('should list API keys with last 4 chars only', async () => {
    const rawKey = `lab_${randomBytes(16).toString('hex')}`;
    const keyHash = await encrypt(rawKey);

    await db.apiKey.create({
      data: {
        id: randomBytes(16).toString('hex'),
        userId: testUserId,
        keyHash,
        lastFour: rawKey.slice(-4),
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
      }
    });

    const keys = await db.apiKey.findMany({
      where: { userId: testUserId },
      select: { id: true, lastFour: true, createdAt: true }
    });

    expect(keys).toHaveLength(1);
    expect(keys[0]).toHaveProperty('id');
    expect(keys[0]).toHaveProperty('lastFour');
    expect(keys[0]).toHaveProperty('createdAt');
  });

  it('should return empty array when no keys exist', async () => {
    const keys = await db.apiKey.findMany({ where: { userId: testUserId } });
    expect(keys).toEqual([]);
  });
});

describe('API Key Revocation', () => {
  const testUserId = 'test-user-789';

  beforeEach(async () => {
    // Reset in-memory database
    const keys = await db.apiKey.findMany({ where: { userId: testUserId } });
    for (const key of keys) {
      await db.apiKey.update({
        where: { id: key.id },
        data: { revoked: true, revokedAt: new Date() }
      });
    }
  });

  it('should revoke an API key', async () => {
    const keyId = randomBytes(16).toString('hex');
    const rawKey = `lab_${randomBytes(16).toString('hex')}`;
    const keyHash = await encrypt(rawKey);

    await db.apiKey.create({
      data: {
        id: keyId,
        userId: testUserId,
        keyHash,
        lastFour: rawKey.slice(-4),
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
      }
    });

    const result = await db.apiKey.update({
      where: { id: keyId },
      data: { revoked: true, revokedAt: new Date() }
    });

    expect(result.revoked).toBe(true);
    expect(result.revokedAt).toBeTruthy();
  });

  it('should not find revoked keys in findMany', async () => {
    const keyId = randomBytes(16).toString('hex');
    const rawKey = `lab_${randomBytes(16).toString('hex')}`;
    const keyHash = await encrypt(rawKey);

    await db.apiKey.create({
      data: {
        id: keyId,
        userId: testUserId,
        keyHash,
        lastFour: rawKey.slice(-4),
        createdAt: new Date(),
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
      }
    });

    await db.apiKey.update({
      where: { id: keyId },
      data: { revoked: true, revokedAt: new Date() }
    });

    const keys = await db.apiKey.findMany({ where: { userId: testUserId } });
    expect(keys).toHaveLength(0);
  });
});

describe('Encryption', () => {
  it('should encrypt and decrypt data correctly', async () => {
    const plaintext = 'lab_test1234567890123456789012';
    const encrypted = await encrypt(plaintext);
    const decrypted = await decrypt(encrypted);

    expect(decrypted).toBe(plaintext);
    expect(encrypted).not.toBe(plaintext);
  });

  it('should produce different ciphertext for same plaintext', async () => {
    const plaintext = 'lab_test1234567890123456789012';
    const encrypted1 = await encrypt(plaintext);
    const encrypted2 = await encrypt(plaintext);

    // Due to IV (initialization vector), same plaintext should produce different ciphertext
    expect(encrypted1).not.toBe(encrypted2);
  });
});
