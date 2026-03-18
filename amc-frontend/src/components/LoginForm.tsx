'use client';

import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import { useMemo, useState } from 'react';

const betaLaunchDate = 'March 24, 2026';
const betaEmail = 'beta@faintech.ro';

const productScreens = [
  {
    title: 'Write memories fast',
    description: 'Store agent outcomes, decisions, and customer context through one authenticated API.',
    accent: 'from-blue-500/20 to-cyan-500/20',
  },
  {
    title: 'Search what matters',
    description: 'Keyword and semantic retrieval keep teams from losing prior learnings between runs.',
    accent: 'from-violet-500/20 to-fuchsia-500/20',
  },
  {
    title: 'See activity in one dashboard',
    description: 'Track memories, projects, and usage from the same operator surface used in the demo flow.',
    accent: 'from-emerald-500/20 to-teal-500/20',
  },
];

function looksLikeJwt(value: string) {
  return value.split('.').length === 3;
}

export default function LoginForm() {
  const { setApiKey } = useAuth();
  const [token, setToken] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [signupEmail, setSignupEmail] = useState('');
  const [signupName, setSignupName] = useState('');
  const [signupCompany, setSignupCompany] = useState('');
  const [signupError, setSignupError] = useState('');

  const betaMailtoHref = useMemo(() => {
    const subject = encodeURIComponent('Agent Memory Cloud beta signup');
    const body = encodeURIComponent(
      [
        'Hi Faintech team,',
        '',
        'I want beta access to Agent Memory Cloud.',
        '',
        `Name: ${signupName || 'Not provided'}`,
        `Company: ${signupCompany || 'Not provided'}`,
        `Email: ${signupEmail || 'Not provided'}`,
        '',
        'Please send me onboarding details and early-access steps.',
      ].join('\n')
    );

    return `mailto:${betaEmail}?subject=${subject}&body=${body}`;
  }, [signupCompany, signupEmail, signupName]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const trimmedToken = token.trim();

    if (!trimmedToken) {
      setError('Please enter your JWT access token');
      return;
    }

    if (!looksLikeJwt(trimmedToken)) {
      setError('Invalid token format. Paste the JWT access token returned by /v1/auth/login.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError('');
      await api.validateToken(trimmedToken);
      setApiKey(trimmedToken);
    } catch {
      setError('Token validation failed. Make sure the backend is running and the token is still valid.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBetaSignup = (e: React.MouseEvent<HTMLAnchorElement>) => {
    if (!signupEmail.trim() || !signupEmail.includes('@')) {
      e.preventDefault();
      setSignupError('Enter a valid work email to join the beta waitlist.');
      return;
    }

    setSignupError('');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col gap-12 px-4 py-8 sm:px-6 lg:px-8 lg:py-12">
        <header className="flex flex-col gap-4 rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-slate-950/30 backdrop-blur lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-300">Agent Memory Cloud</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">
              Launch the beta with a landing page that actually converts.
            </h1>
            <p className="mt-3 max-w-2xl text-sm text-slate-300 sm:text-base">
              Capture memory writes, search across prior context, and give your agents a usable dashboard from day one.
              Beta opens on {betaLaunchDate}.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 text-sm text-slate-200">
            <a
              href="#beta-signup"
              className="rounded-full bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300"
            >
              Join beta
            </a>
            <a
              href="#dashboard-access"
              className="rounded-full border border-white/15 px-5 py-3 font-semibold transition hover:border-cyan-300 hover:text-cyan-200"
            >
              Existing customer login
            </a>
          </div>
        </header>

        <main id="main-content" className="grid gap-8 lg:grid-cols-[1.35fr_0.9fr]">
          <section className="space-y-8">
            <div className="grid gap-4 md:grid-cols-3">
              {productScreens.map((screen) => (
                <article
                  key={screen.title}
                  className="overflow-hidden rounded-3xl border border-white/10 bg-slate-900/80 shadow-xl shadow-slate-950/20"
                >
                  <div className={`h-28 bg-gradient-to-br ${screen.accent}`} />
                  <div className="space-y-3 p-5">
                    <p className="text-xs font-semibold uppercase tracking-[0.25em] text-cyan-300">Product preview</p>
                    <h2 className="text-lg font-semibold text-white">{screen.title}</h2>
                    <p className="text-sm leading-6 text-slate-300">{screen.description}</p>
                  </div>
                </article>
              ))}
            </div>

            <div className="grid gap-4 rounded-3xl border border-white/10 bg-white/5 p-6 md:grid-cols-3">
              <div>
                <p className="text-3xl font-semibold text-white">3 mins</p>
                <p className="mt-2 text-sm text-slate-300">Guided demo flow: login → write memory → search → dashboard.</p>
              </div>
              <div>
                <p className="text-3xl font-semibold text-white">API-first</p>
                <p className="mt-2 text-sm text-slate-300">Early access includes SDK support and dashboard visibility for operators.</p>
              </div>
              <div>
                <p className="text-3xl font-semibold text-white">Free beta</p>
                <p className="mt-2 text-sm text-slate-300">Join before launch and get onboarding help while the beta cohort is still small.</p>
              </div>
            </div>

            <section id="beta-signup" className="rounded-3xl border border-cyan-400/20 bg-cyan-400/10 p-6">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-2xl">
                  <p className="text-sm font-semibold uppercase tracking-[0.3em] text-cyan-200">Beta signup CTA</p>
                  <h2 className="mt-2 text-2xl font-semibold text-white">Request early access before outreach starts.</h2>
                  <p className="mt-3 text-sm leading-6 text-slate-200">
                    Share your work email and we prepare a beta invite request to {betaEmail}. This keeps the signup flow usable now,
                    while backend signup automation is still being built.
                  </p>
                </div>
                <a
                  href={betaMailtoHref}
                  onClick={handleBetaSignup}
                  className="inline-flex items-center justify-center rounded-full bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-100"
                >
                  Send beta request
                </a>
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-3">
                <label className="block text-sm text-slate-100">
                  Name
                  <input
                    type="text"
                    value={signupName}
                    onChange={(e) => setSignupName(e.target.value)}
                    placeholder="Ada Lovelace"
                    className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white placeholder:text-slate-400 focus:border-cyan-300 focus:outline-none"
                  />
                </label>
                <label className="block text-sm text-slate-100">
                  Company
                  <input
                    type="text"
                    value={signupCompany}
                    onChange={(e) => setSignupCompany(e.target.value)}
                    placeholder="Example AI"
                    className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white placeholder:text-slate-400 focus:border-cyan-300 focus:outline-none"
                  />
                </label>
                <label className="block text-sm text-slate-100">
                  Work email
                  <input
                    type="email"
                    value={signupEmail}
                    onChange={(e) => setSignupEmail(e.target.value)}
                    placeholder="you@company.com"
                    className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white placeholder:text-slate-400 focus:border-cyan-300 focus:outline-none"
                  />
                </label>
              </div>

              {signupError ? (
                <p className="mt-3 text-sm text-rose-200" role="alert">
                  {signupError}
                </p>
              ) : (
                <p className="mt-3 text-sm text-cyan-100">
                  The CTA opens a pre-filled beta request with your details so the waitlist flow is live today.
                </p>
              )}
            </section>
          </section>

          <aside
            id="dashboard-access"
            className="rounded-3xl border border-white/10 bg-white p-6 text-slate-900 shadow-2xl shadow-slate-950/30"
          >
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-600">Dashboard access</p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-900">Already have an API key?</h2>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                Sign in to the authenticated dashboard to create memories, search context, and validate the demo flow.
              </p>
            </div>

            <form className="mt-8 space-y-6" onSubmit={handleSubmit} noValidate>
              <div>
                <label htmlFor="jwt-token" className="mb-1 block text-sm font-medium text-slate-700">
                  JWT Access Token
                </label>
                <textarea
                  id="jwt-token"
                  name="jwt-token"
                  autoComplete="off"
                  required
                  aria-required="true"
                  aria-describedby={error ? 'jwt-token-error' : 'jwt-token-help'}
                  rows={4}
                  className="block w-full rounded-2xl border border-slate-200 px-4 py-3 text-slate-900 placeholder:text-slate-400 focus:border-blue-500 focus:outline-none font-mono text-xs"
                  placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                />
                <p id="jwt-token-help" className="mt-2 text-xs text-slate-500">
                  Expected format: Bearer token returned by POST /v1/auth/login or /v1/auth/register.
                </p>
              </div>

              {error && (
                <div id="jwt-token-error" className="text-center text-sm text-red-600" role="alert" aria-live="polite">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="flex w-full justify-center rounded-2xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Validating token...' : 'Sign in to dashboard'}
              </button>
            </form>

            <div className="mt-6 rounded-2xl bg-slate-100 p-4 text-sm text-slate-600">
              <p className="font-medium text-slate-900">What the beta includes</p>
              <ul className="mt-3 space-y-2">
                <li>• Memory write/read/search API endpoints</li>
                <li>• Dashboard visibility for projects, agents, and context</li>
                <li>• Direct onboarding support while the beta cohort is small</li>
              </ul>
            </div>
          </aside>
        </main>
      </div>
    </div>
  );
}
