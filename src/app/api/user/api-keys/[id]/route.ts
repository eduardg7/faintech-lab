import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/lib/db'
import { randomBytes } from 'crypto'

import { encrypt } from '@/lib/encryption'

// GET /api/user/api-keys - List user's API keys
export async function GET(request: NextRequest) {
  try {
    const userId = request.headers.get('x-user-id')
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const apiKeys = await db.apiKey.findMany({
      where: { userId },
      select: {
        id: true,
        lastFour: true,
        createdAt: true,
        expiresAt: true,
        lastUsedAt: true
      },
      orderBy: { createdAt: 'desc' }
    })

    return NextResponse.json({ apiKeys })
  } catch (error) {
    console.error('Failed to list API keys:', error)
    return NextResponse.json({
      error: 'Failed to list API keys'
    }, { status: 500 })
  }
}

// DELETE /api/user/api-keys/[id] - Revoke API key
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const userId = request.headers.get('x-user-id')
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { id } = params

    // Verify key belongs to user
    const apiKey = await db.apiKey.findFirst({
      where: { id, userId }
    })

    if (!apiKey) {
      return NextResponse.json({ error: 'API key not found' }, { status: 404 })
    }

    // Soft delete (mark as revoked)
    await db.apiKey.update({
      where: { id },
      data: {
        revokedAt: new Date(),
        revoked: true
      }
    })

    return NextResponse.json({ message: 'API key revoked' })
  } catch (error) {
    console.error('Failed to revoke API key:', error)
    return NextResponse.json({
      error: 'Failed to revoke API key'
    }, { status: 500 })
  }
}
