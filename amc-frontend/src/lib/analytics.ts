/**
 * Analytics Event Tracking for Faintech Lab
 *
 * Tracks core user events using PostHog
 * Task: OS-20260321013947-EC6B - AC2/5
 *
 * Events:
 * - user_signup
 * - email_verified
 * - agent_created
 * - memory_created
 * - search_executed
 * - user_login
 */

import { PostHog } from 'posthog-js';

let posthogInstance: PostHog | null = null;

// Event names
export const ANALYTICS_EVENTS = {
  USER_SIGNUP: 'user_signup',
  EMAIL_VERIFIED: 'email_verified',
  AGENT_CREATED: 'agent_created',
  MEMORY_CREATED: 'memory_created',
  SEARCH_EXECUTED: 'search_executed',
  USER_LOGIN: 'user_login',
} as const;

export type AnalyticsEvent = typeof ANALYTICS_EVENTS[keyof typeof ANALYTICS_EVENTS];

export interface AnalyticsEventProperties {
  user_id?: string;
  timestamp?: string;
  [key: string]: unknown;
}

/**
 * Initialize PostHog analytics
 * Call this once during app initialization
 */
export function initAnalytics(): void {
  if (typeof window === 'undefined') return;

  const posthogKey = process.env.NEXT_PUBLIC_POSTHOG_KEY;
  const posthogHost = process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com';

  if (!posthogKey) {
    console.warn('[Analytics] PostHog key not configured. Analytics disabled.');
    return;
  }

  // Dynamic import for PostHog
  if (posthogInstance) {
    console.warn('[Analytics] Already initialized');
    return;
  }

  // @ts-ignore - PostHog will be available at runtime
  const { posthog } = require('posthog-js');
  posthogInstance = posthog(posthogKey, {
    api_host: posthogHost,
    loaded: (ph: any) => {
      posthogInstance = ph;
      console.log('[Analytics] PostHog initialized');
    },
  });
}

/**
 * Track an analytics event
 */
export function trackEvent(
  eventName: AnalyticsEvent,
  properties?: AnalyticsEventProperties
): void {
  if (!posthogInstance) {
    console.warn('[Analytics] PostHog not initialized. Event not tracked:', eventName);
    return;
  }

  const enrichedProperties = {
    ...properties,
    timestamp: properties?.timestamp || new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
  };

  console.log('[Analytics] Tracking:', eventName, enrichedProperties);
  posthogInstance.capture(eventName, enrichedProperties);
}

/**
 * Track user signup (called after onboarding completion)
 */
export function trackUserSignup(userId: string, email?: string): void {
  trackEvent(ANALYTICS_EVENTS.USER_SIGNUP, {
    user_id: userId,
    email,
  });
}

/**
 * Track email verification (if applicable)
 */
export function trackEmailVerified(userId: string): void {
  trackEvent(ANALYTICS_EVENTS.EMAIL_VERIFIED, {
    user_id: userId,
  });
}

/**
 * Track agent creation
 */
export function trackAgentCreated(
  userId: string,
  agentId: string,
  agentType?: string
): void {
  trackEvent(ANALYTICS_EVENTS.AGENT_CREATED, {
    user_id: userId,
    agent_id: agentId,
    agent_type: agentType,
  });
}

/**
 * Track memory creation
 */
export function trackMemoryCreated(
  userId: string,
  memoryId: string,
  memoryType?: string
): void {
  trackEvent(ANALYTICS_EVENTS.MEMORY_CREATED, {
    user_id: userId,
    memory_id: memoryId,
    memory_type: memoryType,
  });
}

/**
 * Track search execution
 */
export function trackSearchExecuted(
  userId: string,
  query: string,
  resultCount?: number
): void {
  trackEvent(ANALYTICS_EVENTS.SEARCH_EXECUTED, {
    user_id: userId,
    query,
    result_count: resultCount,
  });
}

/**
 * Track user login
 */
export function trackUserLogin(userId: string, method?: string): void {
  trackEvent(ANALYTICS_EVENTS.USER_LOGIN, {
    user_id: userId,
    login_method: method,
  });
}

/**
 * Get PostHog instance (for advanced use cases)
 */
export function getPostHog(): PostHog | null {
  return posthogInstance;
}
