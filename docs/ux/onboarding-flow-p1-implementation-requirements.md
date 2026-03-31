# Onboarding Flow P1 - Implementation Requirements

**Created:** 2026-03-31 17:45 EET
**Author:** faintech-product-designer
**Target:** faintech-frontend
**Priority:** P1 - Week 2 GTM Conversion Optimization
**Timeline:** 6 hours (April 1-2, 2026)

---

## Executive Summary

**Current State:** Onboarding flow exists but has critical gaps:
- Missing agent creation step
- Missing search memory step
- Uses localStorage instead of actual API calls
- Doesn't demonstrate full value loop (write → retrieve)

**Required State:** 5-step flow with actual backend integration:
1. Welcome (20s)
2. Setup Agent (60s) - **CREATE AGENT VIA API**
3. Write First Memory (120s) - **CREATE MEMORY VIA API**
4. Search Memory (90s) - **SEARCH VIA API** ← **MISSING IN CURRENT IMPLEMENTATION**
5. Success (10s)

**Impact:** Without search step, users don't experience the core value proposition (retrieval), leading to lower activation rates and higher churn.

---

## Gap Analysis

### Current Implementation vs Design Spec

| Aspect | Current Implementation | Design Spec | Gap |
|--------|----------------------|-------------|-----|
| **Step 2** | Workspace name (localStorage) | Agent creation with name + type (API call) | **Critical** - No agent created |
| **Step 3** | API key input (manual) | First memory creation (API call) | **Critical** - No memory written |
| **Step 4** | Memory draft (localStorage) | Search memory (API call) | **Critical** - Missing step |
| **Step 5** | Success (no data) | Success (shows completion time) | Minor - Missing metrics |
| **API Integration** | None (localStorage only) | Full backend integration | **Critical** |
| **State Persistence** | localStorage only | localStorage + backend sync | **High** |

---

## Implementation Requirements

### P1-A: Add Agent Creation Step (Replace Step 2)

**Current:** `/Users/eduardgridan/faintech-lab/amc-frontend/src/components/OnboardingFlow.tsx` - Step 2 is "workspace"

**Required Changes:**

1. **Rename Step 2 from "workspace" to "agent-setup"**
   ```typescript
   type StepId = 'welcome' | 'agent-setup' | 'api-key' | 'first-memory' | 'search-memory' | 'success';
   ```

2. **Add agent type selection**
   ```typescript
   const [agentName, setAgentName] = useState('');
   const [agentType, setAgentType] = useState<'general' | 'code' | 'research'>('general');
   ```

3. **Create agent via API**
   ```typescript
   const handleAgentSubmit = async (event: FormEvent<HTMLFormElement>) => {
     event.preventDefault();

     if (!agentName.trim()) {
       setError('Choose an agent name to continue.');
       return;
     }

     try {
       const response = await fetch('/api/agents', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({
           name: agentName.trim(),
           type: agentType
         })
       });

       if (!response.ok) throw new Error('Failed to create agent');

       const agent = await response.json();
       localStorage.setItem('amc_agent_id', agent.id);
       localStorage.setItem('amc_agent_name', agent.name);
       goToStep('api-key');
     } catch (err) {
       setError('Failed to create agent. Please try again.');
     }
   };
   ```

4. **Update UI to match design spec**
   - Add agent type radio buttons
   - Add example agent names
   - Update validation (3-50 chars)

**Success Criteria:**
- Agent created via `/api/agents` endpoint
- Agent ID stored in localStorage
- User can proceed to next step
- Error handling for API failures

---

### P1-B: Convert Memory Draft to Actual Memory Creation (Update Step 4)

**Current:** Step 4 is "first-memory" with localStorage draft

**Required Changes:**

1. **Create memory via API instead of localStorage**
   ```typescript
   const handleMemorySubmit = async () => {
     const agentId = localStorage.getItem('amc_agent_id');
     const trimmedMemory = memoryDraft.trim();

     try {
       const response = await fetch('/api/memories', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({
           agentId,
           content: trimmedMemory,
           tags: [] // Optional
         })
       });

       if (!response.ok) throw new Error('Failed to create memory');

       const memory = await response.json();
       localStorage.setItem('amc_first_memory_id', memory.id);
       goToStep('search-memory');
     } catch (err) {
       setError('Failed to save memory. Please try again.');
     }
   };
   ```

2. **Update button label**
   ```typescript
   <button onClick={handleMemorySubmit}>
     Save Memory →
   </button>
   ```

**Success Criteria:**
- Memory created via `/api/memories` endpoint
- Memory ID stored in localStorage
- User can proceed to search step
- Error handling for API failures

---

### P1-C: Add Search Memory Step (NEW Step 5)

**Current:** Missing entirely

**Required Changes:**

1. **Add new step to flow**
   ```typescript
   type StepId = 'welcome' | 'agent-setup' | 'api-key' | 'first-memory' | 'search-memory' | 'success';
   const steps: StepId[] = ['welcome', 'agent-setup', 'api-key', 'first-memory', 'search-memory', 'success'];
   ```

2. **Add search state**
   ```typescript
   const [searchQuery, setSearchQuery] = useState('');
   const [searchResults, setSearchResults] = useState<Memory[]>([]);
   const [searching, setSearching] = useState(false);
   ```

3. **Implement search functionality**
   ```typescript
   const handleSearch = async () => {
     const agentId = localStorage.getItem('amc_agent_id');

     if (!searchQuery.trim()) {
       setError('Enter a search query to continue.');
       return;
     }

     setSearching(true);
     try {
       const response = await fetch(
         `/api/memories/search?q=${encodeURIComponent(searchQuery)}&agentId=${agentId}`
       );

       if (!response.ok) throw new Error('Search failed');

       const data = await response.json();
       setSearchResults(data.results);
       goToStep('success');
     } catch (err) {
       setError('Search failed. Please try again.');
     } finally {
       setSearching(false);
     }
   };
   ```

4. **Add UI for search step**
   ```typescript
   {step === 'search-memory' && (
     <div className="space-y-6">
       <div>
         <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-primary">
           Search Memory
         </p>
         <h2 className="mt-2 text-3xl font-semibold text-slate-950">
           Now find what you wrote
         </h2>
         <p className="mt-3 text-sm leading-6 text-slate-600">
           Search your agent's memory to retrieve information instantly.
         </p>
       </div>

       <div>
         <label htmlFor="search-query" className="block text-sm font-medium text-slate-700">
           Search query
         </label>
         <input
           id="search-query"
           value={searchQuery}
           onChange={(e) => setSearchQuery(e.target.value)}
           className="mt-2 block w-full rounded-2xl border border-slate-300 px-4 py-3"
           placeholder="What did I store about databases?"
         />
       </div>

       {searchResults.length > 0 && (
         <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
           <p className="text-sm font-medium text-emerald-900">
             ✅ Found {searchResults.length} match(es)
           </p>
           {searchResults.map((result) => (
             <div key={result.id} className="mt-3 text-sm text-emerald-800">
               {result.content}
             </div>
           ))}
         </div>
       )}

       <div className="flex gap-3">
         <button onClick={() => goToStep('first-memory')}>Back</button>
         <button onClick={handleSearch} disabled={searching}>
           {searching ? 'Searching...' : 'Search →'}
         </button>
       </div>
     </div>
   )}
   ```

5. **Pre-populate search query**
   ```typescript
   // Extract keywords from first memory
   useEffect(() => {
     if (step === 'search-memory' && memoryDraft) {
       const keywords = extractKeywords(memoryDraft);
       setSearchQuery(keywords[0] || '');
     }
   }, [step, memoryDraft]);

   const extractKeywords = (text: string): string[] => {
     // Simple keyword extraction - can be improved
     const words = text.toLowerCase().split(/\s+/);
     const stopWords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'];
     return words.filter(word => word.length > 3 && !stopWords.includes(word)).slice(0, 3);
   };
   ```

**Success Criteria:**
- Search query submitted via `/api/memories/search` endpoint
- Results displayed to user
- User experiences "first magic moment" (retrieval)
- Proceed to success step

---

### P1-D: Update Success Step (Step 6)

**Current:** Shows generic success message

**Required Changes:**

1. **Add completion metrics**
   ```typescript
   const [startTime] = useState(Date.now());

   const completionTime = Math.round((Date.now() - startTime) / 1000);
   const minutes = Math.floor(completionTime / 60);
   const seconds = completionTime % 60;
   ```

2. **Update success UI**
   ```typescript
   {step === 'success' && (
     <div className="space-y-6">
       <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-100 text-2xl text-emerald-700">
         ✓
       </div>
       <div>
         <p className="text-sm font-medium uppercase tracking-[0.2em] text-amc-success">
           Congratulations!
         </p>
         <h2 className="mt-2 text-3xl font-semibold text-slate-950">
           You just gave your AI agent persistent memory
         </h2>
       </div>

       <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
         <p className="font-semibold">What you accomplished:</p>
         <ul className="mt-2 space-y-1">
           <li>✓ Created your first agent</li>
           <li>✓ Wrote your first memory</li>
           <li>✓ Searched and retrieved it</li>
         </ul>
         <p className="mt-3 text-emerald-700 font-medium">
           Time: {minutes}m {seconds}s
         </p>
       </div>

       <button onClick={() => window.location.href = '/dashboard'}>
         Go to Dashboard →
       </button>
     </div>
   )}
   ```

**Success Criteria:**
- Shows actual completion time
- Mirrors promises from welcome step
- Clear next steps (dashboard)

---

## API Requirements

### Backend Endpoints Needed

1. **POST /api/agents**
   ```typescript
   Request:
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

2. **POST /api/memories**
   ```typescript
   Request:
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

3. **GET /api/memories/search**
   ```typescript
   Query params:
   - q: string (search query, 2-200 chars)
   - agentId: string

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

**Status:** Verify these endpoints exist in backend. If not, create them before implementing frontend changes.

---

## Testing Requirements

### Critical Tests

1. **Agent Creation**
   - [ ] Agent created via API on step 2
   - [ ] Agent ID stored in localStorage
   - [ ] Validation: 3-50 chars
   - [ ] Error handling for API failure

2. **Memory Creation**
   - [ ] Memory created via API on step 4
   - [ ] Memory ID stored in localStorage
   - [ ] Validation: 10-5000 chars
   - [ ] Error handling for API failure

3. **Search Memory**
   - [ ] Search query submitted via API
   - [ ] Results displayed to user
   - [ ] Pre-populated with keywords from memory
   - [ ] Error handling for API failure

4. **Flow Completion**
   - [ ] All 6 steps complete successfully
   - [ ] Completion time shown on success screen
   - [ ] Redirect to dashboard works
   - [ ] State persisted across page reloads

---

## Success Metrics

### Week 2 GTM Targets (April 3-10)

- **Landing → Signup conversion:** >5% (vs. 0% Week 1)
- **Onboarding completion rate:** >80% (complete all 6 steps)
- **First memory creation:** >90% (users who write first memory)
- **Search success rate:** >85% (users who retrieve first memory)
- **Time to value:** <5 minutes to first search

### Tracking

- `onboarding_started` - User lands on welcome screen
- `onboarding_step_completed` - User completes each step
- `agent_created` - Agent created via API
- `memory_created` - Memory created via API
- `search_performed` - Search query submitted
- `onboarding_completed` - User reaches success screen

---

## Implementation Timeline

| Date | Task | Owner | Duration |
|------|------|-------|----------|
| April 1 | Backend API verification | faintech-backend | 1h |
| April 1 | Add agent creation step | faintech-frontend | 2h |
| April 1 | Convert memory draft to API call | faintech-frontend | 1h |
| April 2 | Add search memory step | faintech-frontend | 2h |
| April 2 | Update success step with metrics | faintech-frontend | 0.5h |
| April 2 | Testing and QA | qa | 1h |
| April 2 | Deployment | devops | 0.5h |

**Total Duration:** 8 hours (can be completed by April 2, 18:00 EET)

---

## Dependencies

### Required for P1 Implementation

- **Backend APIs:** Verify `/api/agents`, `/api/memories`, `/api/memories/search` exist
- **Design specs:** Already CLARIFIED (onboarding-flow-first-run-spec.md, search-memory-step-spec.md)
- **Engineering handoff:** This document
- **Review:** pm or cpo
- **Deployment:** devops

### External Blockers

- **HUNTER_API_KEY:** Not required for onboarding flow
- **LinkedIn credentials:** Not required for onboarding flow
- **Custom domains:** Not required for onboarding flow

---

## Risk Mitigation

### Technical Risks

1. **Backend APIs not ready**
   - **Mitigation:** Verify endpoints exist before starting frontend work
   - **Fallback:** Use mock API responses for testing

2. **Search API performance**
   - **Mitigation:** Ensure <2s response time
   - **Fallback:** Add loading state and timeout handling

3. **State persistence issues**
   - **Mitigation:** Test localStorage across page reloads
   - **Fallback:** Add "Save & Continue Later" option

### User Experience Risks

1. **Low completion rate**
   - **Mitigation:** Add skip option for power users
   - **Fallback:** Track drop-off points and optimize

2. **API failures**
   - **Mitigation:** Show inline errors with retry buttons
   - **Fallback:** Allow skip with warning

---

## Next Steps

### For faintech-frontend

1. Verify backend APIs exist (coordinate with faintech-backend)
2. Implement agent creation step (P1-A)
3. Convert memory draft to API call (P1-B)
4. Add search memory step (P1-C)
5. Update success step with metrics (P1-D)
6. Test complete flow
7. Submit PR for review

### For faintech-backend

1. Verify `/api/agents` endpoint exists
2. Verify `/api/memories` endpoint exists
3. Verify `/api/memories/search` endpoint exists
4. Ensure semantic search is working
5. Test performance (<2s response time)

### For qa

1. Test complete onboarding flow
2. Verify all API integrations
3. Test error handling
4. Test state persistence
5. Test mobile responsiveness

---

## Questions for Engineering

1. **Backend API Status:** Do the required API endpoints (`/api/agents`, `/api/memories`, `/api/memories/search`) currently exist? If not, what's the timeline for creating them?

2. **Search Implementation:** Is semantic search (embeddings-based) currently implemented in the backend, or is it keyword-based? This affects the search pre-population strategy.

3. **State Persistence:** Should we sync onboarding progress to the backend in addition to localStorage, or is localStorage sufficient for the MVP?

4. **Error Handling:** What's the preferred error handling pattern for API failures in this codebase? Should we use toast notifications or inline error messages?

5. **Performance Targets:** Are the current API response times acceptable (<500ms for agent creation, <600ms for memory creation, <800ms for search)?

---

**Status:** READY FOR IMPLEMENTATION
**Handoff Date:** 2026-03-31 17:45 EET
**Target Completion:** April 2, 18:00 EET
**Week 2 GTM Launch:** April 3, 2026

---

**References:**
- Design spec: `/Users/eduardgridan/faintech-lab/docs/design/onboarding-flow-first-run-spec.md`
- Engineering clarification: `/Users/eduardgridan/faintech-lab/docs/design/onboarding-flow-engineering-clarification.md`
- Search memory spec: `/Users/eduardgridan/faintech-lab/docs/design/search-memory-step-spec.md`
- Current implementation: `/Users/eduardgridan/faintech-lab/amc-frontend/src/components/OnboardingFlow.tsx`
