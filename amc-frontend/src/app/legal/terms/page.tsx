import Link from "next/link";

export const metadata = {
  title: "Terms of Service | Faintech Lab",
  description: "Faintech Lab Beta Terms of Service",
};

export default function TermsOfServicePage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <nav className="mb-6">
          <Link href="/legal" className="text-blue-600 hover:underline text-sm">
            ← Back to Legal
          </Link>
        </nav>

        <article className="bg-white shadow rounded-lg p-8 prose prose-gray max-w-none">
          <h1>Faintech Lab Beta Terms of Service</h1>

          <p className="text-sm text-gray-500 not-prose mb-6">
            <strong>Effective Date:</strong> March 24, 2026<br />
            <strong>Version:</strong> Beta 1.0
          </p>

          <h2>1. Acceptance of Terms</h2>
          <p>
            By accessing or using Faintech Lab (&quot;Service&quot;) during the beta period, you (&quot;User&quot;)
            agree to be bound by these Terms of Service (&quot;Terms&quot;). If you do not agree to these Terms,
            do not use the Service.
          </p>

          <h2>2. Beta Program Nature</h2>

          <h3>2.1 Experimental Service</h3>
          <p>Faintech Lab is currently in beta testing phase. The Service:</p>
          <ul>
            <li>May contain bugs, errors, or inaccuracies</li>
            <li>May change functionality without notice</li>
            <li>May experience downtime or performance issues</li>
            <li>Is provided for testing and feedback purposes</li>
          </ul>

          <h3>2.2 No Service Level Guarantees</h3>
          <p>During the beta period, we do not guarantee:</p>
          <ul>
            <li>Uptime or availability</li>
            <li>Data preservation or backup</li>
            <li>Feature stability or backward compatibility</li>
            <li>Response time for support requests</li>
          </ul>

          <h2>3. User Accounts</h2>

          <h3>3.1 Registration</h3>
          <p>You must provide accurate and complete information during registration. You are responsible for:</p>
          <ul>
            <li>Maintaining the confidentiality of your account credentials</li>
            <li>All activities that occur under your account</li>
            <li>Notifying us immediately of any unauthorized access</li>
          </ul>

          <h3>3.2 Account Termination</h3>
          <p>We reserve the right to suspend or terminate accounts that:</p>
          <ul>
            <li>Violate these Terms</li>
            <li>Abuse the Service or other users</li>
            <li>Engage in fraudulent or illegal activities</li>
          </ul>

          <h2>4. Acceptable Use</h2>

          <h3>4.1 Permitted Uses</h3>
          <p>You may use Faintech Lab for:</p>
          <ul>
            <li>Personal or business AI agent memory management</li>
            <li>Testing and providing feedback on features</li>
            <li>Legitimate research and development purposes</li>
          </ul>

          <h3>4.2 Prohibited Uses</h3>
          <p>You may NOT:</p>
          <ul>
            <li>Upload malicious code, malware, or harmful content</li>
            <li>Attempt to reverse engineer or extract our AI models</li>
            <li>Use the Service to violate any laws or regulations</li>
            <li>Interfere with other users&apos; data or accounts</li>
            <li>Overload or abuse our infrastructure</li>
            <li>Process illegally obtained personal data</li>
          </ul>

          <h2>5. Data and Privacy</h2>
          <p>
            Your use of the Service is governed by our{" "}
            <Link href="/legal/privacy" className="text-blue-600 hover:underline">Privacy Policy</Link>.
          </p>
          <ul>
            <li>We process personal data as described in our Privacy Policy</li>
            <li>You retain ownership of your content and data</li>
            <li>You may request data export or deletion at any time</li>
          </ul>

          <h2>6. Intellectual Property</h2>

          <h3>6.1 Our Rights</h3>
          <p>
            Faintech Lab, including its AI models, algorithms, interfaces, and documentation,
            is the property of Faintech Solutions SRL and protected by intellectual property laws.
          </p>

          <h3>6.2 Your Rights</h3>
          <p>
            You retain all rights to content you upload or create using the Service.
            You grant us a non-exclusive, worldwide, royalty-free license to process your
            content solely to provide the Service.
          </p>

          <h2>7. Disclaimers</h2>
          <p>
            THE SERVICE IS PROVIDED &quot;AS IS&quot; AND &quot;AS AVAILABLE&quot; WITHOUT WARRANTIES OF ANY KIND,
            EXPRESS OR IMPLIED.
          </p>
          <p>
            <strong>AI Output Disclaimer:</strong> AI-generated content may contain inaccuracies or biases.
            You are responsible for verifying AI output before relying on it.
          </p>

          <h2>8. Limitation of Liability</h2>
          <p>
            TO THE MAXIMUM EXTENT PERMITTED BY LAW, FAINTECH SOLUTIONS SRL SHALL NOT BE LIABLE FOR
            DIRECT, INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES.
          </p>
          <p>
            <strong>Beta-Specific Limitation:</strong> During beta, our total liability is limited to €100 EUR per user.
          </p>

          <h2>9. Governing Law</h2>
          <p>
            These Terms are governed by the laws of Romania. Any disputes shall be resolved
            in the courts of Bucharest, Romania.
          </p>

          <h2>10. Contact Information</h2>
          <p>
            <strong>Faintech Solutions SRL</strong><br />
            Email: <a href="mailto:legal@faintechlab.com" className="text-blue-600 hover:underline">legal@faintechlab.com</a>
          </p>
        </article>
      </div>
    </div>
  );
}
