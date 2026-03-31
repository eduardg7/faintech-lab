'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import OnboardingFlow from '@/components/OnboardingFlow';
import LandingPage from '@/components/LandingPage';
import MemoryList from '@/components/MemoryList';

export default function Home() {
  const { isAuthenticated } = useAuth();
  const [showOnboarding, setShowOnboarding] = useState(false);

  // If authenticated, check onboarding status
  if (isAuthenticated) {
    // Check if onboarding was completed previously
    const onboardingCompleted = typeof window !== 'undefined' && localStorage.getItem('amc_onboarding_completed') === 'true';

    if (!onboardingCompleted) {
      return <OnboardingFlow />;
    }

    return <MemoryList />;
  }

  // For unauthenticated users:
  // Show landing page first, then onboarding flow when they click "Get Started"
  if (showOnboarding) {
    return <OnboardingFlow />;
  }

  return <LandingPage onStartOnboarding={() => setShowOnboarding(true)} />;
}
