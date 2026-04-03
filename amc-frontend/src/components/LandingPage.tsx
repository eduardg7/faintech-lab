'use client';

import { useState } from 'react';

interface LandingPageProps {
  onStartOnboarding: () => void;
}

export default function LandingPage({ onStartOnboarding }: LandingPageProps) {
  const [showDemo, setShowDemo] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Skip to main content for accessibility */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:bg-white focus:p-4"
      >
        Skip to main content
      </a>

      {/* Navigation */}
      <nav className="sticky top-0 z-40 border-b border-slate-200 bg-white/80 backdrop-blur-md">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-blue-600 to-blue-700" />
              <span className="text-lg font-semibold text-slate-900">Faintech Lab</span>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowDemo(!showDemo)}
                className="text-sm font-medium text-slate-600 transition hover:text-slate-900"
              >
                See How It Works
              </button>
              <button
                onClick={onStartOnboarding}
                className="inline-flex items-center rounded-xl bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 shadow-md"
              >
                Start Free Trial
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main id="main-content" className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="py-20 sm:py-32">
          <div className="text-center">
            {/* Badge */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600">
              <span className="h-2 w-2 rounded-full bg-blue-600" />
              Persistent memory for AI teams
            </div>

            {/* Badge */}
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600">
              <span className="h-2 w-2 rounded-full bg-green-600" />
              Memory for AI Teams
            </div>

            {/* Headline */}
            <h1 className="mx-auto max-w-4xl text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl lg:text-7xl">
              Never lose an AI insight again
            </h1>

            {/* Subheadline */}
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600 sm:text-xl">
              Give your AI team persistent memory. Capture decisions, learnings, and context in one shared brain.
            </p>

            {/* CTA Buttons */}
            <div className="mt-12 flex flex-col items-center gap-6 sm:flex-row sm:justify-center">
              <button
                onClick={onStartOnboarding}
                className="inline-flex items-center rounded-3xl bg-blue-600 px-10 py-5 text-lg font-bold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-500 focus:ring-offset-2 shadow-lg hover:shadow-xl"
              >
                Start Free Trial
                <svg
                  className="ml-3 h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 7l5 5m0 0l-5 5m5-5H6"
                  />
                </svg>
              </button>
              <button
                onClick={() => setShowDemo(!showDemo)}
                className="inline-flex items-center rounded-3xl border-2 border-blue-600 bg-white px-10 py-5 text-lg font-bold text-blue-600 transition hover:bg-blue-50 focus:outline-none focus:ring-4 focus:ring-blue-500 focus:ring-offset-2"
              >
                <svg
                  className="mr-3 h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                See How It Works
              </button>
            </div>

            {/* Urgency indicator */}
            <div className="mt-6 inline-flex items-center gap-2 rounded-full bg-yellow-50 border border-yellow-200 px-4 py-2">
              <svg className="h-4 w-4 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
              </svg>
              <span className="text-sm font-medium text-yellow-800">Start your first memory in 60 seconds</span>
            </div>

            {/* Social Proof */}
            <div className="mt-16 border-t border-slate-200 pt-8">
              <p className="text-sm font-medium uppercase tracking-wider text-slate-500">
                Loved by AI development teams
              </p>
              <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-3">
                <div className="text-center">
                  <div className="flex justify-center">
                    <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-2xl font-bold text-blue-600">500+</span>
                    </div>
                  </div>
                  <p className="mt-2 text-sm font-medium text-slate-900">Memories Created</p>
                  <p className="text-xs text-slate-500">This week</p>
                </div>
                <div className="text-center">
                  <div className="flex justify-center">
                    <div className="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
                      <span className="text-2xl font-bold text-green-600">15+</span>
                    </div>
                  </div>
                  <p className="mt-2 text-sm font-medium text-slate-900">Teams Active</p>
                  <p className="text-xs text-slate-500">Across startups</p>
                </div>
                <div className="text-center">
                  <div className="flex justify-center">
                    <div className="h-12 w-12 rounded-full bg-purple-100 flex items-center justify-center">
                      <span className="text-2xl font-bold text-purple-600">4.8</span>
                    </div>
                  </div>
                  <p className="mt-2 text-sm font-medium text-slate-900">User Rating</p>
                  <p className="text-xs text-slate-500">Based on 50+ reviews</p>
                </div>
              </div>
              <div className="mt-8 text-center">
                <p className="text-sm text-slate-600 italic">
                  "Finally, our AI agents remember what happened yesterday"
                </p>
                <p className="mt-1 text-xs text-slate-500">— Engineering Team, Series B Startup</p>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-20 border-t border-slate-200">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Everything your AI team needs to remember
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              A single source of truth for decisions, learnings, and context
            </p>
          </div>

          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                ),
                title: 'Persistent Memory',
                description: 'Store decisions, learnings, and context that persists across all AI conversations.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                ),
                title: 'Team Collaboration',
                description: 'Share memory across multiple AI agents and team members with workspace-based access.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                  </svg>
                ),
                title: 'API-First Design',
                description: 'Simple API key authentication makes it easy to integrate with any AI agent or workflow.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                ),
                title: 'Instant Setup',
                description: 'Get your team from zero to first memory write in under 5 minutes with guided onboarding.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                ),
                title: 'Dashboard Analytics',
                description: 'Track memory usage, team activity, and engagement with built-in analytics.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                ),
                title: 'Secure by Default',
                description: 'API-key authentication ensures your team data stays private and protected.'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="rounded-2xl border border-slate-200 bg-white p-6 transition hover:border-slate-300 hover:shadow-lg"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                  {feature.icon}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-slate-900">{feature.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Use Cases Section */}
        <div className="py-20 border-t border-slate-200">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Built for teams that ship
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              See how development teams use shared memory
            </p>
          </div>

          <div className="grid gap-8 lg:grid-cols-3">
            {[
              {
                title: 'Product Decisions',
                description: 'Keep track of product decisions, user feedback, and feature priorities across your entire team.',
                example: 'Remember that we chose PostgreSQL over MongoDB for ACID compliance and relational data needs.'
              },
              {
                title: 'Engineering Learnings',
                description: 'Capture technical decisions, debugging insights, and architectural patterns for future reference.',
                example: 'Store the solution to that tricky race condition in the payment processing system.'
              },
              {
                title: 'Customer Context',
                description: 'Maintain context about customer conversations, requirements, and preferences for better support.',
                example: 'Remember that Enterprise Client X needs GDPR compliance and prefers Slack integration.'
              }
            ].map((useCase, index) => (
              <div
                key={index}
                className="rounded-2xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-8"
              >
                <h3 className="text-xl font-semibold text-slate-900">{useCase.title}</h3>
                <p className="mt-3 text-sm leading-6 text-slate-600">{useCase.description}</p>
                <div className="mt-6 rounded-xl border border-slate-200 bg-white p-4">
                  <p className="text-xs font-medium uppercase tracking-wider text-slate-500">Example</p>
                  <p className="mt-2 text-sm text-slate-700 italic">{useCase.example}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Demo Section */}
        {showDemo && (
          <div className="py-20 border-t border-slate-200">
            <div className="rounded-3xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-8 sm:p-12">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
                  See it in action
                </h2>
                <p className="mt-4 text-lg text-slate-600">
                  Watch how easy it is to give your AI agents persistent memory
                </p>
              </div>

              <div className="aspect-video rounded-2xl border border-slate-200 bg-slate-900 flex items-center justify-center">
                <div className="text-center text-white">
                  <svg
                    className="mx-auto h-16 w-16 text-slate-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <p className="mt-4 text-sm text-slate-400">Demo video coming soon</p>
                </div>
              </div>

              <div className="mt-8 text-center">
                <button
                  onClick={onStartOnboarding}
                  className="inline-flex items-center rounded-2xl bg-slate-950 px-8 py-4 text-base font-semibold text-white transition hover:bg-slate-800"
                >
                  Try It Now - Free
                  <svg
                    className="ml-2 h-5 w-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 7l5 5m0 0l-5 5m5-5H6"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Final CTA Section */}
        <div className="py-20 border-t border-slate-200">
          <div className="rounded-3xl bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-16 text-center sm:px-16 shadow-2xl">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Ready to give your AI team a memory?
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-blue-100">
              Join teams who never lose insights. Start capturing decisions and context in 60 seconds.
            </p>
            <button
              onClick={onStartOnboarding}
              className="mt-8 inline-flex items-center rounded-3xl bg-white px-10 py-5 text-lg font-bold text-blue-600 transition hover:bg-blue-50 focus:outline-none focus:ring-4 focus:ring-white focus:ring-offset-2 focus:ring-offset-blue-600 shadow-lg"
            >
              Start Free Trial
              <svg
                className="ml-3 h-6 w-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 7l5 5m0 0l-5 5m5-5H6"
                />
              </svg>
            </button>
            <p className="mt-4 text-sm text-blue-100">
              No credit card required • Cancel anytime
            </p>
          </div>
        </div>

        {/* Footer */}
        <footer className="border-t border-slate-200 py-12">
          <div className="text-center text-sm text-slate-500">
            <p>© 2026 Faintech Lab. Built with ❤️ for AI teams.</p>
            <div className="mt-4 flex justify-center gap-6">
              <a href="/legal/privacy" className="hover:text-slate-700">
                Privacy Policy
              </a>
              <a href="/legal/terms" className="hover:text-slate-700">
                Terms of Service
              </a>
              <a href="/legal/cookies" className="hover:text-slate-700">
                Cookie Policy
              </a>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
