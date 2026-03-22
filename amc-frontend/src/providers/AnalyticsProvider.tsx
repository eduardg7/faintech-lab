"use client";

import { useEffect } from "react";
import { initAnalytics } from "@/lib/analytics";

/**
 * Analytics Provider - Initializes PostHog on client-side mount
 * Task: OS-20260321013947-704F - AC3/5 (Wire up analytics initialization)
 */
export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize PostHog analytics on client-side mount
    initAnalytics();
  }, []);

  return <>{children}</>;
}
