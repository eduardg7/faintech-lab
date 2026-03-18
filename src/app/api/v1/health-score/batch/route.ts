/**
 * Health Score Batch Calculate API Endpoint
 *
 * POST /v1/health-score/batch
 *
 * Task: OS-20260318091956-478B - AC3/5
 *
 * Calculates health scores for multiple users in a single request.
 */

import { NextRequest, NextResponse } from 'next/server';
import {
  HealthScoreCalculator,
  type UserActivityData,
  type HealthScoreBreakdown,
} from '@/lib/analytics/health-score-calculator';

export interface BatchCalculateHealthScoreRequest {
  users: UserActivityData[];
}

export interface UserHealthScoreResult {
  userId: string;
  success: boolean;
  data?: HealthScoreBreakdown;
  error?: {
    code: string;
    message: string;
  };
}

export interface BatchCalculateHealthScoreResponse {
  success: true;
  data: {
    results: UserHealthScoreResult[];
    summary: {
      total: number;
      successful: number;
      failed: number;
    };
  };
}

export interface BatchCalculateHealthScoreErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
  };
}

type ApiResponse =
  | BatchCalculateHealthScoreResponse
  | BatchCalculateHealthScoreErrorResponse;

/**
 * POST /v1/health-score/batch
 *
 * Calculate health scores for multiple users.
 *
 * Request body:
 * {
 *   "users": [
 *     {
 *       "userId": "string",
 *       "signupDate": "ISO date string",
 *       "lastActiveAt": "ISO date string",
 *       "sessionsCount": number,
 *       "tasksCompleted": number,
 *       "featuresUsed": string[],
 *       "npsScore": number | null,
 *       "feedbackSentiment": "positive" | "neutral" | "negative" | null
 *     },
 *     ...
 *   ]
 * }
 *
 * Response includes individual results per user and a summary.
 */
export async function POST(request: NextRequest): Promise<NextResponse<ApiResponse>> {
  try {
    const body = await request.json() as BatchCalculateHealthScoreRequest;

    // Validate request
    if (!body.users) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'MISSING_USERS',
          message: 'Request body must contain a "users" array',
        },
      }, { status: 400 });
    }

    if (!Array.isArray(body.users)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_USERS',
          message: '"users" must be an array',
        },
      }, { status: 400 });
    }

    if (body.users.length === 0) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'EMPTY_USERS',
          message: '"users" array cannot be empty',
        },
      }, { status: 400 });
    }

    if (body.users.length > 100) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'TOO_MANY_USERS',
          message: 'Maximum 100 users allowed per batch request',
        },
      }, { status: 400 });
    }

    const calculator = new HealthScoreCalculator();
    const results: UserHealthScoreResult[] = [];
    let successful = 0;
    let failed = 0;

    for (const user of body.users) {
      try {
        // Validate required fields
        const requiredFields: (keyof UserActivityData)[] = [
          'userId',
          'signupDate',
          'lastActiveAt',
          'sessionsCount',
          'tasksCompleted',
          'featuresUsed',
        ];

        const missingField = requiredFields.find(
          field => user[field] === undefined || user[field] === null
        );

        if (missingField) {
          results.push({
            userId: user.userId || 'unknown',
            success: false,
            error: {
              code: 'MISSING_FIELD',
              message: `Missing required field: ${missingField}`,
            },
          });
          failed++;
          continue;
        }

        // Validate userId
        if (typeof user.userId !== 'string' || !user.userId.trim()) {
          results.push({
            userId: 'invalid',
            success: false,
            error: {
              code: 'INVALID_USER_ID',
              message: 'userId must be a non-empty string',
            },
          });
          failed++;
          continue;
        }

        // Validate dates
        const signupDate = new Date(user.signupDate);
        const lastActiveAt = new Date(user.lastActiveAt);

        if (isNaN(signupDate.getTime())) {
          results.push({
            userId: user.userId,
            success: false,
            error: {
              code: 'INVALID_SIGNUP_DATE',
              message: 'signupDate must be a valid ISO date string',
            },
          });
          failed++;
          continue;
        }

        if (isNaN(lastActiveAt.getTime())) {
          results.push({
            userId: user.userId,
            success: false,
            error: {
              code: 'INVALID_LAST_ACTIVE_AT',
              message: 'lastActiveAt must be a valid ISO date string',
            },
          });
          failed++;
          continue;
        }

        // Calculate health score
        const healthScore = calculator.calculate(user);

        results.push({
          userId: user.userId,
          success: true,
          data: healthScore,
        });
        successful++;
      } catch (error) {
        results.push({
          userId: user.userId || 'unknown',
          success: false,
          error: {
            code: 'CALCULATION_ERROR',
            message: error instanceof Error ? error.message : 'Unknown error occurred',
          },
        });
        failed++;
      }
    }

    return NextResponse.json({
      success: true,
      data: {
        results,
        summary: {
          total: body.users.length,
          successful,
          failed,
        },
      },
    });
  } catch (error) {
    console.error('Batch health score calculation error:', error);

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
        message: 'An unexpected error occurred while calculating health scores',
      },
    }, { status: 500 });
  }
}
