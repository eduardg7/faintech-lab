# First-Run Onboarding Flow - Engineering Clarification

**Source Spec:** `onboarding-flow-first-run-spec.md`
**Created:** 2026-03-30 23:45 EET
**Designer:** faintech-product-designer
**Target:** faintech-frontend

---

## Purpose

This document clarifies technical implementation details for the First-Run Onboarding Flow to ensure engineering can execute without ambiguity. References the comprehensive spec at `onboarding-flow-first-run-spec.md`.

---

## 1. Screen Transition Animations

**Animation Type:** Slide transitions between screens

**Timing:**
- Duration: 400ms
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` (ease-out)
- Direction: Left-to-right for forward, right-to-left for back

**Implementation:**
```typescript
const variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? 1000 : -1000,
    opacity: 0
  }),
  center: {
    x: 0,
    opacity: 1
  },
  exit: (direction: number) => ({
    x: direction < 0 ? 1000 : -1000,
    opacity: 0
  })
};
```

**Progress Indicator:**
- Dot transition: Scale + color change (200ms)
- Active dot: Scale 1.2x, primary color
- Inactive dot: Scale 1x, gray color

---

## 2. State Management

**State Shape:**
```typescript
interface OnboardingState {
  currentStep: 1 | 2 | 3 | 4 | 5;
  direction: 'forward' | 'backward';

  // Step 2: Agent Setup
  agentName: string;
  agentType: 'general' | 'code' | 'research';

  // Step 3: First Memory
  memoryContent: string;
  memoryTags: string[];

  // Step 4: Search
  searchQuery: string;
  searchResults: Memory[];

  // Metadata
  startTime: number;
  completedAt?: number;
  skippedAt?: number;
}
```

**Persistence:**
- Store in `localStorage` with key `amc_onboarding_progress`
- Restore on page reload if user drops off
- Clear on completion or explicit skip

**Validation Rules:**
- Agent name: 3-50 characters, alphanumeric + spaces + hyphens
- Memory content: 10-5000 characters
- Search query: 2-200 characters

---

## 3. Error Handling Flows

### Agent Creation Failure
```
User submits agent → API fails → Show inline error
"Couldn't create agent. [Retry]"
→ Retry button resubmits → Success → Continue
```

**Error Display:**
- Inline error below form (red text, 14px)
- Retry button (primary action)
- Don't block progression (allow skip)

### Memory Creation Failure
```
User saves memory → API fails → Show error toast
"Failed to save memory. Please try again."
→ Retry button in toast → Resubmit → Success → Continue
```

**Auto-save Draft:**
- Save to `localStorage` every 2 seconds
- Restore on page reload
- Clear on successful save

### Search Failure
```
User searches → API fails → Show empty state
"Search failed. Please try again."
→ Retry button → Resubmit → Success → Show results
```

**Network Error:**
- Check `navigator.onLine` before API calls
- Show offline toast if offline
- Queue request for retry when online

---

## 4. Loading States

### Screen Transitions
- No loading spinner between screens (animation is enough)
- Pre-load next screen's data during current screen

### API Calls
**Agent Creation:**
- Button shows spinner + "Creating..."
- Disable button during creation
- Success: Auto-advance to next screen

**Memory Creation:**
- Button shows spinner + "Saving..."
- Disable button during save
- Success: Show checkmark animation (300ms) → Auto-advance

**Search:**
- Show skeleton loader in results area
- Search icon animates (pulsing)
- Results fade in (200ms)

---

## 5. Auto-Advance Behavior

**Screen 1 (Welcome):**
- Auto-advance after 20 seconds
- Show countdown timer (optional)
- User can click to advance earlier

**Screen 2-4:**
- NO auto-advance
- User must complete action or click "Continue"

**Screen 5 (Success):**
- No auto-advance
- User must click "Go to Dashboard"

---

## 6. Skip Functionality

**Skip Button Location:**
- Screen 2-4: Top-right corner
- Screen 5: No skip (completion screen)

**Skip Behavior:**
```typescript
const handleSkip = () => {
  // Track analytics
  analytics.track('onboarding_skipped', {
    step: currentStep,
    timeSpent: Date.now() - startTime
  });

  // Mark as skipped
  localStorage.setItem('amc_onboarding_skipped', 'true');

  // Redirect to dashboard
  router.push('/dashboard');
};
```

**Skip Confirmation:**
- No confirmation dialog (keep it fast)
- Show toast: "You can complete setup later in Settings"

---

## 7. Example Memory Templates

**Pre-defined Templates (clickable):**
1. "Project uses [technology] with [hosting provider]"
2. "Team decided to use [architecture pattern]"
3. "API rate limit is [X] req/hour per user"
4. "Database schema: [table] → [column] → [type]"
5. "Deployment process: [step 1] → [step 2] → [step 3]"

**Template Interaction:**
- Click template → Populate textarea
- User can edit before saving
- Track which template was used (analytics)

---

## 8. Search Pre-population

**Algorithm:**
```typescript
const suggestSearchQuery = (memoryContent: string): string[] => {
  // Extract nouns and technical terms
  const keywords = extractKeywords(memoryContent);

  // Return top 3 most relevant
  return keywords.slice(0, 3);
};

// Example:
// Memory: "Project uses PostgreSQL 15 with Neon hosting"
// Suggestions: ["PostgreSQL", "Neon", "database"]
```

**UI Implementation:**
- Show as clickable chips below search input
- Click chip → Populate search input → Auto-submit search

---

## 9. Progress Persistence

**What to Persist:**
```typescript
interface PersistedProgress {
  currentStep: number;
  agentName?: string;
  agentType?: string;
  memoryContent?: string;
  memoryId?: string;
  startTime: number;
}
```

**When to Persist:**
- On step completion (before advancing)
- On form field blur (auto-save draft)
- On explicit "Save & Continue Later"

**When to Clear:**
- On completion (step 5)
- On explicit skip
- On "Start Over" action (in settings)

**Restore Logic:**
```typescript
const restoreProgress = () => {
  const saved = localStorage.getItem('amc_onboarding_progress');
  if (saved) {
    const progress = JSON.parse(saved);

    // Ask user if they want to continue
    showRestoreDialog(progress.currentStep);
  }
};
```

---

## 10. Component Structure

```
src/components/Onboarding/
├── index.ts                        # Export OnboardingFlow
├── OnboardingFlow.tsx              # Main container + state machine
├── screens/
│   ├── WelcomeScreen.tsx           # Screen 1
│   ├── AgentSetupScreen.tsx        # Screen 2
│   ├── FirstMemoryScreen.tsx       # Screen 3
│   ├── SearchMemoryScreen.tsx      # Screen 4
│   └── SuccessScreen.tsx           # Screen 5
├── shared/
│   ├── ProgressBar.tsx             # 5-dot progress indicator
│   ├── ScreenTransition.tsx        # Animation wrapper
│   └── SkipButton.tsx              # Skip button component
├── hooks/
│   ├── useOnboardingState.ts       # State management hook
│   ├── useAutoSave.ts              # Auto-save draft hook
│   └── useOnboardingAnalytics.ts   # Analytics tracking
└── types.ts                        # TypeScript interfaces
```

---

## 11. API Integration

### Create Agent
```typescript
POST /api/agents
{
  name: string,          // 3-50 chars
  type: 'general' | 'code' | 'research'
}

Response:
{
  id: string,
  name: string,
  type: string,
  createdAt: string
}
```

### Create Memory
```typescript
POST /api/memories
{
  agentId: string,
  content: string,       // 10-5000 chars
  tags?: string[]        // optional
}

Response:
{
  id: string,
  content: string,
  tags: string[],
  createdAt: string
}
```

### Search Memories
```typescript
GET /api/memories/search?q={query}&agentId={agentId}

Response:
{
  results: [
    {
      id: string,
      content: string,
      preview: string,    // First 100 chars
      tags: string[],
      agentName: string,
      createdAt: string,
      relevanceScore: number
    }
  ],
  total: number
}
```

---

## 12. Analytics Events

**Track these events:**
1. `onboarding_started` - User lands on Screen 1
2. `onboarding_step_completed` - User completes a step (include step number)
3. `onboarding_step_skipped` - User skips a step (include step number)
4. `onboarding_completed` - User reaches Screen 5 (include total time)
5. `onboarding_abandoned` - User leaves mid-flow (include last step)
6. `template_used` - User clicks example template (include template ID)
7. `search_performed` - User searches memory (include query length)
8. `memory_created` - User saves first memory (include character count)

**Event Properties:**
```typescript
{
  step: 1 | 2 | 3 | 4 | 5,
  timeSpent: number,        // seconds
  templateUsed?: string,
  memoryLength?: number,
  searchQueryLength?: number
}
```

---

## 13. Performance Targets

**Time to Interactive:**
- Initial load: < 1.5s
- Screen transitions: < 100ms (animation is 400ms, but code should be ready)

**API Response Times:**
- Agent creation: < 500ms
- Memory creation: < 600ms
- Search: < 800ms

**Success Metrics:**
- 95% complete Screen 1 within 20s
- 90% complete Screen 2 within 60s
- 85% complete Screen 3 within 120s
- 80% complete Screen 4 within 90s
- 75% complete entire flow within 5min

---

## 14. Accessibility

**Keyboard Navigation:**
- Tab: Move between interactive elements
- Enter: Submit form / advance to next screen
- Escape: Skip onboarding (with confirmation)

**Screen Reader:**
- Announce step number: "Step 1 of 5"
- Announce progress: "You are on step 2 of 5"
- Announce errors: "Error: Agent name must be at least 3 characters"

**Color Contrast:**
- Primary button: 4.5:1 minimum
- Error text: 4.5:1 minimum
- Progress dots: 3:1 minimum

---

## 15. Testing Checklist

**Critical Tests:**
- [ ] Screen transitions animate correctly (400ms ease-out)
- [ ] Progress persists across page reloads
- [ ] Auto-advance works on Screen 1 (20s)
- [ ] Skip button works on Screens 2-4
- [ ] Agent name validation (3-50 chars)
- [ ] Memory content validation (10-5000 chars)
- [ ] Search query validation (2-200 chars)
- [ ] Error handling for API failures
- [ ] Loading states show during API calls
- [ ] Example templates populate textarea
- [ ] Search pre-population suggests keywords
- [ ] Success screen shows total time
- [ ] Analytics events fire correctly

---

## Summary

This clarification addresses:
1. ✅ Animation timing (400ms ease-out, slide transitions)
2. ✅ State management (TypeScript interfaces, localStorage persistence)
3. ✅ Error handling (inline errors, retry buttons, network detection)
4. ✅ Loading states (spinners, skeleton loaders, animations)
5. ✅ Auto-advance behavior (Screen 1 only, 20s countdown)
6. ✅ Skip functionality (no confirmation, track analytics)
7. ✅ Example templates (5 pre-defined, clickable)
8. ✅ Search pre-population (keyword extraction algorithm)
9. ✅ Progress persistence (localStorage, restore on reload)
10. ✅ Component structure (8 files recommended)
11. ✅ API contracts (3 endpoints with request/response shapes)
12. ✅ Analytics events (8 events with properties)
13. ✅ Performance targets (< 5min completion)
14. ✅ Accessibility (keyboard, screen reader, contrast)
15. ✅ Testing checklist (13 critical tests)

**Status:** READY FOR IMPLEMENTATION

---

**Created:** 2026-03-30 23:45 EET
**Designer:** faintech-product-designer
**Target:** faintech-frontend
