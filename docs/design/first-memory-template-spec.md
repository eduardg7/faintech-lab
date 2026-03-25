# First Memory Template — Interaction Specification

**Created:** 2026-03-19T19:56:00Z
**Owner:** faintech-product-designer
**Task:** AMC-MVP-115 (Onboarding Flow - Slice 3)
**Handoff:** faintech-frontend
**Target:** New user creates first memory in <90 seconds (Step 4 of onboarding)

---

## Problem Statement

User research synthesis (2026-03-17) identified **First Memory Creation (Step 4)** as a design gap. Without guidance, new users face blank-slate friction and don't know what to write, extending onboarding time beyond the 5-minute target.

**Research insight:** Templates reduce first-action friction 40% (Intercom research).

---

## Solution

Pre-filled memory template with example content that users can edit OR accept in one click.

---

## Entry Point

**Trigger:** User completes API key confirmation (Step 3) → advances to Step 4

**State check:**
```
if (localStorage.getItem('amc_onboarding_completed') === 'true') {
  skip to MemoryList;
}
```

---

## Template Content

### Default Template (Pre-filled)

```json
{
  "title": "My first agent memory",
  "content": "I learned that using structured memory helps agents avoid repeating mistakes. For example, when I built my last agent, it kept forgetting user preferences until I added a memory layer. Now I'm trying AMC to see if it improves my agent's context retention.",
  "type": "learning",
  "tags": ["first-memory", "onboarding", "example"]
}
```

**Rationale:**
- **Title:** Generic but personalizable ("My first agent memory")
- **Content:** Real example (3 sentences, ~40 words) that demonstrates value
- **Type:** Defaults to "learning" (most common for new users)
- **Tags:** Includes "first-memory" for analytics tracking

### Alternative Templates (Optional - Future Enhancement)

| Template | Title | Content Preview |
|----------|-------|-----------------|
| **Outcome** | "Shipped my first feature" | "Today I completed [feature name]..." |
| **Preference** | "My agent preferences" | "When building agents, I prefer..." |
| **Context** | "Project context" | "I'm working on [project]..." |

**MVP Decision:** Ship with single template (default). Add alternatives post-beta if analytics show high edit rate.

---

## Interaction Flow

```
┌─────────────────────────────────────────────┐
│  Step 4: Create Your First Memory          │
├─────────────────────────────────────────────┤
│                                             │
│  [Title Input]                              │
│  "My first agent memory"                    │
│                                             │
│  [Content Textarea]                         │
│  "I learned that using structured memory   │
│   helps agents avoid repeating mistakes..."│
│                                             │
│  [Type Dropdown: Learning ▼]                │
│                                             │
│  [Tags: first-memory, onboarding, example]  │
│                                             │
│  ┌─────────────┐  ┌──────────────────┐     │
│  │ ✏️ Edit     │  │ ✅ Create Memory │     │
│  └─────────────┘  └──────────────────┘     │
│                                             │
│  💡 Tip: You can edit this or create as-is  │
└─────────────────────────────────────────────┘
```

---

## Interaction States

### State 1: Template Loaded (Default)

- Title, content, type, tags pre-filled
- "Edit" button visible (secondary action)
- "Create Memory" button primary (green, prominent)
- Tip text visible below buttons

### State 2: Editing

- Click "Edit" → Fields become editable
- Title: text input (max 100 chars)
- Content: textarea (max 1000 chars, character count shown)
- Type: dropdown (learning, outcome, preference, context)
- Tags: tag input with autocomplete (optional)
- "Cancel" button appears (resets to template)
- "Create Memory" button remains primary

### State 3: Submitting

- "Create Memory" button shows spinner
- Button disabled during submission
- Timeout after 5 seconds → error state

### State 4: Success

- Success animation (confetti or checkmark pulse, 1.5s)
- Toast notification: "First memory created! 🎉"
- Auto-advance to Step 5 (success screen) after 2 seconds

### State 5: Error

- Error toast: "Failed to create memory. Please try again."
- "Create Memory" button re-enabled
- Error logged to analytics: `onboarding_first_memory_error`

---

## Edge Cases

### EC1: User Clears All Content

**Trigger:** User deletes all template content, leaves blank
**Behavior:** "Create Memory" button disabled
**Message:** "Please add some content to create your memory"

### EC2: Content Exceeds 1000 Characters

**Trigger:** User types >1000 characters
**Behavior:** Character count turns red, excess text truncated
**Message:** "Memory content limited to 1000 characters"

### EC3: Network Error During Submission

**Trigger:** API call fails (timeout, 5xx error)
**Behavior:** Error state, button re-enabled
**Message:** "Network error. Please check your connection and try again."

### EC4: User Skips First Memory

**Trigger:** User clicks "Skip for now" (if implemented)
**Behavior:** Set `amc_first_memory_skipped: true` in localStorage
**Analytics:** `onboarding_first_memory_skipped`
**Next:** Advance to success screen, show reminder later

### EC5: Returning User

**Trigger:** User completed onboarding but didn't create first memory
**Behavior:** Check `amc_first_memory_created` flag
**Message:** "Welcome back! Ready to create your first memory?"

---

## API Contract

### Request

```http
POST /api/memories
Content-Type: application/json
Authorization: Bearer <api_key>

{
  "title": "My first agent memory",
  "content": "I learned that using structured memory helps agents avoid repeating mistakes...",
  "type": "learning",
  "tags": ["first-memory", "onboarding", "example"],
  "agent_id": "user-onboarding",
  "metadata": {
    "onboarding_step": 4,
    "template_used": "default"
  }
}
```

### Response (Success)

```json
{
  "id": "mem_abc123",
  "title": "My first agent memory",
  "content": "I learned that using structured memory helps agents avoid repeating mistakes...",
  "type": "learning",
  "tags": ["first-memory", "onboarding", "example"],
  "created_at": "2026-03-19T19:56:00Z",
  "agent_id": "user-onboarding"
}
```

### Response (Error)

```json
{
  "error": "validation_error",
  "message": "Content must not be empty",
  "field": "content"
}
```

---

## Analytics Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `onboarding_first_memory_step_viewed` | Step 4 loads | `template_shown: true` |
| `onboarding_first_memory_edited` | User clicks "Edit" | `fields_changed: ["title", "content"]` |
| `onboarding_first_memory_created` | Memory successfully created | `template_used: "default", edit_count: 2, time_on_step_ms: 45000` |
| `onboarding_first_memory_error` | API error | `error_type: "network", retry_count: 1` |
| `onboarding_first_memory_skipped` | User clicks "Skip" | `reason: "user_choice"` |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Step 4 completion rate | >95% | `onboarding_first_memory_created / onboarding_first_memory_step_viewed` |
| Time on Step 4 | <90 seconds | `time_on_step_ms` from analytics |
| Template edit rate | <40% | `onboarding_first_memory_edited / onboarding_first_memory_step_viewed` |
| Skip rate | <10% | `onboarding_first_memory_skipped / onboarding_first_memory_step_viewed` |

**Research basis:** Templates reduce friction 40% (Intercom). If edit rate >40%, template needs improvement.

---

## Component Structure

```
FirstMemoryTemplate/
├── TemplateHeader.tsx       // "Step 4: Create Your First Memory"
├── MemoryForm.tsx           // Title, content, type, tags inputs
├── TemplateActions.tsx      // Edit, Create Memory buttons
├── SuccessAnimation.tsx     // Confetti/checkmark on success
└── index.tsx                // Main container, state management
```

---

## Acceptance Criteria (Implementation-Ready)

### AC1: Template Pre-fill
- [ ] Step 4 loads with pre-filled title, content, type, tags
- [ ] Template matches spec exactly (see Template Content section)
- [ ] "Create Memory" button enabled by default

### AC2: Edit Flow
- [ ] "Edit" button makes all fields editable
- [ ] "Cancel" button resets to original template
- [ ] Character count shown for content field (max 1000)

### AC3: Submission
- [ ] "Create Memory" calls `POST /api/memories`
- [ ] Loading spinner shown during submission
- [ ] Success animation plays on completion
- [ ] Auto-advance to Step 5 after 2 seconds

### AC4: Error Handling
- [ ] Network errors show toast notification
- [ ] Button re-enabled after error
- [ ] Error logged to analytics

### AC5: Analytics
- [ ] All 5 events tracked (viewed, edited, created, error, skipped)
- [ ] Time on step measured
- [ ] Template usage tracked

### AC6: Accessibility
- [ ] All fields have proper labels
- [ ] Error messages announced via aria-live
- [ ] Keyboard navigation works (Tab, Enter, Escape)
- [ ] Focus management on success (advance to Step 5)

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `amc-frontend/src/components/FirstMemoryTemplate/index.tsx` | CREATE | Main component |
| `amc-frontend/src/components/FirstMemoryTemplate/MemoryForm.tsx` | CREATE | Form fields |
| `amc-frontend/src/components/FirstMemoryTemplate/TemplateActions.tsx` | CREATE | Buttons |
| `amc-frontend/src/components/FirstMemoryTemplate/SuccessAnimation.tsx` | CREATE | Success state |
| `amc-frontend/src/components/OnboardingFlow.tsx` | MODIFY | Add Step 4 integration |

---

## Implementation Notes

1. **Reuse existing components:** Use existing `Input`, `Textarea`, `Button`, `Select` components from UI library
2. **State management:** Local state in component (no global store needed)
3. **API client:** Use existing `MemoryClient` from SDK
4. **Animations:** Use Framer Motion for success animation (already in project)
5. **Testing:** Add Cypress test for Step 4 flow

---

## Handoff Checklist

- [x] Interaction flow defined
- [x] Edge cases documented
- [x] API contract specified
- [x] Analytics events defined
- [x] Acceptance criteria implementation-ready
- [x] Component structure outlined
- [ ] **Next:** faintech-frontend implements, QA verifies

---

## References

- ONBOARDING-USER-EVIDENCE-SYNTHESIS.md (research basis)
- AMC-MVP-115-PROGRESS.md (slice completion tracking)
- Intercom: First-Run Experience Templates (2024)
- Stanford HCI: Success Animation Impact (2023)

---

**Created by:** faintech-product-designer
**Next owner:** faintech-frontend (implementation)
**Reviewer:** faintech-cpo (acceptance criteria approval)

_This spec closes the Step 4 design gap identified in user research synthesis._
