'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import {
  trackOnboardingStarted,
  trackSignupCompleted,
  trackFirstMemoryCreated,
  trackEvent,
} from '@/lib/analytics';

type StepId = 'welcome' | 'workspace' | 'api-key' | 'first-memory' | 'success';

const steps: StepId[] = ['welcome', 'workspace', 'api-key', 'first-memory', 'success'];
const defaultMemory = 'Track product decisions, customer feedback, and engineering learnings in one shared memory cloud.';

export default function OnboardingFlow() {
  const { setApiKey } = useAuth();
  const [step, setStep] = useState<StepId>('welcome');
  const [workspaceName, setWorkspaceName] = useState('Faintech Lab');
  const [key, setKey] = useState('');
  const [memoryDraft, setMemoryDraft] = useState(defaultMemory);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const currentIndex = steps.indexOf(step);
  const progress = ((currentIndex + 1) / steps.length) * 100;

  // Track onboarding started on first mount
  useEffect(() => {
    const hasStartedOnboarding = sessionStorage.getItem('amc_onboarding_started');
    if (!hasStartedOnboarding) {
      // Generate a temporary user ID for tracking purposes
      const tempUserId = `temp_user_${Date.now()}`;
      trackOnboardingStarted(tempUserId, { onboarding_version: 'v1' });
      sessionStorage.setItem('amc_onboarding_started', 'true');
      sessionStorage.setItem('amc_temp_user_id', tempUserId);
    }
  }, []);

  const generatedPreviewKey = useMemo(() => {
    const slug = workspaceName
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_+|_+$/g, '') || 'workspace';

    return `amc_live_${slug}_preview_2026`;
  }, [workspaceName]);

  const goToStep = (nextStep: StepId) => {
    setError('');
    setCopied(false);

    // Track step completion if moving forward
    const nextIndex = steps.indexOf(nextStep);
    if (nextIndex > currentIndex) {
      trackEvent('onboarding_step_completed' as any, {
        step: nextStep,
        step_number: nextIndex + 1,
        total_steps: steps.length,
        progress_percent: Math.round(((nextIndex + 1) / steps.length) * 100),
        timestamp: new Date().toISOString(),
      });
    }

    setStep(nextStep);
  };

  const handleWorkspaceSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!workspaceName.trim()) {
      setError('Choose a workspace name to continue.');
      return;
    }

    goToStep('api-key');
  };

  const handleApiKeySubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!key.trim()) {
      setError('Paste the API key to unlock the workspace.');
      return;
    }

    if (!key.startsWith('amc_live_')) {
      setError('Invalid API key format. Key should start with "amc_live_".');
      return;
    }

    goToStep('first-memory');
  };

  const handleCopyPreview = async () => {
    try {
      await navigator.clipboard.writeText(generatedPreviewKey);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  };

  const finishOnboarding = () => {
    const trimmedWorkspace = workspaceName.trim();
    const trimmedMemory = memoryDraft.trim();
    const trimmedKey = key.trim();

    // Get or generate user ID for tracking
    const userId = sessionStorage.getItem('amc_temp_user_id') || `user_${Date.now()}`;

    // Track signup completion (activation funnel step 1)
    trackSignupCompleted(userId);

    // Track first memory creation (activation funnel step 3)
    trackFirstMemoryCreated(userId, {
      memory_id: `memory_${Date.now()}`,
      memory_type: 'onboarding_draft',
    });

    // Track final step completion
    trackEvent('onboarding_completed' as any, {
      workspace_name: trimmedWorkspace,
      has_custom_memory: trimmedMemory !== defaultMemory,
      timestamp: new Date().toISOString(),
    });

    localStorage.setItem('amc_onboarding_completed', 'true');
    localStorage.setItem('amc_workspace_name', trimmedWorkspace);
    localStorage.setItem('amc_first_memory_draft', trimmedMemory);
    localStorage.setItem('amc_onboarding_completed_at', new Date().toISOString());
    setApiKey(trimmedKey);
    goToStep('success');
  };

  const cardClass = 'rounded-3xl border border-slate-200 bg-white/95 p-6 shadow-xl shadow-slate-200/70 sm:p-8';

  return (
    <main id="main-content" className="min-h-screen bg-slate-950 px-4 py-10 text-slate-950 sm:px-6 lg:px-8">
      <div className="mx-auto grid max-w-6xl gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <section className="rounded-[32px] border border-slate-800 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 p-8 text-white shadow-2xl shadow-slate-950/30 sm:p-10">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm text-slate-200">
            <span className="h-2 w-2 rounded-full bg-amc-success" />
            Guided first-run setup
          </div>
          <h1 className="max-w-xl text-4xl font-semibold tracking-tight sm:text-5xl">
            Bring your agent workspace online in under five minutes.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
            This onboarding flow gets a new team from zero to first memory write with a clear workspace,
            a ready API key, and a safe first prompt to test the platform.
          </p>

          <div className="mt-10 grid gap-4 sm:grid-cols-3">
            {[
              ['Step 1', 'Clarify the workspace and why it exists.'],
              ['Step 2', 'Connect auth and save the first API key.'],
              ['Step 3', 'Write the first memory, then open the dashboard.'],
            ].map(([title, copy]) => (
              <div key={title} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="text-sm font-semibold text-white">{title}</p>
                <p className="mt-2 text-sm leading-6 text-slate-300">{copy}</p>
              </div>
            ))}
          </div>

          <div className="mt-10 rounded-2xl border border-white/10 bg-black/20 p-5">
            <div className="flex items-center justify-between text-sm text-slate-300">
              <span>Flow completion</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="mt-3 h-2 rounded-full bg-white/10">
              <div className="h-2 rounded-full bg-gradient-to-r from-amc-primary via-amc-secondary to-amc-success" style={{ width: `${progress}%` }} />
            </div>
            <ol className="mt-4 space-y-2 text-sm text-slate-300">
              {steps.map((item, index) => {
                const active = index <= currentIndex;
                return (
                  <li key={item} className={`flex items-center gap-3 ${active ? 'text-white' : 'text-slate-500'}`}>
                    <span className={`flex h-6 w-6 items-center justify-center rounded-full border text-xs ${active ? 'border-amc-success bg-amc-success/20' : 'border-white/10'}`}>
                      {index + 1}
                    </span>
                    <span className="capitalize">{item.replace('-', ' ')}</span>
                  </li>
                );
              })}
            </ol>
          </div>
        </section>

        <section className={cardClass}>
          {step === 'welcome' && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">Welcome</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Persistent memory for your AI team</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  Start with a lightweight guided setup before opening the dashboard. You can refine the
                  workspace details later without losing this first-run progress.
                </p>
              </div>
              <div className="grid gap-3 rounded-2xl bg-slate-50 p-4 text-sm text-slate-600">
                <p>• Capture team decisions and product learnings in one place.</p>
                <p>• Use API-key auth to protect workspace data per team.</p>
                <p>• Give a first memory example so new users understand the value instantly.</p>
              </div>
              <button
                type="button"
                onClick={() => goToStep('workspace')}
                className="inline-flex w-full items-center justify-center rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              >
                Start onboarding
              </button>
            </div>
          )}

          {step === 'workspace' && (
            <form className="space-y-6" onSubmit={handleWorkspaceSubmit}>
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">Workspace setup</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Name the workspace</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  This name seeds the API-key preview and gives the onboarding flow a team-specific tone.
                </p>
              </div>
              <div>
                <label htmlFor="workspace-name" className="block text-sm font-medium text-slate-700">
                  Workspace name
                </label>
                <input
                  id="workspace-name"
                  name="workspace-name"
                  value={workspaceName}
                  onChange={(event) => setWorkspaceName(event.target.value)}
                  className="mt-2 block w-full rounded-2xl border border-slate-300 px-4 py-3 text-slate-950 outline-none ring-0 transition focus:border-amc-primary focus:ring-2 focus:ring-amc-primary/20"
                  placeholder="Acme Research Workspace"
                />
              </div>
              {error && <p className="text-sm text-amc-error">{error}</p>}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => goToStep('welcome')}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                >
                  Back
                </button>
                <button
                  type="submit"
                  className="inline-flex flex-1 items-center justify-center rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
                >
                  Continue
                </button>
              </div>
            </form>
          )}

          {step === 'api-key' && (
            <form className="space-y-6" onSubmit={handleApiKeySubmit} noValidate>
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">API access</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Generate and save the first API key</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  Backend auto-generation is still pending, so this frontend slice shows the final UX with a
                  preview key and copy affordance while preserving the current manual auth path.
                </p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Preview key</p>
                <p className="mt-2 break-all rounded-xl bg-slate-950 px-4 py-3 font-mono text-sm text-emerald-300">
                  {generatedPreviewKey}
                </p>
                <button
                  type="button"
                  onClick={handleCopyPreview}
                  className="mt-3 inline-flex items-center rounded-xl border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-white"
                >
                  {copied ? 'Preview copied' : 'Copy preview'}
                </button>
              </div>
              <div>
                <label htmlFor="api-key" className="block text-sm font-medium text-slate-700">
                  Paste active API key
                </label>
                <input
                  id="api-key"
                  name="api-key"
                  type="password"
                  autoComplete="off"
                  aria-describedby={error ? 'api-key-error' : undefined}
                  value={key}
                  onChange={(event) => setKey(event.target.value)}
                  className="mt-2 block w-full rounded-2xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-amc-primary focus:ring-2 focus:ring-amc-primary/20"
                  placeholder="amc_live_xxxxxxxxxxxxxxxxxxxx"
                />
              </div>
              {error && (
                <p id="api-key-error" className="text-sm text-amc-error" role="alert">
                  {error}
                </p>
              )}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => goToStep('workspace')}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                >
                  Back
                </button>
                <button
                  type="submit"
                  className="inline-flex flex-1 items-center justify-center rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
                >
                  Continue
                </button>
              </div>
            </form>
          )}

          {step === 'first-memory' && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">First memory</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Teach the team what to store</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  Give new users a realistic starting point they can edit before sending the first memory to
                  the API. This primes the value prop before the dashboard loads.
                </p>
              </div>
              <div>
                <label htmlFor="memory-draft" className="block text-sm font-medium text-slate-700">
                  First memory tutorial draft
                </label>
                <textarea
                  id="memory-draft"
                  name="memory-draft"
                  rows={6}
                  value={memoryDraft}
                  onChange={(event) => setMemoryDraft(event.target.value)}
                  className="mt-2 block w-full rounded-2xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-amc-primary focus:ring-2 focus:ring-amc-primary/20"
                />
              </div>
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
                Completion state is saved to localStorage now so returning users can bypass the first-run flow.
                Hook the final submit CTA to the upcoming API key generation + analytics endpoints in the next slice.
              </div>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => goToStep('api-key')}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                >
                  Back
                </button>
                <button
                  type="button"
                  onClick={finishOnboarding}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl bg-amc-success px-4 py-3 text-sm font-semibold text-white transition hover:bg-emerald-600"
                >
                  Mark onboarding complete
                </button>
              </div>
            </div>
          )}

          {step === 'success' && (
            <div className="space-y-6">
              <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-100 text-2xl text-emerald-700">
                ✓
              </div>
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-success">Success</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Ready to code</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {workspaceName.trim() || 'Your workspace'} is configured. The API key is stored locally and the
                  first memory draft is saved as onboarding seed content.
                </p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                The dashboard will open automatically after this screen because the auth context now has a valid key.
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
