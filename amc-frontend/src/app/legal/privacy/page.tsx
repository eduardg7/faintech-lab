import Link from "next/link";

export const metadata = {
  title: "Privacy Policy | Faintech Lab",
  description: "Faintech Lab Beta Privacy Policy - How we collect, use, and protect your personal data",
};

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <nav className="mb-6">
          <Link href="/legal" className="text-blue-600 hover:underline text-sm">
            ← Back to Legal
          </Link>
        </nav>

        <article className="bg-white shadow rounded-lg p-8 prose prose-gray max-w-none">
          <h1>Faintech Lab - Beta Privacy Policy</h1>

          <p className="text-sm text-gray-500 not-prose mb-6">
            <strong>Last Updated:</strong> 2026-03-17<br />
            <strong>Effective Date:</strong> 2026-03-24 (Beta Launch)<br />
            <strong>Version:</strong> Beta 1.0
          </p>

          <h2>Overview</h2>
          <p>
            Faintech Lab (&quot;we,&quot; &quot;our,&quot; or &quot;us&quot;) is committed to protecting your personal data and privacy.
            This Privacy Policy explains how we collect, use, and protect your information when you use
            Faintech Lab during our beta testing phase.
          </p>

          <h2>1. Information We Collect</h2>

          <h3>1.1 Account Information</h3>
          <ul>
            <li><strong>Email address or internal user ID</strong> - for authentication and access control</li>
            <li><strong>User profile settings</strong> - preferences and configuration choices</li>
            <li><strong>Usage data</strong> - session information, interaction history, and feature usage patterns</li>
          </ul>

          <h3>1.2 Content and Memories</h3>
          <ul>
            <li><strong>Text content</strong> - notes, documents, and other textual data you store in Faintech Lab</li>
            <li><strong>Voice/audio recordings</strong> - if you enable voice input (opt-in only)</li>
            <li><strong>Interaction history</strong> - your conversations and interactions with AI agents</li>
          </ul>

          <h3>1.3 Technical Data</h3>
          <ul>
            <li><strong>Device information</strong> - browser type, operating system, screen resolution</li>
            <li><strong>Log data</strong> - IP address, access times, request details</li>
            <li><strong>Performance data</strong> - response times, error logs, system metrics</li>
          </ul>

          <h2>2. How We Use Your Information</h2>

          <h3>2.1 Core Product Functions</h3>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th>Purpose</th>
                <th>Data Used</th>
                <th>Legal Basis</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>Authentication & access</td><td>Email/user ID</td><td>Contractual necessity</td></tr>
              <tr><td>Memory storage & retrieval</td><td>Text content, embeddings</td><td>Contractual necessity</td></tr>
              <tr><td>Semantic search</td><td>Text content, embeddings</td><td>Contractual necessity</td></tr>
              <tr><td>Voice input (if enabled)</td><td>Audio recordings</td><td>Explicit consent</td></tr>
            </tbody>
          </table>

          <h3>2.2 Voice Input (Beta Feature)</h3>
          <p><strong>Voice input is opt-in only.</strong> By default, Faintech Lab uses text-only input.</p>
          <p>If you enable voice input:</p>
          <ul>
            <li>Audio recordings are processed to convert speech to text</li>
            <li>Audio recordings are retained for <strong>90 days</strong> for training purposes, then automatically deleted</li>
            <li>You can disable voice input at any time from your account settings</li>
          </ul>

          <h2>3. Data Storage and Security</h2>

          <h3>3.1 Data Retention</h3>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr><th>Data Type</th><th>Retention Period</th></tr>
            </thead>
            <tbody>
              <tr><td>Account information</td><td>Until account deletion</td></tr>
              <tr><td>Text content & memories</td><td>Until deletion by you</td></tr>
              <tr><td>Voice/audio recordings</td><td>90 days (training) / 30 days (experiment)</td></tr>
              <tr><td>Behavioral patterns</td><td>12 months (anonymized after 6 months)</td></tr>
              <tr><td>System logs</td><td>90 days</td></tr>
            </tbody>
          </table>

          <h3>3.2 Data Security</h3>
          <ul>
            <li><strong>Encryption in transit:</strong> All data is transmitted using TLS 1.3</li>
            <li><strong>Encryption at rest:</strong> We are implementing AES-256 encryption (in progress)</li>
            <li><strong>Access controls:</strong> Strict access controls and authentication</li>
          </ul>

          <h2>4. Data Sharing</h2>
          <p>We do <strong>not sell, rent, or monetize</strong> your personal data to third parties.</p>

          <h2>5. Your GDPR Rights</h2>
          <ul>
            <li><strong>Right to Access (Article 15)</strong> - Request a copy of your data</li>
            <li><strong>Right to Rectification (Article 16)</strong> - Correct inaccurate data</li>
            <li><strong>Right to Erasure (Article 17)</strong> - Request deletion (&quot;right to be forgotten&quot;)</li>
            <li><strong>Right to Restrict Processing (Article 18)</strong> - Limit how we use your data</li>
            <li><strong>Right to Data Portability (Article 20)</strong> - Receive data in portable format</li>
            <li><strong>Right to Object (Article 21)</strong> - Object to certain processing</li>
            <li><strong>Right to Withdraw Consent (Article 7)</strong> - Withdraw consent at any time</li>
          </ul>

          <p>See our <Link href="/legal/data-rights" className="text-blue-600 hover:underline">Data Subject Rights</Link> page for detailed instructions.</p>

          <h2>6. Children&apos;s Privacy</h2>
          <p>Faintech Lab is not intended for users under 16 years of age.</p>

          <h2>7. Contact Us</h2>
          <p>
            <strong>Faintech Solutions SRL</strong><br />
            Email: <a href="mailto:privacy@faintech.ro" className="text-blue-600 hover:underline">privacy@faintech.ro</a><br />
            GDPR inquiries: <a href="mailto:dpo@faintech.ro" className="text-blue-600 hover:underline">dpo@faintech.ro</a>
          </p>
        </article>
      </div>
    </div>
  );
}
