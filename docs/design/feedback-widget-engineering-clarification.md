# Feedback Widget - Engineering Clarification

**Source Spec:** `user-feedback-widget-spec.md` (14KB)
**Created:** 2026-03-28 10:15 EET
**Designer:** faintech-product-designer
**Target:** faintech-frontend

---

## Purpose

This document clarifies implementation details for the Feedback Widget to ensure engineering can execute without ambiguity. References the comprehensive spec at `user-feedback-widget-spec.md`.

---

## 1. Layout Decision: Drawer (FINAL)

**Decision:** Use slide-in drawer from right

**Implementation:**
- Desktop (≥1024px): 400px wide, slides from right
- Tablet (768-1023px): 50% width, slides from right
- Mobile (<768px): 100% width, slides from **bottom** (not right)

**Animation:**
- Duration: 300ms
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` (ease-out)
- Overlay: Semi-transparent black (rgba(0,0,0,0.5)), fade in 200ms

---

## 2. Form Validation UX

**Validation Timing:**
- **On Blur:** Show validation errors when user leaves a field
- **On Submit:** Validate all fields, scroll to first error
- **Real-time:** Min character count (10) updates as user types

**Error Display:**
- Inline below field (red text, 12px)
- Red border on invalid field
- No error icons (keep it minimal)

**Success Indicator:**
- Green checkmark in submit button
- Button text changes to "Sent! ✓"

---

## 3. Screenshot Upload Implementation

**Preview Dimensions:**
- Thumbnail: 80x60px (4:3 aspect ratio)
- Max preview width: 100% of container
- Border radius: 8px

**Compression (Client-side):**
- Max file size before upload: 5MB
- If > 1MB: Compress to 80% quality using Canvas API
- Format: Keep original format (PNG/JPEG)
- Show progress bar during compression

**Upload Flow:**
1. User selects file
2. Show loading spinner
3. Compress if needed
4. Upload to `/api/feedback/upload`
5. Show preview thumbnail
6. Store URL in form state

---

## 4. Success/Error Toast Behavior

**Success Toast:**
- Message: "Thanks! We'll review this within 24h"
- Duration: 4000ms (4 seconds)
- Position: Bottom-right (matches FAB position)
- Style: Green background, white text, checkmark icon

**Error Toast:**
- Message: "Failed to send feedback. Please try again."
- Duration: 6000ms (6 seconds) - longer for actionable errors
- Position: Bottom-right
- Style: Red background, white text, error icon
- Action: "Retry" button (resubmits form)

**Network Error:**
- Show inline error above submit button
- Add "Retry" button
- Don't close drawer on network error

---

## 5. Mobile Drawer Gestures

**Swipe to Close:**
- Direction: Swipe down
- Threshold: 100px or 30% of drawer height
- Velocity: > 0.5 (fast swipe closes immediately)
- Animation: Follow finger during drag, snap to close/open

**Tap Outside:**
- Desktop/Tablet: Tap overlay to close
- Mobile: Disabled (easy to accidentally close)

**Back Button (Android):**
- Close drawer (don't navigate back)

---

## 6. Auto-Captured Metadata

**Implementation:**
```typescript
const metadata = {
  browser: getBrowser(),      // "Chrome 122.0"
  os: getOS(),                // "macOS 14.3"
  screen_resolution: `${window.screen.width}x${window.screen.height}`,
  user_agent: navigator.userAgent,
  viewport: `${window.innerWidth}x${window.innerHeight}`,
  url: window.location.pathname,
  timestamp: new Date().toISOString()
};
```

**Helper Functions:**
- Use `bowser` package for browser/OS detection
- Or implement simple regex from UA string

---

## 7. Offline Queuing (Edge Case)

**Implementation:**
- Check `navigator.onLine` before submit
- If offline: Show toast "You're offline. Feedback will be sent when connected."
- Store feedback in `localStorage` with key `pending_feedback`
- Listen for `online` event, retry submission
- Clear from localStorage on success

**Max Queue Size:** 5 items (prevent storage bloat)

---

## 8. Rate Limiting (Client-side)

**Limit:** 5 submissions per hour per user

**Implementation:**
- Store timestamps in `localStorage` with key `feedback_submissions`
- Before submit: Check if 5 submissions in last hour
- If exceeded: Show error "You've sent a lot of feedback recently. Please wait before sending more."

---

## 9. Keyboard Shortcuts

**Global Shortcut:** `Cmd+K` → `F` (Mac) / `Ctrl+K` → `F` (Windows)

**Implementation:**
- Listen for `Cmd+K` (opens command palette if exists)
- If no command palette, directly open feedback drawer
- Inside drawer: `Escape` to close, `Tab` to navigate, `Enter` to submit

---

## 10. Component Structure (Recommended)

```
src/components/FeedbackWidget/
├── index.ts                    # Export FeedbackWidget
├── FeedbackFAB.tsx             # Floating action button
├── FeedbackDrawer.tsx          # Drawer wrapper + animations
├── FeedbackForm.tsx            # Form with react-hook-form
├── FeedbackTypeSelector.tsx    # Type radio/segmented control
├── ScreenshotUpload.tsx        # File upload + preview
├── FeedbackSuccess.tsx         # Success state
├── useFeedbackSubmission.ts    # Hook for API calls + offline queue
└── types.ts                    # TypeScript interfaces
```

---

## 11. API Integration

**Submit Feedback:**
```typescript
POST /api/feedback
{
  type: 'bug' | 'feature' | 'general',
  severity?: 'minor' | 'moderate' | 'critical',
  description: string,
  page_url: string,
  screenshot_url?: string,
  user_email?: string,
  metadata: {
    browser: string,
    os: string,
    screen_resolution: string,
    user_agent: string,
    viewport: string,
    url: string,
    timestamp: string
  }
}
```

**Response:**
```typescript
{
  id: string,
  status: 'received',
  message: string
}
```

---

## 12. Analytics Events

**Track these events:**
1. `feedback_widget_opened` - Drawer opened
2. `feedback_type_selected` - Type chosen (include type in event)
3. `feedback_submitted` - Successful submission (include type)
4. `feedback_error` - Validation or network error (include error type)
5. `screenshot_uploaded` - Screenshot attached

---

## 13. Testing Checklist (Quick)

**Critical Tests:**
- [ ] Drawer opens/closes with animation
- [ ] Form validates on blur
- [ ] Screenshot upload + preview works
- [ ] Success toast appears
- [ ] Network error shows retry button
- [ ] Mobile: Slides from bottom
- [ ] Mobile: Swipe down to close
- [ ] Keyboard: Escape closes drawer
- [ ] Offline: Queues feedback locally

---

## 14. Dependencies

**Required:**
- `react-hook-form` - Form validation
- `react-dropzone` - File upload
- `sonner` or `react-toastify` - Toast notifications (if not already installed)

**Optional:**
- `bowser` - Browser detection (can use simple UA parsing instead)
- `framer-motion` - Animations (if already in project)

---

## Summary

This clarification addresses:
1. ✅ Drawer vs Modal decision (Drawer)
2. ✅ Animation timing (300ms ease-out)
3. ✅ Form validation UX (on-blur + on-submit)
4. ✅ Screenshot compression (client-side, 80% quality if > 1MB)
5. ✅ Toast behavior (4s success, 6s error, bottom-right)
6. ✅ Mobile gestures (swipe down to close, 100px threshold)
7. ✅ Auto-captured metadata (browser, OS, resolution, URL)
8. ✅ Offline queuing (localStorage, retry on online)
9. ✅ Rate limiting (5/hour client-side)
10. ✅ Component structure (8 files recommended)

**Status:** READY FOR IMPLEMENTATION

---

**Created:** 2026-03-28 10:15 EET
**Designer:** faintech-product-designer
**Target:** faintech-frontend
