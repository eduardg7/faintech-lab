'use client';

import { ApiKeySummary, CurrentUser } from '@/lib/api';

interface OnboardingShellProps {
  user: CurrentUser;
  apiKeys: ApiKeySummary[];
  onPrefillMemory: () => void;
}

interface CtaCardProps {
  eyebrow: string;
  title: string;
  description: string;
  actionLabel: string;
  actionHint: string;
  status: 'ready' | 'complete';
  onAction?: () => void;
}

function CtaCard({ eyebrow, title, description, actionLabel, actionHint, status, onAction }: CtaCardProps) {
  const isComplete = status === 'complete';

  return (
    <section className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between gap-3">
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-amc-primary">{eyebrow}</span>
        <span
          className={`rounded-full px-2.5 py-1 text-xs font-medium ${
            isComplete ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-800'
          }`}
        >
          {isComplete ? 'Ready' : 'Next step'}
        </span>
      </div>

      <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-gray-600">{description}</p>

      <div className="mt-6 space-y-3">
        <button
          type="button"
          onClick={onAction}
          disabled={!onAction}
          className="inline-flex w-full items-center justify-center rounded-lg bg-amc-primary px-4 py-2.5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-default disabled:bg-gray-200 disabled:text-gray-600"
        >
          {actionLabel}
        </button>
        <p className="rounded-lg bg-gray-50 px-3 py-2 font-mono text-xs text-gray-600">{actionHint}</p>
      </div>
    </section>
  );
}

export default function OnboardingShell({ user, apiKeys, onPrefillMemory }: OnboardingShellProps) {
  const hasApiKeys = apiKeys.length > 0;

  return (
    <div className="rounded-3xl border border-dashed border-amc-primary/30 bg-gradient-to-br from-blue-50 via-white to-indigo-50 p-6 sm:p-8">
      <div className="max-w-3xl">
        <p className="text-sm font-medium text-amc-primary">First-run onboarding</p>
        <h2 className="mt-2 text-3xl font-bold tracking-tight text-gray-900">Your workspace is live. Seed it with the first real signals.</h2>
        <p className="mt-3 text-sm leading-6 text-gray-600">
          We already confirmed your authenticated session and workspace from live backend data. The dashboard is empty because this account has no stored memories yet.
        </p>
      </div>

      <dl className="mt-6 grid gap-4 rounded-2xl bg-white/70 p-4 sm:grid-cols-2 xl:grid-cols-4">
        <div>
          <dt className="text-xs uppercase tracking-wide text-gray-500">Workspace</dt>
          <dd className="mt-1 text-sm font-medium text-gray-900">{user.workspace_id}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-gray-500">User</dt>
          <dd className="mt-1 text-sm font-medium text-gray-900">{user.full_name || user.email}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-gray-500">API keys</dt>
          <dd className="mt-1 text-sm font-medium text-gray-900">{apiKeys.length}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-gray-500">Next unlock</dt>
          <dd className="mt-1 text-sm font-medium text-gray-900">Write first memory</dd>
        </div>
      </dl>

      <div className="mt-8 grid gap-4 xl:grid-cols-3">
        <CtaCard
          eyebrow="1. Workspace"
          title="Create workspace"
          description="Registration already created a live workspace for this account, so there is nothing else to provision before using the app."
          actionLabel="Workspace ready"
          actionHint={`workspace_id=${user.workspace_id}`}
          status="complete"
        />

        <CtaCard
          eyebrow="2. API key"
          title="Generate API key"
          description="Create a workspace API key for service-to-service writes. The UI only points to the flow and never exposes stored secret values after creation."
          actionLabel={hasApiKeys ? 'API key exists' : 'Use POST /v1/api-keys'}
          actionHint={hasApiKeys ? apiKeys[0].key_preview : 'POST /v1/api-keys { "name": "first-ingestion-key" }'}
          status={hasApiKeys ? 'complete' : 'ready'}
        />

        <CtaCard
          eyebrow="3. Seed data"
          title="Write first memory"
          description="Use the authenticated dashboard state you already have and jump straight into the first memory write flow so this empty workspace becomes queryable."
          actionLabel="Prefill first memory payload"
          actionHint='POST /v1/memories { "agent_id": "founder", "memory_type": "learning", "content": "First memory" }'
          status="ready"
          onAction={onPrefillMemory}
        />
      </div>
    </div>
  );
}
