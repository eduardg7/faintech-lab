# Onboarding Optimization Variants - A/B Test Preparation

**Created:** 2026-03-28 19:05 EET
**Owner:** faintech-frontend
**Task:** LAB-ONBOARDING-PREP-002
**Status:** READY FOR REVIEW
**Priority:** P2

---

## Overview

This document defines 3 onboarding flow variants for A/B testing to validate the hypothesis: **"If we simplify the onboarding flow to achieve time-to-first-memory < 5 minutes, then we will achieve 60%+ 24h activation rate."**

**Test Framework:**
- Traffic split: 33/33/33
- Minimum sample size: n=50 per variant
- Statistical significance: 95% confidence
- Test duration: 7 days minimum
- Primary metric: 24h activation rate (user creates first memory within 24h)
- Secondary metric: Time-to-first-memory (median time from signup to first memory)

---

## Variant A: Control (Current Multi-Step Flow)

### Description
The existing 5-step onboarding flow that guides users through workspace setup, API key configuration, and first memory creation.

### Current Implementation
**File:** `/Users/eduardgridan/faintech-lab/amc-frontend/src/components/OnboardingFlow.tsx`

**Steps:**
1. **Welcome** - Introduction to persistent memory for AI teams
2. **Workspace Setup** - Name input (e.g., "Faintech Lab")
3. **API Access** - Paste existing API key + preview key display
4. **First Memory** - Text area with default content about product decisions
5. **Success** - Confirmation and dashboard redirect

### User Flow
```
Landing → Welcome → Workspace Name → API Key → First Memory Draft → Success → Dashboard
```

### Measurement Points
1. **onboarding_started** - User lands on onboarding flow
2. **onboarding_step_completed** - User completes each step (5 events)
3. **onboarding_completed** - User finishes all steps and reaches success
4. **first_memory_created** - User creates first memory in dashboard (separate event)

### Strengths
- Clear, linear progression
- Educational content at each step
- Explicit value proposition
- Progress indicator shows completion status

### Weaknesses
- 5 steps may feel lengthy
- Requires API key upfront (friction)
- Users may drop off before completing all steps
- Time-to-first-memory may exceed 5 minutes

### Implementation Spec
- **Status:** ✅ Already implemented
- **Files:** `OnboardingFlow.tsx`, `page.tsx`
- **Routes:** `/` (root page when unauthenticated)
- **Dependencies:** None (already in production)

---

## Variant B: Simplified (Single-Step Inline)

### Description
A single-page onboarding that combines all inputs into one view with inline guidance and immediate feedback.

### Mockup

```
┌─────────────────────────────────────────────────────────────────┐
│  🎯 Set Up Your AI Memory Workspace                              │
│  Start capturing team knowledge in under 5 minutes              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Workspace Name                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Faintech Lab                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│  💡 This helps organize your team's memories                    │
│                                                                  │
│  API Key (Required)                                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ •••••••••••••••••••••••••••••••••••••••••••••••••••    │  │
│  └──────────────────────────────────────────────────────────┘  │
│  🔑 Get your API key from the dashboard settings               │
│                                                                  │
│  First Memory (Optional)                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Track product decisions, customer feedback, and          │  │
│  │ engineering learnings in one shared memory cloud.        │  │
│  │                                                          │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│  📝 We'll save this as your first memory to get you started    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ✨ Get Started                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ✓ Skip first memory (you can add it later in the dashboard)   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### User Flow
```
Landing → Single Form (all inputs) → Submit → Dashboard
```

### Key Changes from Control
1. **Single page** - All inputs visible at once
2. **Optional first memory** - Reduces friction, can skip
3. **Inline help text** - Contextual guidance next to each field
4. **Immediate validation** - Real-time feedback on inputs
5. **Shorter copy** - Less verbose explanations

### Measurement Points
1. **onboarding_started** - User views single-step form
2. **onboarding_form_field_completed** - User fills each field (3 events)
3. **onboarding_completed** - User submits form
4. **first_memory_skipped** - User skipped optional first memory field
5. **first_memory_created** - User creates first memory in dashboard

### Implementation Spec

**New Component:** `OnboardingFlowSimplified.tsx`

**Structure:**
```tsx
// Single form with 3 fields
- Workspace name (required)
- API key (required, validation)
- First memory (optional, textarea)
- "Get Started" CTA button
- "Skip first memory" checkbox
```

**Validation:**
- Workspace name: Required, min 2 characters
- API key: Required, must start with "amc_live_"
- First memory: Optional, max 500 characters

**Success State:**
- Save workspace name to localStorage
- Save API key to AuthContext
- If first memory provided, save draft to localStorage
- Redirect to dashboard
- Show toast: "Welcome! Your workspace is ready."

**Files to Create:**
- `/amc-frontend/src/components/OnboardingFlowSimplified.tsx`
- Update `/amc-frontend/src/app/page.tsx` to conditionally render based on A/B test variant

**Dependencies:**
- PostHog feature flag for A/B test assignment
- Existing AuthContext for API key storage
- localStorage for workspace name and first memory draft

### Strengths
- Faster perceived completion (single page)
- Optional first memory reduces friction
- Less cognitive load (all context visible)
- Faster time-to-first-memory potential

### Weaknesses
- May feel overwhelming (too many inputs at once)
- Less educational (less hand-holding)
- Users might skip first memory (lower initial engagement)
- No progress indication

---

## Variant C: Guided (Interactive Tutorial)

### Description
An interactive, step-by-step tutorial that teaches users how to use the platform while onboarding, with sample memory creation and guided exploration.

### Mockup

```
┌─────────────────────────────────────────────────────────────────┐
│  🎓 Learn by Doing: Interactive Tutorial                         │
│  Step 1 of 4: Understanding AI Memory                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  What is Agent Memory Cloud?                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  Imagine your AI assistant remembers every decision, learns     │
│  from every mistake, and shares knowledge across your team.     │
│                                                                  │
│  That's what we're building. Let's try it:                      │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  📝 Sample Memory:                                        │  │
│  │                                                           │  │
│  │  "We decided to use PostgreSQL instead of MongoDB for    │  │
│  │   the agent memory system because relational data        │  │
│  │   structures better match our query patterns."          │  │
│  │                                                           │  │
│  │  👆 Click this memory to see how it works               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Progress: ●●●○○ (Step 1 of 4)                                 │
│                                                                  │
│  ┌────────────┐  ┌───────────────────────────────────────────┐ │
│  │   Skip     │  │  Next: Set Up Your Workspace →            │ │
│  └────────────┘  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Step 2: Workspace Setup**
```
┌─────────────────────────────────────────────────────────────────┐
│  🎓 Learn by Doing: Interactive Tutorial                         │
│  Step 2 of 4: Your Workspace                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Create Your Workspace                                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  Your workspace is where your team's memories live.             │
│                                                                  │
│  Workspace Name:                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Faintech Lab                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ✅ Good choice! This will appear in your dashboard.           │
│                                                                  │
│  💡 Pro Tip: Use your team or project name                      │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Progress: ●●●●○ (Step 2 of 4)                                 │
│                                                                  │
│  ┌────────────┐  ┌───────────────────────────────────────────┐ │
│  │   Back     │  │  Next: Connect Your API Key →             │ │
│  └────────────┘  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Step 3: API Key + First Memory (Combined)**
```
┌─────────────────────────────────────────────────────────────────┐
│  🎓 Learn by Doing: Interactive Tutorial                         │
│  Step 3 of 4: Create Your First Memory                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Time to Write Your First Memory!                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  API Key (paste here):                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ •••••••••••••••••••••••••••••••••••••••••••••••••••    │  │
│  └──────────────────────────────────────────────────────────┘  │
│  🔑 This authenticates your workspace                          │
│                                                                  │
│  Now, let's capture something your team should remember:        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ [Editable textarea with sample memory]                    │  │
│  │                                                           │  │
│  │ "We learned that users prefer single-step forms over     │  │
│  │  multi-step wizards for simple tasks."                   │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ✨ Great! This memory is now saved in your workspace.         │
│                                                                  │
│  💡 Try It: Edit this memory or write your own                  │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Progress: ●●●●● (Step 3 of 4)                                 │
│                                                                  │
│  ┌────────────┐  ┌───────────────────────────────────────────┐ │
│  │   Back     │  │  Finish: Open Dashboard →                 │ │
│  └────────────┘  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Step 4: Success + Dashboard Tour Prompt**
```
┌─────────────────────────────────────────────────────────────────┐
│  🎓 Learn by Doing: Interactive Tutorial                         │
│  Step 4 of 4: You're Ready!                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🎉 Congratulations!                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  You've just:                                                   │
│  ✓ Created your workspace: Faintech Lab                        │
│  ✓ Connected your API key                                      │
│  ✓ Written your first memory                                   │
│                                                                  │
│  Your workspace is now live and ready to use!                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🎯 Quick Tour (2 min)                                   │  │
│  │  Learn how to search, filter, and organize memories      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🚀 Skip Tour, Go to Dashboard                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Progress: ●●●●● (Complete!)                                   │
└─────────────────────────────────────────────────────────────────┘
```

### User Flow
```
Landing → Tutorial Intro → Workspace Setup → First Memory (interactive) → Success → Dashboard (with optional tour)
```

### Key Features
1. **Educational content** - Explains concepts before asking for input
2. **Sample memories** - Shows realistic examples users can interact with
3. **Interactive elements** - Clickable samples, editable fields with live feedback
4. **Progressive disclosure** - One concept at a time
5. **Optional dashboard tour** - Continues learning after onboarding
6. **Encouraging feedback** - Positive reinforcement at each step

### Measurement Points
1. **onboarding_started** - User starts tutorial
2. **tutorial_step_completed** - User completes each tutorial step (4 events)
3. **sample_memory_clicked** - User interacts with sample memory (engagement)
4. **first_memory_edited** - User edits sample memory (customization)
5. **onboarding_completed** - User finishes tutorial
6. **dashboard_tour_started** - User starts optional tour (secondary engagement)
7. **first_memory_created** - User creates memory in dashboard

### Implementation Spec

**New Component:** `OnboardingFlowGuided.tsx`

**Structure:**
```tsx
// 4-step interactive tutorial
- Step 1: Concept intro (sample memory interaction)
- Step 2: Workspace name (with validation and feedback)
- Step 3: API key + first memory (combined, with sample)
- Step 4: Success + dashboard tour prompt

// Interactive elements
- Clickable sample memories
- Editable textareas with live preview
- Real-time validation with positive feedback
- Optional dashboard tour after completion
```

**Interactive Features:**
- Sample memories are clickable (expand to show details)
- Users can edit sample memory before submitting
- Progress indicator shows completion status
- "Pro tips" appear contextually
- Success animations on completion

**Dashboard Tour (Optional):**
- Overlay tour highlighting key features
- 3-5 steps covering: search, filters, memory list, settings
- Can be dismissed and resumed later
- Stored in localStorage to not show again

**Files to Create:**
- `/amc-frontend/src/components/OnboardingFlowGuided.tsx`
- `/amc-frontend/src/components/DashboardTour.tsx`
- Update `/amc-frontend/src/app/page.tsx` for A/B test routing

**Dependencies:**
- PostHog feature flag for A/B test assignment
- Existing AuthContext for API key storage
- localStorage for workspace name, first memory, and tour completion status

### Strengths
- Highly educational (users understand product better)
- Interactive and engaging (clickable samples)
- Builds user confidence before dashboard
- Optional tour continues learning
- May lead to higher long-term retention

### Weaknesses
- Longest flow (4 steps + optional tour)
- Most complex implementation
- May feel slow to experienced users
- Highest development effort

---

## A/B Test Implementation Requirements

### 1. Feature Flag Setup (PostHog)

**Feature Flag Name:** `onboarding-variant`

**Variants:**
- `control` (33%): Variant A - Current multi-step flow
- `simplified` (33%): Variant B - Single-step inline form
- `guided` (34%): Variant C - Interactive tutorial

**Assignment Logic:**
```typescript
// In PostHog dashboard
- Set up feature flag with 3 variants
- Configure rollout percentage: 33/33/34
- Enable for all users (100% rollout)
- Persist variant assignment per user
```

### 2. Routing Logic

**Update `/amc-frontend/src/app/page.tsx`:**
```typescript
import { usePostHog } from 'posthog-js/react';

export default function Home() {
  const { isAuthenticated } = useAuth();
  const posthog = usePostHog();

  if (!isAuthenticated) {
    // Get variant from PostHog feature flag
    const variant = posthog.getFeatureFlag('onboarding-variant');

    if (variant === 'simplified') {
      return <OnboardingFlowSimplified />;
    } else if (variant === 'guided') {
      return <OnboardingFlowGuided />;
    } else {
      return <OnboardingFlow />; // Control (default)
    }
  }

  // ... rest of component
}
```

### 3. Analytics Events

**Shared Events (All Variants):**
- `onboarding_started` - User views onboarding flow
- `onboarding_completed` - User finishes onboarding
- `first_memory_created` - User creates first memory in dashboard

**Variant-Specific Events:**

**Variant A (Control):**
- `onboarding_step_completed` - Step ID and number
- Progress: 5 events (one per step)

**Variant B (Simplified):**
- `onboarding_form_field_completed` - Field name
- `first_memory_skipped` - Boolean (if skipped)
- Progress: 3 field events + 1 completion

**Variant C (Guided):**
- `tutorial_step_completed` - Step ID and number
- `sample_memory_clicked` - Engagement tracking
- `first_memory_edited` - Customization tracking
- `dashboard_tour_started` - Secondary engagement
- Progress: 4 step events + interaction events

### 4. PostHog Dashboard Setup

**Activation Funnel Dashboard:**
1. **Funnel 1: Onboarding Completion**
   - Steps: onboarding_started → onboarding_completed → first_memory_created
   - Breakdown by variant
   - Time to complete each step

2. **Funnel 2: 24h Activation**
   - Steps: onboarding_completed → first_memory_created (within 24h)
   - Breakdown by variant
   - Conversion rate comparison

3. **Metric: Time-to-First-Memory**
   - Custom metric: Time between onboarding_started and first_memory_created
   - Breakdown by variant
   - Median and p95 values

4. **Segment: Variant Performance**
   - Segment users by onboarding-variant flag
   - Compare: completion rate, activation rate, time-to-first-memory

### 5. Success Criteria

**Primary Metric: 24h Activation Rate**
- **Success:** ≥60% activation rate (any variant)
- **Mixed:** 40-60% activation rate (iterate on winning variant)
- **Failure:** <40% activation rate (fundamental PMF reassessment)

**Secondary Metrics:**
- **Time-to-First-Memory:** Target <5 minutes median
- **Onboarding Completion Rate:** Target 80%+
- **Day 7 Retention:** Target 3+ return visits

**Statistical Significance:**
- 95% confidence interval
- Minimum sample size: n=50 per variant
- Test duration: 7 days minimum

---

## Implementation Timeline

### Week 1 (Current): Preparation ✅
- [x] Document all 3 variants with mockups
- [x] Define measurement points and analytics events
- [x] Specify implementation requirements
- [ ] Review with CPO and PM for approval
- [ ] Prioritize development based on complexity

### Week 2 (Apr 4-10): Development
- [ ] Implement Variant B (Simplified) - 2 days
- [ ] Implement Variant C (Guided) - 3 days
- [ ] Set up PostHog feature flag - 0.5 days
- [ ] Implement routing logic - 0.5 days
- [ ] Add analytics events to all variants - 1 day
- [ ] QA testing all variants - 1 day

### Week 3 (Apr 11-17): Launch & Monitoring
- [ ] Deploy A/B test to production (33/33/34 split)
- [ ] Monitor daily activation metrics
- [ ] Ensure 50+ signups per variant
- [ ] Daily check-in on variant performance

### Week 4 (Apr 18-24): Analysis & Iteration
- [ ] Analyze results (statistical significance check)
- [ ] Identify winning variant
- [ ] Document learnings and next steps
- [ ] Plan Week 5 roadmap based on results

---

## Risk Assessment

### High Risk
- **Insufficient sample size:** <50 signups per variant → delay analysis
- **Distribution blocking:** HUNTER_API_KEY value missing → no user data
- **Implementation delays:** Variant C complexity → Week 3 launch at risk

### Medium Risk
- **Statistical insignificance:** High variance in user behavior → extend test duration
- **Variant imbalance:** Uneven traffic split → reconfigure feature flags

### Low Risk
- **Technical debt:** New components increase codebase size → manageable
- **Analytics gaps:** Missing events → add instrumentation post-launch

---

## Dependencies

### External Dependencies
1. **Distribution Unblock:** HUNTER_API_KEY value from CEO (CRITICAL - blocks user data)
2. **GTM Execution:** CMO to execute distribution channels (Week 1 signups target: 5-10)
3. **PostHog Setup:** Feature flag configuration for A/B test

### Internal Dependencies
1. **Tracking Implementation:** LAB-TRACKING-ACTIVATION-001 must be complete (PostHog events)
2. **Backend API:** API key generation endpoints (currently manual)
3. **QA Resources:** Testing all 3 variants before launch

---

## Next Steps

### Immediate (Today - Mar 28)
1. ✅ Create this document with all variant specifications
2. [ ] Schedule review meeting with CPO and PM
3. [ ] Get approval on variant designs and success criteria
4. [ ] Update TASK_DB.json with implementation tasks

### This Week (Mar 29 - Apr 3)
1. [ ] Begin Variant B implementation (lowest complexity)
2. [ ] Set up PostHog feature flag
3. [ ] Add analytics events to Variant A (Control)
4. [ ] Create shared component library for variants

### Next Week (Apr 4 - Apr 10)
1. [ ] Complete Variant C implementation
2. [ ] QA all 3 variants
3. [ ] Deploy to staging for final review
4. [ ] Prepare launch checklist

---

## References

- **Product Hypothesis:** `/Users/eduardgridan/faintech-lab/docs/product/PRODUCT-HYPOTHESIS-WE2.md`
- **Current Onboarding:** `/Users/eduardgridan/faintech-lab/amc-frontend/src/components/OnboardingFlow.tsx`
- **Task Definition:** LAB-ONBOARDING-PREP-002 in TASK_DB.json
- **Industry Benchmarks:** Mixpanel 2024 Product Benchmarks Report

---

**Last Updated:** 2026-03-28 19:05 EET
**Next Review:** 2026-03-29 10:00 EET (with CPO)
**Status:** READY FOR CPO/PM REVIEW
