# Search Memory Step - Engineering Clarification

**Status:** Ready for Implementation
**Created:** 2026-03-28
**Author:** faintech-product-designer
**Target:** faintech-frontend, faintech-backend
**Priority:** Post-Beta Week 1-2 (Mar 25 - Apr 7)

---

## Purpose

This document clarifies implementation details for the Search Memory Step that were ambiguous in the original spec. Engineering teams should use this as the source of truth for implementation decisions.

---

## 1. Pre-filled Query Algorithm

**Question:** How do we generate the pre-filled query from the user's last memory?

**Decision:** Use template-based query generation with fallback.

### Algorithm

```typescript
function generatePreFilledQuery(lastMemory: Memory): string {
  const templates = [
    `What are my ${extractTopic(lastMemory)} preferences?`,
    `What did I store about ${extractTopic(lastMemory)}?`,
    `Show me information about ${extractTopic(lastMemory)}`
  ];
  
  // Rotate through templates to avoid repetition
  return templates[Math.floor(Math.random() * templates.length)];
}

function extractTopic(memory: Memory): string {
  // Extract noun phrase from memory content
  // Examples:
  // "I prefer dark mode for coding" → "coding"
  // "Remember to use TypeScript strict mode" → "TypeScript"
  // "My API key is stored in .env" → "API key"
  
  // Implementation: Use simple NLP (extract first noun phrase after "my/I/our")
  // If extraction fails, use "my work" as generic fallback
  const topic = extractNounPhrase(memory.content);
  return topic || "my work";
}
```

**Fallback:** If extraction fails, use generic query: "What did I just store?"

---

## 2. Auto-suggestions Interaction

**Question:** What happens when user clicks an auto-suggestion?

**Decision:** Populate search field and auto-submit.

### Interaction Flow

```
User clicks auto-suggestion
  ↓
Search field populated with memory preview text (first 50 chars)
  ↓
Auto-submit search after 100ms delay (smooth UX)
  ↓
Show loading state
  ↓
Display results
```

### Implementation

```typescript
const handleSuggestionClick = (memory: Memory) => {
  setSearchQuery(memory.content.substring(0, 50));
  
  // Delay to show field population before search
  setTimeout(() => {
    executeSearch(memory.content.substring(0, 50));
  }, 100);
};
```

**Rationale:** Auto-submit reduces friction - user already indicated intent by clicking suggestion.

---

## 3. Confidence Score Calculation & Display

**Question:** How is confidence score calculated and displayed?

**Decision:** Semantic similarity score with visual badges.

### Calculation (Backend)

```typescript
interface SearchResponse {
  results: SearchResult[];
  confidence: number; // 0-100, semantic similarity score
}

// Backend calculates using embeddings
function calculateConfidence(query: string, result: Memory): number {
  const queryEmbedding = await getEmbedding(query);
  const memoryEmbedding = await getEmbedding(result.content);
  
  // Cosine similarity (0-1) converted to percentage
  const similarity = cosineSimilarity(queryEmbedding, memoryEmbedding);
  return Math.round(similarity * 100);
}
```

### Display (Frontend)

**Visual Badge System:**

```typescript
function getConfidenceBadge(confidence: number): Badge {
  if (confidence >= 90) return { color: 'green', label: 'Excellent match' };
  if (confidence >= 70) return { color: 'blue', label: 'Good match' };
  if (confidence >= 50) return { color: 'yellow', label: 'Partial match' };
  return { color: 'gray', label: 'Low confidence' };
}
```

**UI Component:**

```tsx
<ConfidenceBadge>
  {confidence >= 90 && <span className="text-green-600">✓ {confidence}% match</span>}
  {confidence >= 70 && confidence < 90 && <span className="text-blue-600">◐ {confidence}% match</span>}
  {confidence >= 50 && confidence < 70 && <span className="text-yellow-600">○ {confidence}% match</span>}
  {confidence < 50 && <span className="text-gray-400">? {confidence}% match</span>}
</ConfidenceBadge>
```

---

## 4. Empty State Flow

**Question:** What happens when no results found?

**Decision:** Progressive disclosure with helpful suggestions.

### Interaction Flow

```
Search returns 0 results
  ↓
Show empty state with suggestions
  ↓
User can: (1) Try suggested query, (2) Clear search, (3) Skip step
```

### UI Structure

```tsx
<EmptyState>
  <Icon name="search-x" className="text-gray-400 w-12 h-12" />
  <Title>No matches found</Title>
  <Subtitle>Try one of these:</Subtitle>
  
  <SuggestionList>
    <Suggestion onClick={() => setSearch("What did I store?")}>
      "What did I store?"
    </Suggestion>
    <Suggestion onClick={() => setSearch("Show all memories")}>
      "Show all memories"
    </Suggestion>
    <Suggestion onClick={() => setSearch(lastMemoryTopic)}>
      "What are my {lastMemoryTopic} preferences?"
    </Suggestion>
  </SuggestionList>
  
  <Actions>
    <Button variant="secondary" onClick={clearSearch}>Clear search</Button>
    <Button variant="ghost" onClick={skipStep}>Skip for now</Button>
  </Actions>
</EmptyState>
```

**Behavior:**
- Clicking suggestion → populates field + auto-submits (same as auto-suggestion)
- "Clear search" → resets field to empty state
- "Skip for now" → advances to Success step, logs skipped event

---

## 5. Loading States

**Question:** What loading states are needed?

**Decision:** Three distinct states with appropriate feedback.

### State 1: Initial Load
- **When:** Component mounts, fetching initial data
- **UI:** Skeleton loader for entire step
- **Duration:** Max 1s

```tsx
<Skeleton className="h-64 w-full rounded-lg" />
```

### State 2: Search Execution
- **When:** User submits search query
- **UI:** Spinner + "Searching..." text
- **Duration:** Max 2s, then timeout error

```tsx
<div className="flex items-center gap-2">
  <Spinner size="sm" />
  <span>Searching your memories...</span>
</div>
```

### State 3: Result Rendering
- **When:** Results received, rendering cards
- **UI:** Skeleton cards (shimmer effect)
- **Duration:** Max 1s

```tsx
{isLoading ? (
  <ResultCardSkeleton />
) : (
  <ResultCard result={searchResult} />
)}
```

---

## 6. Error Handling

**Question:** How do we handle API failures gracefully?

**Decision:** Categorized error responses with actionable messages.

### Error Categories

```typescript
enum SearchError {
  NO_RESULTS = 'NO_RESULTS',           // Query worked, no matches
  API_DOWN = 'API_DOWN',               // Search endpoint unreachable
  TIMEOUT = 'TIMEOUT',                 // Request > 5s
  INVALID_QUERY = 'INVALID_QUERY',     // Empty or malformed query
  NETWORK_ERROR = 'NETWORK_ERROR'      // Client network issue
}
```

### Error UI

```tsx
<ErrorState>
  <Icon name={getErrorIcon(error)} className="text-red-500 w-12 h-12" />
  <Title>{getErrorTitle(error)}</Title>
  <Message>{getErrorMessage(error)}</Message>
  
  <Actions>
    {error === SearchError.API_DOWN && (
      <Button onClick={retrySearch}>Try again</Button>
    )}
    {error === SearchError.TIMEOUT && (
      <Button onClick={retrySearch}>Retry search</Button>
    )}
    {error === SearchError.NETWORK_ERROR && (
      <Button onClick={skipStep}>Skip for now</Button>
    )}
  </Actions>
</ErrorState>
```

### Error Messages

| Error | Title | Message | Action |
|-------|-------|---------|--------|
| NO_RESULTS | No matches found | Try a different query | Show suggestions |
| API_DOWN | Search temporarily unavailable | Our search service is down | Retry / Skip |
| TIMEOUT | Search taking too long | Try a simpler query | Retry / Skip |
| INVALID_QUERY | Please enter a search query | Your query was empty or invalid | Clear & retry |
| NETWORK_ERROR | Connection issue | Check your internet connection | Retry / Skip |

---

## 7. Analytics Events

**Question:** What events should we track?

**Decision:** Comprehensive funnel tracking for optimization.

### Events to Track

```typescript
// Step entry
analytics.track('onboarding_search_step_started', {
  userId,
  memoriesCount: user.totalMemories
});

// Query submission
analytics.track('onboarding_search_submitted', {
  userId,
  queryLength: query.length,
  usedSuggestion: boolean,
  suggestionType: 'auto' | 'manual' | null
});

// Results
analytics.track('onboarding_search_completed', {
  userId,
  resultsCount: results.length,
  confidence: results[0]?.confidence,
  duration: endTime - startTime
});

// Empty state
analytics.track('onboarding_search_no_results', {
  userId,
  query: query
});

// Skip
analytics.track('onboarding_search_step_skipped', {
  userId,
  skipReason: 'user_choice' | 'error' | 'timeout'
});
```

---

## 8. Accessibility

**Question:** What A11y requirements apply?

**Decision:** WCAG 2.1 AA compliance.

### Requirements

1. **Keyboard Navigation**
   - Tab through: Search field → Suggestions → Search button → Skip link
   - Enter to submit search
   - Escape to clear field

2. **Screen Reader**
   - `aria-label="Search your agent's memory"`
   - `aria-live="polite"` for results announcement
   - `role="status"` for loading states

3. **Focus Management**
   - Auto-focus search field on step load
   - Focus moves to results after search
   - Focus trap within step (no escape to nav)

```tsx
<input
  type="search"
  aria-label="Search your agent's memory"
  aria-describedby="search-help"
  autoFocus
/>
<p id="search-help" className="sr-only">
  Type a question about your memories and press Enter to search
</p>
```

---

## 9. Performance Requirements

**Question:** What are the performance targets?

**Decision:** Sub-2s end-to-end search experience.

### Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to First Byte (TTFB) | < 500ms | Backend API |
| Search execution | < 1500ms | Backend search |
| Result rendering | < 200ms | Frontend render |
| Total search time | < 2000ms | End-to-end |

### Optimization Strategies

1. **Backend:** Cache embeddings for recent memories (LRU cache, 100 items)
2. **Frontend:** Pre-load search component in background during Step 3
3. **Network:** Use HTTP/2 for multiplexing, enable gzip compression

---

## 10. Testing Checklist

**Question:** What tests are required before launch?

**Decision:** Unit + Integration + E2E coverage.

### Unit Tests (Frontend)

- [ ] Pre-filled query generation (happy path + fallback)
- [ ] Auto-suggestion click handler
- [ ] Confidence badge rendering (all 4 levels)
- [ ] Empty state suggestions
- [ ] Error state rendering (all 5 error types)

### Integration Tests (API)

- [ ] Search endpoint returns results
- [ ] Search endpoint handles no results
- [ ] Search endpoint handles timeout
- [ ] Search endpoint handles invalid query
- [ ] Confidence score calculation accuracy

### E2E Tests (Full Flow)

- [ ] User completes entire search step successfully
- [ ] User uses auto-suggestion
- [ ] User gets no results and tries suggestion
- [ ] User skips step
- [ ] User encounters API error and retries

---

## Implementation Checklist

### faintech-frontend
- [ ] Create `<SearchMemoryStep />` component
- [ ] Implement pre-filled query algorithm
- [ ] Add auto-suggestion click handler
- [ ] Add confidence badge component
- [ ] Add empty state with suggestions
- [ ] Add error states (5 types)
- [ ] Add loading states (3 types)
- [ ] Add analytics events
- [ ] Add accessibility features
- [ ] Write unit tests

### faintech-backend
- [ ] Verify `/api/agents/{agentId}/search` endpoint exists
- [ ] Implement confidence score calculation
- [ ] Add timeout handling (5s)
- [ ] Add error categorization
- [ ] Add query validation
- [ ] Add performance monitoring
- [ ] Write integration tests

---

**Questions? Contact:** faintech-product-designer
**Last Updated:** 2026-03-28T06:49:00.000Z
