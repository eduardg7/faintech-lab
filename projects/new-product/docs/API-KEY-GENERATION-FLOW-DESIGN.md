# API Key Generation Flow — Design Specification

**Created:** 2026-03-17  
**Owner:** faintech-product-designer  
**Status:** Implementation-ready  
**Priority:** P0 (blocks beta launch)

---

## Problem Statement

Current onboarding flow requires users to **paste** an API key, but there's no UI for **generating** one. This blocks the user journey at Step 3 (API key) and prevents beta users from completing onboarding.

**Evidence:** 
- `OnboardingFlow.tsx` asks: "Paste active API key"
- No `/api-keys` route exists in `amc-frontend/src/app/`
- Backend has `POST /v1/api-keys` endpoint (per MVP-FEATURE-PRIORITIZATION.md)

---

## User Flow

```
Onboarding Step 3: API Key
├─ Option A: Generate new key (recommended for new users)
│  ├─ Click "Generate API key"
│  ├─ Backend creates key via POST /v1/api-keys
│  ├─ Show key ONCE with copy button
│  ├─ Store key locally (localStorage + AuthContext)
│  └─ Continue to Step 4
│
└─ Option B: Paste existing key (for returning users)
   ├─ Paste into input field
   ├─ Validate format (amc_live_*)
   └─ Continue to Step 4
```

---

## Screen Hierarchy

### 1. API Key Generation Modal (new)

**Location:** Overlay on `OnboardingFlow.tsx` Step 3  
**Trigger:** Click "Generate API key" button

**Components:**
```
<APIKeyGenerationModal>
  <ModalHeader>
    "Generate API key"
  </ModalHeader>
  
  <ModalBody>
    <Form>
      <Label>Key name</Label>
      <Input placeholder="e.g., 'Production' or 'Testing'" />
      
      <Label>Environment</Label>
      <Select options={["Production", "Development"]} />
      
      <Button variant="primary">Generate key</Button>
    </Form>
  </ModalBody>
</APIKeyGenerationModal>
```

### 2. Key Display Screen (one-time view)

**Location:** Replace modal content after generation  
**Behavior:** Key shown ONCE, never again

**Components:**
```
<APIKeyDisplayScreen>
  <Alert variant="warning">
    "Copy this key now. It won't be shown again."
  </Alert>
  
  <APIKeyValue>
    <MonospaceText>{generated_key}</MonospaceText>
    <CopyButton />
  </APIKeyValue>
  
  <Checkbox>
    "I've saved this key securely"
  </Checkbox>
  
  <Button variant="primary" disabled={!checkbox_checked}>
    Continue to workspace
  </Button>
</APIKeyDisplayScreen>
```

### 3. Success State (existing)

**Location:** Current `OnboardingFlow.tsx` Step 5  
**Change:** Auto-populate `apiKey` state instead of requiring manual paste

---

## Interaction Patterns

### Pattern 1: Key Generation (new users)

1. User reaches Step 3 (API key)
2. **Primary CTA:** "Generate API key" button (prominent, styled as primary)
3. **Secondary CTA:** "Paste existing key" link (subtle, below input field)
4. User clicks "Generate API key"
5. Modal opens with form (key name + environment)
6. User fills form, clicks "Generate"
7. Backend returns: `{ key: "amc_live_xxx", name: "Production", environment: "production", created_at: "..." }`
8. **Critical UX:** Key displayed ONCE with large copy button
9. User must check "I've saved this key" before continuing
10. Key auto-populates onboarding flow
11. User continues to Step 4 (first memory)

### Pattern 2: Key Paste (returning users)

1. User reaches Step 3 (API key)
2. User sees input field (current implementation)
3. User pastes existing key
4. Validation: format must start with `amc_live_`
5. On valid input, "Continue" button enables
6. User continues to Step 4 (first memory)

---

## State Management

### New State Variables (in `OnboardingFlow.tsx`)

```typescript
const [showKeyGenerationModal, setShowKeyGenerationModal] = useState(false);
const [generatedKey, setGeneratedKey] = useState<string | null>(null);
const [keyName, setKeyName] = useState('Default');
const [keyEnvironment, setKeyEnvironment] = useState<'production' | 'development'>('production');
const [keyConfirmed, setKeyConfirmed] = useState(false);
```

### Backend Contract

**Endpoint:** `POST /v1/api-keys`

**Request:**
```json
{
  "name": "Production",
  "environment": "production"
}
```

**Response:**
```json
{
  "id": "key_abc123",
  "key": "amc_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "name": "Production",
  "environment": "production",
  "created_at": "2026-03-17T01:30:00Z",
  "key_preview": "amc_live_...xxxx"
}
```

**Critical:** Backend must return the **full key** in this response. Future GET requests should only return `key_preview`.

---

## Empty States

### Empty State 1: No API keys exist

**Location:** Dashboard `/api-keys` route (future)  
**Message:** "No API keys yet. Generate your first key to start writing memories."  
**CTA:** "Generate API key"

### Empty State 2: Key generation failed

**Location:** API key generation modal  
**Message:** "Failed to generate key. Please try again or contact support."  
**CTA:** "Retry" + "Contact support" link

---

## Error States

### Error 1: Invalid key format (paste flow)

**Trigger:** User pastes key that doesn't start with `amc_live_`  
**Message:** "Invalid API key format. Key should start with 'amc_live_'."  
**Recovery:** Clear input, show inline error, re-enable submit on valid input

### Error 2: Backend unavailable

**Trigger:** POST /v1/api-keys returns 500 or times out  
**Message:** "Unable to generate key right now. Please try again in a moment."  
**Recovery:** Retry button, contact support link

### Error 3: Key already exists

**Trigger:** User tries to generate duplicate key name  
**Message:** "A key with this name already exists. Choose a different name."  
**Recovery:** Focus on name input, clear value

---

## Accessibility Requirements

- **Keyboard navigation:** Tab through form fields, Enter to submit
- **Screen readers:** ARIA labels for all buttons and inputs
- **Focus management:** Auto-focus on key name input when modal opens
- **Color contrast:** WCAG AA compliance for all text
- **Copy button:** Announce "Copied to clipboard" via aria-live

---

## Analytics Events

Track these events to measure onboarding success:

1. `onboarding_api_key_step_viewed` - User reaches Step 3
2. `onboarding_generate_key_clicked` - User clicks "Generate API key"
3. `onboarding_key_generated` - Backend successfully creates key
4. `onboarding_key_copied` - User clicks copy button
5. `onboarding_key_confirmed` - User checks "I've saved this key"
6. `onboarding_paste_key_used` - User uses paste flow instead
7. `onboarding_key_error` - Any error during key generation

---

## Implementation Notes for Engineering

### File Changes Required

1. **Create new component:** `amc-frontend/src/components/APIKeyGenerationModal.tsx`
2. **Update:** `amc-frontend/src/components/OnboardingFlow.tsx`
   - Add "Generate API key" button
   - Add modal state management
   - Handle generated key flow
3. **Create new route (future):** `amc-frontend/src/app/api-keys/page.tsx`
4. **Backend:** Ensure `POST /v1/api-keys` returns full key on creation

### Acceptance Criteria

- [ ] User can generate new API key via modal form
- [ ] Generated key is shown ONCE with copy button
- [ ] User must confirm key is saved before continuing
- [ ] Key auto-populates onboarding flow after generation
- [ ] Paste flow still works for returning users
- [ ] Error states handled gracefully
- [ ] All analytics events firing

### Testing Checklist

- [ ] New user: Generate key → Copy → Confirm → Continue
- [ ] Returning user: Paste existing key → Continue
- [ ] Invalid paste: Show error, clear input
- [ ] Backend down: Show error, retry option
- [ ] Duplicate key name: Show error, focus input
- [ ] Keyboard navigation works
- [ ] Screen reader announces all states

---

## Design Rationale

**Why modal?** Keeps user in onboarding flow context, doesn't break mental model.

**Why show key once?** Security best practice (follows Stripe, GitHub, OpenAI patterns).

**Why require confirmation?** Prevents users from losing keys by accidentally closing the window.

**Why two options (generate vs paste)?** Supports both new and returning users without creating separate flows.

---

## Timeline

**Design:** Complete (this document)  
**Engineering:** 1 day estimate  
**Testing:** 0.5 day  
**Target completion:** 2026-03-18 (before beta launch)

---

**Next Owner:** faintech-frontend (implementation)  
**Reviewer:** faintech-product-designer (UX review after implementation)  
**Blockers:** None (backend endpoint exists)

---

_Created by faintech-product-designer on 2026-03-17_
_This design is implementation-ready. Engineering can proceed without further design input._
