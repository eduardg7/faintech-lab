import Link from "next/link";

export const metadata = {
  title: "Cookie Policy | Faintech Lab",
  description: "Faintech Lab Cookie Policy - How we use cookies and similar technologies",
};

export default function CookiePolicyPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <nav className="mb-6">
          <Link href="/legal" className="text-blue-600 hover:underline text-sm">
            ← Back to Legal
          </Link>
        </nav>

        <article className="bg-white shadow rounded-lg p-8 prose prose-gray max-w-none">
          <h1>Faintech Lab Cookie Policy</h1>

          <p className="text-sm text-gray-500 not-prose mb-6">
            <strong>Effective Date:</strong> March 24, 2026<br />
            <strong>Version:</strong> Beta 1.0
          </p>

          <h2>1. Introduction</h2>
          <p>
            This Cookie Policy explains how Faintech Lab (&quot;we,&quot; &quot;us,&quot; &quot;our&quot;) uses cookies
            and similar technologies on our website and application. By using Faintech Lab,
            you consent to the use of cookies as described in this policy.
          </p>

          <h2>2. What Are Cookies?</h2>
          <p>
            Cookies are small text files stored on your device when you visit a website.
            They help us remember your preferences, understand how you use our service,
            and improve your experience.
          </p>

          <h2>3. Types of Cookies We Use</h2>

          <h3>3.1 Essential Cookies (Always Active)</h3>
          <p>These cookies are necessary for the Service to function properly.</p>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr><th>Cookie Name</th><th>Purpose</th><th>Duration</th></tr>
            </thead>
            <tbody>
              <tr><td>session_id</td><td>Maintains your logged-in session</td><td>Session</td></tr>
              <tr><td>csrf_token</td><td>Prevents cross-site request forgery</td><td>Session</td></tr>
              <tr><td>auth_token</td><td>Authenticates your account</td><td>30 days</td></tr>
              <tr><td>preferences</td><td>Stores UI preferences</td><td>1 year</td></tr>
            </tbody>
          </table>

          <h3>3.2 Functional Cookies</h3>
          <p>These cookies enable enhanced functionality and personalization.</p>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr><th>Cookie Name</th><th>Purpose</th><th>Duration</th></tr>
            </thead>
            <tbody>
              <tr><td>theme</td><td>Remembers your theme preference</td><td>1 year</td></tr>
              <tr><td>language</td><td>Remembers your language selection</td><td>1 year</td></tr>
              <tr><td>sidebar_state</td><td>Remembers sidebar position</td><td>Session</td></tr>
            </tbody>
          </table>

          <h3>3.3 Analytics Cookies</h3>
          <p>These cookies help us understand how users interact with our Service.</p>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr><th>Cookie Name</th><th>Purpose</th><th>Duration</th></tr>
            </thead>
            <tbody>
              <tr><td>_ga</td><td>Google Analytics - distinguishes users</td><td>2 years</td></tr>
              <tr><td>_ga_*</td><td>Google Analytics - maintains session state</td><td>2 years</td></tr>
              <tr><td>usage_stats</td><td>Aggregated feature usage</td><td>30 days</td></tr>
            </tbody>
          </table>

          <h2>4. Cookie Consent</h2>
          <p>
            When you first visit Faintech Lab, you will see a cookie consent banner allowing you to:
          </p>
          <ul>
            <li>Accept all cookies</li>
            <li>Accept only essential cookies</li>
            <li>Customize cookie preferences</li>
          </ul>
          <p>
            You can change your cookie preferences at any time by clicking &quot;Cookie Settings&quot; in the footer
            or accessing your account settings.
          </p>

          <h2>5. Legal Basis for Cookie Use (GDPR)</h2>
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr><th>Cookie Type</th><th>Legal Basis</th></tr>
            </thead>
            <tbody>
              <tr><td>Essential</td><td>Contractual necessity (Article 6(1)(b))</td></tr>
              <tr><td>Functional</td><td>Consent (Article 6(1)(a))</td></tr>
              <tr><td>Analytics</td><td>Legitimate interest (Article 6(1)(f)) or Consent</td></tr>
            </tbody>
          </table>

          <h2>6. How to Manage Cookies</h2>
          <p>Most browsers allow you to:</p>
          <ul>
            <li>View cookies stored on your device</li>
            <li>Delete individual or all cookies</li>
            <li>Block cookies from specific sites</li>
            <li>Block all cookies</li>
          </ul>

          <h3>Browser-Specific Instructions</h3>
          <ul>
            <li><strong>Chrome:</strong> Settings → Privacy and security → Cookies and other site data</li>
            <li><strong>Firefox:</strong> Settings → Privacy &amp; Security → Cookies and Site Data</li>
            <li><strong>Safari:</strong> Preferences → Privacy → Manage Website Data</li>
            <li><strong>Edge:</strong> Settings → Cookies and site permissions → Cookies and site data</li>
          </ul>

          <h2>7. Contact Us</h2>
          <p>
            <strong>Email:</strong>{" "}
            <a href="mailto:privacy@faintechlab.com" className="text-blue-600 hover:underline">
              privacy@faintechlab.com
            </a>
          </p>
        </article>
      </div>
    </div>
  );
}
