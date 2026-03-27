import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { randomBytes } from 'crypto'

import { encrypt } from '@/lib/encryption'

// POST /api/user/api-keys - Generate new API key
export async function POST(request: NextRequest) {
  try {
    const userId = request.headers.get('x-user-id')
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Check rate limit (max 5 keys per user)
    const keyCount = await db.apiKey.count({
      where: { userId }
    })

    if (keyCount >= 5) {
      return NextResponse.json({
        error: 'Maximum API keys limit reached (5 keys per user)'
        }, { status: 400 })
    }

    // Generate new API key
    const rawKey = `lab_${randomBytes(16).toString('hex')}`
    const keyHash = await encrypt(rawKey)
    const displayKey = rawKey // Show once, not stored
    const expiresAt = new Date(Date.now() + 90 * 24 * 60 * 60 * 1000) // 90 days from now

    // Store encrypted key
    const apiKey = await db.apiKey.create({
      data: {
        id: randomBytes(16).toString('hex'),
        userId,
        keyHash,
        lastFour: rawKey.slice(-4),
        createdAt: new Date(),
        expiresAt
      }
    })

    return NextResponse.json({
      apiKey: displayKey,
      message: 'Store this key securely. It will not be shown again.'
    }, { status: 201 })
  } catch (error) {
    console.error('Failed to generate API key:', error)
    return NextResponse.json({
      error: 'Failed to generate API key',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}
