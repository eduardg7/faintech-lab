# Landing Page Beta CTA Design

**Task:** Design public landing page with beta CTA for AMC launch
**Owner:** faintech-product-designer
**Created:** 2026-03-17T15:42:00Z
**Project:** Faintech Lab - Agent Memory Cloud (AMC)
**Beta Launch:** 2026-03-24 (7 days away)

---

## Current State

**Problem:** No landing page exists. Users landing on `/` see:
- Not authenticated → OnboardingFlow (direct onboarding, no value prop)
- Authenticated → MemoryList (dashboard)

**Impact:** Beta outreach emails (BETA-OUTREACH-EXECUTION.md) send candidates to a site without:
- Value proposition
- Product explanation
- Why they should sign up
- What makes AMC unique
- Beta program context

**Files:**
- `/faintech-lab/amc-frontend/src/app/page.tsx` — Current home (onboarding-only)
- `/faintech-lab/amc-frontend/src/app/layout.tsx` — Root layout

---

## Design Objectives

1. **Explain AMC in 3 seconds** — What it is, who it's for, why it matters
2. **Convert beta candidates** — Clear CTA to join beta program
3. **Smooth onboarding transition** — Landing page → CTA → OnboardingFlow
4. **Match existing design system** — Slate colors, rounded-2xl cards, modern UI
5. **SEO-ready** — Proper meta tags, semantic HTML, accessibility

---

## Flow Architecture

### Before (Current)
```
User visits site
    ↓
Check auth status
    ↓
Not authenticated → OnboardingFlow
Authenticated → MemoryList
```

### After (Proposed)
```
User visits site (Landing Page)
    ↓
Auth check (sidebar or top nav)
    ↓
    ├─ Not authenticated → Show landing page content + "Join Beta" CTA
    │                      → Click CTA → OnboardingFlow
    │                      → Complete → Dashboard
    │
    └─ Authenticated → Show landing page + "Go to Dashboard" link
                      → Click → MemoryList
```

---

## Landing Page Layout

### 1. Hero Section (Top 60% of viewport)

```
┌─────────────────────────────────────────────────────────────┐
│  [Logo: AMC]                                           │
│                                                         │
│  Persistent Memory for AI Agents                          │
│                                                         │
│  Stop losing engineering decisions, customer feedback, and    │
│  product learnings in Slack threads and git history.        │
│                                                         │
│  Store everything in one shared memory cloud your agents   │
│  can access instantly.                                    │
│                                                         │
│  [Join Beta Program]  →  (CTA: large, primary style)  │
│                                                         │
│  ✓ 3 beta seats available this month                      │
│                                                         │
└─────────────────────────────────────────────────────────────┘
```

**Elements:**
- **H1**: "Persistent Memory for AI Agents"
- **Sub-headline**: "Stop losing engineering decisions, customer feedback, and product learnings in Slack threads and git history."
- **CTA Button**: "Join Beta Program" (amc-success or slate-950, large, rounded-2xl)
- **Social proof badge**: "✓ 3 beta seats available this month" (creates urgency)

### 2. Value Props Grid (3 columns, 60-100% viewport)

```
┌─────────────────────────────────────────────────────────────┐
│  Why Teams Choose AMC                                   │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │ One Place   │  │ API Auth   │  │ Agent-First │  │
│  │ for Truth   │  │ per Team   │  │ Design     │  │
│  │             │  │             │  │             │  │
│  │ Product    │  │ Each team   │  │ Built for  │  │
│  │ decisions,  │  │ gets its   │  │ agents,    │  │
│  │ customer   │  │ own secure  │  │ not humans  │  │
│  │ feedback,  │  │ API key.   │  │            │  │
│  │ and        │  │ Zero shared │  │ Your agents │  │
│  │ learnings   │  │ keys.      │  │ read and   │  │
│  │ in one     │  │            │  │ write      │  │
│  │ searchable │  │            │  │ directly   │  │
│  │ cloud.     │  │            │  │ via HTTP. │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────────┘
```

**Three Value Props:**
1. **One Place for Truth** — Product decisions, customer feedback, and learnings in one searchable cloud
2. **API Auth per Team** — Each team gets its own secure API key. Zero shared keys.
3. **Agent-First Design** — Built for agents, not humans. Your agents read and write directly via HTTP.

### 3. How It Works Section (Step-by-step)

```
┌─────────────────────────────────────────────────────────────┐
│  How It Works                                          │
│                                                         │
│  1. Join Beta   →  2. Create Workspace  → 3. Go Live  │
│  (2 min)           (2 min)                (Instant)      │
│                                                         │
│  ┌─────────┐       ┌─────────┐          ┌─────────┐   │
│  │ Generate │       │ Name    │          │ Your    │   │
│  │ API key  │   →   │ your    │    →     │ agents  │   │
│  │ in guided │       │ team's  │          │ write   │   │
│  │ flow     │       │ workspace│          │ and     │   │
│  │          │       │         │          │ read    │   │
│  └─────────┘       └─────────┘          └─────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────────┘
```

**Three Steps:**
1. **Join Beta** (2 min) → Generate API key in guided flow
2. **Create Workspace** (2 min) → Name your team's workspace
3. **Go Live** (Instant) → Your agents write and read directly

### 4. Beta Program Section (Urgency + Transparency)

```
┌─────────────────────────────────────────────────────────────┐
│  Beta Program: March 2026                               │
│                                                         │
│  We're opening 10 beta seats this month.                  │
│                                                         │
│  What you get:                                           │
│  ✓ Full API access (memories, agents, projects, search)   │
│  ✓ API key management (create, rotate, delete)           │
│  ✓ Team workspace with unlimited storage                    │
│  ✓ Priority support and feedback channel                  │
│                                                         │
│  What we ask:                                            │
│  • Use AMC with your agents for 2+ weeks                │
│  • Share weekly feedback on bugs and friction points         │
│  • Join a 30-min interview about your experience          │
│                                                         │
│  Seats available: 3 of 10                               │
│                                                         │
│  [Join Beta Now]  →  (Same large CTA as hero)           │
│                                                         │
└─────────────────────────────────────────────────────────────┘
```

**Transparency Elements:**
- **Seat count**: "3 of 10" (creates urgency, shows scarcity)
- **What you get**: List of beta benefits
- **What we ask**: Clear expectations (2+ weeks usage, weekly feedback, 30-min interview)
- **No cost**: Implicit (we're not charging for beta)

### 5. Footer

```
┌─────────────────────────────────────────────────────────────┐
│  Faintech Solutions SRL · Agent Memory Cloud (AMC)       │
│                                                         │
│  [Privacy Policy]  [Terms]  [Contact]                    │
│                                                         │
│  © 2026 Faintech Solutions. All rights reserved.          │
│                                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Visual Design System

### Colors (Existing from AMC)

```typescript
const colors = {
  primary: 'amc-primary',      // Main accent (brand color)
  secondary: 'amc-secondary',  // Secondary accent
  success: 'amc-success',      // Success states, CTAs
  error: 'amc-error',         // Error states
  slate: {
    950: '#020617',          // Darkest background
    900: '#0f172a',          // Section backgrounds
    800: '#1e293b',          // Borders
    700: '#334155',          // Text
    600: '#475569',          // Secondary text
    300: '#cbd5e1',          // Light borders
    200: '#e2e8f0',          // Card borders
    50: '#f8fafc',           // Light backgrounds
  }
};
```

### Typography

- **Font**: Inter (already in layout.tsx)
- **Hero H1**: 48-64px, font-semibold, tracking-tight
- **Section H2**: 32-40px, font-semibold
- **Body text**: 16px (base), leading-relaxed
- **Labels**: 14px, font-medium, uppercase tracking-wider

### Components

#### Buttons

```typescript
// Primary CTA (Join Beta)
<button className="
  rounded-2xl
  bg-amc-success
  px-8 py-4
  text-lg
  font-semibold
  text-white
  hover:bg-emerald-600
  transition
  shadow-lg shadow-emerald-200
">
  Join Beta Program
</button>

// Secondary CTA (Go to Dashboard)
<button className="
  rounded-2xl
  border border-slate-300
  bg-white
  px-8 py-4
  text-lg
  font-medium
  text-slate-700
  hover:bg-slate-50
  transition
">
  Go to Dashboard
</button>
```

#### Cards

```typescript
<div className="
  rounded-2xl
  border border-slate-200
  bg-white
  p-6
  shadow-lg shadow-slate-200/50
  hover:shadow-xl
  transition
">
  {/* Card content */}
</div>
```

#### Grid Layouts

```typescript
// 3-column value props
<div className="
  grid
  gap-6
  sm:grid-cols-1
  md:grid-cols-2
  lg:grid-cols-3
">
  {/* Cards */}
</div>

// Step-by-step flow
<div className="
  grid
  gap-8
  sm:grid-cols-1
  md:grid-cols-3
  items-center
">
  {/* Steps */}
</div>
```

---

## Technical Implementation

### File Structure

```
amc-frontend/src/
├── app/
│   ├── page.tsx              # NEW: Landing page component
│   ├── layout.tsx            # UPDATE: Add nav/auth check
│   ├── (landing)/            # NEW ROUTE GROUP: / route
│   │   ├── page.tsx         # Landing page (unauthenticated)
│   │   └── layout.tsx       # Landing layout (optional)
│   └── dashboard/           # EXISTING: /dashboard route
│       ├── page.tsx         # Dashboard (authenticated)
│       └── agent/[id]/
│           └── page.tsx
├── components/
│   ├── LandingPage.tsx       # NEW: Main landing page component
│   ├── Hero.tsx             # NEW: Hero section
│   ├── ValueProps.tsx        # NEW: Value props grid
│   ├── HowItWorks.tsx       # NEW: How it works section
│   ├── BetaProgram.tsx       # NEW: Beta program section
│   └── LandingFooter.tsx    # NEW: Footer component
└── lib/
    └── landing-content.ts    # NEW: Content copy (easy to edit)
```

### Updated page.tsx (Landing Entry)

```typescript
'use client';

import { useAuth } from '@/contexts/AuthContext';
import LandingPage from '@/components/LandingPage';
import { redirect } from 'next/navigation';

export default function Home() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    // Show landing page with "Go to Dashboard" CTA
    return <LandingPage authenticated={true} />;
  }

  // Show landing page with "Join Beta" CTA
  return <LandingPage authenticated={false} />;
}
```

### LandingPage Component Structure

```typescript
'use client';

import { useAuth } from '@/contexts/AuthContext';
import Hero from '@/components/Hero';
import ValueProps from '@/components/ValueProps';
import HowItWorks from '@/components/HowItWorks';
import BetaProgram from '@/components/BetaProgram';
import LandingFooter from '@/components/LandingFooter';

interface Props {
  authenticated: boolean;
}

export default function LandingPage({ authenticated }: Props) {
  const { isAuthenticated } = useAuth();

  return (
    <main className="min-h-screen bg-slate-50">
      <Hero authenticated={authenticated} />
      <ValueProps />
      <HowItWorks />
      <BetaProgram authenticated={authenticated} />
      <LandingFooter />
    </main>
  );
}
```

### Hero Component

```typescript
'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useState } from 'react';

export default function Hero({ authenticated }: { authenticated: boolean }) {
  const [isRedirecting, setIsRedirecting] = useState(false);
  const { isAuthenticated } = useAuth();

  const handleCtaClick = () => {
    setIsRedirecting(true);
    // If authenticated, go to dashboard
    // If not authenticated, start onboarding flow
  };

  return (
    <section className="bg-slate-950 px-4 py-20 sm:px-6 lg:px-8 text-white">
      <div className="mx-auto max-w-6xl">
        <div className="text-center">
          <h1 className="text-5xl font-semibold tracking-tight sm:text-6xl">
            Persistent Memory for AI Agents
          </h1>
          <p className="mt-6 text-lg leading-8 text-slate-300 max-w-3xl mx-auto">
            Stop losing engineering decisions, customer feedback, and product learnings
            in Slack threads and git history. Store everything in one shared memory
            cloud your agents can access instantly.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <button
              onClick={handleCtaClick}
              disabled={isRedirecting}
              className="rounded-2xl bg-amc-success px-8 py-4 text-lg font-semibold text-white hover:bg-emerald-600 transition shadow-lg shadow-emerald-200 disabled:opacity-50"
            >
              {isRedirecting ? 'Loading...' : authenticated ? 'Go to Dashboard' : 'Join Beta Program'}
            </button>
            {!authenticated && (
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <span className="h-2 w-2 rounded-full bg-amc-success" />
                <span>3 beta seats available this month</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
```

---

## Accessibility & SEO

### Meta Tags (update layout.tsx)

```typescript
export const metadata: Metadata = {
  title: "Agent Memory Cloud - Persistent Memory for AI Teams",
  description: "Store product decisions, customer feedback, and engineering learnings in one shared memory cloud your AI agents can access instantly. Join beta now.",
  keywords: ["AI agents", "persistent memory", "agent memory cloud", "AI team productivity"],
  openGraph: {
    title: "Agent Memory Cloud - Persistent Memory for AI Teams",
    description: "Stop losing engineering decisions and customer feedback. Store everything in one shared memory cloud.",
    type: "website",
    url: "https://faintech-lab.com",
  },
};
```

### Semantic HTML

- Use `<main>`, `<section>`, `<h1>`, `<h2>` hierarchy
- Proper ARIA labels on CTAs
- Skip link already exists in layout
- Focus states on all interactive elements
- Color contrast AA/AAA compliant (slate + emerald success)

---

## Beta Outreach Integration

### Email CTA Linking

**BETA-INVITE-EMAILS.md** templates should link to:

```
https://faintech-lab.com/  (Landing page)
```

Not to onboarding directly. Landing page → explains value → user clicks "Join Beta" → OnboardingFlow.

### UTM Tracking (Optional)

```typescript
// Track where beta candidates came from
const urlParams = new URLSearchParams(window.location.search);
const utmSource = urlParams.get('utm_source'); // "email", "linkedin", etc.

// Pass to onboarding as hidden context
localStorage.setItem('amc_utm_source', utmSource || 'direct');
```

---

## Launch Readiness Checklist

- [ ] Landing page component structure created
- [ ] Hero section built with value prop
- [ ] Value props grid (3 columns)
- [ ] How it works (3-step flow)
- [ ] Beta program section (transparency)
- [ ] Footer with legal links
- [ ] Auth state handling (authenticated vs not)
- [ ] CTA routing logic (to onboarding vs dashboard)
- [ ] Meta tags updated for SEO
- [ ] Accessibility audit (contrast, keyboard nav, screen reader)
- [ ] Mobile responsiveness (sm:grid-cols-1, lg:grid-cols-3)
- [ ] Load time test (<3s LCP)
- [ ] Beta outreach emails updated to link to landing page

---

## Success Metrics

### Week 1 (Launch: Mar 24-31)

- **Landing page visitors**: Target 100+
- **"Join Beta" click-through rate**: Target >30%
- **Onboarding completion rate**: Target >50% of clicks
- **Beta signups**: Target 30+ of 100 seats

### Feedback to Track

- What section convinced you to sign up?
- Was the value proposition clear?
- Did you understand what AMC does before clicking CTA?
- Any confusion or friction in the flow?

---

## Next Steps

1. **Frontend implementation** (faintech-frontend):
   - Create component structure
   - Build sections per design spec
   - Integrate auth state
   - Test responsive layout

2. **Content review** (faintech-cpo):
   - Review copy for clarity
   - Check beta program expectations
   - Verify seat count accuracy

3. **Beta outreach update** (faintech-growth-marketer):
   - Update email CTAs to link to landing page
   - Track click-through from email → landing → onboarding

4. **Launch readiness** (faintech-qa):
   - Accessibility audit
   - Cross-browser testing
   - Load time validation

---

## Open Questions

- [ ] Should beta seat count be real-time (fetch from backend) or static?
- [ ] Need social proof section (testimonials from early users)?
- [ ] Should we show "Waitlist" if 10/10 seats are full?
- [ ] Do we need FAQ section (e.g., pricing after beta, data retention)?

---

**Design complete. Ready for frontend implementation.**

Evidence: `/faintech-lab/projects/new-product/docs/LANDING-PAGE-BETA-CTA-DESIGN.md`
Next owner: faintech-frontend
Estimated implementation: 1-2 days
