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
                className="inline-flex items-center rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
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

            {/* Headline */}
            <h1 className="mx-auto max-w-4xl text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl lg:text-7xl">
              Give your AI agents a{' '}
              <span className="bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                shared brain
              </span>
            </h1>

            {/* Subheadline */}
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600 sm:text-xl">
              Capture decisions, learnings, and context in one memory cloud. Your AI agents finally remember everything across conversations.
            </p>

            {/* CTA Buttons */}
            <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
              <button
                onClick={onStartOnboarding}
                className="inline-flex items-center rounded-2xl bg-slate-950 px-8 py-4 text-base font-semibold text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2"
              >
                Start Free Trial
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
              <button
                onClick={() => setShowDemo(!showDemo)}
                className="inline-flex items-center rounded-2xl border border-slate-300 bg-white px-8 py-4 text-base font-semibold text-slate-900 transition hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2"
              >
                <svg
                  className="mr-2 h-5 w-5 text-blue-600"
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

            {/* Social Proof */}
            <div className="mt-16 border-t border-slate-200 pt-8">
              <p className="text-sm font-medium uppercase tracking-wider text-slate-500">
                Trusted by development teams
              </p>
              <div className="mt-6 flex items-center justify-center gap-8 text-slate-400">
                <div className="flex items-center gap-2">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                  </svg>
                  <span className="text-sm">Shared Memory</span>
                </div>
                <div className="flex items-center gap-2">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span className="text-sm">Instant Access</span>
                </div>
                <div className="flex items-center gap-2">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-sm">API-First</span>
                </div>
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
                title: 'Save 2+ Hours Per Week',
                description: 'Stop re-explaining context to AI agents. Persistent memory eliminates repetitive explanations and context-switching overhead.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                ),
                title: 'Eliminate Team Misalignment',
                description: 'Ensure all AI agents work from the same context. No more conflicting decisions or duplicated work across team members.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                  </svg>
                ),
                title: 'Integrate in Minutes, Not Days',
                description: 'Simple API key authentication. Connect your existing AI agents in under 5 minutes with zero infrastructure changes.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                ),
                title: 'First Memory in 60 Seconds',
                description: 'Get from signup to first memory write in under 1 minute with guided onboarding. No complex setup or configuration required.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                ),
                title: 'Track ROI Instantly',
                description: 'See time saved, decisions captured, and team productivity gains in real-time. Dashboard analytics show immediate impact.'
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                ),
                title: 'Enterprise-Grade Security',
                description: 'API-key authentication with workspace isolation. Your team data stays private and protected, no external dependencies.'
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

        {/* Differentiation Section */}
        <div className="py-20 border-t border-slate-200 bg-gradient-to-b from-white to-slate-50">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Why teams choose Faintech Lab
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              The only memory system built specifically for AI agent coordination
            </p>
          </div>

          <div className="grid gap-8 lg:grid-cols-3">
            {[
              {
                title: 'vs. Manual Notes',
                before: 'Copy-paste context into ChatGPT, lose track in scattered docs',
                after: 'Structured memory with instant retrieval, AI agents automatically access relevant context',
                metric: '87% reduction in context recreation time'
              },
              {
                title: 'vs. Vector Databases',
                before: 'Complex setup, requires ML expertise, no coordination features',
                after: 'Zero-config setup, built for AI teams, automatic cross-agent synchronization',
                metric: '5-minute setup vs. 2+ weeks for vector DB'
              },
              {
                title: 'vs. Knowledge Base Tools',
                before: 'Static documentation, no AI integration, manual updates',
                after: 'Dynamic memory that AI agents can read/write automatically',
                metric: '15x faster knowledge retrieval for AI agents'
              }
            ].map((comparison, index) => (
              <div
                key={index}
                className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm"
              >
                <h3 className="text-xl font-semibold text-slate-900">{comparison.title}</h3>

                <div className="mt-6 space-y-4">
                  <div className="rounded-lg bg-red-50 border border-red-200 p-4">
                    <p className="text-xs font-medium uppercase tracking-wider text-red-600 mb-1">Before</p>
                    <p className="text-sm text-red-900">{comparison.before}</p>
                  </div>

                  <div className="rounded-lg bg-green-50 border border-green-200 p-4">
                    <p className="text-xs font-medium uppercase tracking-wider text-green-600 mb-1">After Faintech Lab</p>
                    <p className="text-sm text-green-900">{comparison.after}</p>
                  </div>
                </div>

                <div className="mt-6 flex items-center justify-center">
                  <div className="inline-flex items-center gap-2 rounded-full bg-blue-100 px-4 py-2">
                    <svg className="h-4 w-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm font-semibold text-blue-900">{comparison.metric}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-16 text-center">
            <div className="inline-flex items-center gap-3 rounded-2xl border border-blue-200 bg-blue-50 px-6 py-4">
              <svg className="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <div className="text-left">
                <p className="text-sm font-semibold text-blue-900">The AI Agent Coordination Advantage</p>
                <p className="text-xs text-blue-700">Built from the ground up for teams with multiple AI agents working together</p>
              </div>
            </div>
          </div>
        </div>

        {/* Use Cases Section */}
        <div className="py-20 border-t border-slate-200">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Built for teams that ship
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              See how development teams save hours every week with shared memory
            </p>
          </div>

          <div className="grid gap-8 lg:grid-cols-2">
            {[
              {
                title: 'Product Decisions',
                scenario: 'Product team tracks feature decisions across 15+ customer conversations',
                before: {
                  problem: 'Scattered across Slack, Notion, and email threads',
                  impact: '3+ hours/week recreating context, 2x duplicate work on features',
                  time: '45 minutes to find why a feature was prioritized'
                },
                after: {
                  solution: 'AI agents automatically store and retrieve product decisions',
                  impact: 'Instant context retrieval, zero duplicate work',
                  time: '30 seconds to find any decision rationale'
                },
                example: 'Remember that we chose PostgreSQL over MongoDB for ACID compliance and relational data needs.',
                savings: '3+ hours/week saved per product manager'
              },
              {
                title: 'Engineering Debugging',
                scenario: 'Engineering team solves complex bugs that require multi-session debugging',
                before: {
                  problem: 'Each debugging session starts from scratch, re-explaining the problem',
                  impact: 'Repeated investigation, lost insights between sessions',
                  time: '2+ hours re-investigating the same issue'
                },
                after: {
                  solution: 'AI agents remember investigation steps, failed approaches, and partial solutions',
                  impact: 'Build on previous work, never lose progress',
                  time: 'Resume debugging in 30 seconds with full context'
                },
                example: 'Store the solution to that tricky race condition in the payment processing system.',
                savings: '50% faster bug resolution, 2+ hours saved per complex bug'
              },
              {
                title: 'Customer Context',
                scenario: 'Support team handles 50+ customer conversations per week',
                before: {
                  problem: 'Each agent asks customers to re-explain their setup and requirements',
                  impact: 'Frustrated customers, longer resolution times',
                  time: '15 minutes per ticket recreating customer context'
                },
                after: {
                  solution: 'AI agents automatically access customer history, preferences, and past issues',
                  impact: 'Personalized support from first message, faster resolutions',
                  time: 'Instant customer context, zero re-explanation'
                },
                example: 'Remember that Enterprise Client X needs GDPR compliance and prefers Slack integration.',
                savings: '15 minutes saved per support ticket, 12+ hours/week per agent'
              },
              {
                title: 'Architecture Decisions',
                scenario: 'Team makes critical infrastructure choices affecting 6-month roadmap',
                before: {
                  problem: 'Architecture rationale lost after 3 months, team re-debates same decisions',
                  impact: 'Repeated discussions, risk of inconsistent choices',
                  time: '2+ hours per decision recreating evaluation criteria'
                },
                after: {
                  solution: 'AI agents store decision criteria, trade-offs, and rationale permanently',
                  impact: 'Consistent architecture choices, informed new team members',
                  time: '30 seconds to understand why a decision was made'
                },
                example: 'Remember we chose Kubernetes over Docker Swarm for better scaling and ecosystem support.',
                savings: '2+ hours saved per architecture decision, prevents costly re-decisions'
              },
              {
                title: 'Code Review Insights',
                scenario: 'Senior engineers share knowledge through code review feedback',
                before: {
                  problem: 'Review insights lost in GitHub comments, not accessible to future AI agents',
                  impact: 'Repeated mistakes, knowledge silos',
                  time: '30+ minutes searching for why a pattern was approved/rejected'
                },
                after: {
                  solution: 'AI agents remember code review patterns, best practices, and team conventions',
                  impact: 'Consistent code quality, faster onboarding',
                  time: 'Instant access to team coding standards'
                },
                example: 'Remember that we always use dependency injection for database connections to enable testing.',
                savings: '30% faster code reviews, 50% reduction in repeated mistakes'
              }
            ].map((useCase, index) => (
              <div
                key={index}
                className="rounded-2xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-8"
              >
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-xl font-semibold text-slate-900">{useCase.title}</h3>
                  <div className="inline-flex items-center gap-1 rounded-full bg-green-100 px-3 py-1">
                    <svg className="h-4 w-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-xs font-semibold text-green-900">{useCase.savings}</span>
                  </div>
                </div>

                <p className="text-sm text-slate-600 mb-6">{useCase.scenario}</p>

                <div className="space-y-4 mb-6">
                  <div className="rounded-lg bg-red-50 border border-red-200 p-4">
                    <p className="text-xs font-medium uppercase tracking-wider text-red-600 mb-2">Before Faintech Lab</p>
                    <p className="text-sm font-medium text-red-900 mb-1">❌ {useCase.before.problem}</p>
                    <p className="text-xs text-red-700">• {useCase.before.impact}</p>
                    <p className="text-xs text-red-700">• {useCase.before.time}</p>
                  </div>

                  <div className="rounded-lg bg-green-50 border border-green-200 p-4">
                    <p className="text-xs font-medium uppercase tracking-wider text-green-600 mb-2">After Faintech Lab</p>
                    <p className="text-sm font-medium text-green-900 mb-1">✓ {useCase.after.solution}</p>
                    <p className="text-xs text-green-700">• {useCase.after.impact}</p>
                    <p className="text-xs text-green-700">• {useCase.after.time}</p>
                  </div>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-4">
                  <p className="text-xs font-medium uppercase tracking-wider text-slate-500">Example Memory</p>
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
          <div className="rounded-3xl bg-gradient-to-r from-slate-900 to-slate-800 px-8 py-16 text-center sm:px-16">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Ready to give your AI agents a memory?
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-300">
              Start capturing decisions, learnings, and context today. No credit card required.
            </p>
            <button
              onClick={onStartOnboarding}
              className="mt-8 inline-flex items-center rounded-2xl bg-white px-8 py-4 text-base font-semibold text-slate-900 transition hover:bg-slate-100"
            >
              Start Free Trial
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
