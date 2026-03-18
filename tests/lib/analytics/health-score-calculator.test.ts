/**
 * Tests for Health Score Calculator
 *
 * Task: OS-20260318091956-B64C - Implement HealthScoreCalculator class with unit tests
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

const FIXED_NOW = new Date('2026-03-18T12:00:00Z');

// Helper to create mock user data
const createMockData = (overrides: Partial<any> = {}): any => ({
  userId: 'user-001',
  signupDate: '2026-02-15T00:00:00Z',
  lastActiveAt: '2026-03-17T14:00:00Z',
  sessionsCount: 20,
  tasksCompleted: 15,
  featuresUsed: ['task_creation', 'agent_collaboration'],
  npsScore: 8,
  feedbackSentiment: 'positive',
  ...overrides,
});

describe('HealthScoreCalculator', () => {
  let HealthScoreCalculator: any;
  let calculator: any;

  beforeEach(async () => {
    vi.resetModules();
    calculator = null;

    // Import with mocked Date
    const module = await import('../../../src/lib/analytics/health-score-calculator');
    HealthScoreCalculator = module.HealthScoreCalculator;
    calculator = new HealthScoreCalculator({ now: () => FIXED_NOW });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('constructor', () => {
    it('should create instance with default features', () => {
      const calc = new HealthScoreCalculator();
      expect(calc).toBeDefined();
    });

    it('should accept custom features', () => {
      const customFeatures = [
        { id: 'custom_feature', name: 'Custom', weight: 1.0 },
      ];
      const calc = new HealthScoreCalculator({ features: customFeatures });
      expect(calc).toBeDefined();
    });

    it('should accept custom now function', () => {
      const customNow = () => new Date('2026-01-01T00:00:00Z');
      const calc = new HealthScoreCalculator({ now: customNow });
      expect(calc).toBeDefined();
    });
  });

  describe('calculate', () => {
    it('should return health score breakdown', () => {
      const data = createMockData();
      const result = calculator.calculate(data);

      expect(result.total).toBeGreaterThanOrEqual(0);
      expect(result.total).toBeLessThanOrEqual(100);
      expect(result.engagementScore).toBeDefined();
      expect(result.activityScore).toBeDefined();
      expect(result.retentionScore).toBeDefined();
      expect(result.feedbackScore).toBeDefined();
      expect(result.riskLevel).toBeDefined();
    });

    it('should include component details', () => {
      const data = createMockData();
      const result = calculator.calculate(data);

      expect(result.components.featureAdoptionRate).toBeDefined();
      expect(result.components.loginFrequency).toBeDefined();
      expect(result.components.daysSinceSignup).toBeDefined();
      expect(result.components.daysSinceActive).toBeDefined();
      expect(result.components.normalizedNps).toBeDefined();
    });

    it('should clamp total score to 0-100', () => {
      // Test with very high values
      const highData = createMockData({
        sessionsCount: 1000,
        tasksCompleted: 500,
        featuresUsed: ['task_creation', 'agent_collaboration', 'standup_automation', 'api_integration', 'custom_workflows'],
        npsScore: 10,
      });
      const highResult = calculator.calculate(highData);
      expect(highResult.total).toBeLessThanOrEqual(100);

      // Test with very low values
      const lowData = createMockData({
        sessionsCount: 0,
        tasksCompleted: 0,
        featuresUsed: [],
        npsScore: -10,
        lastActiveAt: '2026-02-01T00:00:00Z',
      });
      const lowResult = calculator.calculate(lowData);
      expect(lowResult.total).toBeGreaterThanOrEqual(0);
    });
  });

  describe('calculateEngagementScore', () => {
    it('should return score based on feature adoption', () => {
      const data = createMockData({
        featuresUsed: ['task_creation'],
        tasksCompleted: 0,
      });
      const score = calculator.calculateEngagementScore(data);
      expect(score).toBeGreaterThanOrEqual(0);
      expect(score).toBeLessThanOrEqual(100);
    });

    it('should reward task completion', () => {
      const lowTaskData = createMockData({ tasksCompleted: 0 });
      const highTaskData = createMockData({ tasksCompleted: 50 });

      const lowScore = calculator.calculateEngagementScore(lowTaskData);
      const highScore = calculator.calculateEngagementScore(highTaskData);

      expect(highScore).toBeGreaterThan(lowScore);
    });

    it('should reward more feature adoption', () => {
      const fewFeatures = createMockData({
        featuresUsed: ['task_creation'],
        tasksCompleted: 5,
      });
      const manyFeatures = createMockData({
        featuresUsed: ['task_creation', 'agent_collaboration', 'standup_automation'],
        tasksCompleted: 5,
      });

      const fewScore = calculator.calculateEngagementScore(fewFeatures);
      const manyScore = calculator.calculateEngagementScore(manyFeatures);

      expect(manyScore).toBeGreaterThan(fewScore);
    });
  });

  describe('calculateActivityScore', () => {
    it('should return score based on login frequency', () => {
      const data = createMockData({ sessionsCount: 10 });
      const score = calculator.calculateActivityScore(data);
      expect(score).toBeGreaterThanOrEqual(0);
      expect(score).toBeLessThanOrEqual(100);
    });

    it('should reward recent activity', () => {
      const recentData = createMockData({
        lastActiveAt: '2026-03-18T10:00:00Z',
        sessionsCount: 10,
      });
      const oldData = createMockData({
        lastActiveAt: '2026-02-01T00:00:00Z',
        sessionsCount: 10,
      });

      const recentScore = calculator.calculateActivityScore(recentData);
      const oldScore = calculator.calculateActivityScore(oldData);

      expect(recentScore).toBeGreaterThan(oldScore);
    });

    it('should reward higher login frequency', () => {
      const lowFreq = createMockData({ sessionsCount: 5 });
      const highFreq = createMockData({ sessionsCount: 50 });

      const lowScore = calculator.calculateActivityScore(lowFreq);
      const highScore = calculator.calculateActivityScore(highFreq);

      expect(highScore).toBeGreaterThan(lowScore);
    });
  });

  describe('calculateRetentionScore', () => {
    it('should return score based on time since signup', () => {
      const data = createMockData();
      const score = calculator.calculateRetentionScore(data);
      expect(score).toBeGreaterThanOrEqual(0);
      expect(score).toBeLessThanOrEqual(100);
    });

    it('should reward longer tenure', () => {
      const newData = createMockData({
        signupDate: '2026-03-15T00:00:00Z',
        lastActiveAt: '2026-03-18T10:00:00Z',
      });
      const oldData = createMockData({
        signupDate: '2026-01-01T00:00:00Z',
        lastActiveAt: '2026-03-18T10:00:00Z',
      });

      const newScore = calculator.calculateRetentionScore(newData);
      const oldScore = calculator.calculateRetentionScore(oldData);

      expect(oldScore).toBeGreaterThan(newScore);
    });

    it('should penalize inactivity', () => {
      const activeData = createMockData({
        lastActiveAt: '2026-03-18T10:00:00Z',
      });
      const inactiveData = createMockData({
        lastActiveAt: '2026-02-01T00:00:00Z',
      });

      const activeScore = calculator.calculateRetentionScore(activeData);
      const inactiveScore = calculator.calculateRetentionScore(inactiveData);

      expect(activeScore).toBeGreaterThan(inactiveScore);
    });
  });

  describe('calculateFeedbackScore', () => {
    it('should return score based on NPS', () => {
      const data = createMockData({ npsScore: 8 });
      const score = calculator.calculateFeedbackScore(data);
      expect(score).toBeGreaterThanOrEqual(0);
      expect(score).toBeLessThanOrEqual(100);
    });

    it('should reward positive NPS', () => {
      const lowNps = createMockData({ npsScore: 2 });
      const highNps = createMockData({ npsScore: 10 });

      const lowScore = calculator.calculateFeedbackScore(lowNps);
      const highScore = calculator.calculateFeedbackScore(highNps);

      expect(highScore).toBeGreaterThan(lowScore);
    });

    it('should adjust for positive sentiment', () => {
      const neutral = createMockData({
        npsScore: 7,
        feedbackSentiment: 'neutral',
      });
      const positive = createMockData({
        npsScore: 7,
        feedbackSentiment: 'positive',
      });

      const neutralScore = calculator.calculateFeedbackScore(neutral);
      const positiveScore = calculator.calculateFeedbackScore(positive);

      expect(positiveScore).toBeGreaterThanOrEqual(neutralScore);
    });

    it('should adjust for negative sentiment', () => {
      const neutral = createMockData({
        npsScore: 7,
        feedbackSentiment: 'neutral',
      });
      const negative = createMockData({
        npsScore: 7,
        feedbackSentiment: 'negative',
      });

      const neutralScore = calculator.calculateFeedbackScore(neutral);
      const negativeScore = calculator.calculateFeedbackScore(negative);

      expect(negativeScore).toBeLessThanOrEqual(neutralScore);
    });

    it('should handle missing NPS', () => {
      const data = createMockData({ npsScore: null, feedbackSentiment: null });
      const score = calculator.calculateFeedbackScore(data);
      expect(score).toBe(50); // Neutral score
    });

    it('should handle undefined NPS', () => {
      const data = createMockData({ npsScore: undefined, feedbackSentiment: null });
      const score = calculator.calculateFeedbackScore(data);
      expect(score).toBe(50); // Neutral score
    });
  });

  describe('calculateFeatureAdoptionRate', () => {
    it('should return 0 for no features used', () => {
      const data = createMockData({ featuresUsed: [] });
      const rate = calculator.calculateFeatureAdoptionRate(data);
      expect(rate).toBe(0);
    });

    it('should return 100 for all features used', () => {
      const data = createMockData({
        featuresUsed: ['task_creation', 'agent_collaboration', 'standup_automation', 'api_integration', 'custom_workflows'],
      });
      const rate = calculator.calculateFeatureAdoptionRate(data);
      expect(rate).toBe(100);
    });

    it('should return partial rate for some features', () => {
      const data = createMockData({
        featuresUsed: ['task_creation', 'agent_collaboration'],
      });
      const rate = calculator.calculateFeatureAdoptionRate(data);
      expect(rate).toBeGreaterThan(0);
      expect(rate).toBeLessThan(100);
    });
  });

  describe('calculateLoginFrequency', () => {
    it('should calculate logins per week', () => {
      const data = createMockData({
        signupDate: '2026-03-04T00:00:00Z', // 2 weeks ago
        sessionsCount: 14,
      });
      const freq = calculator.calculateLoginFrequency(data);
      expect(freq).toBe(7); // 14 sessions / 2 weeks = 7 per week
    });

    it('should handle same-day signup', () => {
      const data = createMockData({
        signupDate: '2026-03-18T00:00:00Z',
        sessionsCount: 5,
      });
      const freq = calculator.calculateLoginFrequency(data);
      expect(freq).toBe(5);
    });
  });

  describe('normalizeNps', () => {
    it('should normalize NPS 10 to 100', () => {
      const normalized = calculator.normalizeNps(10);
      expect(normalized).toBe(100);
    });

    it('should normalize NPS 0 to 50', () => {
      const normalized = calculator.normalizeNps(0);
      expect(normalized).toBe(50);
    });

    it('should normalize NPS -10 to 0', () => {
      const normalized = calculator.normalizeNps(-10);
      expect(normalized).toBe(0);
    });

    it('should normalize NPS 5 to 75', () => {
      const normalized = calculator.normalizeNps(5);
      expect(normalized).toBe(75);
    });

    it('should return 50 for null', () => {
      const normalized = calculator.normalizeNps(null);
      expect(normalized).toBe(50);
    });

    it('should return 50 for undefined', () => {
      const normalized = calculator.normalizeNps(undefined);
      expect(normalized).toBe(50);
    });
  });

  describe('determineRiskLevel', () => {
    it('should return low for score >= 80', () => {
      expect(calculator.determineRiskLevel(80)).toBe('low');
      expect(calculator.determineRiskLevel(95)).toBe('low');
      expect(calculator.determineRiskLevel(100)).toBe('low');
    });

    it('should return medium for score 50-79', () => {
      expect(calculator.determineRiskLevel(50)).toBe('medium');
      expect(calculator.determineRiskLevel(65)).toBe('medium');
      expect(calculator.determineRiskLevel(79)).toBe('medium');
    });

    it('should return high for score 30-49', () => {
      expect(calculator.determineRiskLevel(30)).toBe('high');
      expect(calculator.determineRiskLevel(40)).toBe('high');
      expect(calculator.determineRiskLevel(49)).toBe('high');
    });

    it('should return critical for score < 30', () => {
      expect(calculator.determineRiskLevel(29)).toBe('critical');
      expect(calculator.determineRiskLevel(15)).toBe('critical');
      expect(calculator.determineRiskLevel(0)).toBe('critical');
    });
  });

  describe('Health score formula validation', () => {
    it('should match documented formula weights', () => {
      // According to docs:
      // healthScore = engagement * 0.3 + activity * 0.25 + retention * 0.25 + feedback * 0.2
      const data = createMockData({
        featuresUsed: ['task_creation', 'agent_collaboration', 'standup_automation'],
        sessionsCount: 20,
        tasksCompleted: 15,
        npsScore: 8,
        feedbackSentiment: 'positive',
      });

      const result = calculator.calculate(data);

      // Verify the calculation matches the formula
      const expectedTotal = Math.round(
        result.engagementScore * 0.30 +
        result.activityScore * 0.25 +
        result.retentionScore * 0.25 +
        result.feedbackScore * 0.20
      );

      expect(result.total).toBe(expectedTotal);
    });

    it('should produce consistent results for same input', () => {
      const data = createMockData();

      const result1 = calculator.calculate(data);
      const result2 = calculator.calculate(data);

      expect(result1.total).toBe(result2.total);
      expect(result1.engagementScore).toBe(result2.engagementScore);
      expect(result1.activityScore).toBe(result2.activityScore);
    });
  });

  describe('Edge cases', () => {
    it('should handle user with zero sessions', () => {
      const data = createMockData({ sessionsCount: 0 });
      const result = calculator.calculate(data);
      expect(result.total).toBeGreaterThanOrEqual(0);
    });

    it('should handle very old signup date', () => {
      const data = createMockData({
        signupDate: '2020-01-01T00:00:00Z',
      });
      const result = calculator.calculate(data);
      expect(result.total).toBeGreaterThanOrEqual(0);
      expect(result.total).toBeLessThanOrEqual(100);
    });

    it('should handle future signup date gracefully', () => {
      const data = createMockData({
        signupDate: '2027-01-01T00:00:00Z',
      });
      const result = calculator.calculate(data);
      expect(result.total).toBeGreaterThanOrEqual(0);
    });
  });
});

describe('Helper functions', () => {
  beforeEach(async () => {
    vi.resetModules();
  });

  describe('getHealthScoreCalculator', () => {
    it('should return singleton instance', async () => {
      const { getHealthScoreCalculator } = await import('../../../src/lib/analytics/health-score-calculator');
      const calc1 = getHealthScoreCalculator();
      const calc2 = getHealthScoreCalculator();
      expect(calc1).toBe(calc2);
    });
  });

  describe('configureHealthScoreCalculator', () => {
    it('should create new instance with options', async () => {
      const { configureHealthScoreCalculator } = await import('../../../src/lib/analytics/health-score-calculator');
      const calc = configureHealthScoreCalculator({
        now: () => FIXED_NOW,
      });
      expect(calc).toBeDefined();
    });
  });

  describe('calculateHealthScore', () => {
    it('should calculate health score for user', async () => {
      const { calculateHealthScore } = await import('../../../src/lib/analytics/health-score-calculator');
      const data = createMockData();
      const result = calculateHealthScore(data);
      expect(result.total).toBeGreaterThanOrEqual(0);
      expect(result.total).toBeLessThanOrEqual(100);
    });
  });

  describe('calculateHealthScores', () => {
    it('should calculate scores for multiple users', async () => {
      const { calculateHealthScores } = await import('../../../src/lib/analytics/health-score-calculator');
      const users = [
        createMockData({ userId: 'user-001' }),
        createMockData({ userId: 'user-002' }),
        createMockData({ userId: 'user-003' }),
      ];

      const results = calculateHealthScores(users);

      expect(results.size).toBe(3);
      expect(results.has('user-001')).toBe(true);
      expect(results.has('user-002')).toBe(true);
      expect(results.has('user-003')).toBe(true);
    });

    it('should return empty map for empty array', async () => {
      const { calculateHealthScores } = await import('../../../src/lib/analytics/health-score-calculator');
      const results = calculateHealthScores([]);
      expect(results.size).toBe(0);
    });
  });
});
