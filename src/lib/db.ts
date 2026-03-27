/**
 * Database Module for Faintech Lab
 *
 * Simple in-memory database for API key management.
 * Can be replaced with Prisma + PostgreSQL later.
 */

// In-memory store for API keys
const apiKeyStore = new Map<string, {
  id: string;
  userId: string;
  keyHash: string;
  lastFour: string;
  createdAt: Date;
  expiresAt: Date;
  lastUsedAt: Date | null;
  revokedAt: Date | null;
  revoked: boolean;
}>();

export const db = {
  apiKey: {
    count: async ({ where }: { where: { userId: string } }) => {
      let count = 0;
      // Use Array.from to convert MapIterator to array for ES2015 compatibility
      for (const key of Array.from(apiKeyStore.values())) {
        if (key.userId === where.userId && !key.revoked) {
          count++;
        }
      }
      return count;
    },

    create: async ({ data }: {
      data: {
        id: string;
        userId: string;
        keyHash: string;
        lastFour: string;
        createdAt: Date;
        expiresAt: Date;
      }
    }) => {
      const apiKey = {
        ...data,
        lastUsedAt: null,
        revokedAt: null,
        revoked: false
      };
      apiKeyStore.set(data.id, apiKey);
      return apiKey;
    },

    findMany: async ({ where, select, orderBy }: {
      where: { userId: string };
      select?: Record<string, boolean>;
      orderBy?: { createdAt: 'desc' | 'asc' };
    }) => {
      const results = [];
      for (const key of Array.from(apiKeyStore.values())) {
        if (key.userId === where.userId && !key.revoked) {
          if (select) {
            const selected: Record<string, unknown> = {};
            for (const field of Object.keys(select)) {
              selected[field] = key[field as keyof typeof key];
            }
            results.push(selected);
          } else {
            results.push(key);
          }
        }
      }
      if (orderBy?.createdAt === 'desc') {
        results.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
      }
      return results;
    },

    findFirst: async ({ where }: {
      where: { id: string; userId: string }
    }) => {
      const key = apiKeyStore.get(where.id);
      if (key && key.userId === where.userId && !key.revoked) {
        return key;
      }
      return null;
    },

    update: async ({ where, data }: {
      where: { id: string };
      data: { revokedAt?: Date; revoked?: boolean };
    }) => {
      const key = apiKeyStore.get(where.id);
      if (key) {
        const updated = { ...key, ...data };
        apiKeyStore.set(where.id, updated);
        return updated;
      }
      throw new Error('API key not found');
    }
  }
};

export default db;
