'use client';

import { useAuth } from '@/contexts/AuthContext';
import OnboardingFlow from '@/components/OnboardingFlow';
import MemoryList from '@/components/MemoryList';

export default function Home() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <OnboardingFlow />;
  }

  return <MemoryList />;
}
