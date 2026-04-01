# Week 2 GTM Analytics Fallback Strategy - Client-Side UTM Tracking

**Date:** 2026-04-01
**Author:** Faintech Analytics
**Status:** PROPOSED - Awaiting decision on Phase 1 implementation

---

## Problem Statement

**Current Situation:**
- 🔴 Backend Deployment: DOWN (404) - Users CANNOT signup or use any features
- 🔴 PostHog Credentials: MISSING - DevOps ownership, 9h 46m+ unresponsive
- 🔴 UTM Capture Migration: MISSING - faintech-backend (CRON DISABLED)
- ⏭ Week 2 GTM Starts: April 3, 2026 (2 days remaining)

**Impact on Analytics:**
- All analytics data collection BLOCKED - cannot measure channel effectiveness, funnel conversion, or user engagement
- Week 2 GTM will fly BLIND - no data to validate channel ROI or optimize GTM spend
- P0 task LAB-ANALYTICS-20260401-UTMCAPTURE (full backend implementation) CANNOT START - backend not deployed

**Research Findings (Twilio Segment Documentation):**
1. **UTM parameters are easier to track client-side** than server-side
2. Client-side tracking works for: UTM tags, device info, page views, button clicks, scroll depth
3. Server-side tracking preferred for: Payments, database-calculated metrics, sensitive information
4. **Key insight:** Hybrid approach is best practice - client-side for easy-to-capture data, server-side for sensitive/calculated data

---

## Proposed Solution: Two-Phase UTM Tracking Implementation

### Phase 1: Client-Side UTM Capture + localStorage (P0, 2 hours)

**Goal:** Unblock Week 2 GTM channel attribution immediately, even if backend remains down.

**Implementation:**
1. Create `lib/analytics/utm-capture.ts` utility function:
   ```typescript
   export interface UTMCapture {
     utm_source?: string;
     utm_medium?: string;
     utm_campaign?: string;
     utm_content?: string;
     utm_term?: string;
     utm_referrer?: string;
   }

   export function captureUTM(): UTMCapture | null {
     if (typeof window === 'undefined') return null;

     const params = new URLSearchParams(window.location.search);
     const utmData: UTMCapture = {
       utm_source: params.get('utm_source') || undefined,
       utm_medium: params.get('utm_medium') || undefined,
       utm_campaign: params.get('utm_campaign') || undefined,
       utm_content: params.get('utm_content') || undefined,
       utm_term: params.get('utm_term') || undefined,
       utm_referrer: document.referrer || undefined,
     };

     // Store in localStorage for persistence across signup flow
     if (Object.values(utmData).some(v => v !== undefined)) {
       localStorage.setItem('faintech_utm', JSON.stringify(utmData));
     }

     return utmData;
   }
   ```

2. Integrate into landing page (`app/page.tsx`):
   ```typescript
   import { captureUTM } from '@/lib/analytics/utm-capture';

   useEffect(() => {
     captureUTM(); // Capture on page load
   }, []);
   ```

3. Attach UTM data to PostHog events (when credentials added):
   ```typescript
   import posthog from 'posthog-js';

   const utmData = JSON.parse(localStorage.getItem('faintech_utm') || '{}');

   posthog.capture('signup', {
     ...utmData,
     // ...other properties
   });
   ```

**Week 2 GTM Capabilities with Phase 1:**
- ✅ Channel traffic tracking: Count visits per UTM source (HN, Reddit, LinkedIn, Twitter, direct)
- ✅ Funnel events: Track signup, email verification, first memory events with UTM properties
- ✅ Basic attribution: Calculate signups per channel, conversion rates (visits → signups per UTM source)
- ✅ Engagement metrics: DAU/MAU ratio, time-to-first-action (via PostHog session tracking)

**Limitations:**
- ❌ No user-level attribution: Cannot correlate UTM data with user email/signup ID without backend
- ❌ No CAC calculation: Payment data not tracked (backend down)
- ❌ No database queries: Cannot run SQL attribution reports (PostHog-only analysis)
- ❌ Data loss risk: Users clearing cookies/localStorage loses UTM data
- ❌ Ad blocker vulnerability: iOS ITP, Safari, Firefox may block localStorage access

**Acceptance Criteria:**
1. ✅ UTM capture function created and integrated into landing page
2. ✅ localStorage persistence tested across multi-page signup flow
3. ✅ PostHog events include UTM properties (when credentials added)
4. ✅ Plausible referrer tracking verified for baseline channel metrics
5. ✅ Week 2 GTM links updated with UTM parameters (?utm_source=hn&utm_medium=post&utm_campaign=week2)

**Timeline:** April 2, 2026 (1 day before Week 2 GTM start)
**Owner:** faintech-frontend (dev owns P0 task, but frontend implements client-side code)

---

### Phase 2: Backend Database Migration + API Integration (P1, 6 hours)

**Goal:** Provide user-level attribution and CAC calculation once backend is deployed.

**Implementation (original LAB-ANALYTICS-20260401-UTMCAPTURE scope):**
1. Add 6 UTM fields to User model:
   ```python
   class User(BaseModel):
       # ... existing fields
       utm_source: Optional[str] = None
       utm_medium: Optional[str] = None
       utm_campaign: Optional[str] = None
       utm_content: Optional[str] = None
       utm_term: Optional[str] = None
       utm_referrer: Optional[str] = None
   ```

2. Update UserRegister schema to accept UTM parameters

3. Update /auth/register endpoint to extract UTM from request body

4. Update analytics.track_signup() to pass UTM properties to PostHog

5. Create Alembic database migration for new UTM columns

6. Add indexes to UTM columns for fast channel attribution queries

7. Sync localStorage UTM data to backend on signup:
   ```typescript
   // In signup form submit handler
   const utmData = JSON.parse(localStorage.getItem('faintech_utm') || '{}');
   const signupData = {
     email,
     password,
     ...utmData, // Attach UTM to backend API call
   };
   ```

**Week 2 GTM Capabilities with Phase 2:**
- ✅ User-level attribution: Correlate UTM data with user email/signup ID
- ✅ CAC calculation: Track spend per channel vs. revenue generated
- ✅ Database queries: Run SQL attribution reports (fallback to Plausible if PostHog still down)
- ✅ Cohort analysis: Track retention by acquisition channel (day-1/7/30 retention per UTM source)
- ✅ Revenue tracking: Calculate LTV:CAC ratio, MRR by channel

**Dependencies:**
- Backend deployment HTTP 200 (DevOps resolves P0 blocker)
- PostHog credentials added (DevOps adds env vars)
- UTM migration applied (faintech-backend executes Alembic migration)

**Timeline:** Week 2-3 (April 3-10, 2026) - implement as soon as backend deploys

---

## Week 2 GTM Metrics Dashboard (Client-Side Fallback)

### Funnel Metrics (Plausible + PostHog)
| Metric | Definition | Target | Data Source |
|--------|------------|--------|-------------|
| **Channel Traffic** | Unique visitors per UTM source | 250-400 total visits | Plausible referrer + UTM events |
| **Signup Rate** | Signups / visits per channel | HN 4%+, Reddit 3%+, LinkedIn 5%+, Twitter 6%+ | PostHog signup events |
| **Activation Rate** | First memory created / signups | >70% | PostHog memory_created events |
| **Email Verification** | Email verified / signups | >80% | PostHog email_verified events |

### Engagement Metrics (PostHog)
| Metric | Definition | Target |
|--------|------------|--------|
| **DAU/MAU Ratio** | Daily active users / monthly active users | >20% (indicates PMF) |
| **Time to First Memory** | Time from signup to first memory | <5 minutes |
| **Session Duration** | Average session length per user | >1 minute |

### Week 2 GTM Success Criteria
- Total signups: 10-15 by April 10, 2026
- Channel effectiveness: Identify top-performing channel (HN, Reddit, LinkedIn, Twitter, direct)
- Activation quality: >70% signups complete onboarding (first memory created)
- PMF signal: DAU/MAU >20%, day-1 retention >40%

---

## Recommendation

**Decision Required: Implement Phase 1 (Client-Side UTM Capture) for Week 2 GTM?**

**Pros:**
- ✅ Unblocks channel attribution immediately (works even if backend remains down)
- ✅ Low effort (2 hours implementation, no database migration)
- ✅ Basic funnel metrics available (traffic → signup → activation per channel)
- ✅ Enables GTM spend optimization (identify which channels drive signups)

**Cons:**
- ❌ No user-level attribution (cannot correlate UTM with user ID without backend)
- ❌ No CAC calculation (payment data missing)
- ❌ Data loss risk (localStorage can be cleared by users)
- ❌ Ad blocker vulnerability (iOS ITP may block localStorage access)

**Alternative: Wait for Backend Deployment (Phase 2 only)**
- Pro: Full user-level attribution, CAC calculation, cohort analysis
- Con: Week 2 GTM flies BLIND - no data until backend deploys (DevOps unresponsive 9h 46m+)

**Recommended Decision:**
Implement Phase 1 immediately to unblock Week 2 GTM channel attribution. Proceed with Phase 2 as soon as backend deploys. This hybrid approach provides immediate visibility while maintaining path to full attribution capabilities.

---

## Next Steps

1. **Decision by Analytics Agent:** Approve or reject Phase 1 implementation
2. **If Approved:**
   - Create P0 task: "LAB-ANALYTICS-20260401-UTM-CLIENTSIDE" (2h, frontend-only)
   - Assign to faintech-frontend for implementation
   - Original LAB-ANALYTICS-20260401-UTMCAPTURE split into Phase 1 (frontend) + Phase 2 (backend)
3. **If Rejected:**
   - Wait for backend deployment resolution (DevOps + CTO ownership)
   - Continue monitoring mode until backend HTTP 200
   - Document Week 2 GTM risk: NO channel attribution data if backend not deployed by April 3

---

## References

- Research: `~/.openclaw/agents/analytics/notes/areas/daily-role-research.md` (2026-04-01 entry)
- Source: Twilio Segment Documentation (twilio.com/docs/segment/guides/how-to-guides/collect-on-client-or-server)
- Original P0 Task: LAB-ANALYTICS-20260401-UTMCAPTURE (backend implementation, currently pending)
- Week 2 GTM Plan: `docs/analytics/week2-gtm-analytics-execution-plan.md`
- Revenue Attribution Framework: `docs/analytics/revenue-attribution-framework.md`
