import Link from "next/link";

export const metadata = {
  title: "Data Subject Rights (GDPR) | Faintech Lab",
  description: "Your GDPR rights and how to exercise them",
};

export default function DataSubjectRightsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <nav className="mb-6">
          <Link href="/legal" className="text-blue-600 hover:underline text-sm">
            ← Back to Legal
          </Link>
        </nav>

        <article className="bg-white shadow rounded-lg p-8 prose prose-gray max-w-none">
          <h1>Data Subject Rights (GDPR)</h1>

          <p className="text-sm text-gray-500 not-prose mb-6">
            <strong>Effective Date:</strong> March 24, 2026<br />
            <strong>Version:</strong> Beta 1.0
          </p>

          <h2>1. Introduction</h2>
          <p>
            This document explains your rights under the General Data Protection Regulation (GDPR)
            regarding your personal data processed by Faintech Lab. As a data controller,
            Faintech Solutions SRL is committed to respecting and facilitating these rights.
          </p>

          <h2>2. Your Rights Overview</h2>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr><th>Right</th><th>Article</th><th>Summary</th></tr>
            </thead>
            <tbody>
              <tr><td>Right of Access</td><td>Art. 15</td><td>Obtain a copy of your data</td></tr>
              <tr><td>Right to Rectification</td><td>Art. 16</td><td>Correct inaccurate data</td></tr>
              <tr><td>Right to Erasure</td><td>Art. 17</td><td>Request deletion of your data</td></tr>
              <tr><td>Right to Restrict Processing</td><td>Art. 18</td><td>Limit how we use your data</td></tr>
              <tr><td>Right to Data Portability</td><td>Art. 20</td><td>Receive data in portable format</td></tr>
              <tr><td>Right to Object</td><td>Art. 21</td><td>Object to certain processing</td></tr>
              <tr><td>Right to Withdraw Consent</td><td>Art. 7(3)</td><td>Withdraw consent at any time</td></tr>
              <tr><td>Right to Lodge a Complaint</td><td>Art. 77</td><td>Complain to a supervisory authority</td></tr>
            </tbody>
          </table>

          <h2>3. How to Exercise Your Rights</h2>

          <h3>3.1 Contact Information</h3>
          <p>
            <strong>Email:</strong>{" "}
            <a href="mailto:privacy@faintechlab.com" className="text-blue-600 hover:underline">
              privacy@faintechlab.com
            </a>
            <br />
            <strong>Subject Line:</strong> &quot;Data Subject Rights Request&quot;
            <br />
            <strong>Response Time:</strong> Within 30 days (extendable to 90 days for complex requests)
          </p>

          <h3>3.2 Verification</h3>
          <p>To protect your data, we may ask you to:</p>
          <ul>
            <li>Confirm your identity via email verification</li>
            <li>Provide additional information if identity is unclear</li>
            <li>Use a verified account email address</li>
          </ul>

          <h3>3.3 Online Self-Service</h3>
          <p>During beta, you can exercise some rights directly in the app:</p>
          <ul>
            <li><strong>Access:</strong> Settings → Privacy → Download My Data</li>
            <li><strong>Erasure:</strong> Settings → Privacy → Delete My Account</li>
            <li><strong>Portability:</strong> Settings → Privacy → Export Data</li>
          </ul>

          <h2>4. Right of Access (Article 15)</h2>
          <p>You have the right to obtain:</p>
          <ul>
            <li>Confirmation that your data is being processed</li>
            <li>A copy of your personal data</li>
            <li>Information about processing purposes, categories, recipients, retention periods</li>
          </ul>
          <p><strong>Response Format:</strong> JSON or PDF</p>

          <h2>5. Right to Erasure (Article 17)</h2>
          <p>Also known as the &quot;Right to Be Forgotten.&quot; You can request erasure when:</p>
          <ul>
            <li>Data is no longer necessary for original purpose</li>
            <li>You withdraw consent (and no other legal basis exists)</li>
            <li>You object to processing (and no overriding legitimate interests)</li>
            <li>Data was unlawfully processed</li>
          </ul>

          <h3>5.1 Exceptions</h3>
          <p>We may refuse erasure when processing is necessary for:</p>
          <ul>
            <li>Exercising freedom of expression and information</li>
            <li>Compliance with legal obligations</li>
            <li>Establishment, exercise, or defense of legal claims</li>
          </ul>

          <h2>6. Right to Data Portability (Article 20)</h2>
          <p>You can request your data in a portable format:</p>
          <ul>
            <li><strong>Primary:</strong> JSON (structured, machine-readable)</li>
            <li><strong>Secondary:</strong> CSV (spreadsheet-compatible)</li>
            <li><strong>Upon request:</strong> XML, plain text</li>
          </ul>

          <h2>7. Right to Object (Article 21)</h2>
          <p>You can object to processing based on:</p>
          <ul>
            <li>Legitimate interests (including profiling)</li>
            <li>Direct marketing (absolute right)</li>
            <li>Research/statistics (public interest)</li>
          </ul>

          <h2>8. Right to Withdraw Consent (Article 7(3))</h2>
          <p>Consent is our legal basis for:</p>
          <ul>
            <li>Voice/audio recording for agent training</li>
            <li>Marketing communications</li>
            <li>Non-essential cookies</li>
          </ul>
          <p>
            <strong>How to withdraw:</strong> In-app (Settings → Privacy → Manage Consent) or
            email privacy@faintechlab.com
          </p>

          <h2>9. Right to Lodge a Complaint (Article 77)</h2>
          <p>If you believe your rights have been violated, you can complain to:</p>
          <p>
            <strong>Romanian National Supervisory Authority for Personal Data Processing (ANSPDCP)</strong>
            <br />
            Website:{" "}
            <a href="https://www.dataprotection.ro" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
              https://www.dataprotection.ro
            </a>
            <br />
            Email: anspdcp@dataprotection.ro
          </p>

          <h2>10. Response Times Summary</h2>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr><th>Request Type</th><th>Standard Response</th><th>Extended Response</th></tr>
            </thead>
            <tbody>
              <tr><td>Access</td><td>30 days</td><td>Up to 90 days</td></tr>
              <tr><td>Rectification</td><td>30 days</td><td>N/A</td></tr>
              <tr><td>Erasure</td><td>30 days</td><td>Up to 90 days</td></tr>
              <tr><td>Portability</td><td>30 days</td><td>Up to 90 days</td></tr>
              <tr><td>Objection</td><td>30 days</td><td>N/A</td></tr>
            </tbody>
          </table>

          <h2>11. Contact Information</h2>
          <p>
            <strong>Data Controller:</strong> Faintech Solutions SRL
            <br />
            <strong>Data Protection Contact:</strong>{" "}
            <a href="mailto:privacy@faintechlab.com" className="text-blue-600 hover:underline">
              privacy@faintechlab.com
            </a>
          </p>
        </article>
      </div>
    </div>
  );
}
