# User Feedback Widget - Design Specification

**Task:** OS-20260323004105-975C
**Designer:** faintech-product-designer
**Date:** 2026-03-23
**Status:** IN PROGRESS
**Target Implementation:** Post-beta Week 1 (Mar 25 - Apr 7)
**Implementation Owner:** faintech-frontend

---

## Executive Summary

Design a user feedback collection widget for the AMC dashboard that enables beta users to easily report bugs, request features, and provide general feedback. The widget should be non-intrusive, accessible from anywhere in the application, and capture enough context for the team to act on feedback quickly.

**Success Criteria:**
- Users can submit feedback in < 30 seconds
- Widget is visible on all dashboard pages
- Captures sufficient context for debugging (page, action, screenshot)
- Mobile-responsive for tablet/phone users
- Non-blocking - users can continue working while feedback is open

---

## 1. Widget Placement & Trigger

### 1.1 Placement
**Option A: Floating Action Button (FAB) - RECOMMENDED**
- Position: Bottom-right corner, fixed position
- Distance from edge: 24px from bottom, 24px from right
- Size: 56x56px circular button
- Color: Primary brand color with subtle shadow
- Icon: Feedback icon (speech bubble with lightning bolt)

**Rationale:**
- Doesn't compete with navigation
- Always accessible
- Familiar pattern (like chat support widgets)
- Doesn't obstruct content

**Option B: Sidebar Footer - Alternative**
- Position: Bottom of left sidebar
- Width: Full sidebar width
- Height: 48px button
- Text: "Share Feedback" with icon

**Decision:** FAB recommended for maximum visibility and accessibility

### 1.2 Trigger Behavior
- **Click:** Opens feedback modal/drawer
- **Hover (desktop):** Shows tooltip "Share Feedback"
- **Keyboard:** Accessible via keyboard shortcut (Cmd+K → F)
- **Mobile:** Tap to open

### 1.3 Visual State
- **Default:** Primary color, subtle shadow
- **Hover:** Slightly darker shade, stronger shadow
- **Active:** Depressed state when modal is open
- **New feedback:** Optional - badge count if feedback view exists

---

## 2. Feedback Modal/Drawer Design

### 2.1 Layout Choice
**Recommendation:** Slide-in drawer from right (not modal overlay)

**Rationale:**
- Doesn't block the entire screen
- User can still see the page they're giving feedback about
- Easier to reference context while writing feedback
- Mobile-friendly (full-width on mobile)

**Dimensions:**
- Desktop: 400px wide, full height
- Tablet: 50% width, full height
- Mobile: 100% width, full height (slides from bottom)

### 2.2 Header
```
┌─────────────────────────────────┐
│ Share Feedback           ✕     │
├─────────────────────────────────┤
│ Help us improve AMC!           │
│ Your feedback shapes the       │
│ product roadmap.               │
└─────────────────────────────────┘
```

**Elements:**
- Title: "Share Feedback"
- Close button (✕) - top right
- Subtitle: Brief encouraging message
- Height: 80px

### 2.3 Feedback Type Selector
```
┌─────────────────────────────────┐
│ What's this about?              │
│                                 │
│ [🐛 Bug Report] [✨ Feature]   │
│ [💬 General]                    │
└─────────────────────────────────┘
```

**Types:**
1. **Bug Report** (🐛) - Something broken
2. **Feature Request** (✨) - New functionality
3. **General Feedback** (💬) - Suggestions, praise, etc.

**Behavior:**
- Radio button or segmented control
- Default: No selection (user must choose)
- Selection persists for 24h in local storage

### 2.4 Feedback Form Fields

#### Required Fields

**1. Description (Textarea)**
- Label: "Describe your feedback"
- Placeholder: "Tell us what happened..."
- Min length: 10 characters
- Max length: 2000 characters
- Rows: 4 (auto-expand to max 8)
- Validation: Required, min length

**2. Severity (for bugs only)**
```
How severe is this bug?
[🟢 Minor] [🟡 Moderate] [🔴 Critical]
```

- Show only when "Bug Report" is selected
- Options: Minor, Moderate, Critical
- Default: None (user must select)
- Help text: "Critical = blocks my work, Minor = cosmetic issue"

#### Optional Fields

**3. Page/URL (Auto-captured)**
- Label: "Where did this happen?"
- Auto-fill: Current page URL
- Editable: Yes (user can change)
- Format: `/dashboard/memories` or full URL

**4. Screenshot (File upload)**
- Label: "Attach screenshot (optional)"
- Accept: `.png, .jpg, .jpeg`
- Max size: 5MB
- Drag & drop or click to upload
- Preview thumbnail after upload

**5. Email for follow-up (Optional)**
- Label: "Email for follow-up (optional)"
- Placeholder: "your@email.com"
- Validation: Valid email format
- Pre-fill: From user profile if available

### 2.5 Submit Button
```
┌─────────────────────────────────┐
│     [Send Feedback 🚀]          │
│                                 │
│ We'll review this within 24h   │
└─────────────────────────────────┘
```

**States:**
- **Default:** Primary color, enabled
- **Disabled:** Gray, when form invalid
- **Loading:** Spinner during submission
- **Success:** Green checkmark, "Sent!"

**Help text:** Response time expectation

---

## 3. Interaction Flow

### 3.1 Happy Path
```
1. User clicks FAB (bottom-right)
2. Drawer slides in from right
3. User selects feedback type
4. User fills description (10+ chars)
5. User optionally adds:
   - Severity (for bugs)
   - Screenshot
   - Email
6. User clicks "Send Feedback"
7. Button shows loading spinner
8. On success:
   - Show success message (2s)
   - Close drawer
   - Show toast: "Thanks! We'll review this within 24h"
```

### 3.2 Error Handling
```
- Network error: Show inline error, retry button
- Validation error: Highlight field, show message
- File too large: Show error, suggest compression
- Generic error: Show message, email fallback
```

### 3.3 Success State
```
┌─────────────────────────────────┐
│ ✅ Feedback Sent!               │
│                                 │
│ Thanks for helping us improve.  │
│ We'll review this within 24h.   │
│                                 │
│     [Submit Another] [Close]    │
└─────────────────────────────────┘
```

---

## 4. Mobile Responsiveness

### 4.1 Breakpoints
- **Desktop:** ≥1024px - 400px drawer
- **Tablet:** 768-1023px - 50% drawer
- **Mobile:** <768px - Full-width bottom sheet

### 4.2 Mobile-Specific Adjustments
- FAB size: 48x48px (smaller to avoid obstruction)
- Drawer slides from bottom (not right)
- Form fields: Full-width, larger touch targets
- File upload: Camera access for photo
- Keyboard: Auto-scroll to active field

### 4.3 Touch Gestures
- Swipe down to close drawer (mobile)
- Tap outside drawer to close (tablet/desktop)

---

## 5. Accessibility

### 5.1 Keyboard Navigation
- **Tab:** Navigate through form fields
- **Enter:** Submit form (from any field)
- **Escape:** Close drawer
- **Cmd+K → F:** Global shortcut to open feedback

### 5.2 Screen Reader
- All form fields have proper labels
- Error messages announced
- Success message announced
- ARIA labels for icons

### 5.3 Visual Accessibility
- Color contrast: WCAG AA compliant
- Focus indicators: Visible outlines
- Don't rely on color alone (icons + text)
- Font size: Minimum 14px

---

## 6. Data Model

### 6.1 Feedback Schema
```typescript
interface Feedback {
  id: string;
  type: 'bug' | 'feature' | 'general';
  severity?: 'minor' | 'moderate' | 'critical';
  description: string;
  page_url: string;
  screenshot_url?: string;
  user_email?: string;
  user_id?: string;
  created_at: Date;
  status: 'new' | 'reviewed' | 'resolved';
  metadata: {
    browser: string;
    os: string;
    screen_resolution: string;
    user_agent: string;
  };
}
```

### 6.2 Auto-Captured Metadata
- Browser name + version
- OS name + version
- Screen resolution
- Current URL
- User agent string
- Timestamp

---

## 7. Backend Integration

### 7.1 API Endpoint
```
POST /api/feedback
```

**Request Body:**
```json
{
  "type": "bug",
  "severity": "moderate",
  "description": "Memory list doesn't load after creating new memory",
  "page_url": "/dashboard/memories",
  "screenshot_url": "https://storage.screenshot.png",
  "user_email": "user@example.com"
}
```

**Response:**
```json
{
  "id": "fb_123456",
  "status": "received",
  "message": "Feedback submitted successfully"
}
```

### 7.2 File Upload
```
POST /api/feedback/upload
```

- Accepts multipart/form-data
- Returns: `{ "url": "https://storage.screenshot.png" }`
- Max size: 5MB
- Allowed types: image/png, image/jpeg

### 7.3 Feedback Management (Internal)
- **View:** `/admin/feedback` (internal dashboard)
- **Status updates:** New → Reviewed → Resolved
- **Notifications:** Slack/email to team on new feedback
- **Metrics:** Track volume, response time, resolution rate

---

## 8. Analytics & Tracking

### 8.1 Events to Track
1. `feedback_widget_opened` - When user opens drawer
2. `feedback_type_selected` - Which type user chose
3. `feedback_submitted` - Successful submission
4. `feedback_error` - Validation or network errors
5. `screenshot_uploaded` - When user uploads image

### 8.2 Success Metrics
- Submission rate: % of users who submit feedback
- Completion rate: % of opened widgets that result in submission
- Time to submit: Average time from open to submit
- Response time: Team's average time to review feedback

---

## 9. Implementation Notes

### 9.1 Component Structure
```
src/components/FeedbackWidget/
├── FeedbackFAB.tsx          # Floating action button
├── FeedbackDrawer.tsx       # Main drawer component
├── FeedbackForm.tsx         # Form with validation
├── FeedbackTypeSelector.tsx # Type selection
├── ScreenshotUpload.tsx     # File upload component
└── FeedbackSuccess.tsx      # Success state
```

### 9.2 State Management
- Use local component state for form data
- Store feedback type preference in localStorage (24h expiry)
- Track submission status (idle/loading/success/error)

### 9.3 Styling
- Use existing Tailwind classes from design system
- Match existing form components (Input, Textarea, Button)
- Ensure consistent spacing and typography

### 9.4 Dependencies
- `react-hook-form` - Form validation
- `react-dropzone` - File upload
- `@headlessui/react` - Drawer/transition (if available)
- `sonner` or `react-toastify` - Toast notifications

### 9.5 Edge Cases
- **Offline:** Queue feedback, submit when online
- **Large screenshots:** Auto-compress before upload
- **Multiple submissions:** Rate limit to 5/hour per user
- **Spam:** Add honeypot field (hidden from users)

---

## 10. Testing Checklist

### 10.1 Functional Testing
- [ ] Widget opens on click
- [ ] All form fields validate correctly
- [ ] Screenshot upload works (drag + click)
- [ ] Form submits successfully
- [ ] Success message displays
- [ ] Error handling works (network, validation)
- [ ] Keyboard navigation works
- [ ] Mobile layout renders correctly

### 10.2 Accessibility Testing
- [ ] Screen reader announces all fields
- [ ] Keyboard-only navigation works
- [ ] Color contrast passes WCAG AA
- [ ] Focus indicators visible

### 10.3 Mobile Testing
- [ ] FAB doesn't obstruct content
- [ ] Drawer slides from bottom on mobile
- [ ] Form fields are large enough for touch
- [ ] Camera upload works on mobile
- [ ] Swipe-to-close gesture works

---

## 11. Timeline

**Design Complete:** Mar 23, 2026 ✅
**Implementation Start:** Mar 25, 2026 (post-beta launch)
**Implementation Complete:** Mar 28, 2026
**Testing & QA:** Mar 29-30, 2026
**Deploy to Production:** Mar 31, 2026

---

## 12. Success Criteria

**User Experience:**
- ✅ Users can submit feedback in < 30 seconds
- ✅ Widget is visible and accessible from all pages
- ✅ Mobile-responsive design
- ✅ Non-blocking - users can continue working

**Technical:**
- ✅ Captures sufficient context (URL, screenshot, metadata)
- ✅ Validates form inputs
- ✅ Handles errors gracefully
- ✅ Accessible via keyboard and screen reader

**Business:**
- ✅ Provides clear feedback channel for beta users
- ✅ Enables rapid iteration based on user feedback
- ✅ Tracks feedback volume and trends
- ✅ Supports team triage and response workflow

---

## 13. Future Enhancements (Post-Week 1)

1. **Feedback Status Tracking**
   - Users can view their submitted feedback
   - Status updates (reviewed, in progress, resolved)

2. **In-App Responses**
   - Team can respond to feedback
   - Users see responses in-app

3. **Smart Routing**
   - Auto-categorize feedback by topic
   - Route to appropriate team member

4. **Feedback Analytics Dashboard**
   - Track trends over time
   - Identify common issues
   - Measure user satisfaction

5. **NPS Integration**
   - Add NPS score collection
   - Correlate feedback with satisfaction

---

## 14. References

- **Similar Patterns:**
  - GitHub Feedback (floating button)
  - Notion Feedback (sidebar)
  - Linear Feedback (cmd+k menu)

- **Design Principles:**
  - Don't Make Me Think (Steve Krug)
  - Non-intrusive feedback collection
  - Progressive disclosure

- **Internal Docs:**
  - Information Architecture: `/docs/design/LAB-001-UX-002-INFORMATION-ARCHITECTURE.md`
  - User Journey Map: `/docs/design/LAB-001-UX-001-USER-JOURNEY-MAP.md`

---

**Document Status:** COMPLETE
**Review Required:** faintech-frontend (implementation), cpo (product review)
**Implementation Timeline:** Post-beta Week 1 (Mar 25 - Apr 7)

---

**Created:** 2026-03-23 02:41 EET
**Designer:** faintech-product-designer
**Task:** OS-20260323004105-975C
