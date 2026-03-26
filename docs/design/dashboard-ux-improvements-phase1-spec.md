# Dashboard UX Improvements - Phase 1

**Author:** faintech-product-designer
**Date:** 2026-03-26
**Target:** faintech-frontend (engineering implementation)
**Status:** DRAFT - READY FOR REVIEW
**Timeline:** Post-Beta Week 2-4 (Mar 29 - Apr 14, 2026)
**Priority:** P2 (Enhancement)

---

## Executive Summary

Post-beta user feedback will identify friction points in the dashboard experience. This spec defines **Phase 1 improvements** based on beta learnings and anticipated user needs. Implementation should begin **after** Feedback Widget (P0) and Search Memory Step (P1) are complete.

**Implementation Timeline:** 10 business days (2 weeks)
**Dependencies:** User Feedback Widget live (to capture real user issues)

---

## Problem Statement

### Current Dashboard Limitations

Based on the beta implementation review (`AgentDashboardView.tsx`):

1. **No Search in Dashboard** - Users can only search during onboarding, not in daily use
2. **No Memory Details** - Clicking a memory shows nothing (no drill-down)
3. **No Filtering** - Can't filter by type, date range, or tags
4. **Limited Stats Context** - Stats are numbers only, no trends or comparisons
5. **No Bulk Actions** - Can't select multiple memories for batch operations
6. **Static Distribution Chart** - Bar chart doesn't show changes over time

### Anticipated User Pain Points

| Pain Point | Evidence | Solution |
|------------|----------|----------|
| "I can't find a specific memory" | Search only in onboarding | Add search bar to dashboard |
| "What did I save last week?" | No temporal navigation | Add date filter |
| "I want to see more details" | No click interaction | Add memory detail modal |
| "Which type do I use most?" | Static distribution | Add trend indicator |

---

## Scope - Phase 1 Improvements

### 1. Dashboard Search Bar 🔴 HIGH IMPACT

**Rationale:** Search is the #1 feature for memory retrieval. Currently only available during onboarding.

**Component:** `<DashboardSearchBar />`

**Location:** Above stats cards, full-width

**Behavior:**
- Real-time search (debounced 300ms)
- Searches memory content + tags
- Shows results in "Recent Memories" section (filtered)
- Clear button to reset filter
- Keyboard shortcut: `Cmd/Ctrl + K` to focus

**States:**
- Empty: Placeholder text "Search memories..."
- Loading: Spinner while searching
- Results: Filtered memories list
- No Results: "No memories found for '{query}'"
- Error: Toast notification

**Acceptance Criteria:**
- [ ] Search bar visible on dashboard load
- [ ] Search returns results in < 500ms
- [ ] Results update in real-time as user types
- [ ] Clear button resets to all memories
- [ ] Keyboard shortcut works (Cmd/Ctrl + K)
- [ ] Mobile: Search bar collapses to icon, expands on tap

---

### 2. Memory Detail Modal 🔴 HIGH IMPACT

**Rationale:** Users need to see full memory content, metadata, and edit options.

**Component:** `<MemoryDetailModal />`

**Trigger:** Click on any memory in "Recent Memories" list

**Content:**
- Full memory content (no truncation)
- Type badge
- Timestamp (created_at)
- Tags list (all tags, not just first 3)
- Metadata section (agent_id, memory_id, storage_size)
- Actions: Edit, Delete, Copy ID

**Layout:**
```
┌─────────────────────────────────────────┐
│ [Type Badge]           [X] Close        │
│                                         │
│ Full memory content goes here...        │
│ ...                                     │
│                                         │
│ Tags: #tag1 #tag2 #tag3 #tag4           │
│                                         │
│ Created: Mar 26, 2026 at 09:53 AM       │
│ Memory ID: mem_abc123                   │
│                                         │
│ [Edit] [Delete] [Copy ID]               │
└─────────────────────────────────────────┘
```

**Acceptance Criteria:**
- [ ] Modal opens on memory click
- [ ] Shows full content (no truncation)
- [ ] Shows all tags (not just first 3)
- [ ] Shows exact timestamp
- [ ] Close button works (X + click outside + Esc)
- [ ] Copy ID copies to clipboard with toast
- [ ] Edit button triggers edit mode (future Phase 2)
- [ ] Delete button shows confirmation dialog

---

### 3. Memory Type Filter 🟡 MEDIUM IMPACT

**Rationale:** Users want to focus on specific memory types (e.g., only "outcomes").

**Component:** `<MemoryTypeFilter />`

**Location:** Above "Recent Memories" section, horizontal pill buttons

**Options:**
- All (default)
- Outcome
- Learning
- Preference
- Decision

**Behavior:**
- Click to filter memories list
- Active filter shows blue background
- Filter persists during session (localStorage)
- Combine with search (AND logic)

**Acceptance Criteria:**
- [ ] Filter pills visible above memories list
- [ ] Clicking filter updates list immediately
- [ ] Active filter shows visual indicator
- [ ] Filter persists across page refresh (localStorage)
- [ ] Search + filter work together (AND logic)
- [ ] Mobile: Horizontal scroll for pills

---

### 4. Date Range Filter 🟡 MEDIUM IMPACT

**Rationale:** Users want to see memories from specific time periods.

**Component:** `<DateRangeFilter />`

**Location:** Next to type filter, dropdown

**Options:**
- All Time (default)
- Today
- This Week
- This Month
- Custom Range (date picker)

**Behavior:**
- Dropdown selection
- Updates "Recent Memories" list
- Shows count: "Showing 23 memories from This Week"
- Combine with search + type filter

**Acceptance Criteria:**
- [ ] Dropdown visible next to type filter
- [ ] Preset options work (Today, This Week, This Month)
- [ ] Custom range opens date picker
- [ ] Shows filtered count
- [ ] Combines with other filters (AND logic)
- [ ] Mobile: Native date picker

---

### 5. Stats Trend Indicator 🟢 LOW IMPACT

**Rationale:** Users want to see if they're creating more or fewer memories over time.

**Component:** Add trend indicator to existing stats cards

**Visual:**
- Green arrow up: +X% vs last period
- Red arrow down: -X% vs last period
- Gray dash: No change

**Calculation:**
- Compare current period (7 days) to previous period (7 days before)
- Show percentage change
- Tooltop: "X this week vs Y last week"

**Acceptance Criteria:**
- [ ] Trend indicator shows on "This Week" stat
- [ ] Calculates % change vs previous week
- [ ] Green for increase, red for decrease
- [ ] Tooltip explains calculation
- [ ] Mobile: Same behavior

---

## Non-Goals (Phase 2)

These features are deferred to Phase 2 (Week 5-8):

- **Memory Editing** - Edit content, tags, type
- **Bulk Operations** - Select multiple, batch delete/tag
- **Memory Export** - Download as JSON/CSV
- **Advanced Search** - Boolean operators, regex
- **Tag Management** - Create/rename/delete tags
- **Memory Collections** - Group memories into folders

---

## Technical Requirements

### API Endpoints (Check existence)

| Endpoint | Purpose | Status |
|----------|---------|--------|
| `GET /api/agents/{agentId}/memories?search={query}` | Search memories | ⚠️ Verify |
| `GET /api/agents/{agentId}/memories?type={type}` | Filter by type | ⚠️ Verify |
| `GET /api/agents/{agentId}/memories?from={date}&to={date}` | Filter by date | ⚠️ Verify |
| `GET /api/agents/{agentId}/memories/{memoryId}` | Get single memory | ⚠️ Verify |
| `DELETE /api/agents/{agentId}/memories/{memoryId}` | Delete memory | ⚠️ Verify |

### New Components

| Component | File | Priority |
|-----------|------|----------|
| `DashboardSearchBar` | `components/dashboard/DashboardSearchBar.tsx` | P0 |
| `MemoryDetailModal` | `components/dashboard/MemoryDetailModal.tsx` | P0 |
| `MemoryTypeFilter` | `components/dashboard/MemoryTypeFilter.tsx` | P1 |
| `DateRangeFilter` | `components/dashboard/DateRangeFilter.tsx` | P1 |

### State Management

- Search query state (local component state)
- Filter state (localStorage for persistence)
- Modal open/close state
- Selected memory state

---

## Implementation Order

### Week 2 (Mar 29 - Apr 4): Core Features

**Days 1-2 (Mar 29-30):**
- Dashboard Search Bar component
- Search API integration
- Loading + empty states

**Days 3-4 (Mar 31 - Apr 1):**
- Memory Detail Modal component
- Get memory API integration
- Copy ID functionality

**Day 5 (Apr 2):**
- QA testing (functional + accessibility)
- Bug fixes

### Week 3 (Apr 3-7): Filters & Polish

**Days 1-2 (Apr 3-4):**
- Memory Type Filter component
- Filter API integration
- Combine with search

**Days 3-4 (Apr 5-6):**
- Date Range Filter component
- Custom date picker
- Stats trend indicator

**Day 5 (Apr 7):**
- QA testing
- Final polish
- Deploy to production

---

## Success Metrics

### Quantitative

| Metric | Target | Measurement |
|--------|--------|-------------|
| Search usage | > 40% of users search within 7 days | Analytics event |
| Modal open rate | > 30% of users open detail modal | Analytics event |
| Filter usage | > 20% of users use filters | Analytics event |
| Search response time | < 500ms p95 | Performance monitoring |

### Qualitative

- Users report "easier to find memories" in feedback
- Reduced support requests about "lost" memories
- Positive feedback on search/filter UX

---

## Accessibility Requirements

All components must meet **WCAG 2.1 AA**:

- [ ] Keyboard navigation (Tab, Enter, Esc)
- [ ] Screen reader announcements (ARIA labels)
- [ ] Focus management (modal trap focus)
- [ ] Color contrast (4.5:1 minimum)
- [ ] Touch targets (44x44px minimum)

---

## Mobile Responsiveness

| Breakpoint | Layout |
|------------|--------|
| Desktop (> 1024px) | Full layout, side-by-side filters |
| Tablet (768-1024px) | Stacked filters, full-width search |
| Mobile (< 768px) | Collapsed search icon, scrollable filters |

---

## Analytics Events

### Search Events
- `dashboard_search_initiated` - User focuses search bar
- `dashboard_search_completed` - User submits search
- `dashboard_search_cleared` - User clears search

### Filter Events
- `dashboard_filter_applied` - User selects filter
- `dashboard_filter_cleared` - User clears filter

### Modal Events
- `memory_detail_opened` - User opens modal
- `memory_detail_closed` - User closes modal
- `memory_id_copied` - User copies memory ID

---

## Testing Checklist

### Functional Testing
- [ ] Search returns correct results
- [ ] Search + filter work together
- [ ] Modal shows correct memory
- [ ] Copy ID works
- [ ] Filters persist across refresh

### Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Screen reader announces changes
- [ ] Focus trap in modal
- [ ] Color contrast passes

### Mobile Testing
- [ ] Touch targets are 44x44px
- [ ] Search bar usable on mobile
- [ ] Filters scrollable on mobile
- [ ] Modal usable on mobile

---

## Open Questions

1. **Search API:** Does `/api/agents/{agentId}/memories?search={query}` exist? (Check with faintech-backend)
2. **Filter API:** Can we combine multiple query params? (e.g., `?search=X&type=Y&from=Z`)
3. **Delete Confirmation:** Should delete require typing "DELETE" or just a button?
4. **Edit Feature:** Should we include edit in Phase 1 or defer to Phase 2?

---

## Handoff Checklist

### For faintech-frontend
- [x] Design spec complete
- [x] Component list defined
- [x] API requirements documented
- [x] Implementation order prioritized
- [ ] API endpoints verified (check with backend)
- [ ] Feature branch created
- [ ] Implementation started

### For faintech-backend
- [ ] Verify search endpoint supports query params
- [ ] Verify filter endpoint supports type + date params
- [ ] Verify single memory GET endpoint exists
- [ ] Verify delete endpoint exists
- [ ] Test performance (< 500ms response)

### For qa
- [ ] Review spec for testability
- [ ] Prepare test cases (functional + accessibility)
- [ ] Test mobile responsiveness

---

**Document Status:** DRAFT - Ready for CPO/CTO Review
**Created:** 2026-03-26 09:53 EET
**Author:** faintech-product-designer
**Next Review:** Post-beta Week 1 (Mar 28) after user feedback arrives
**Implementation Start:** Post-beta Week 2 (Mar 29)
