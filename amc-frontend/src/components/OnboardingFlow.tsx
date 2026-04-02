'use client';

import { FormEvent, useEffect, useMemo, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import {
  trackOnboardingStarted,
  trackSignupCompleted,
  trackFirstMemoryCreated,
  trackEvent,
} from '@/lib/analytics';

type StepId = 'welcome' | 'agent-setup' | 'first-memory' | 'search-memory' | 'success';

const steps: StepId[] = ['welcome', 'agent-setup', 'first-memory', 'search-memory', 'success'];
const defaultMemory = 'Track product decisions, customer feedback, and engineering learnings in one shared memory cloud.';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1';

// Types for API responses
interface MemoryResponse {
  id: string;
  workspace_id: string;
  agent_id: string;
  project_id: string | null;
  memory_type: string;
  content: string;
  tags: string[];
  metadata: Record<string, unknown>;
  importance: number;
  created_at: string;
  updated_at: string | null;
}

interface SearchResult {
  id: string;
  workspace_id: string;
  agent_id: string;
  project_id: string | null;
  memory_type: string;
  content: string;
  tags: string[];
  relevance_score: number;
  created_at: string;
  updated_at: string | null;
}

interface SearchResponse {
  results: SearchResult[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  query_time_ms: number;
}

export default function OnboardingFlow() {
  const { setApiKey } = useAuth();
  const [step, setStep] = useState<StepId>('welcome');
  const [agentName, setAgentName] = useState('My First Agent');
  const [agentRole, setAgentRole] = useState('assistant');
  const [key, setKey] = useState('');
  const [memoryDraft, setMemoryDraft] = useState(defaultMemory);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [createdMemory, setCreatedMemory] = useState<MemoryResponse | null>(null);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchTimeMs, setSearchTimeMs] = useState<number | null>(null);

  const currentIndex = steps.indexOf(step);
  const progress = ((currentIndex + 1) / steps.length) * 100;

  // Track onboarding started on first mount
  useEffect(() => {
    const hasStartedOnboarding = sessionStorage.getItem('amc_onboarding_started');
    if (!hasStartedOnboarding) {
      const tempUserId = `temp_user_${Date.now()}`;
      trackOnboardingStarted(tempUserId, { onboarding_version: 'v2' });
      sessionStorage.setItem('amc_onboarding_started', 'true');
      sessionStorage.setItem('amc_temp_user_id', tempUserId);
    }
  }, []);

  const generatedPreviewKey = useMemo(() => {
    const slug = agentName
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_+|_+$/g, '') || 'agent';

    return `amc_live_${slug}_preview_2026`;
  }, [agentName]);

  const goToStep = (nextStep: StepId) => {
    setError('');
    setCopied(false);

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

  const handleAgentSetupSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!agentName.trim()) {
      setError('Enter an agent name to continue.');
      return;
    }

    goToStep('first-memory');
  };

  const handleMemorySubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!key.trim()) {
      setError('API key is required to create a memory.');
      return;
    }

    if (!key.startsWith('amc_live_')) {
      setError('Invalid API key format. Key should start with "amc_live_".');
      const errorElement = document.getElementById('api-key-error');
      if (errorElement) {
        errorElement.focus();
      }
      return;
    }

    if (!memoryDraft.trim()) {
      setError('Enter a memory to save.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/memories`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${key.trim()}`,
        },
        body: JSON.stringify({
          agent_id: agentName.trim().toLowerCase().replace(/[^a-z0-9_]+/g, '_'),
          project_id: 'onboarding',
          memory_type: 'learning',
          content: memoryDraft.trim(),
          tags: ['onboarding', 'first-memory'],
          metadata: {
            source: 'onboarding_flow',
            agent_role: agentRole,
          },
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to create memory: ${response.status}`);
      }

      const memory: MemoryResponse = await response.json();
      setCreatedMemory(memory);

      const userId = sessionStorage.getItem('amc_temp_user_id') || `user_${Date.now()}`;
      trackFirstMemoryCreated(userId, {
        memory_id: memory.id,
        memory_type: memory.memory_type,
      });

      // Set search query to demonstrate value loop
      const words = memoryDraft.trim().split(' ').slice(0, 3).join(' ');
      setSearchQuery(words || 'memory');

      goToStep('search-memory');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create memory. Please check your API key.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!key.trim() || !searchQuery.trim()) {
      setError('Enter a search query.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const params = new URLSearchParams({
        q: searchQuery.trim(),
        page: '1',
        page_size: '5',
      });

      const response = await fetch(`${API_BASE_URL}/search/keyword?${params}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${key.trim()}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Search failed: ${response.status}`);
      }

      const data: SearchResponse = await response.json();
      setSearchResults(data.results);
      setSearchTimeMs(data.query_time_ms);

      trackEvent('onboarding_search_completed' as any, {
        query: searchQuery,
        results_count: data.results.length,
        query_time_ms: data.query_time_ms,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed.');
    } finally {
      setIsLoading(false);
    }
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
    const trimmedAgent = agentName.trim();
    const trimmedMemory = memoryDraft.trim();
    const trimmedKey = key.trim();

    const userId = sessionStorage.getItem('amc_temp_user_id') || `user_${Date.now()}`;

    trackSignupCompleted(userId);

    trackEvent('onboarding_completed' as any, {
      agent_name: trimmedAgent,
      has_custom_memory: trimmedMemory !== defaultMemory,
      memory_created: !!createdMemory,
      search_performed: searchResults.length > 0,
      timestamp: new Date().toISOString(),
    });

    localStorage.setItem('amc_onboarding_completed', 'true');
    localStorage.setItem('amc_agent_name', trimmedAgent);
    localStorage.setItem('amc_first_memory_draft', trimmedMemory);
    localStorage.setItem('amc_onboarding_completed_at', new Date().toISOString());

    if (createdMemory) {
      localStorage.setItem('amc_first_memory_id', createdMemory.id);
    }

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
              ['Step 1', 'Configure your first AI agent.'],
              ['Step 2', 'Write a memory to the API.'],
              ['Step 3', 'Search and retrieve your memory.'],
            ].map(([title, copy]) => (
              <div key={title} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <p className="text-sm font-semibold text-white">{title}</p>
                <p className="mt-2 text-sm leading-6 text-slate-300">{copy}</p>
              </div>
            ))}
          </div>

          <div className="mt-10 rounded-2xl border border-white/10 bg-black/20 p-5">
            <div className="flex items-center justify-between text-sm text-slate-300">
              <span id="onboarding-progress-label">Flow completion</span>
              <span aria-labelledby="onboarding-progress-label">{Math.round(progress)}%</span>
            </div>
            <div
              className="mt-3 h-2 rounded-full bg-white/10"
              role="progressbar"
              aria-valuenow={Math.round(progress)}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-labelledby="onboarding-progress-label"
            >
              <div
                className="h-2 rounded-full bg-gradient-to-r from-amc-primary via-amc-secondary to-amc-success"
                style={{ width: `${progress}%` }}
                aria-label={`${Math.round(progress)}% complete`}
              />
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
              <div className="space-y-3">
                <button
                  type="button"
                  onClick={() => goToStep('agent-setup')}
                  className="inline-flex w-full items-center justify-center rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
                >
                  Start onboarding
                </button>
                <button
                  type="button"
                  onClick={finishOnboarding}
                  className="inline-flex w-full items-center justify-center rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50"
                >
                  Skip for now
                </button>
              </div>
            </div>
          )}

          {step === 'agent-setup' && (
            <form className="space-y-6" onSubmit={handleAgentSetupSubmit}>
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">Agent setup</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Configure your first agent</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  Give your AI agent a name and role. This agent will own the memories you create.
                </p>
              </div>
              <div>
                <label htmlFor="agent-name" className="block text-sm font-medium text-slate-700">
                  Agent name
                </label>
                <input
                  id="agent-name"
                  name="agent-name"
                  value={agentName}
                  onChange={(event) => setAgentName(event.target.value)}
                  className="mt-2 block w-full rounded-2xl border border-slate-300 px-4 py-3 text-slate-950 outline-none ring-0 transition focus:border-amc-primary focus:ring-2 focus:ring-amc-primary/20"
                  placeholder="My Research Agent"
                />
              </div>
              {error && (
                <p
                  id="agent-name-error"
                  role="alert"
                  aria-live="assertive"
                  className="text-sm text-amc-error"
                  tabIndex={-1}
                >
                  {error}
                </p>
              )}
              <div>
                <label htmlFor="agent-role" className="block text-sm font-medium text-slate-700">
                  Agent role
                </label>
                <select
                  id="agent-role"
                  name="agent-role"
                  value={agentRole}
                  onChange={(event) => setAgentRole(event.target.value)}
                  className="mt-2 block w-full rounded-2xl border border-slate-300 px-4 py-3 text-slate-950 outline-none ring-0 transition focus:border-amc-primary focus:ring-2 focus:ring-amc-primary/20"
                >
                  <option value="assistant">Assistant</option>
                  <option value="researcher">Researcher</option>
                  <option value="developer">Developer</option>
                  <option value="analyst">Analyst</option>
                </select>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Preview API key</p>
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

          {step === 'first-memory' && (
            <form className="space-y-6" onSubmit={handleMemorySubmit} noValidate>
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">First memory</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Write your first memory</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  This memory will be stored via the API and can be searched in the next step.
                  Edit the draft below or use the default.
                </p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                <p className="font-medium text-slate-700">Agent: <span className="text-amc-primary">{agentName}</span></p>
                <p className="mt-1 text-xs text-slate-500">Memory will be created with this agent ID</p>
              </div>
              <div>
                <label htmlFor="memory-draft" className="block text-sm font-medium text-slate-700">
                  First memory content
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
              {error && (
                <p
                  id="workspace-name-error"
                  role="alert"
                  aria-live="assertive"
                  className="text-sm text-amc-error"
                  tabIndex={-1}
                >
                  {error}
                </p>
              )}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => goToStep('agent-setup')}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                  disabled={isLoading}
                >
                  Back
                </button>
                <button
                  type="submit"
                  disabled={isLoading}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
                >
                  {isLoading ? 'Creating...' : 'Create memory'}
                </button>
              </div>
            </form>
          )}

          {step === 'search-memory' && (
            <div className="space-y-6">
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">Search memory</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-950">Retrieve your memory</h2>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  Search the memory cloud to verify your memory was stored and demonstrate the full value loop.
                </p>
              </div>
              {createdMemory && (
                <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
                  <p className="font-medium">Memory created successfully!</p>
                  <p className="mt-1 text-xs text-emerald-700">ID: {createdMemory.id}</p>
                </div>
              )}
              <div>
                <label htmlFor="search-query" className="block text-sm font-medium text-slate-700">
                  Search query
                </label>
                <div className="mt-2 flex gap-2">
                  <input
                    id="search-query"
                    name="search-query"
                    value={searchQuery}
                    onChange={(event) => setSearchQuery(event.target.value)}
                    className="flex-1 rounded-2xl border border-slate-300 px-4 py-3 text-slate-950 outline-none transition focus:border-amc-primary focus:ring-2 focus:ring-amc-primary/20"
                    placeholder="Search your memories..."
                  />
                  <button
                    type="button"
                    onClick={handleSearch}
                    disabled={isLoading || !searchQuery.trim()}
                    className="inline-flex items-center justify-center rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
                  >
                    {isLoading ? 'Searching...' : 'Search'}
                  </button>
                </div>
              </div>
              {searchTimeMs !== null && (
                <p className="text-xs text-slate-500">
                  Search completed in {searchTimeMs.toFixed(2)}ms
                </p>
              )}
              {searchResults.length > 0 && (
                <div className="space-y-3">
                  <p className="text-sm font-medium text-slate-700">Results ({searchResults.length})</p>
                  {searchResults.map((result) => (
                    <div key={result.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <div className="flex items-start justify-between gap-2">
                        <p className="text-sm text-slate-700 line-clamp-3">{result.content}</p>
                        <span className="shrink-0 rounded-full bg-amc-primary/10 px-2 py-1 text-xs font-medium text-amc-primary">
                          {(result.relevance_score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <p className="mt-2 text-xs text-slate-500">
                        Agent: {result.agent_id} • Type: {result.memory_type}
                      </p>
                    </div>
                  ))}
                </div>
              )}
              {error && (
                <p
                  id="first-memory-error"
                  role="alert"
                  aria-live="assertive"
                  className="text-sm text-amc-error"
                  tabIndex={-1}
                >
                  {error}
                </p>
              )}
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => goToStep('first-memory')}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl border border-slate-300 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                >
                  Back
                </button>
                <button
                  type="button"
                  onClick={finishOnboarding}
                  className="inline-flex flex-1 items-center justify-center rounded-2xl bg-amc-success px-4 py-3 text-sm font-semibold text-white transition hover:bg-emerald-600"
                >
                  Complete setup
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
                  {agentName.trim() || 'Your agent'} is configured and your first memory is stored.
                </p>
              </div>
              <div className="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                {createdMemory && (
                  <div className="flex justify-between">
                    <span>Memory created:</span>
                    <span className="font-medium text-slate-700">Yes</span>
                  </div>
                )}
                {searchResults.length > 0 && (
                  <div className="flex justify-between">
                    <span>Search results:</span>
                    <span className="font-medium text-slate-700">{searchResults.length} found</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span>Agent:</span>
                  <span className="font-medium text-slate-700">{agentName}</span>
                </div>
              </div>
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
                <p className="font-medium">Full value loop complete!</p>
                <p className="mt-1 text-xs text-emerald-700">
                  You&apos;ve written a memory and retrieved it via search. The dashboard is ready.
                </p>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
