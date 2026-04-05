import { NextRequest, NextResponse } from 'next/server';

// In-memory storage for demo purposes
// In production, this would be replaced with a proper database
let memories: Array<{
  id: string;
  title: string;
  content: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}> = [];

interface CreateMemoryRequest {
  title: string;
  content: string;
  tags?: string[];
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = Number(searchParams.get('limit')) || 10;
    const offset = Number(searchParams.get('offset')) || 0;

    const paginatedMemories = memories.slice(offset, offset + limit);

    return NextResponse.json({
      memories: paginatedMemories,
      total: memories.length,
      limit,
      offset,
    });
  } catch (error) {
    console.error('[Memories GET Error]', error);
    return NextResponse.json(
      { error: 'Failed to fetch memories' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body: CreateMemoryRequest = await request.json();

    // Validate required fields
    if (!body.title || !body.content) {
      return NextResponse.json(
        { error: 'Missing required fields: title and content' },
        { status: 400 }
      );
    }

    const newMemory = {
      id: `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: body.title,
      content: body.content,
      tags: body.tags || [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    memories.push(newMemory);

    return NextResponse.json({
      memory: newMemory,
      message: 'Memory created successfully',
    }, { status: 201 });
  } catch (error) {
    console.error('[Memories POST Error]', error);
    return NextResponse.json(
      { error: 'Failed to create memory' },
      { status: 500 }
    );
  }
}
