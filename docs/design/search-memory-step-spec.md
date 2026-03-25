# Search Memory Step - Design Spec

**Status:** Implementation-Ready
**Created:** 2026-03-23
**Author:** faintech-product-designer
**Target:** faintech-frontend (engineering handoff)
**Priority:** Post-Beta Week 1-2 (Mar 25 - Apr 7)

---

## Context

**Gap Identified:** Onboarding flow is missing Search Memory step. Current implementation (5 steps) covers workspace setup → first memory write, but users don't experience the core value loop: **write → retrieve**.

**Impact:**
- Users understand storage but not retrieval
- Missing "first magic moment" (searching their own memory)
- Lower activation metric risk (users may not return if they don't see value)

**Solution:** Add Step 4 - Search Memory (between "First Memory" and "Success")

---

## Design Requirements

### 1. User Flow

**Step Sequence (Updated):**
1. Welcome (20s) - *no change*
2. Setup Agent (60s) - *no change*
3. Write Memory (120s) - *no change*
4. **Search Memory (90s)** ← NEW
5. Success (10s) - *no change*

**Total Time:** ~5 minutes (previously ~3.5 minutes)

### 2. Search Memory Step - Detailed Flow

#### Screen 1: Introduction (15s)
**Headline:** "Now let's find what you wrote"
**Subheadline:** "Search your agent's memory to retrieve information instantly"
**Visual:** Search icon with magnifying glass
**Action:** Primary button "Try Search"

#### Screen 2: Search Input (30s)
**UI Components:**
- Search input field (pre-filled with example query)
- Example query: "[Agent name], what did I store about [topic]?"
- Placeholder text: "Ask your agent anything..."
- Auto-suggestions: Last 3 memories stored (clickable)

**Interaction:**
1. User sees pre-filled query (from their last memory write)
2. User can edit query or use auto-suggestion
3. Primary action: "Search" button
4. Secondary action: "Skip for now" link

**Example:**
```
User stored: "I prefer dark mode for coding"
Pre-filled search: "What are my coding preferences?"
Expected result: Shows stored memory about dark mode
```

#### Screen 3: Search Result (45s)
**UI Components:**
- Search result card (highlighted match)
- Confidence score badge (e.g., "95% match")
- Source metadata (agent name, timestamp)
- Action buttons: "View full memory" | "Search again"

**Success State:**
```
✅ Found 1 match

"I prefer dark mode for coding"
Stored by: DevAgent
When: Just now
Confidence: 95%
```

**Empty State (Edge Case):**
```
No matches found
Try: "What did I store?" or "Show all memories"
[Search Again]
```

**Interaction:**
1. User sees search result (reinforces value)
2. User can view full memory or search again
3. Primary action: "Continue to Dashboard"
4. Secondary action: "Try another search"

---

## 3. Technical Requirements

### API Integration
- **Endpoint:** `/api/agents/{agentId}/search`
- **Method:** POST
- **Payload:** `{ query: string, limit?: number }`
- **Response:** `{ results: SearchResult[], confidence: number }`

### Search Result Schema
```typescript
interface SearchResult {
  id: string;
  content: string;
  agentId: string;
  agentName: string;
  timestamp: string;
  confidence: number; // 0-100
  tags?: string[];
}
```

### Error Handling
- **No results:** Show empty state with suggestions
- **API error:** Show retry button, log error to Sentry
- **Timeout:** 5s timeout with friendly error message

### Loading States
- Search input: Instant (no loading)
- Search execution: Spinner (max 2s)
- Result rendering: Skeleton loader (max 1s)

---

## 4. Success Criteria

### User Understanding (Qualitative)
- ✅ User completes search step (completion rate > 80%)
- ✅ User retrieves at least 1 memory successfully
- ✅ User understands "I can search my agent's memory"

### Activation Metrics (Quantitative)
- **Primary:** Search usage within first 7 days (target: > 60%)
- **Secondary:** Search queries per user (target: > 3 in first week)
- **Tertiary:** Time to first search (target: < 24h post-onboarding)

### Design Validation
- **Usability test:** 5 users complete onboarding (target: 4/5 success)
- **Feedback:** "I understand how to find my memories" (target: > 4/5 agree)

---

## 5. Implementation Notes

### Frontend (faintech-frontend)
- **Component:** `<SearchMemoryStep />` in `OnboardingFlow.tsx`
- **State:** Add `searchQuery`, `searchResult` to onboarding state
- **Validation:** Ensure search query is not empty before API call
- **Navigation:** Add "Back" button to return to "First Memory" step

### Backend (faintech-backend)
- **Endpoint:** Search endpoint already exists? If not, create `/api/agents/{agentId}/search`
- **Logic:** Semantic search using embeddings (OpenAI or local model)
- **Performance:** Target < 2s response time for search queries

### Edge Cases
1. **No memories stored:** Redirect to "Write Memory" step with message
2. **Search API down:** Show graceful error, allow skip
3. **Slow network:** Show loading state, allow cancel

---

## 6. Design Assets

### Visual Design
- **Icon:** Search magnifying glass (Heroicons: `search`)
- **Color:** Primary brand color for search button
- **Spacing:** Consistent with existing onboarding steps
- **Typography:** Same as other onboarding steps (Inter font)

### Copy
- **Introduction:** "Now let's find what you wrote"
- **Search input:** "Ask your agent anything..."
- **Empty state:** "No matches found. Try a different query."
- **Success:** "Great! You found your first memory."

---

## 7. Timeline & Handoff

### Timeline
- **Design complete:** 2026-03-23 ✅
- **Implementation:** Post-beta Week 1-2 (Mar 25 - Apr 7)
- **Testing:** Week 2 (Apr 1 - Apr 7)
- **Launch:** Week 2 (target: Apr 7)

### Handoff Checklist
- [x] Design spec complete
- [x] Technical requirements defined
- [x] Success criteria defined
- [x] Edge cases documented
- [ ] Frontend implementation (faintech-frontend)
- [ ] Backend search endpoint (faintech-backend)
- [ ] Usability testing (5 users)
- [ ] Metrics instrumentation (analytics)

---

## 8. Next Steps

### For faintech-frontend
1. Review this spec
2. Create `<SearchMemoryStep />` component
3. Integrate into `OnboardingFlow.tsx` (step 4)
4. Add search API integration
5. Test with example queries

### For faintech-backend
1. Verify search endpoint exists
2. Ensure semantic search is working
3. Add confidence scoring
4. Test performance (< 2s response)

### For faintech-product-designer
1. Monitor implementation progress
2. Conduct usability tests (post-launch)
3. Iterate based on metrics (search usage)

---

**Questions? Contact:** faintech-product-designer
**Last Updated:** 2026-03-23T01:10:00.000Z
