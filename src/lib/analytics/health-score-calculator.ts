/**
 * Health Score Calculator
 *
 * Calculates composite health scores for beta users based on:
 * - Engagement Score (30%): Based on feature adoption
 * - Activity Score (25%): Based on login frequency
 * - Retention Score (25%): Based on time since signup
 * - Feedback Score (20%): Based on NPS/sentiment
 *
 * Task: OS-20260318091956-B64C - Implement HealthScoreCalculator class
 */

export interface UserActivityData {
  userId: string;
  signupDate: string;
  lastActiveAt: string;
  sessionsCount: number;
  tasksCompleted: number;
  featuresUsed: string[];
  npsScore?: number | null;
  feedbackSentiment?: 'positive' | 'neutral' | 'negative' | null;
}

export interface FeatureDefinition {
  id: string;
  name: string;
  weight: number;
}

export interface HealthScoreBreakdown {
  total: number;
  engagementScore: number;
  activityScore: number;
  retentionScore: number;
  feedbackScore: number;
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  components: {
    featureAdoptionRate: number;
    loginFrequency: number;
    daysSinceSignup: number;
    daysSinceActive: number;
    normalizedNps: number;
  };
}

const DEFAULT_FEATURES: FeatureDefinition[] = [
  { id: 'task_creation', name: 'Task Creation', weight: 1.0 },
  { id: 'agent_collaboration', name: 'Agent Collaboration', weight: 1.2 },
  { id: 'standup_automation', name: 'Standup Automation', weight: 1.1 },
  { id: 'api_integration', name: 'API Integration', weight: 1.3 },
  { id: 'custom_workflows', name: 'Custom Workflows', weight: 1.2 },
];

const WEIGHTS = {
  engagement: 0.30,
  activity: 0.25,
  retention: 0.25,
  feedback: 0.20,
} as const;

const RISK_THRESHOLDS = {
  low: 80,
  medium: 50,
  high: 30,
} as const;

export class HealthScoreCalculator {
  private features: FeatureDefinition[];
  private now: () => Date;

  constructor(options?: { features?: FeatureDefinition[]; now?: () => Date }) {
    this.features = options?.features || DEFAULT_FEATURES;
    this.now = options?.now || (() => new Date());
  }

  /**
   * Calculate comprehensive health score for a user
   */
  calculate(data: UserActivityData): HealthScoreBreakdown {
    const engagementScore = this.calculateEngagementScore(data);
    const activityScore = this.calculateActivityScore(data);
    const retentionScore = this.calculateRetentionScore(data);
    const feedbackScore = this.calculateFeedbackScore(data);

    const total = Math.round(
      engagementScore * WEIGHTS.engagement +
      activityScore * WEIGHTS.activity +
      retentionScore * WEIGHTS.retention +
      feedbackScore * WEIGHTS.feedback
    );

    const clampedTotal = Math.max(0, Math.min(100, total));

    return {
      total: clampedTotal,
      engagementScore,
      activityScore,
      retentionScore,
      feedbackScore,
      riskLevel: this.determineRiskLevel(clampedTotal),
      components: {
        featureAdoptionRate: this.calculateFeatureAdoptionRate(data),
        loginFrequency: this.calculateLoginFrequency(data),
        daysSinceSignup: this.daysSince(data.signupDate),
        daysSinceActive: this.daysSince(data.lastActiveAt),
        normalizedNps: this.normalizeNps(data.npsScore),
      },
    };
  }

  /**
   * Calculate engagement score based on feature adoption
   */
  calculateEngagementScore(data: UserActivityData): number {
    const adoptionRate = this.calculateFeatureAdoptionRate(data);

    // Base score from adoption rate (0-70 points)
    let score = adoptionRate * 0.7;

    // Bonus for task completion (0-30 points)
    const tasksBonus = Math.min(30, data.tasksCompleted * 2);
    score += tasksBonus;

    return Math.round(Math.max(0, Math.min(100, score)));
  }

  /**
   * Calculate activity score based on login frequency
   */
  calculateActivityScore(data: UserActivityData): number {
    const loginFrequency = this.calculateLoginFrequency(data);
    const daysSinceActive = this.daysSince(data.lastActiveAt);

    // Base score from login frequency (0-50 points)
    let score = Math.min(50, loginFrequency * 10);

    // Recency bonus (up to 50 points, decreasing with inactivity)
    if (daysSinceActive <= 1) {
      score += 50;
    } else if (daysSinceActive <= 3) {
      score += 40;
    } else if (daysSinceActive <= 7) {
      score += 25;
    } else if (daysSinceActive <= 14) {
      score += 10;
    }
    // No bonus if inactive > 14 days

    return Math.round(Math.max(0, Math.min(100, score)));
  }

  /**
   * Calculate retention score based on time since signup
   */
  calculateRetentionScore(data: UserActivityData): number {
    const daysSinceSignup = this.daysSince(data.signupDate);
    const daysSinceActive = this.daysSince(data.lastActiveAt);

    // Retention score increases with time but is penalized by inactivity
    let score = 50; // Base score

    // Time bonus (users who stay longer get higher scores)
    if (daysSinceSignup >= 60) {
      score += 30;
    } else if (daysSinceSignup >= 30) {
      score += 20;
    } else if (daysSinceSignup >= 14) {
      score += 10;
    } else if (daysSinceSignup >= 7) {
      score += 5;
    }

    // Inactivity penalty
    if (daysSinceActive > 14) {
      score -= 40;
    } else if (daysSinceActive > 7) {
      score -= 20;
    }

    return Math.round(Math.max(0, Math.min(100, score)));
  }

  /**
   * Calculate feedback score based on NPS and sentiment
   */
  calculateFeedbackScore(data: UserActivityData): number {
    const normalizedNps = this.normalizeNps(data.npsScore);
    const sentiment = data.feedbackSentiment;

    // Base score from normalized NPS
    let score = normalizedNps;

    // Sentiment adjustment
    if (sentiment === 'positive') {
      score = Math.min(100, score + 10);
    } else if (sentiment === 'negative') {
      score = Math.max(0, score - 15);
    }

    return Math.round(Math.max(0, Math.min(100, score)));
  }

  /**
   * Calculate feature adoption rate (0-100)
   */
  calculateFeatureAdoptionRate(data: UserActivityData): number {
    if (this.features.length === 0) return 0;

    const usedFeatures = new Set(data.featuresUsed);
    const totalWeight = this.features.reduce((sum, f) => sum + f.weight, 0);
    const adoptedWeight = this.features
      .filter(f => usedFeatures.has(f.id))
      .reduce((sum, f) => sum + f.weight, 0);

    return Math.round((adoptedWeight / totalWeight) * 100);
  }

  /**
   * Calculate login frequency (logins per week since signup)
   */
  calculateLoginFrequency(data: UserActivityData): number {
    const daysSinceSignup = this.daysSince(data.signupDate);
    if (daysSinceSignup === 0) return data.sessionsCount;

    const weeksSinceSignup = Math.max(1, daysSinceSignup / 7);
    return Number((data.sessionsCount / weeksSinceSignup).toFixed(2));
  }

  /**
   * Normalize NPS score from -10..10 range to 0..100 range
   */
  normalizeNps(nps: number | null | undefined): number {
    if (nps === null || nps === undefined) {
      return 50; // Neutral score if no NPS
    }

    // NPS is -10 to 10, normalize to 0-100
    return Math.round(((nps + 10) / 20) * 100);
  }

  /**
   * Determine risk level based on total health score
   */
  determineRiskLevel(score: number): 'low' | 'medium' | 'high' | 'critical' {
    if (score >= RISK_THRESHOLDS.low) return 'low';
    if (score >= RISK_THRESHOLDS.medium) return 'medium';
    if (score >= RISK_THRESHOLDS.high) return 'high';
    return 'critical';
  }

  /**
   * Calculate days since a date
   */
  private daysSince(dateStr: string): number {
    const date = new Date(dateStr);
    const now = this.now();
    const diffMs = now.getTime() - date.getTime();
    return Math.max(0, Math.floor(diffMs / (1000 * 60 * 60 * 24)));
  }
}

// Singleton instance
let calculatorInstance: HealthScoreCalculator | null = null;

/**
 * Get or create calculator instance
 */
export function getHealthScoreCalculator(): HealthScoreCalculator {
  if (!calculatorInstance) {
    calculatorInstance = new HealthScoreCalculator();
  }
  return calculatorInstance;
}

/**
 * Configure global calculator
 */
export function configureHealthScoreCalculator(
  options?: ConstructorParameters<typeof HealthScoreCalculator>[0]
): HealthScoreCalculator {
  calculatorInstance = new HealthScoreCalculator(options);
  return calculatorInstance;
}

/**
 * Calculate health score for a single user
 */
export function calculateHealthScore(data: UserActivityData): HealthScoreBreakdown {
  return getHealthScoreCalculator().calculate(data);
}

/**
 * Calculate health scores for multiple users
 */
export function calculateHealthScores(
  users: UserActivityData[]
): Map<string, HealthScoreBreakdown> {
  const calculator = getHealthScoreCalculator();
  const results = new Map<string, HealthScoreBreakdown>();

  for (const user of users) {
    results.set(user.userId, calculator.calculate(user));
  }

  return results;
}

export default HealthScoreCalculator;
