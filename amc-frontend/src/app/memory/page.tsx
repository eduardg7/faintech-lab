import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "AI Memory Management for Production Systems | Faintech Lab",
  description: "Production-grade memory for autonomous AI agents. Persistent state, multi-modal storage, and OS-level integration. Join beta.",
  keywords: [
    "AI memory management system",
    "persistent AI agent memory",
    "vector database for AI agents",
    "long-term memory for LLMs",
    "memory layer for autonomous agents"
  ],
  openGraph: {
    title: "AI Memory Management for Production Systems | Faintech Lab",
    description: "Production-grade memory for autonomous AI agents. Persistent state, multi-modal storage, and OS-level integration.",
    type: "website",
    url: "https://faintech-lab.com/memory",
  },
  twitter: {
    card: "summary_large_image",
    title: "AI Memory Management for Production Systems | Faintech Lab",
    description: "Production-grade memory for autonomous AI agents. Persistent state, multi-modal storage, and OS-level integration.",
  },
};

export default function LandingPage() {
  return (
    <>
      <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
          Stop Losing Agent State Every Session
        </h1>
        <p className="text-xl md:text-2xl text-slate-300 mb-8 max-w-3xl mx-auto">
          Production-grade memory for autonomous AI agents. Persistent, scalable, and fully integrated.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/dashboard"
            className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
          >
            Join Beta
          </Link>
          <Link
            href="/docs"
            className="px-8 py-4 bg-slate-700 hover:bg-slate-600 text-white font-semibold rounded-lg transition-colors"
          >
            Read Documentation
          </Link>
        </div>
      </section>

      {/* Problem Statement */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">
          The Agent Memory Problem
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {[
            "Agents restart = memory loss",
            "Vector databases ≠ production memory systems",
            "No unified layer across multi-agent swarms",
            "State persistence is an afterthought"
          ].map((problem, idx) => (
            <div key={idx} className="bg-slate-800 p-6 rounded-lg border border-slate-700">
              <p className="text-slate-300">{problem}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Solution */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">
          Memory-First Architecture
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          {[
            {
              title: "Automatic State Persistence",
              desc: "Agents remember everything without manual implementation"
            },
            {
              title: "Multi-Modal Storage",
              desc: "Vectors, documents, structured data, embeddings - all unified"
            },
            {
              title: "Memory-as-API",
              desc: "Simple integration layer for any agent framework"
            },
            {
              title: "Temporal Queries",
              desc: "Query what agents remembered X days ago"
            }
          ].map((feature, idx) => (
            <div key={idx} className="bg-slate-800 p-6 rounded-lg border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-slate-300">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* OS-Level vs Library */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">
          Why OS-Level Memory Matters
        </h2>
        <div className="max-w-4xl mx-auto bg-slate-800 p-8 rounded-lg border border-slate-700">
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Library-Level Memory</h3>
              <p className="text-slate-300 mb-4">Memory is an add-on you implement yourself</p>
              <ul className="space-y-2 text-slate-400">
                <li>• Manual state management</li>
                <li>• No automatic persistence</li>
                <li>• Agent lifecycle = app lifecycle</li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">OS-Level Memory</h3>
              <p className="text-slate-300 mb-4">Memory is a platform agents use automatically</p>
              <ul className="space-y-2 text-slate-400">
                <li>• Built-in persistence layer</li>
                <li>• Agent lifecycle = OS lifecycle</li>
                <li>• Shared state across swarms</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Comparison */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">
          Memory vs Vector Databases
        </h2>
        <div className="max-w-4xl mx-auto bg-slate-800 p-8 rounded-lg border border-slate-700 overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="pb-4 text-white font-semibold">Feature</th>
                <th className="pb-4 text-white font-semibold">Vector Database</th>
                <th className="pb-4 text-white font-semibold">AI Memory System</th>
              </tr>
            </thead>
            <tbody>
              {[
                { feature: "Similarity search", vectorDb: "✓ Primary", aiMemory: "✓ Secondary" },
                { feature: "Temporal queries", vectorDb: "✗", aiMemory: "✓ Primary" },
                { feature: "Multi-agent sync", vectorDb: "✗", aiMemory: "✓ Primary" },
                { feature: "Context management", vectorDb: "✗", aiMemory: "✓ Primary" },
                { feature: "Production orchestration", vectorDb: "✗", aiMemory: "✓ Primary" }
              ].map((row, idx) => (
                <tr key={idx} className="border-b border-slate-700">
                  <td className="py-4 text-slate-300">{row.feature}</td>
                  <td className="py-4 text-slate-400">{row.vectorDb}</td>
                  <td className="py-4 text-slate-400">{row.aiMemory}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Social Proof */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center bg-slate-800 p-8 rounded-lg border border-slate-700">
          <p className="text-2xl text-white font-semibold mb-2">
            Join 200+ developers waiting for beta access
          </p>
          <p className="text-slate-400 mb-6">
            Be first to experience production-grade agent memory
          </p>
          <Link
            href="/dashboard"
            className="inline-block px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
          >
            Join Beta Waitlist
          </Link>
        </div>
      </section>

      {/* Footer CTA */}
      <footer className="container mx-auto px-4 py-12">
        <div className="text-center">
          <Link
            href="/dashboard"
            className="inline-block px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
          >
            Join Beta Waitlist
          </Link>
          <div className="mt-6">
            <Link
              href="/docs"
              className="text-slate-400 hover:text-white transition-colors"
            >
              Read Documentation
            </Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
ter>
    </main>
  );
}
