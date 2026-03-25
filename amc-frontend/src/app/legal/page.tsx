import Link from "next/link";

export const metadata = {
  title: "Legal | Faintech Lab",
  description: "Legal documents for Faintech Lab beta",
};

export default function LegalPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Legal</h1>

        <div className="bg-white shadow rounded-lg divide-y divide-gray-200">
          <Link
            href="/legal/privacy"
            className="block p-6 hover:bg-gray-50 transition-colors"
          >
            <h2 className="text-lg font-semibold text-gray-900">Privacy Policy</h2>
            <p className="mt-1 text-sm text-gray-500">
              How we collect, use, and protect your personal data during the beta phase
            </p>
            <p className="mt-2 text-xs text-gray-400">Last updated: March 17, 2026</p>
          </Link>

          <Link
            href="/legal/terms"
            className="block p-6 hover:bg-gray-50 transition-colors"
          >
            <h2 className="text-lg font-semibold text-gray-900">Terms of Service</h2>
            <p className="mt-1 text-sm text-gray-500">
              Terms and conditions for using Faintech Lab during beta testing
            </p>
            <p className="mt-2 text-xs text-gray-400">Last updated: March 19, 2026</p>
          </Link>

          <Link
            href="/legal/cookies"
            className="block p-6 hover:bg-gray-50 transition-colors"
          >
            <h2 className="text-lg font-semibold text-gray-900">Cookie Policy</h2>
            <p className="mt-1 text-sm text-gray-500">
              Information about cookies and similar technologies we use
            </p>
            <p className="mt-2 text-xs text-gray-400">Last updated: March 19, 2026</p>
          </Link>

          <Link
            href="/legal/data-rights"
            className="block p-6 hover:bg-gray-50 transition-colors"
          >
            <h2 className="text-lg font-semibold text-gray-900">Data Subject Rights (GDPR)</h2>
            <p className="mt-1 text-sm text-gray-500">
              Your rights under GDPR and how to exercise them
            </p>
            <p className="mt-2 text-xs text-gray-400">Last updated: March 19, 2026</p>
          </Link>
        </div>

        <div className="mt-8 text-sm text-gray-500">
          <p>
            <strong>Contact:</strong>{" "}
            <a href="mailto:privacy@faintech.ro" className="text-blue-600 hover:underline">
              privacy@faintech.ro
            </a>
          </p>
          <p className="mt-2">
            <strong>Company:</strong> Faintech Solutions SRL
          </p>
        </div>
      </div>
    </div>
  );
}
