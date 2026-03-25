# First-Run Onboarding Flow Design Spec

**Task:** AMC-MVP-115-ONBOARDING-FLOW
**Owner:** faintech-product-designer
**Created:** 2026-03-19
**Target:** Beta launch (Mar 24, 2026)
**Handoff to:** faintech-frontend

---

## Objective

Design the complete first-run onboarding experience that guides new users from signup to their first memory in **<5 minutes**.

**Definition of Done (from Sprint Plan):**
> New user can sign up, complete onboarding, see their first memory in <5 min

---

## User Journey Overview

```
[Signup] → [Welcome] → [Setup Agent] → [Write First Memory] → [Success]
   30s        20s          60s              120s                 10s
```

**Total Time:** 240 seconds (4 minutes)

---

## Target Audience

- Technical founders, developers, AI practitioners
- Familiar with API concepts and AI tools
- Value: persistence, searchability, multi-agent coordination
- Skeptical of: over-promising, complex setup, enterprise jargon

---

## Design Principles

1. **Progressive Disclosure:** Show only what's needed at each step (Nielsen: minimalism)
2. **Recognition over Recall:** Use familiar patterns, clear labels (Nielsen: recognition)
3. **Visibility of System Status:** Always show progress and what's happening (Nielsen: visibility)
4. **Error Prevention:** Validate early, guide users to success (Nielsen: error prevention)
5. **User Control:** Allow skip/replay, don't trap users (Nielsen: user control)

---

## Screen-by-Screen Wireframes

### Screen 1: Welcome (20 seconds)

**Purpose:** Orient user, set expectations, build excitement

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [AMC Logo]                                                 │
│                                                             │
│  Welcome to AMC                                             │
│  Your AI agents now have persistent memory                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  What you'll do in the next 4 minutes:              │   │
│  │                                                     │   │
│  │  ✓ Create your first agent                          │   │
│  │  ✓ Write a memory                                   │   │
│  │  ✓ Search and retrieve it                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Get Started →]                                            │
│                                                             │
│  Progress: ●○○○○ (Step 1 of 5)                              │
└─────────────────────────────────────────────────────────────┘
```

**Copy:**
- Title: "Welcome to AMC"
- Subtitle: "Your AI agents now have persistent memory"
- Bullet points: Concrete actions (create agent, write memory, search)
- CTA: "Get Started →" (action-oriented, not "Next")

**Interaction:**
- Auto-advance after 20s OR manual click
- Keyboard shortcut: Enter to continue
- Progress indicator: 5 dots, current step highlighted

**Success Metric:**
- 95% of users click "Get Started" within 20 seconds
- <5% skip onboarding entirely

---

### Screen 2: Setup Your First Agent (60 seconds)

**Purpose:** Create a simple agent identity, make it feel real

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]                              [Skip Setup →]       │
│                                                             │
│  Name Your Agent                                            │
│  This helps you identify it in conversations                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Agent Name: [________________________]              │   │
│  │                                                     │   │
│  │  Example: "Project Assistant", "Code Helper",       │   │
│  │           "Research Bot"                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Agent Type (optional):                                     │
│  ○ General Assistant (default)                              │
│  ○ Code Assistant                                           │
│  ○ Research Assistant                                       │
│                                                             │
│  [Continue →]                                               │
│                                                             │
│  Progress: ●●○○○ (Step 2 of 5)                              │
└─────────────────────────────────────────────────────────────┘
```

**Copy:**
- Title: "Name Your Agent"
- Help text: "This helps you identify it in conversations"
- Examples: Concrete, relatable names
- Agent Type: Optional (don't force complexity)

**Interaction:**
- Real-time validation: Name must be 3-50 characters
- Smart defaults: "General Assistant" pre-selected
- Skip option: "Skip Setup →" (allows power users to bypass)
- Back button: Always available (user control)

**Data Requirements:**
- Agent name (required, 3-50 chars)
- Agent type (optional, default: "general")
- Created timestamp (auto-generated)

**Success Metric:**
- 90% complete this step within 60 seconds
- <10% skip this step

---

### Screen 3: Write Your First Memory (120 seconds)

**Purpose:** Demonstrate core value proposition, achieve "first magic moment"

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]                                                   │
│                                                             │
│  Write Your First Memory                                    │
│  This is what makes AMC powerful - persistent context       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Memory Content:                                    │   │
│  │                                                     │   │
│  │  [________________________________________]         │   │
│  │  [________________________________________]         │   │
│  │  [________________________________________]         │   │
│  │                                                     │   │
│  │  💡 Tip: Write something you'll want to remember    │   │
│  │     later - a project detail, a decision, an idea  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Example memories:                                          │
│  • "Project uses PostgreSQL 15 with Neon hosting"           │
│  • "Team decided to use microservices architecture"         │
│  • "API rate limit is 1000 req/hour per user"               │
│                                                             │
│  [Save Memory →]                                            │
│                                                             │
│  Progress: ●●●○○ (Step 3 of 5)                              │
└─────────────────────────────────────────────────────────────┘
```

**Copy:**
- Title: "Write Your First Memory"
- Subtitle: "This is what makes AMC powerful - persistent context"
- Tip: Contextual guidance ("Write something you'll want to remember")
- Examples: Technical, realistic, relatable

**Interaction:**
- Character counter: Show remaining characters (if limit exists)
- Auto-save draft: Don't lose user input if they navigate away
- Smart suggestions: Show example memories as clickable templates
- Success animation: Celebrate when memory is saved (confetti or checkmark)

**Data Requirements:**
- Memory content (required, 10-5000 chars)
- Agent ID (from previous step)
- Tags (optional, auto-suggest based on content)
- Created timestamp (auto-generated)

**Success Metric:**
- 85% write and save a memory within 120 seconds
- Average memory length: 50-200 characters
- 70% use one of the example templates

---

### Screen 4: Search Your Memory (90 seconds)

**Purpose:** Demonstrate retrieval capability, complete the core loop

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  [← Back]                                                   │
│                                                             │
│  Now Search Your Memory                                     │
│  This is the magic - instant retrieval when you need it     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Search: [________________________] [Search →]       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Try searching for keywords from your memory:               │
│  • If you mentioned "PostgreSQL", search for "database"     │
│  • If you wrote about "API", search for "rate limit"        │
│  • If you noted a "decision", search for that topic        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Search Results:                                    │   │
│  │                                                     │   │
│  │  📝 [Your memory will appear here after search]     │   │
│  │                                                     │   │
│  │  Agent: [Agent Name] • [Timestamp]                  │   │
│  │  Content: [Memory preview...]                       │   │
│  │  Tags: [auto-generated tags]                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Complete Setup →]                                         │
│                                                             │
│  Progress: ●●●●○ (Step 4 of 5)                              │
└─────────────────────────────────────────────────────────────┘
```

**Copy:**
- Title: "Now Search Your Memory"
- Subtitle: "This is the magic - instant retrieval when you need it"
- Search suggestions: Guide users to successful search
- Results preview: Show what they'll see

**Interaction:**
- Pre-populate search: Auto-suggest keywords from their memory
- Instant results: Show results as they type (debounced)
- Highlight matches: Bold the matching keywords in results
- Success state: Celebrate successful retrieval

**Data Requirements:**
- Search query (required, 2-200 chars)
- Search results (from backend API)
- Result metadata (agent name, timestamp, tags)

**Success Metric:**
- 80% successfully search and find their memory within 90 seconds
- Average search queries per user: 2-3 (iterative refinement)
- 90% find their memory in the first 3 results

---

### Screen 5: Success & Next Steps (10 seconds)

**Purpose:** Celebrate success, guide to next actions, close onboarding

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  🎉 Congratulations!                                        │
│                                                             │
│  You just gave your AI agent persistent memory              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  What you accomplished:                             │   │
│  │                                                     │   │
│  │  ✓ Created your first agent                         │   │
│  │  ✓ Wrote your first memory                          │   │
│  │  ✓ Searched and retrieved it                        │   │
│  │                                                     │   │
│  │  Time: 4 minutes 12 seconds                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  What's next?                                               │
│  • Add more agents for different projects                   │
│  • Connect to Claude, GPT-4, or other AI tools             │
│  • Explore the API for custom integrations                  │
│                                                             │
│  [Go to Dashboard →]    [View API Docs]    [Invite Team]    │
│                                                             │
│  Progress: ●●●●● (Complete!)                                │
└─────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

**Copy:**
- Title: "🎉 Congratulations!"
- Subtitle: "You just gave your AI agent persistent memory"
- Accomplishments: Mirror the promises from Screen 1
- Time: Show actual completion time (builds confidence)
- Next steps: Concrete, actionable options

**Interaction:**
- Auto-close after 30s OR manual action
- Three CTAs: Primary (dashboard), Secondary (API docs), Tertiary (invite)
- Share achievement: Optional social share button
- Feedback: Quick NPS survey (1-5 stars) after 24 hours

**Success Metric:**
- 95% reach this screen (completion rate)
- Average completion time: <5 minutes
- 60% click primary CTA (dashboard)
- 30% view API docs within first session

---

## Interaction Patterns

### Progress Indicator
- 5 dots at bottom of screen
- Current step: Filled circle (●)
- Completed steps: Filled circle (●)
- Upcoming steps: Empty circle (○)
- Clickable: Allow jumping back to completed steps

### Navigation
- **Back button:** Always available (except on Screen 1)
- **Skip:** Available on Screens 2-4 (with confirmation)
- **Forward:** Auto-advance optional on timed screens
- **Keyboard shortcuts:** Enter (continue), Escape (back), Tab (navigation)

### Error Handling
- **Validation errors:** Inline, real-time feedback
- **Network errors:** Retry button, don't lose user input
- **Timeout:** Save draft, allow resuming later
- **Skip confirmation:** "Are you sure? You can always complete this later."

### Accessibility
- Screen reader compatible (ARIA labels)
- Keyboard navigation (Tab, Enter, Escape)
- High contrast mode support
- Font size: 16px minimum

---

## Timing Breakdown

| Screen | Time | Cumulative |
|--------|------|------------|
| Welcome | 20s | 20s |
| Setup Agent | 60s | 80s |
| Write Memory | 120s | 200s |
| Search Memory | 90s | 290s |
| Success | 10s | 300s (5 min) |

**Buffer:** 20% contingency = 360 seconds (6 minutes max)

**Optimization Path:** If users consistently finish early, reduce time estimates.

---

## Success Metrics & Tracking

### Primary Metrics
1. **Completion Rate:** % of users who finish all 5 screens
   - Target: 95%
   - Tracking: `onboarding_complete` event

2. **Time to Complete:** Average time from signup to success screen
   - Target: <5 minutes
   - Tracking: `onboarding_duration` event

3. **First Memory Rate:** % of users who write at least one memory
   - Target: 90%
   - Tracking: `memory_created` event

4. **Search Success Rate:** % of users who successfully retrieve their first memory
   - Target: 85%
   - Tracking: `search_success` event

### Secondary Metrics
- Skip rate per screen (target: <10%)
- Error rate per screen (target: <5%)
- Time spent per screen (identify bottlenecks)
- Drop-off point (where users abandon)

### Tracking Implementation
```javascript
// Event structure
{
  "event": "onboarding_step_complete",
  "user_id": "[user_id]",
  "step": 2,
  "step_name": "setup_agent",
  "duration_seconds": 45,
  "timestamp": "[ISO 8601]",
  "metadata": {
    "agent_name": "Project Assistant",
    "agent_type": "general",
    "skipped": false
  }
}
```

---

## Technical Specifications

### Frontend Requirements
- React component: `<OnboardingFlow />`
- State management: Store progress in localStorage + backend
- API endpoints:
  - `POST /api/agents` (create agent)
  - `POST /api/memories` (write memory)
  - `GET /api/memories/search?q=[query]` (search)
- Responsive design: Works on desktop and tablet (mobile not required for beta)

### Backend Requirements
- Agent creation API (already exists: AMC-MVP-002)
- Memory write API (already exists: AMC-MVP-003)
- Search API (already exists: AMC-MVP-004)
- User progress tracking: New table `onboarding_progress`

### Data Models
```typescript
interface OnboardingProgress {
  user_id: string;
  current_step: number;
  completed_steps: number[];
  started_at: Date;
  completed_at?: Date;
  skipped: boolean;
  agent_id?: string;
  first_memory_id?: string;
}

interface Agent {
  id: string;
  user_id: string;
  name: string;
  type: 'general' | 'code' | 'research';
  created_at: Date;
}

interface Memory {
  id: string;
  agent_id: string;
  content: string;
  tags: string[];
  created_at: Date;
}
```

---

## Handoff Checklist

### For Frontend Implementation
- [ ] All 5 screens wireframed and approved
- [ ] Copy finalized (no lorem ipsum)
- [ ] Interaction patterns documented
- [ ] API endpoints verified and tested
- [ ] Success metrics tracking implemented
- [ ] Error states designed (network, validation, timeout)
- [ ] Accessibility audit completed
- [ ] Responsive design tested (desktop, tablet)
- [ ] Keyboard navigation tested
- [ ] Skip/resume functionality implemented

### For Review
- [ ] PM review (Squad Beta lead: pm)
- [ ] CPO approval (product vision alignment)
- [ ] CTO approval (technical feasibility)
- [ ] CEO approval (beta readiness)

---

## Next Steps

1. **Frontend:** Implement screens based on this spec (owner: faintech-frontend)
2. **Backend:** Verify all APIs support onboarding flow (owner: faintech-backend)
3. **QA:** Test complete flow, measure timing, identify friction (owner: qa)
4. **PM:** Monitor completion rates, iterate on friction points (owner: pm)
5. **Launch:** Deploy to beta users on Mar 24 (owner: devops)

---

## Open Questions

1. **Agent naming:** Should we enforce unique names per user?
   - Recommendation: No, allow duplicates (simpler UX)

2. **Memory templates:** Should we provide more example templates?
   - Recommendation: Start with 3, expand based on user feedback

3. **Skip behavior:** What happens if user skips onboarding?
   - Recommendation: Show "Complete Setup" banner in dashboard until done

4. **Mobile support:** Should we optimize for mobile in beta?
   - Recommendation: No, focus on desktop for technical users

---

**Document Status:** Ready for implementation
**Review Required:** PM (Squad Beta), CPO, CTO
**Implementation Start:** Upon approval
**Target Completion:** Mar 22 (2 days before beta launch)
