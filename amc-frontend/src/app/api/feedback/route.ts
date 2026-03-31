import { NextRequest, NextResponse } from 'next/server';

interface FeedbackRequest {
  type: 'bug' | 'feature' | 'general';
  message: string;
  email?: string;
  metadata?: Record<string, unknown>;
}

export async function POST(request: NextRequest) {
  try {
    const body: FeedbackRequest = await request.json();

    // Validate required fields
    if (!body.message || !body.type) {
      return NextResponse.json(
        { error: 'Missing required fields: type and message' },
        { status: 400 }
      );
    }

    // Validate type
    const validTypes = ['bug', 'feature', 'general'];
    if (!validTypes.includes(body.type)) {
      return NextResponse.json(
        { error: 'Invalid feedback type. Must be: bug, feature, or general' },
        { status: 400 }
      );
    }

    // Log feedback (in production, this would go to a database or service)
    console.log('[Feedback]', {
      timestamp: new Date().toISOString(),
      type: body.type,
      message: body.message,
      email: body.email || 'anonymous',
      metadata: body.metadata || {},
      userAgent: request.headers.get('user-agent'),
      ip: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip'),
    });

    // Return success
    return NextResponse.json({
      success: true,
      message: 'Thank you for your feedback! We appreciate it.',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('[Feedback Error]', error);
    return NextResponse.json(
      { error: 'Failed to process feedback. Please try again.' },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    endpoint: '/api/feedback',
    methods: ['POST'],
    description: 'Submit user feedback (bug reports, feature requests, general feedback)',
    version: '1.0.0',
  });
}
