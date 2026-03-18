export default function StructuredData() {
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Faintech Lab - AI Memory Management",
    "applicationCategory": "DeveloperApplication",
    "operatingSystem": "Web",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD",
      "availability": "https://schema.org/InStock"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "ratingCount": "50"
    },
    "description": "Production-grade memory for autonomous AI agents. Persistent state, multi-modal storage, and OS-level integration.",
    "featureList": [
      "Automatic state persistence",
      "Multi-modal storage (vectors, documents, structured data)",
      "Memory-as-API for agent integration",
      "Temporal queries",
      "Multi-agent synchronization",
      "Production orchestration"
    ]
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  );
}
