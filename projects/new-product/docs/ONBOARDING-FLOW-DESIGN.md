# Onboarding Flow Design - AMC Beta

**Task:** AMC-MVP-115
**Designer:** faintech-product-designer
**Date:** 2026-03-17
**Status:** READY FOR IMPLEMENTATION
**Related:** API-KEY-GENERATION-FLOW-DESIGN.md, LANDING-PAGE-BETA-CTA-DESIGN.md

---

## Overview

This design spec defines the first-run experience (FRE) for new users joining the AMC (Agent Memory Console) beta program. The goal is to guide users from sign-up to their first successful memory view in under 5 minutes, with zero hand-holding required.

---

## Target User

**Persona:** Indie AI Developer (Primary ICP from strategy doc)
- Technical: Comfortable with APIs, CLI tools, GitHub
- Motivated: Wants to reduce agent coordination overhead
- Context: Running 3-10 agents across multiple projects
- Time-poor: Will abandon if setup takes >10 minutes

---

## Success Criteria

**Quantitative:**
- Time from sign-up to first memory view: <5 minutes (p95)
- Drop-off at step 1: <20%
- Drop-off at step 2: <15%
- Drop-off at step 3: <10%

**Qualitative:**
- User understands what AMC is before account creation
- User sees immediate value after completing onboarding
- User knows where to find help if stuck
- No "what do I do next?" confusion

---

## Onboarding Flow Architecture

### Entry Points

**Entry Point A: Landing Page (Primary)**
- Route: `/`
- Auth state: Unauthenticated
- CTA: "Join Beta Program" → Step 1 (Email Input)
- User expectation: Clear value prop from hero section

**Entry Point B: Direct Sign-up (Secondary)**
- Route: `/signup`
- Auth state: Unauthenticated
- Context: User came from direct link (beta announcement, Hacker News)
- Flow: Skip landing, jump to Step 1

**Entry Point C: Authenticated User Returning**
- Route: `/`
- Auth state: Authenticated
- Context: User already completed onboarding
- Flow: Redirect to Dashboard (skip onboarding)

---

## Step-by-Step Flow

### Step 1: Email Input (Account Creation)

**Goal:** Capture email and verify user is real

**UI Layout:**
```
┌─────────────────────────────────────────┐
│                                     │
│   Join the AMC Beta Program          │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Enter your email address    │   │
│   └─────────────────────────────┘   │
│                                     │
│   [ Continue with Email → ]         │
│                                     │
│   Already have an account?           │
│   [ Sign In ]                       │
│                                     │
│   By continuing, you agree to our  │
│   Privacy Policy and Terms of Use   │
│                                     │
└─────────────────────────────────────────┘
```

**Validation Rules:**
- Email format: Standard email regex
- Disposable emails: Reject (e.g., mailinator, tempmail)
- Rate limiting: 3 attempts per minute

**Error States:**
- Invalid email: "Please enter a valid email address"
- Disposable email: "Please use a real email address"
- Rate limit: "Too many attempts. Please wait 60 seconds."

**Next:** Send verification email, show Step 2 (Verification)

---

### Step 2: Email Verification

**Goal:** Confirm email ownership before account creation

**UI Layout:**
```
┌─────────────────────────────────────────┐
│                                     │
│   Check your inbox                 │
│                                     │
│   We've sent a verification link     │
│   to:                              │
│                                     │
│   [ user@example.com ]             │
│                                     │
│   Click the link to continue, or     │
│   paste your code below:             │
│                                     │
│   ┌─────────────────┐              │
│   │ [ 6-digit code ]│              │
│   └─────────────────┘              │
│                                     │
│   [ Verify Code ]                   │
│   [ Resend Email ]                  │
│                                     │
│   Didn't receive it?                │
│   • Check spam folder               │
│   • Wait 30 seconds for resend      │
│                                     │
└─────────────────────────────────────────┘
```

**Technical Behavior:**
- Email contains: Verification link + 6-digit code (15 min expiry)
- Clicking link: Auto-fills code, submits verification
- Manual code entry: Backups if email link broken
- Resend limit: 3 resends per hour

**Error States:**
- Invalid code: "Verification code is invalid or expired"
- Resend blocked: "Too many resend attempts. Please wait."
- Email bounced: "This email address is invalid. Please try another."

**Next:** On successful verification, show Step 3 (Password Setup)

---

### Step 3: Password Setup & Account Creation

**Goal:** Complete account creation with secure password

**UI Layout:**
```
┌─────────────────────────────────────────┐
│                                     │
│   Create your password             │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Enter password              │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Confirm password            │   │
│   └─────────────────────────────┘   │
│                                     │
│   Password strength: [████░░] Strong │
│                                     │
• At least 8 characters              │
• One uppercase letter               │
• One number or special character   │
                                     │
│   [ Create Account ]                │
│                                     │
│   < Back to verification            │
│                                     │
└─────────────────────────────────────────┘
```

**Validation Rules:**
- Minimum length: 8 characters
- Uppercase: At least 1
- Number or special: At least 1
- Common passwords: Block (e.g., password123, qwerty)

**Strength Indicator:**
- Red (0-2): Weak - easy to crack
- Yellow (3-4): Medium - acceptable
- Green (5): Strong - recommended

**Error States:**
- Passwords don't match: "Passwords do not match"
- Too weak: "Password is too weak. Add more complexity."
- Common password: "Please choose a stronger password."

**Next:** On successful account creation, show Step 4 (Welcome & API Key)

---

### Step 4: Welcome & First API Key

**Goal:** Celebrate signup, guide to first action (API key generation)

**UI Layout:**
```
┌─────────────────────────────────────────┐
│                                     │
│   Welcome to AMC! 🎉             │
│                                     │
│   Your account is ready. Let's set   │
│   up your first API key.            │
│                                     │
│   ┌─────────────────────────────┐   │
│   │ Key Name:                   │   │
│   │ [ My First Key ]           │   │
│   └─────────────────────────────┘   │
│                                     │
│   [ Generate API Key ]              │
│   [ Skip to Dashboard ]             │
│                                     │
│   Need help?                        │
│   [ Quick Start Guide ]             │
│   [ Contact Support ]               │
│                                     │
└─────────────────────────────────────────┘
```

**Behavior:**
- [Generate API Key]: Redirects to API Key Generation flow (see API-KEY-GENERATION-FLOW-DESIGN.md)
- [Skip to Dashboard]: Redirects to empty dashboard with onboarding tooltip
- Key name pre-filled: "My First Key" (editable)

**Smart Defaults:**
- If user came from landing page, use referral UTM to personalize welcome
- If user from Hacker News, mention "HN community beta"

**Next:** Redirect to Dashboard (Step 5) with onboarding completion flag

---

### Step 5: Dashboard (First View)

**Goal:** Show immediate value with empty state that guides action

**UI Layout (Empty State):**
```
┌─────────────────────────────────────────┐
│ [Back] [My API Keys] [+ New Key] │
├─────────────────────────────────────────┤
│                                     │
│         No memories yet            │
│                                     │
│   ┌─────────────────────────────┐   │
│   │     [ Create Memory ]      │   │
│   └─────────────────────────────┘   │
│                                     │
│   Or connect your first agent:       │
│   ┌─────────────────────────────┐   │
│   │ [ View Quick Start Guide ] │   │
│   └─────────────────────────────┘   │
│                                     │
│   💡 Tip: Use the REST API to     │
│   store agent memories automatically  │
│                                     │
└─────────────────────────────────────────┘
```

**Empty State Behavior:**
- CTA: Primary button "Create Memory" (manual entry for testing)
- Secondary: "View Quick Start Guide" (docs link)
- Tooltip: "Start by creating your first memory or connecting an agent"

**Progress Indicator:**
- Badge: "Onboarding Complete" (dismiss after 24 hours)
- Sidebar highlight: "API Keys" section (first 3 views)

**Next:** User creates memory OR connects agent → normal dashboard flow

---

## Technical Implementation Notes

### Route Structure

| Route | Auth Required | Onboarding Step | Description |
|-------|--------------|-----------------|-------------|
| `/` | No | Landing page | Hero + value props + CTA |
| `/signup` | No | Step 1 (Email) | Direct sign-up entry |
| `/signup/verify` | No | Step 2 (Verification) | Email verification UI |
| `/signup/create-account` | No | Step 3 (Password) | Password setup UI |
| `/welcome` | Yes | Step 4 (Welcome) | First API key prompt |
| `/dashboard` | Yes | Step 5 (Dashboard) | Main app (empty state if first-time) |

### State Management

```typescript
interface OnboardingState {
  step: 1 | 2 | 3 | 4 | 5 | 'complete';
  email?: string;
  verificationCode?: string;
  hasCompletedOnboarding: boolean;
  firstTimeUser: boolean;
}

// LocalStorage keys
const ONBOARDING_KEY = 'amc_onboarding_state';
const FIRST_TIME_KEY = 'amc_first_time_user';
```

### Backend API Endpoints Required

**POST /v1/auth/signup**
- Input: `{ email: string }`
- Output: `{ message: "Verification email sent", expiresAt: ISO8601 }`

**POST /v1/auth/verify-email**
- Input: `{ email: string, code: string }`
- Output: `{ token: string, userId: string }`

**POST /v1/auth/create-account**
- Input: `{ email: string, code: string, password: string }`
- Output: `{ accessToken: string, refreshToken: string, user: User }`

**GET /v1/auth/onboarding-status**
- Headers: `Authorization: Bearer <token>`
- Output: `{ hasCompletedOnboarding: boolean, onboardingStep: number }`

### Security Considerations

- Password hashing: bcrypt with salt rounds ≥12
- Verification code: Crypto-random 6 digits, 15 min expiry
- Rate limiting: 3 signup attempts/min, 3 verify attempts/min
- Email verification: Required before password setup (prevents fake accounts)
- Session tokens: JWT with 1 hour expiry, refresh token with 30 days

---

## Accessibility Requirements

### Keyboard Navigation

- `Tab`: Navigate between form fields
- `Enter`: Submit current step
- `Escape`: Cancel and return to previous step
- All CTAs focusable via keyboard

### Screen Reader Support

- ARIA labels: All form fields have `aria-label`
- Live regions: Form errors announced immediately
- Focus management: Focus trapped in modal, restored on close
- Progress: "Step 3 of 5: Create password" announced on step change

### Color Contrast

- WCAG AA: 4.5:1 contrast minimum for all text
- Error states: Red + icon (not color alone)
- Success states: Green + checkmark icon

---

## Mobile Responsiveness

### Mobile (<768px)
- Single column layout
- Larger touch targets (44px min)
- Simplified forms (remove optional fields)
- Back button always visible

### Tablet (768px-1024px)
- Centered container (max-width: 600px)
- Side-by-side CTAs if horizontal space allows
- Collapsible help sections

### Desktop (>1024px)
- Max-width container (800px)
- Two-column layout for help + form
- Sidebar navigation for returning users

---

## Error Recovery

### Scenario 1: Verification Email Lost

**User Action:** Click "Resend Email"
**System Response:** Send new code, invalidate old code
**Notification:** Toast "New verification code sent"

### Scenario 2: Browser Tab Closed During Onboarding

**Recovery:**
- Email link still valid (15 min expiry)
- Re-opening `/signup` resumes at Step 2 (if email verified)
- Password step requires fresh verification if expired

### Scenario 3: Account Creation Failed

**Error Display:**
- Inline error message below form field
- CTA: "Try again" or "Contact support"
- Logging: Error details sent to Sentry for debugging

---

## Success Metrics & Tracking

### Analytics Events

```typescript
// Step completion events
analytics.track('Onboarding Step Complete', {
  step: 1,
  stepName: 'email_input',
  userId: user_id,
  sessionId: session_id
});

// Drop-off events (page unload before step completion)
analytics.track('Onboarding Drop-off', {
  step: 2,
  stepName: 'email_verification',
  dropoffReason: 'page_close',
  timeOnStep: 45 // seconds
});

// Conversion event
analytics.track('Onboarding Complete', {
  totalDuration: 245, // seconds
  firstAction: 'create_api_key' | 'skip_to_dashboard'
});
```

### Funnel Targets

| Metric | Target | Current (TBD) |
|--------|---------|----------------|
| Step 1 → 2 (Email → Verify) | >80% | - |
| Step 2 → 3 (Verify → Password) | >85% | - |
| Step 3 → 4 (Password → Welcome) | >90% | - |
| Step 4 → 5 (Welcome → Dashboard) | >95% | - |
| Total conversion (Email → Dashboard) | >60% | - |

### Time-to-Value Metrics

- Median time: Sign-up → First memory created: <5 minutes
- p95 time: Sign-up → First memory created: <10 minutes
- Drop-off: Users spending >2 minutes on any step (potential confusion)

---

## Next Steps

**Immediate (Implementation):**
- Frontend: Implement Step 1-5 UI components
- Backend: Create auth/signup API endpoints
- Integration: Wire up form submission → API → state updates

**Post-Launch (Beta Week 1):**
- Monitor drop-off at each step (identify friction)
- A/B test: Single-step vs multi-step signup
- Survey: "How easy was onboarding? 1-5 stars"

**Post-Launch (Beta Week 2-4):**
- Add "Skip verification" for trusted domains (internal users)
- Implement social sign-up (GitHub OAuth) if conversion <50%
- Create onboarding video walkthrough (embed in Step 4)

---

## Appendices

### A. Email Templates

**Verification Email:**
```
Subject: Verify your email for AMC Beta

Hi [User],

Welcome to the Agent Memory Console beta!

Your verification code is: [CODE]

Or click this link to verify automatically:
[VERIFICATION_LINK]

This code expires in 15 minutes.

— The Faintech Team
```

**Welcome Email (after account creation):**
```
Subject: Welcome to AMC! Here's how to get started

Hi [User],

You're in! 🎉

Your AMC beta account is ready. Here's how to get started in 5 minutes:

1. Generate your first API key
2. Connect your agent (use our REST API)
3. View your first memory in the dashboard

[Quick Start Guide] →
[API Documentation] →
[Contact Support] →

Happy memory building!

— The Faintech Team
```

### B. Copywriting Guidelines

**Tone:** Technical, concise, confident
**Avoid:** "We're so excited you're here!", "Welcome aboard!"
**Prefer:** "Your account is ready. Let's set up your first API key."

**Call-to-Action Patterns:**
- Primary: Verb-based, action-oriented ("Generate API Key")
- Secondary: Lower urgency, exploratory ("View Quick Start Guide")
- Error: Helpful, not blaming ("Try again" vs "You failed")

### C. Edge Cases

**Edge Case 1: User Already Has Account**
- Detection: Email already exists in database
- Action: Redirect to `/signin` with message "You already have an account. Sign in instead."

**Edge Case 2: Verification Code Expired**
- Detection: Code timestamp >15 minutes ago
- Action: Show expired UI with "Request new code" button

**Edge Case 3: Weak Password After Multiple Attempts**
- Detection: 5 failed password submissions
- Action: Require CAPTCHA or rate-limit to 1 attempt per minute

---

**Document Status:** READY FOR IMPLEMENTATION
**Target Implementation:** 1-2 days (frontend + backend)
**Owner for Implementation:** faintech-frontend (UI), faintech-backend (API)
**Design Review:** Ready for CPO approval
**Updated:** 2026-03-17T19:03:00Z
