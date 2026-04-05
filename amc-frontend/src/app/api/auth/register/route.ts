import { NextRequest, NextResponse } from 'next/server';

interface RegisterRequest {
  email: string;
  password: string;
  name?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
  utm_term?: string;
  utm_referrer?: string;
}

// In-memory user storage for demo purposes
// In production, this would use a proper database with password hashing
let users: Array<{
  id: string;
  email: string;
  name?: string;
  created_at: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
  utm_term?: string;
  utm_referrer?: string;
}> = [];

export async function POST(request: NextRequest) {
  try {
    const body: RegisterRequest = await request.json();

    // Validate required fields
    if (!body.email || !body.password) {
      return NextResponse.json(
        { error: 'Missing required fields: email and password' },
        { status: 400 }
      );
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(body.email)) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      );
    }

    // Check if user already exists
    const existingUser = users.find(user => user.email === body.email);
    if (existingUser) {
      return NextResponse.json(
        { error: 'User with this email already exists' },
        { status: 409 }
      );
    }

    // Create new user
    // In production, we would hash the password here
    const newUser = {
      id: `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      email: body.email,
      name: body.name,
      created_at: new Date().toISOString(),
      utm_source: body.utm_source,
      utm_medium: body.utm_medium,
      utm_campaign: body.utm_campaign,
      utm_content: body.utm_content,
      utm_term: body.utm_term,
      utm_referrer: body.utm_referrer,
    };

    users.push(newUser);

    // Remove sensitive data before returning
    const { password, ...userResponse } = body;

    return NextResponse.json({
      user: {
        id: newUser.id,
        email: newUser.email,
        name: newUser.name,
        created_at: newUser.created_at,
      },
      message: 'User registered successfully',
      utm_captured: {
        source: body.utm_source,
        medium: body.utm_medium,
        campaign: body.utm_campaign,
        content: body.utm_content,
        term: body.utm_term,
        referrer: body.utm_referrer,
      },
    }, { status: 201 });
  } catch (error) {
    console.error('[Register Error]', error);
    return NextResponse.json(
      { error: 'Failed to register user' },
      { status: 500 }
    );
  }
}
