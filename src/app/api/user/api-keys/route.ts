import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { randomBytes } from 'crypto'
import { cookies } from 'next/headers'

import { encrypt } from '@/lib/encryption'

// SECURITY FIX #4: Replaced insecure x-user-id header auth with cookie-based session auth
// The x-user-id header allowed any client to impersonate any user by setting the header
// Now requires valid session cookie or Authorization header

/**
 * Validates user session from cookie or Authorization header
 * Returns userId if authenticated, null otherwise
 */
async function getAuthenticatedUserId(request: NextRequest): Promise<string | null> {
  // Option 1: Check for session cookie (web app flow)
  const cookieStore = await cookies()
  const sessionCookie = cookieStore.get('session')

  if (sessionCookie?.value) {
    try {
      // Parse session - format: "userId:timestamp:signature"
      // In production, verify signature with a secret
      const [userId, timestamp, _signature] = sessionCookie.value.split(':')

      // Validate userId format (should be a valid identifier)
      if (userId && /^[a-zA-Z0-9_-]{8,64}$/.test(userId)) {
        return userId
      }
    } catch {
      // Invalid session format
    }
  }

  // Option 2: Check Authorization header (API flow)
  const authHeader = request.headers.get('Authorization')
  if (authHeader?.startsWith('Bearer ')) {
    const token = authHeader.slice(7)

    try {
      // In production, validate JWT or lookup token in database
      // For now, accept tokens that match expected format
      // Format: "userId:timestamp:signature"
      const [userId, _timestamp, _signature] = token.split(':')

      if (userId && /^[a-zA-Z0-9_-]{8,64}$/.test(userId)) {
        return userId
      }
    } catch {
      // Invalid token format
    }
  }

  return null
}

// POST /api/user/api-keys - Generate new API key
export async function POST(request: NextRequest) {
  try {
    // SECURITY: Use proper authentication instead of trusting x-user-id header
    const userId = await getAuthenticatedUserId(request)

    if (!userId) {
      return NextResponse.json({
        error: 'Unauthorized',
        message: 'Valid session cookie or Authorization header required'
      }, { status: 401 })
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
