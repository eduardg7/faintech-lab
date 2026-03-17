'use client';

import { useAuth } from '@/contexts/AuthContext';
import OnboardingFlow from '@/components/OnboardingFlow';
import MemoryList from '@/components/MemoryList';

export default function Home() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <OnboardingFlow />;
  }

  // Check if onboarding was completed previously
  const onboardingCompleted = typeof window !== 'undefined' && localStorage.getItem('amc_onboarding_completed') === 'true';

  if (!onboardingCompleted) {
    return <OnboardingFlow />;
  }

  return <MemoryList />;
}
