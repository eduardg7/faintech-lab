import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Health check endpoint - confirms the backend is operational
    const healthStatus = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'amc-backend',
      version: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
      uptime: process.uptime ? Math.floor(process.uptime()) : 0,
    };

    return NextResponse.json(healthStatus, { status: 200 });
  } catch (error) {
    console.error('[Health Check Error]', error);
    return NextResponse.json(
      {
        status: 'unhealthy',
        error: 'Health check failed',
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}
