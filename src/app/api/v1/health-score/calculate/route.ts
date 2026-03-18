/**
 * Health Score Calculate API Endpoint
 *
 * POST /v1/health-score/calculate
 *
 * Task: OS-20260318091956-16A1 - AC2/5
 *
 * Calculates health score for a single user using the HealthScoreCalculator.
 */

import { NextRequest, NextResponse } from 'next/server';
import {
  HealthScoreCalculator,
  type UserActivityData,
  type HealthScoreBreakdown,
} from '@/lib/analytics/health-score-calculator';

export interface CalculateHealthScoreRequest {
  user: UserActivityData;
}

export interface CalculateHealthScoreResponse {
  success: true;
  data: HealthScoreBreakdown;
}

export interface CalculateHealthScoreErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
  };
}

type ApiResponse = CalculateHealthScoreResponse | CalculateHealthScoreErrorResponse;

/**
 * POST /v1/health-score/calculate
 *
 * Calculate health score for a single user.
 *
 * Request body:
 * {
 *   "user": {
 *     "userId": "string",
 *     "signupDate": "ISO date string",
 *     "lastActiveAt": "ISO date string",
 *     "sessionsCount": number,
 *     "tasksCompleted": number,
 *     "featuresUsed": string[],
 *     "npsScore": number | null,
 *     "feedbackSentiment": "positive" | "neutral" | "negative" | null
 *   }
 * }
 */
export async function POST(request: NextRequest): Promise<NextResponse<ApiResponse>> {
  try {
    const body = await request.json() as CalculateHealthScoreRequest;

    // Validate request
    if (!body.user) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'MISSING_USER',
          message: 'Request body must contain a "user" object',
        },
      }, { status: 400 });
    }

    const { user } = body;

    // Validate required fields
    const requiredFields: (keyof UserActivityData)[] = [
      'userId',
      'signupDate',
      'lastActiveAt',
      'sessionsCount',
      'tasksCompleted',
      'featuresUsed',
    ];

    for (const field of requiredFields) {
      if (user[field] === undefined || user[field] === null) {
        return NextResponse.json({
          success: false,
          error: {
            code: 'MISSING_FIELD',
            message: `Missing required field: ${field}`,
          },
        }, { status: 400 });
      }
    }

    // Validate field types
    if (typeof user.userId !== 'string' || !user.userId.trim()) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_USER_ID',
          message: 'userId must be a non-empty string',
        },
      }, { status: 400 });
    }

    if (typeof user.sessionsCount !== 'number' || user.sessionsCount < 0) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_SESSIONS_COUNT',
          message: 'sessionsCount must be a non-negative number',
        },
      }, { status: 400 });
    }

    if (typeof user.tasksCompleted !== 'number' || user.tasksCompleted < 0) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_TASKS_COMPLETED',
          message: 'tasksCompleted must be a non-negative number',
        },
      }, { status: 400 });
    }

    if (!Array.isArray(user.featuresUsed)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_FEATURES_USED',
          message: 'featuresUsed must be an array',
        },
      }, { status: 400 });
    }

    // Validate dates
    const signupDate = new Date(user.signupDate);
    const lastActiveAt = new Date(user.lastActiveAt);

    if (isNaN(signupDate.getTime())) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_SIGNUP_DATE',
          message: 'signupDate must be a valid ISO date string',
        },
      }, { status: 400 });
    }

    if (isNaN(lastActiveAt.getTime())) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_LAST_ACTIVE_AT',
          message: 'lastActiveAt must be a valid ISO date string',
        },
      }, { status: 400 });
    }

    // Validate sentiment if provided
    if (user.feedbackSentiment !== undefined && user.feedbackSentiment !== null) {
      const validSentiments = ['positive', 'neutral', 'negative'];
      if (!validSentiments.includes(user.feedbackSentiment)) {
        return NextResponse.json({
          success: false,
          error: {
            code: 'INVALID_SENTIMENT',
            message: `feedbackSentiment must be one of: ${validSentiments.join(', ')}`,
          },
        }, { status: 400 });
      }
    }

    // Calculate health score
    const calculator = new HealthScoreCalculator();
    const result = calculator.calculate(user);

    return NextResponse.json({
      success: true,
      data: result,
    });
  } catch (error) {
    console.error('Health score calculation error:', error);

    if (error instanceof SyntaxError) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_JSON',
          message: 'Request body must be valid JSON',
        },
      }, { status: 400 });
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred while calculating health score',
      },
    }, { status: 500 });
  }
}
