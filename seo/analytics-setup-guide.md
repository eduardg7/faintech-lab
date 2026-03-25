# Analytics Setup Guide for Faintech Lab

## Purpose
Complete guide for implementing Google Analytics 4 (GA4) and Search Console tracking before beta launch (Mar 24, 2026).

## Prerequisites
- [ ] Eduard to create GA4 property and provide Measurement ID (G-XXXXXXXXXX)
- [ ] Eduard to verify domain in Google Search Console
- [ ] Dev team to implement tracking code

---

## Part 1: Google Analytics 4 Setup

### Step 1: Create GA4 Property (Eduard)

1. Go to [Google Analytics](https://analytics.google.com/)
2. Create new property for "Faintech Lab"
3. Enter website URL: `https://faintech-lab.com`
4. Copy Measurement ID (format: `G-XXXXXXXXXX`)

### Step 2: Implement Tracking Code (Dev Team)

#### Option A: Using Next.js Script Component (Recommended)

Add to `/amc-frontend/src/app/layout.tsx`:

```tsx
import Script from 'next/script';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-XXXXXXXXXX');
          `}
        </Script>
      </head>
      <body className={inter.className}>
        {/* ... existing code ... */}
      </body>
    </html>
  );
}
```

#### Option B: Using Environment Variable (Best Practice)

1. Add to `.env.local`:
```bash
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

2. Create `/amc-frontend/src/lib/analytics.ts`:
```typescript
export const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;

// Track page views
export const pageview = (url: string) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', GA_MEASUREMENT_ID!, {
      page_path: url,
    });
  }
};

// Track custom events
export const event = ({
  action,
  category,
  label,
  value,
}: {
  action: string;
  category: string;
  label: string;
  value?: number;
}) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value,
    });
  }
};
```

3. Add TypeScript declarations in `/amc-frontend/src/types/gtag.d.ts`:
```typescript
declare global {
  interface Window {
    gtag: (
      command: 'config' | 'event',
      targetIdOrAction: string,
      config?: Record<string, any>
    ) => void;
    dataLayer: any[];
  }
}

export {};
```

### Step 3: Track Key Events

Add event tracking for beta signup conversions:

#### Track CTA Button Clicks
```typescript
import { event } from '@/lib/analytics';

// On "Get Early Access" button click
<button
  onClick={() => {
    event({
      action: 'signup_click',
      category: 'conversion',
      label: 'beta_early_access',
    });
    // ... existing signup logic
  }}
>
  Get Early Access
</button>
```

#### Track Scroll Depth (for blog engagement)
```typescript
// In a useEffect hook
useEffect(() => {
  const handleScroll = () => {
    const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;

    if (scrollPercent > 25 && !tracked25) {
      event({ action: 'scroll_depth', category: 'engagement', label: '25%' });
      setTracked25(true);
    }
    if (scrollPercent > 50 && !tracked50) {
      event({ action: 'scroll_depth', category: 'engagement', label: '50%' });
      setTracked50(true);
    }
    if (scrollPercent > 75 && !tracked75) {
      event({ action: 'scroll_depth', category: 'engagement', label: '75%' });
      setTracked75(true);
    }
  };

  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

---

## Part 2: Google Search Console Setup

### Step 1: Add Property (Eduard)

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add property: `https://faintech-lab.com`
3. Choose verification method:
   - **DNS verification** (recommended for production)
   - **HTML file upload** (easier for quick setup)
   - **Google Analytics** (if GA4 already set up)

### Step 2: Submit Sitemap

After verification:
1. Go to "Sitemaps" section
2. Enter sitemap URL: `https://faintech-lab.com/sitemap.xml`
3. Click "Submit"
4. Verify indexing status within 24-48 hours

### Step 3: Request Indexing (Manual)

For immediate indexing of critical pages:
1. Use URL Inspection tool
2. Enter: `https://faintech-lab.com/memory`
3. Click "Request indexing"
4. Repeat for other key pages

---

## Part 3: Core Web Vitals Monitoring

### Set Up Web Vitals Reporting

Create `/amc-frontend/src/lib/web-vitals.ts`:

```typescript
import { getCLS, getFID, getLCP, getFCP, getTTFB } from 'web-vitals';
import { event } from './analytics';

const sendToAnalytics = (metric: any) => {
  event({
    action: metric.name,
    category: 'Web Vitals',
    label: metric.id,
    value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
  });
};

export const reportWebVitals = () => {
  getCLS(sendToAnalytics);
  getFID(sendToAnalytics);
  getLCP(sendToAnalytics);
  getFCP(sendToAnalytics);
  getTTFB(sendToAnalytics);
};
```

Add to `layout.tsx`:

```typescript
import { reportWebVitals } from '@/lib/web-vitals';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    reportWebVitals();
  }, []);

  return (
    // ... existing code
  );
}
```

Install web-vitals package:

```bash
npm install web-vitals
```

---

## Part 4: Verification Checklist

Before beta launch (Mar 24):

### GA4
- [ ] Measurement ID configured in environment variables
- [ ] Tracking code loads on all pages (check Network tab)
- [ ] Real-time data appears in GA4 dashboard
- [ ] Custom events fire correctly (test in GA4 DebugView)
- [ ] Beta signup event tracked

### Search Console
- [ ] Domain verified
- [ ] Sitemap submitted
- [ ] /memory page indexed (check with `site:faintech-lab.com/memory`)
- [ ] No critical errors in Coverage report

### Web Vitals
- [ ] CLS < 0.1
- [ ] LCP < 2.5s
- [ ] INP < 200ms
- [ ] All metrics reported to GA4

---

## Success Metrics (First Week)

Track these in GA4/Search Console:

| Metric | Target | Check Date |
|--------|--------|------------|
| Pages indexed | 5+ | Mar 25 |
| Organic sessions | Baseline | Mar 26 |
| Beta signups (all channels) | 5+ | Mar 28 |
| Avg. page load time | < 3s | Mar 27 |
| Bounce rate | < 70% | Mar 28 |

---

## Next Steps

1. **Eduard**: Create GA4 property + Search Console verification
2. **Dev Team**: Implement tracking code (estimated: 2-3 hours)
3. **SEO**: Monitor indexing and analytics data post-launch
4. **All**: Review metrics at weekly sync

---

**Created:** 2026-03-19T16:50:00Z
**Owner:** seo
**Status:** Ready for implementation
**Priority:** Pre-launch requirement (Mar 24 deadline)
