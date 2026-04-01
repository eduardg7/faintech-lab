# Onboarding Flow - Error Handling Pattern

**Created:** 2026-04-01 00:15 EET
**Owner:** faintech-product-designer
**Status:** CLARIFIED for engineering execution
**Priority:** P0 (critical for HN launch)

---

## Context

PR #111 (P1 Onboarding Flow) implements 5-step onboarding with backend API integration. This document clarifies the **error handling flow** for the two critical API calls to ensure graceful degradation during HN launch traffic.

---

## Critical API Calls in Onboarding

### Step 3: Create Agent
**API:** `POST /v1/agents`
**Purpose:** Create user's first AI agent
**Criticality:** HIGH - blocks memory creation

### Step 4: Create Memory
**API:** `POST /v1/memories`
**Purpose:** Store user's first memory
**Criticality:** HIGH - demonstrates core value (write capability)

### Step 5: Search Memory
**API:** `GET /v1/search/keyword`
**Purpose:** Retrieve user's memory
**Criticality:** CRITICAL - demonstrates "magic moment" (retrieve capability)

---

## Error Handling Pattern

### Pattern 1: API Timeout (Network Issues)

**Detection:** Request timeout after 10 seconds

**User Message:**
```
"Connection slow. Retrying..."
```

**Behavior:**
- Show inline spinner with retry message
- Auto-retry once after 3 seconds
- If retry fails, show manual retry button

**Design Spec:**
```
┌─────────────────────────────────────┐
│ [Spinner] Connection slow. Retrying...│
│                                      │
│           [Cancel]                   │
└─────────────────────────────────────┘
```

---

### Pattern 2: API Error (4xx/5xx)

**Detection:** Non-200 response code

**User Message:**
```
"Something went wrong. Let's try again."
```

**Behavior:**
- Show friendly error message (no technical jargon)
- Provide "Try Again" button
- Log error to console for debugging
- Allow user to skip step and continue (for non-critical steps)

**Design Spec:**
```
┌─────────────────────────────────────┐
│ ⚠️ Something went wrong.            │
│    Let's try again.                 │
│                                      │
│   [Try Again]  [Skip for now]       │
└─────────────────────────────────────┘
```

**Critical vs Non-Critical Steps:**
- **Step 3 (Create Agent):** CRITICAL - cannot skip
- **Step 4 (Create Memory):** CRITICAL - cannot skip
- **Step 5 (Search Memory):** HIGH - can skip with warning

---

### Pattern 3: Empty Response (No Results)

**Detection:** 200 OK but empty data array

**User Message:**
```
"No memories found. Let's create one first!"
```

**Behavior:**
- Only applies to Step 5 (Search Memory)
- Redirect to Step 4 (Create Memory) if no memories exist
- Show helpful message explaining why search returned no results

**Design Spec:**
```
┌─────────────────────────────────────┐
│ 🔍 No memories found.               │
│    Let's create one first!          │
│                                      │
│        [Create Memory]              │
└─────────────────────────────────────┘
```

---

### Pattern 4: Rate Limiting (429 Too Many Requests)

**Detection:** HTTP 429 response

**User Message:**
```
"Taking a quick break. Please wait 30 seconds..."
```

**Behavior:**
- Show countdown timer (30 seconds)
- Auto-retry after countdown
- Disable "Try Again" button during countdown

**Design Spec:**
```
┌─────────────────────────────────────┐
│ ⏱️ Taking a quick break.            │
│    Please wait 30 seconds...        │
│                                      │
│         [29s remaining]             │
└─────────────────────────────────────┘
```

---

## Graceful Degradation Strategy

### If All API Calls Fail

**Fallback Behavior:**
1. Show friendly message: "We're having trouble connecting. You can skip onboarding for now."
2. Provide "Skip Onboarding" button
3. Redirect to dashboard with limited functionality
4. Show banner: "Complete setup later in Settings"

**Design Spec:**
```
┌─────────────────────────────────────┐
│ ⚠️ We're having trouble connecting. │
│                                      │
│   [Try Again]  [Skip Onboarding]    │
└─────────────────────────────────────┘
```

### If Only Search Memory Fails

**Fallback Behavior:**
1. Show message: "Search is temporarily unavailable. You can still create memories!"
2. Allow user to proceed to dashboard
3. Memories are stored and searchable later
4. Show success message for completed steps

**Design Spec:**
```
┌─────────────────────────────────────┐
│ ✅ Memory created successfully!     │
│ ⚠️ Search is temporarily down.      │
│                                      │
│   [Continue to Dashboard]           │
└─────────────────────────────────────┘
```

---

## Error Message Tone Guidelines

### DO:
- ✅ Use friendly, conversational tone
- ✅ Explain what happened in simple terms
- ✅ Provide clear next action
- ✅ Offer escape hatch (skip/cancel)
- ✅ Show empathy ("We're having trouble")

### DON'T:
- ❌ Use technical jargon ("500 Internal Server Error")
- ❌ Blame the user ("You entered invalid data")
- ❌ Leave user stuck without options
- ❌ Show raw error codes to users
- ❌ Use alarming language ("CRITICAL ERROR")

---

## Implementation Checklist

- [ ] Add timeout detection (10 seconds) for all API calls
- [ ] Implement retry logic with auto-retry once
- [ ] Create error boundary component for onboarding flow
- [ ] Add "Skip" button for non-critical steps
- [ ] Implement graceful degradation path
- [ ] Add error logging to console for debugging
- [ ] Test all error scenarios before HN launch

---

## Testing Scenarios

1. **Network offline:** Should show timeout message with retry
2. **API returns 500:** Should show friendly error with retry
3. **API returns 429:** Should show countdown timer
4. **Empty search results:** Should redirect to create memory
5. **All APIs fail:** Should allow skip with dashboard redirect

---

## Success Metrics

- **Error recovery rate:** >80% of users who encounter errors complete onboarding
- **Skip rate:** <10% of users skip onboarding due to errors
- **Time to recover:** <30 seconds from error to successful retry
- **Support tickets:** 0 tickets related to onboarding errors during HN launch

---

## Related Documents

- **Onboarding Flow Spec:** `/Users/eduardgridan/faintech-lab/docs/ux/onboarding-flow-p1-implementation-requirements.md`
- **PR #111:** https://github.com/eduardg7/faintech-lab/pull/111
- **Task:** LAB-UX-20260331-CONVERSIONOPT

---

**Status:** Ready for engineering implementation
**Estimated Time:** 2-3 hours (error handling + testing)
**Deadline:** Before HN launch (April 1, 17:00 EET)
