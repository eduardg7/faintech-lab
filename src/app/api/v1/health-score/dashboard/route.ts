/**
 * Health Score Dashboard API Endpoint
 *
 * GET /v1/health-score/dashboard
 *
 * Task: OS-20260318085922-8EFE - CSM AC4/4
 *
 * Returns aggregated health score data for the customer health monitoring dashboard.
 */

import { NextRequest, NextResponse } from 'next/server';
import {
  HealthScoreCalculator,
  type UserActivityData,
  type HealthScoreBreakdown,
} from '@/lib/analytics/health-score-calculator';

export interface DashboardMetrics {
  overview: {
    totalUsers: number;
    averageHealthScore: number;
    healthScoreTrend: 'up' | 'down' | 'stable';
  };
  riskDistribution: {
    low: number;
    medium: number;
    high: number;
    critical: number;
  };
  engagementMetrics: {
    averageFeatureAdoptionRate: number;
    averageLoginFrequency: number;
    activeUsersLast7Days: number;
    activeUsersLast30Days: number;
  };
  retentionMetrics: {
    averageTenure: number;
    churnRiskUsers: number;
  };
  feedbackMetrics: {
    averageNps: number | null;
    sentimentDistribution: {
      positive: number;
      neutral: number;
      negative: number;
      noFeedback: number;
    };
  };
}

export interface DashboardResponse {
  success: true;
  data: DashboardMetrics;
  generatedAt: string;
}

export interface DashboardErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
  };
}

type ApiResponse = DashboardResponse | DashboardErrorResponse;

/**
 * GET /v1/health-score/dashboard
 *
 * Returns aggregated metrics for the health score dashboard.
 *
 * Query parameters:
 * - users: JSON array of UserActivityData objects (required for now)
 *
 * Note: In production, this would fetch from a database. For the template,
 * we accept user data via query parameter.
 */
export async function GET(request: NextRequest): Promise<NextResponse<ApiResponse>> {
  try {
    const searchParams = request.nextUrl.searchParams;
    const usersParam = searchParams.get('users');

    if (!usersParam) {
      // Return template response with example data structure
      return NextResponse.json({
        success: true,
        data: getExampleDashboardMetrics(),
        generatedAt: new Date().toISOString(),
      });
    }

    let users: UserActivityData[];
    try {
      users = JSON.parse(usersParam);
    } catch {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_USERS_PARAM',
          message: 'users parameter must be a valid JSON array',
        },
      }, { status: 400 });
    }

    if (!Array.isArray(users) || users.length === 0) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'EMPTY_USERS',
          message: 'users array cannot be empty',
        },
      }, { status: 400 });
    }

    const metrics = calculateDashboardMetrics(users);

    return NextResponse.json({
      success: true,
      data: metrics,
      generatedAt: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Dashboard metrics calculation error:', error);

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred while calculating dashboard metrics',
      },
    }, { status: 500 });
  }
}

/**
 * Calculate aggregated dashboard metrics from user data
 */
function calculateDashboardMetrics(users: UserActivityData[]): DashboardMetrics {
  const calculator = new HealthScoreCalculator();
  const healthScores: HealthScoreBreakdown[] = users.map(user => calculator.calculate(user));

  const now = new Date();
  const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);

  // Overview metrics
  const totalUsers = users.length;
  const averageHealthScore = Math.round(
    healthScores.reduce((sum, hs) => sum + hs.total, 0) / totalUsers
  );

  // Risk distribution
  const riskDistribution = {
    low: healthScores.filter(hs => hs.riskLevel === 'low').length,
    medium: healthScores.filter(hs => hs.riskLevel === 'medium').length,
    high: healthScores.filter(hs => hs.riskLevel === 'high').length,
    critical: healthScores.filter(hs => hs.riskLevel === 'critical').length,
  };

  // Engagement metrics
  const averageFeatureAdoptionRate = Math.round(
    healthScores.reduce((sum, hs) => sum + hs.components.featureAdoptionRate, 0) / totalUsers
  );
  const averageLoginFrequency = Number((
    healthScores.reduce((sum, hs) => sum + hs.components.loginFrequency, 0) / totalUsers
  ).toFixed(2));

  const activeUsersLast7Days = users.filter(u => new Date(u.lastActiveAt) >= sevenDaysAgo).length;
  const activeUsersLast30Days = users.filter(u => new Date(u.lastActiveAt) >= thirtyDaysAgo).length;

  // Retention metrics
  const averageTenure = Math.round(
    healthScores.reduce((sum, hs) => sum + hs.components.daysSinceSignup, 0) / totalUsers
  );
  const churnRiskUsers = healthScores.filter(hs => hs.riskLevel === 'critical' || hs.riskLevel === 'high').length;

  // Feedback metrics
  const usersWithNps = users.filter(u => u.npsScore !== null && u.npsScore !== undefined);
  const averageNps = usersWithNps.length > 0
    ? Math.round(usersWithNps.reduce((sum, u) => sum + (u.npsScore || 0), 0) / usersWithNps.length)
    : null;

  const sentimentDistribution = {
    positive: users.filter(u => u.feedbackSentiment === 'positive').length,
    neutral: users.filter(u => u.feedbackSentiment === 'neutral').length,
    negative: users.filter(u => u.feedbackSentiment === 'negative').length,
    noFeedback: users.filter(u => !u.feedbackSentiment).length,
  };

  // Determine trend (simplified - in production would compare with historical data)
  const healthScoreTrend: 'up' | 'down' | 'stable' =
    averageHealthScore >= 70 ? 'up' :
    averageHealthScore >= 50 ? 'stable' : 'down';

  return {
    overview: {
      totalUsers,
      averageHealthScore,
      healthScoreTrend,
    },
    riskDistribution,
    engagementMetrics: {
      averageFeatureAdoptionRate,
      averageLoginFrequency,
      activeUsersLast7Days,
      activeUsersLast30Days,
    },
    retentionMetrics: {
      averageTenure,
      churnRiskUsers,
    },
    feedbackMetrics: {
      averageNps,
      sentimentDistribution,
    },
  };
}

/**
 * Get example dashboard metrics for template/preview
 */
function getExampleDashboardMetrics(): DashboardMetrics {
  return {
    overview: {
      totalUsers: 25,
      averageHealthScore: 72,
      healthScoreTrend: 'up',
    },
    riskDistribution: {
      low: 12,
      medium: 8,
      high: 3,
      critical: 2,
    },
    engagementMetrics: {
      averageFeatureAdoptionRate: 58,
      averageLoginFrequency: 4.2,
      activeUsersLast7Days: 18,
      activeUsersLast30Days: 22,
    },
    retentionMetrics: {
      averageTenure: 45,
      churnRiskUsers: 5,
    },
    feedbackMetrics: {
      averageNps: 7,
      sentimentDistribution: {
        positive: 15,
        neutral: 6,
        negative: 2,
        noFeedback: 2,
      },
    },
  };
}
