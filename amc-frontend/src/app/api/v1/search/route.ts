import { NextRequest, NextResponse } from 'next/server';

// In-memory storage - same as memories endpoint
let memories: Array<{
  id: string;
  title: string;
  content: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}> = [];

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get('q') || '';
    const limit = Number(searchParams.get('limit')) || 10;

    if (!query.trim()) {
      return NextResponse.json({
        results: [],
        total: 0,
        query,
        message: 'Search query cannot be empty',
      }, { status: 400 });
    }

    // Simple text-based search (case-insensitive)
    const searchQuery = query.toLowerCase();
    const results = memories.filter(memory => {
      return (
        memory.title.toLowerCase().includes(searchQuery) ||
        memory.content.toLowerCase().includes(searchQuery) ||
        memory.tags.some(tag => tag.toLowerCase().includes(searchQuery))
      );
    });

    // Sort by relevance (simple scoring based on title matches first)
    const scoredResults = results
      .map(memory => ({
        ...memory,
        score: memory.title.toLowerCase().includes(searchQuery) ? 2 : 1,
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);

    return NextResponse.json({
      results: scoredResults,
      total: results.length,
      query,
      limit: scoredResults.length,
    });
  } catch (error) {
    console.error('[Search GET Error]', error);
    return NextResponse.json(
      { error: 'Failed to search memories' },
      { status: 500 }
    );
  }
}
