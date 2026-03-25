import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "AI Memory Management for Production Systems | Faintech Lab",
  description: "Production-grade memory for autonomous AI agents. Persistent state, multi-modal storage, and OS-level integration. Join beta.",
};

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
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

      <section className="container mx-auto px-4 py-16">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-12 text-center">
          Built for Production AI Systems
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-slate-800 p-6 rounded-lg">
            <h3 className="text-xl font-semibold text-white mb-3">Persistent Memory</h3>
            <p className="text-slate-300">Zero state loss between sessions. Your agents remember everything.</p>
          </div>
          <div className="bg-slate-800 p-6 rounded-lg">
            <h3 className="text-xl font-semibold text-white mb-3">Multi-Modal Storage</h3>
            <p className="text-slate-300">Text, embeddings, vectors, and structured data in one unified system.</p>
          </div>
          <div className="bg-slate-800 p-6 rounded-lg">
            <h3 className="text-xl font-semibold text-white mb-3">OS Integration</h3>
            <p className="text-slate-300">Direct integration with file systems, databases, and external APIs.</p>
          </div>
        </div>
      </section>

      <footer className="container mx-auto px-4 py-8 border-t border-slate-700">
        <div className="text-center">
          <p className="text-slate-400 mb-4">Built by Faintech Lab</p>
          <div className="flex gap-4 justify-center">
            <Link href="/dashboard" className="inline-block px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors">
              Join Beta Waitlist
            </Link>
            <Link href="/docs" className="text-slate-400 hover:text-white transition-colors">
              Read Documentation
            </Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
