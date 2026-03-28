import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import { QueryProvider } from "@/providers/QueryProvider";
import { AnalyticsProvider } from "@/providers/AnalyticsProvider";
import SkipLink from "@/components/ui/SkipLink";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Faintech Lab | Agent Memory Cloud - Persistent Memory for AI Workflows & Autonomous Agents",
  description: "Faintech Lab provides persistent, reliable memory storage for AI agents and autonomous workflows. Never lose agent state again with our agent memory cloud.",
  keywords: "agent memory, AI memory, persistent memory, autonomous agents, AI workflows, agent state management, LLM memory, autonomous systems, developer tools, AI infrastructure",
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://faintech-lab.com',
    title: 'Faintech Lab | Agent Memory Cloud - Persistent Memory for AI Workflows',
    description: 'Faintech Lab provides persistent, reliable memory storage for AI agents and autonomous workflows. Never lose agent state again with our agent memory cloud.',
    siteName: 'Faintech Lab',
    images: [
      {
        url: 'https://faintech-lab.com/thumbnail.png',
        width: 1200,
        height: 630,
        alt: 'Faintech Lab - Agent Memory Cloud',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Faintech Lab | Agent Memory Cloud',
    description: 'Persistent memory for AI agents and autonomous workflows. Never lose agent state again.',
    creator: '@faintechlab',
    images: ['https://faintech-lab.com/thumbnail.png'],
  },
  metadataBase: new URL('https://faintech-lab.com'),
  alternates: {
    canonical: '/',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "SoftwareApplication",
              "name": "Faintech Lab - Agent Memory Cloud",
              "description": "Persistent, reliable memory storage for AI agents and autonomous workflows. Never lose agent state again with our agent memory cloud.",
              "url": "https://faintech-lab.com",
              "applicationCategory": "DeveloperApplication",
              "operatingSystem": "Web-based",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock"
              },
              "creator": {
                "@type": "Organization",
                "name": "Faintech Solutions SRL"
              },
              "featureList": [
                "Persistent AI agent memory",
                "Agent state management",
                "Workflow integration",
                "Secure storage",
                "Developer API"
              ],
              "keywords": "agent memory, AI memory, persistent memory, autonomous agents, AI workflows, agent state management, LLM memory"
            })
          }}
        />
      </head>
      <body className={inter.className}>
        <SkipLink targetId="main-content" />
        <QueryProvider>
          <AuthProvider>
            <AnalyticsProvider>
              {children}
            </AnalyticsProvider>
          </AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
