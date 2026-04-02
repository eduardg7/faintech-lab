/**
 * UTM Parameter Capture for Channel Attribution
 * Task: LAB-ANALYTICS-20260401-UTMFALLBACK-PHASE1
 * 
 * Phase 1: Client-side UTM fallback that works WITHOUT backend deployment
 * Enables Week 2 GTM channel attribution (HN, Reddit, LinkedIn, Twitter, direct)
 * 
 * Features:
 * - Extracts 6 UTM parameters from URL
 * - Persists in localStorage to preserve across signup flow
 * - Returns UTM data object for PostHog integration
 * - Graceful degradation if localStorage unavailable
 */

export interface UTMData {
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
  utm_term?: string;
  utm_referrer?: string;
}

const UTM_STORAGE_KEY = 'faintech_utm';
const UTM_PARAMS = [
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'utm_content',
  'utm_term',
] as const;

/**
 * Capture UTM parameters from current page URL
 * Extracts UTM params, stores in localStorage, returns UTM data
 * 
 * @returns UTMData object with captured parameters, or null if none found
 * 
 * @example
 * const utmData = captureUTM();
 * if (utmData) {
 *   console.log('Captured UTM:', utmData);
 *   // Attach to PostHog events
 *   posthog.capture('user_signup', utmData);
 * }
 */
export function captureUTM(): UTMData | null {
  if (typeof window === 'undefined') {
    return null;
  }

  const urlParams = new URLSearchParams(window.location.search);
  const utmData: UTMData = {};

  // Extract all UTM parameters
  UTM_PARAMS.forEach(param => {
    const value = urlParams.get(param);
    if (value) {
      utmData[param] = value;
    }
  });

  // Capture referrer if available
  if (document.referrer) {
    try {
      const referrerUrl = new URL(document.referrer);
      utmData.utm_referrer = referrerUrl.hostname;
    } catch (e) {
      // Invalid referrer URL, skip
    }
  }

  // Store in localStorage if any UTM params found
  const hasUTMParams = Object.values(utmData).some(val => val !== undefined);
  
  if (hasUTMParams) {
    try {
      localStorage.setItem(UTM_STORAGE_KEY, JSON.stringify(utmData));
      
      if (process.env.NODE_ENV === 'development') {
        console.log('[UTM Capture] Stored UTM data:', utmData);
      }
    } catch (e) {
      // localStorage might be disabled (private browsing, quota exceeded)
      console.warn('[UTM Capture] Failed to store UTM data:', e);
    }
    
    return utmData;
  }

  return null;
}

/**
 * Retrieve stored UTM data from localStorage
 * Use this to attach UTM data to analytics events
 * 
 * @returns UTMData object from storage, or null if not found/expired
 * 
 * @example
 * const storedUTM = getStoredUTM();
 * if (storedUTM) {
 *   posthog.capture('user_signup', {
 *     ...storedUTM,
 *     user_id: '123',
 *   });
 * }
 */
export function getStoredUTM(): UTMData | null {
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const stored = localStorage.getItem(UTM_STORAGE_KEY);
    
    if (!stored) {
      return null;
    }

    const utmData = JSON.parse(stored) as UTMData;
    
    if (process.env.NODE_ENV === 'development') {
      console.log('[UTM Capture] Retrieved stored UTM data:', utmData);
    }
    
    return utmData;
  } catch (e) {
    console.error('[UTM Capture] Failed to parse stored UTM data:', e);
    return null;
  }
}

/**
 * Clear stored UTM data from localStorage
 * Call this after successful signup to prevent stale data
 */
export function clearStoredUTM(): void {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    localStorage.removeItem(UTM_STORAGE_KEY);
    
    if (process.env.NODE_ENV === 'development') {
      console.log('[UTM Capture] Cleared stored UTM data');
    }
  } catch (e) {
    console.warn('[UTM Capture] Failed to clear UTM data:', e);
  }
}

/**
 * Attach UTM properties to PostHog event
 * Helper function that combines stored UTM with event properties
 * 
 * @param eventName - PostHog event name
 * @param properties - Event properties
 * @param posthog - PostHog instance
 * 
 * @example
 * import { getPostHog } from '../analytics';
 * 
 * const posthog = getPostHog();
 * if (posthog) {
 *   trackEventWithUTM('user_signup', { user_id: '123' }, posthog);
 * }
 */
export function trackEventWithUTM(
  eventName: string,
  properties: Record<string, unknown>,
  posthog: { capture: (name: string, props: Record<string, unknown>) => void }
): void {
  const utmData = getStoredUTM();
  
  const enrichedProperties = {
    ...properties,
    ...utmData, // Attach UTM data to event
  };

  posthog.capture(eventName, enrichedProperties);

  if (process.env.NODE_ENV === 'development') {
    console.log('[UTM Capture] Event tracked with UTM:', eventName, enrichedProperties);
  }
}

/**
 * Debug helper: Log current UTM state
 * Call from browser console: window.debugUTM()
 */
export function debugUTM(): void {
  if (typeof window === 'undefined') {
    console.log('[UTM Capture] Server-side, no UTM data available');
    return;
  }

  console.group('[UTM Capture] Debug Info');
  console.log('Current URL:', window.location.href);
  console.log('URL params:', window.location.search);
  console.log('Stored UTM:', getStoredUTM());
  console.groupEnd();
}

// Expose debug function globally in development
if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
  (window as any).debugUTM = debugUTM;
}
