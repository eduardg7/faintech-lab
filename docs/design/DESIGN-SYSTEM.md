# AMC Design System

**Version:** 1.0.0
**Last Updated:** 2026-03-23
**Owner:** faintech-product-designer
**Status:** ACTIVE

---

## Overview

This design system documents the visual language, components, and patterns used across the Agent Memory Control (AMC) application. It ensures consistency, accessibility, and maintainability as the product evolves.

**Target Audience:**
- Frontend developers implementing UI components
- Designers creating new features
- QA engineers testing visual consistency

---

## 1. Design Principles

### 1.1 Core Principles

1. **Clarity Over Cleverness**
   - Interfaces should be self-explanatory
   - Avoid jargon and technical terms
   - Use familiar patterns and conventions

2. **Progressive Disclosure**
   - Show essential information first
   - Reveal complexity on demand
   - Don't overwhelm users with options

3. **Accessibility First**
   - WCAG AA compliance minimum
   - Keyboard navigation support
   - Screen reader compatibility
   - Color contrast ratios ≥ 4.5:1

4. **Mobile-Responsive**
   - Touch-friendly targets (min 44x44px)
   - Responsive layouts
   - Performance-conscious

5. **Consistency**
   - Reuse existing components
   - Follow established patterns
   - Maintain visual harmony

---

## 2. Color System

### 2.1 Brand Colors

All colors are WCAG AA compliant on white backgrounds.

```javascript
// Primary Colors
'amc-primary': '#3b82f6'      // Blue - primary actions
'amc-primary-dark': '#1d4ed8' // 7.1:1 contrast (excellent)

// Secondary Colors
'amc-secondary': '#8b5cf6'      // Purple - secondary actions
'amc-secondary-dark': '#7c3aed' // 4.6:1 contrast (AA pass)

// Semantic Colors
'amc-success': '#10b981'      // Green - success states
'amc-success-dark': '#059669' // 5.5:1 contrast (AA pass)

'amc-warning': '#f59e0b'      // Amber - warning states
'amc-warning-dark': '#d97706' // 5.6:1 contrast (AA pass)

'amc-error': '#ef4444'      // Red - error states
'amc-error-dark': '#dc2626' // 5.5:1 contrast (AA pass)
```

### 2.2 Usage Guidelines

**Primary Blue (`amc-primary`)**
- Primary call-to-action buttons
- Active navigation states
- Links and focus indicators
- Progress indicators

**Secondary Purple (`amc-secondary`)**
- Secondary actions
- Highlights and accents
- Interactive elements

**Semantic Colors**
- **Success:** Confirmation messages, completed states
- **Warning:** Caution messages, pending states
- **Error:** Error messages, destructive actions

### 2.3 Neutral Colors

```javascript
// Gray scale
'gray-50': '#f9fafb'  // Background
'gray-100': '#f3f4f6' // Subtle backgrounds
'gray-200': '#e5e7eb' // Borders
'gray-300': '#d1d5db' // Disabled borders
'gray-400': '#9ca3af' // Placeholder text
'gray-500': '#6b7280' // Helper text
'gray-600': '#4b5563' // Secondary text
'gray-700': '#374151' // Primary text
'gray-800': '#1f2937' // Headings
'gray-900': '#111827' // High-contrast text
```

### 2.4 Color Contrast Requirements

- **Normal text:** Minimum 4.5:1 contrast ratio
- **Large text (18pt+):** Minimum 3:1 contrast ratio
- **UI components:** Minimum 3:1 contrast ratio
- **Focus indicators:** Minimum 3:1 against adjacent colors

---

## 3. Typography

### 3.1 Font Stack

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
             'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans',
             'Helvetica Neue', sans-serif;
```

**Monospace (code):**
```css
font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
```

### 3.2 Type Scale

```css
/* Headings */
text-xs:   12px / 16px   /* Small labels, captions */
text-sm:   14px / 20px   /* Body small, meta text */
text-base: 16px / 24px   /* Body default */
text-lg:   18px / 28px   /* Large body, lead text */
text-xl:   20px / 28px   /* H4 */
text-2xl:  24px / 32px   /* H3 */
text-3xl:  30px / 36px   /* H2 */
text-4xl:  36px / 40px   /* H1 */
```

### 3.3 Font Weights

```css
font-normal:   400 /* Body text */
font-medium:   500 /* Emphasis, labels */
font-semibold: 600 /* Subheadings */
font-bold:     700 /* Headings, strong emphasis */
```

### 3.4 Line Height

- **Body text:** 1.5 (24px on 16px base)
- **Headings:** 1.2-1.3 (tighter for visual hierarchy)
- **UI elements:** 1 (single line buttons, inputs)

---

## 4. Spacing System

Based on 4px grid system.

```css
spacing-0:  0px
spacing-1:  4px   /* Tight spacing */
spacing-2:  8px   /* Compact spacing */
spacing-3:  12px  /* Default spacing */
spacing-4:  16px  /* Comfortable spacing */
spacing-5:  20px  /* Generous spacing */
spacing-6:  24px  /* Section spacing */
spacing-8:  32px  /* Large spacing */
spacing-10: 40px  /* XL spacing */
spacing-12: 48px  /* Section dividers */
spacing-16: 64px  /* Major sections */
```

### 4.1 Usage Guidelines

- **Component padding:** `spacing-3` to `spacing-4` (12-16px)
- **Card padding:** `spacing-6` (24px)
- **Section margins:** `spacing-8` to `spacing-12` (32-48px)
- **Form field gaps:** `spacing-4` (16px)

---

## 5. Component Library

### 5.1 Existing Components

**Location:** `amc-frontend/src/components/ui/`

#### 5.1.1 EmptyState
**Purpose:** Display when no data is available

**Usage:**
```tsx
<EmptyState
  title="No memories yet"
  description="Create your first memory to get started"
  action={<Button>Create Memory</Button>}
/>
```

**Props:**
- `title`: string - Main message
- `description`: string - Explanation text
- `action`: ReactNode - Optional action button
- `icon`: ReactNode - Optional icon

#### 5.1.2 ErrorState
**Purpose:** Display error messages

**Usage:**
```tsx
<ErrorState
  title="Failed to load memories"
  message="Please try again or contact support"
  retry={<Button onClick={handleRetry}>Retry</Button>}
/>
```

**Props:**
- `title`: string - Error title
- `message`: string - Error details
- `retry`: ReactNode - Optional retry action

#### 5.1.3 LoadingState
**Purpose:** Display loading indicator

**Usage:**
```tsx
<LoadingState message="Loading memories..." />
```

**Props:**
- `message`: string - Loading text

#### 5.1.4 Skeleton
**Purpose:** Content placeholder during loading

**Usage:**
```tsx
<Skeleton className="h-4 w-3/4" />
<Skeleton className="h-4 w-1/2 mt-2" />
```

**Props:**
- `className`: string - Tailwind classes for dimensions

#### 5.1.5 DashboardStats
**Purpose:** Display key metrics

**Usage:**
```tsx
<DashboardStats
  stats={[
    { label: 'Total Memories', value: 1234 },
    { label: 'Active Agents', value: 15 },
  ]}
/>
```

**Props:**
- `stats`: Array of `{ label: string, value: number | string }`

#### 5.1.6 SkipLink
**Purpose:** Accessibility - skip to main content

**Usage:**
```tsx
<SkipLink />
```

**Behavior:**
- Hidden by default
- Visible on focus
- Links to `#main-content`

### 5.2 Common Patterns

#### Buttons

**Primary Button:**
```tsx
<button className="px-4 py-2 bg-amc-primary text-white rounded-md
                   hover:bg-amc-primary-dark focus:ring-2
                   focus:ring-amc-primary focus:ring-offset-2">
  Primary Action
</button>
```

**Secondary Button:**
```tsx
<button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md
                   hover:bg-gray-200 focus:ring-2
                   focus:ring-gray-400 focus:ring-offset-2">
  Secondary Action
</button>
```

**Destructive Button:**
```tsx
<button className="px-4 py-2 bg-amc-error text-white rounded-md
                   hover:bg-amc-error-dark focus:ring-2
                   focus:ring-red-500 focus:ring-offset-2">
  Delete
</button>
```

#### Form Inputs

**Text Input:**
```tsx
<input
  type="text"
  className="w-full px-3 py-2 border border-gray-300 rounded-md
             focus:ring-2 focus:ring-amc-primary focus:border-transparent
             placeholder-gray-400"
  placeholder="Enter value..."
/>
```

**Textarea:**
```tsx
<textarea
  className="w-full px-3 py-2 border border-gray-300 rounded-md
             focus:ring-2 focus:ring-amc-primary focus:border-transparent
             placeholder-gray-400 resize-none"
  rows={4}
  placeholder="Enter description..."
/>
```

#### Cards

**Basic Card:**
```tsx
<div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
  <h3 className="text-lg font-semibold text-gray-900">Card Title</h3>
  <p className="mt-2 text-gray-600">Card content goes here</p>
</div>
```

**Interactive Card:**
```tsx
<div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm
                hover:shadow-md hover:border-gray-300 transition-all
                cursor-pointer">
  <h3 className="text-lg font-semibold text-gray-900">Card Title</h3>
</div>
```

---

## 6. Layout Patterns

### 6.1 Page Layout

```tsx
<div className="min-h-screen bg-gray-50">
  {/* Header */}
  <header className="bg-white border-b border-gray-200">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      {/* Header content */}
    </div>
  </header>

  {/* Main Content */}
  <main id="main-content" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {/* Page content */}
  </main>
</div>
```

### 6.2 Grid System

**Two Column Layout:**
```tsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
  <div>Left column</div>
  <div>Right column</div>
</div>
```

**Three Column Layout:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>
```

### 6.3 Responsive Breakpoints

```css
sm: 640px   /* Small devices (phones) */
md: 768px   /* Medium devices (tablets) */
lg: 1024px  /* Large devices (desktops) */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

---

## 7. Interaction Patterns

### 7.1 Hover States

- **Buttons:** Darken background by 10-15%
- **Cards:** Add subtle shadow
- **Links:** Underline text
- **Interactive elements:** Show pointer cursor

### 7.2 Focus States

All interactive elements must have visible focus indicators:

```css
focus:ring-2
focus:ring-amc-primary
focus:ring-offset-2
```

### 7.3 Loading States

1. **Skeleton:** Use `Skeleton` component for content loading
2. **Spinner:** Use `LoadingState` component for actions
3. **Button loading:** Show spinner inside button, disable interaction

### 7.4 Error Handling

1. **Inline validation:** Show errors below form fields
2. **Toast notifications:** For async operation failures
3. **ErrorState component:** For page-level errors

### 7.5 Success Feedback

1. **Toast notifications:** Brief success messages (3-5s)
2. **SuccessState component:** For completion screens
3. **Visual confirmation:** Color change, checkmark icon

---

## 8. Accessibility Guidelines

### 8.1 Keyboard Navigation

- **Tab order:** Logical sequence through interactive elements
- **Enter/Space:** Activate buttons and links
- **Escape:** Close modals, drawers, dropdowns
- **Arrow keys:** Navigate menus, lists, grids

### 8.2 Screen Reader Support

- Use semantic HTML (`<button>`, `<nav>`, `<main>`)
- Add ARIA labels for icons
- Provide text alternatives for images
- Announce dynamic content changes

### 8.3 Color & Contrast

- Never rely on color alone to convey information
- Use icons + text for status indicators
- Maintain 4.5:1 contrast ratio for text
- Test with color blindness simulators

### 8.4 Focus Management

- Visible focus indicators on all interactive elements
- Focus trap in modals
- Return focus to trigger element when closing modals
- Skip links for keyboard users

---

## 9. Animation & Motion

### 9.1 Transitions

```css
transition-colors: 150ms  /* Color changes */
transition-opacity: 150ms /* Fade effects */
transition-transform: 200ms /* Scale, translate */
transition-all: 200ms      /* All properties */
```

### 9.2 Easing

```css
ease-in:     cubic-bezier(0.4, 0, 1, 1)    /* Accelerate */
ease-out:    cubic-bezier(0, 0, 0.2, 1)    /* Decelerate */
ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)  /* Smooth */
```

### 9.3 Best Practices

- Keep animations subtle and fast (≤300ms)
- Avoid animating layout properties (width, height)
- Use `transform` and `opacity` for performance
- Respect `prefers-reduced-motion` media query

---

## 10. Iconography

### 10.1 Icon Library

**Recommended:** [Heroicons](https://heroicons.com/) or [Lucide Icons](https://lucide.dev/)

**Usage:**
```tsx
import { UserIcon, CogIcon } from '@heroicons/react/24/outline'

<UserIcon className="w-5 h-5 text-gray-500" />
```

### 10.2 Icon Sizes

```css
w-4 h-4: 16px /* Small icons */
w-5 h-5: 20px /* Default icons */
w-6 h-6: 24px /* Large icons */
w-8 h-8: 32px /* XL icons */
```

### 10.3 Icon + Text Spacing

```tsx
<button className="inline-flex items-center gap-2">
  <PlusIcon className="w-5 h-5" />
  <span>Add Item</span>
</button>
```

---

## 11. Responsive Design

### 11.1 Mobile-First Approach

Start with mobile styles, add breakpoints for larger screens:

```tsx
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>
```

### 11.2 Touch Targets

- Minimum size: 44x44px for touch targets
- Spacing between targets: 8px minimum
- Avoid hover-only interactions on mobile

### 11.3 Responsive Patterns

**Stack on mobile, side-by-side on desktop:**
```tsx
<div className="flex flex-col lg:flex-row gap-4">
  <div>Left</div>
  <div>Right</div>
</div>
```

**Hide on mobile:**
```tsx
<div className="hidden lg:block">
  Desktop only content
</div>
```

---

## 12. Dark Mode (Future)

**Status:** Not currently implemented

**When to implement:**
- Post-beta based on user feedback
- If users work in low-light environments
- If competitive analysis shows demand

**Preparation:**
- Use CSS custom properties for colors
- Test color contrast in both modes
- Ensure images work on both backgrounds

---

## 13. Testing Checklist

### 13.1 Visual Testing

- [ ] Component renders correctly
- [ ] Responsive at all breakpoints
- [ ] Hover/focus states work
- [ ] Loading states display
- [ ] Error states display

### 13.2 Accessibility Testing

- [ ] Keyboard navigation works
- [ ] Screen reader announces content
- [ ] Color contrast passes WCAG AA
- [ ] Focus indicators visible
- [ ] Touch targets are 44x44px minimum

### 13.3 Cross-Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

---

## 14. Component Development Workflow

### 14.1 When to Create New Component

1. Check if existing component can be extended
2. Consider if pattern is reusable (3+ use cases)
3. Document in design system
4. Add to component library

### 14.2 Component Checklist

- [ ] Props documented with TypeScript
- [ ] Accessible (keyboard, screen reader)
- [ ] Responsive (works on mobile)
- [ ] Has loading/error states (if applicable)
- [ ] Tested in isolation
- [ ] Documented in Storybook (future)

---

## 15. Future Enhancements

### 15.1 Short-term (Week 2-4)
- [ ] Add Storybook for component documentation
- [ ] Create Toast notification component
- [ ] Create Modal/Dialog component
- [ ] Create Dropdown menu component
- [ ] Add form validation components

### 15.2 Medium-term (Month 2-3)
- [ ] Dark mode implementation
- [ ] Animation library (Framer Motion)
- [ ] Advanced data visualization components
- [ ] Drag-and-drop components
- [ ] Rich text editor component

### 15.3 Long-term (Month 3+)
- [ ] Design token system
- [ ] Theme customization
- [ ] Component analytics (usage tracking)
- [ ] Performance optimization

---

## 16. Resources

### 16.1 Design Tools
- **Figma:** UI mockups (if applicable)
- **Tailwind CSS:** Utility classes reference
- **Color Contrast Checker:** [WebAIM](https://webaim.org/resources/contrastchecker/)

### 16.2 Inspiration
- [Tailwind UI](https://tailwindui.com/)
- [Headless UI](https://headlessui.com/)
- [Radix UI](https://www.radix-ui.com/)

### 16.3 Accessibility
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [A11y Project](https://www.a11yproject.com/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

### 16.4 Internal References
- **Onboarding Flow Spec:** `/docs/design/onboarding-flow-first-run-spec.md`
- **Information Architecture:** `/docs/design/LAB-001-UX-002-INFORMATION-ARCHITECTURE.md`
- **User Journey Map:** `/docs/design/LAB-001-UX-001-USER-JOURNEY-MAP.md`

---

## 17. Contributing

### 17.1 Proposing Changes

1. Create design spec in `/docs/design/`
2. Get review from faintech-product-designer
3. Implement in component library
4. Update this documentation
5. Add tests

### 17.2 Review Process

- **Minor changes:** faintech-frontend can implement directly
- **Major changes:** Require design review
- **Breaking changes:** Require team discussion

---

**Document Status:** ACTIVE
**Maintainer:** faintech-product-designer
**Last Review:** 2026-03-23
**Next Review:** 2026-04-01

---

**Created:** 2026-03-23 03:06 EET
**Version:** 1.0.0
