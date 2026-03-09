# User Journey Map - Agent Memory System UX

**Task:** LAB-001-UX-001  
**Designer:** faintech-product-designer  
**Date:** 2026-03-09  
**Status:** DRAFT - Section 1 of 10

## Overview

This user journey map defines how **agent operators** interact with the Agent Memory System to view, search, and manage agent memories across Faintech projects.

---

## User Personas

### Primary Persona: Agent Operator (Eduard)
- **Role:** Founder/Operator managing multiple AI agents
- **Goals:** 
  - Monitor agent learning and decision-making patterns
  - Debug agent behavior by reviewing past experiences
  - Optimize agent coordination by identifying repeated mistakes
  - Ensure agents are improving over time
- **Context:** Runs 15+ agents across 3 projects (faintech-os, faintrading, faintech-lab)
- **Pain Points:**
  - Agents sometimes repeat mistakes from previous sessions
  - No visibility into what agents have learned
  - Difficult to debug why an agent made a specific decision
  - Manual effort to transfer knowledge between similar agents

### Secondary Persona: CTO Agent (Automated Operator)
- **Role:** Automated agent monitoring team performance
- **Goals:**
  - Identify patterns in agent mistakes across the team
  - Recommend process improvements based on memory analysis
  - Coordinate knowledge sharing between agents
- **Context:** Runs in autonomous cycles, reads team-wide memories
- **Pain Points:**
  - No structured way to aggregate team learnings
  - Difficulty identifying which agents need coaching
  - No clear handoff protocol for memory-based insights

---

## User Journey: Memory Review Flow

### Stage 1: Discovery (Awareness)

**Trigger:** Agent completes task or encounters blocker

**User Actions:**
1. Agent writes memory entry (automatic on task completion)
   - Type: `outcome`, `learning`, `blocker`, `success`
   - Tags: task-relevant keywords
   - Importance: auto-rated 1-5

**Touchpoints:**
- Agent initialization (memory write happens automatically)
- Task completion hooks
- Error recovery flows

**Emotional State:** Neutral (automated process)

**Opportunities:**
- ✅ Already implemented: Auto-write on task completion
- 🔧 Enhancement: Proactive notification when high-importance memory written
- 🔧 Enhancement: Weekly digest email summarizing key learnings

---

### Stage 2: Search & Retrieval (Consideration)

**Trigger:** Operator needs to understand agent behavior or debug issue

**User Actions:**
1. Navigate to Memory Dashboard (Mission Control)
2. Select project namespace (faintech-os, faintrading, faintech-lab)
3. Apply filters:
   - By agent (e.g., faintech-cpo, faintech-dev)
   - By task (e.g., FT-ANAL-001, LAB-001)
   - By type (outcome, learning, blocker)
   - By tags (e.g., security, testing, ci)
   - By date range (last 7 days, last 30 days, custom)
   - By importance (4-5 only, all)
4. Review filtered memory entries

**Touchpoints:**
- Mission Control dashboard widget
- Memory list view with search bar
- Filter panel (left sidebar)
- Search results with highlighted matches

**Emotional State:** Curious, task-focused, potentially frustrated if search is slow

**Pain Points:**
- No semantic search (substring only in MVP)
- Can't search across all projects simultaneously
- No saved searches or filters
- Large result sets (>100 entries) not paginated

**Opportunities:**
- 🔧 Enhancement: Saved search presets (e.g., "My mistakes this week")
- 🔧 Enhancement: Cross-project search with project badges
- 🔧 Enhancement: Pagination and infinite scroll for large result sets
- 🔧 Enhancement: Semantic search with embeddings (Phase 2)

---

### Stage 3: Analysis (Evaluation)

**Trigger:** Operator finds relevant memory entries

**User Actions:**
1. Click memory entry to expand detail view
2. Review full content, metadata, tags
3. Identify patterns:
   - Repeated blockers across multiple tasks
   - Successful approaches to similar problems
   - Agent preferences and decision patterns
4. Cross-reference with related memories (same task, same tags)
5. Assess agent performance and improvement over time

**Touchpoints:**
- Memory detail card (expandable)
- Timeline visualization (memories over time)
- Related memories panel (right sidebar)
- Agent performance metrics widget

**Emotional State:** Analytical, potentially concerned if negative patterns emerge

**Pain Points:**
- No timeline view to visualize memory evolution
- Related memories not automatically linked
- No performance metrics (e.g., "Agent improved 15% this month")
- Can't annotate or add notes to existing memories

**Opportunities:**
- 🔧 Enhancement: Timeline view with memory density visualization
- 🔧 Enhancement: Auto-link related memories by tags/task
- 🔧 Enhancement: Agent performance dashboard with improvement metrics
- 🔧 Enhancement: Operator annotations on memories (meta-commentary)

---

### Stage 4: Action (Decision)

**Trigger:** Operator identifies actionable insight from memory analysis

**User Actions:**
1. **Option A: Direct Intervention**
   - Modify agent configuration based on memory insights
   - Update agent prompts or tool access
   - Escalate to human review (e.g., security concern)

2. **Option B: Knowledge Sharing**
   - Tag memory for team review
   - Promote learning to shared-learnings.md
   - Create task to address systemic issue

3. **Option C: Archive/Compress**
   - Mark old memories for compression
   - Delete irrelevant or incorrect memories
   - Tag as "resolved" to prevent future confusion

**Touchpoints:**
- Action menu on memory detail (3-dot menu)
- Promote to shared-learnings button
- Create task from memory button
- Archive/delete confirmation dialog

**Emotional State:** Decisive, empowered if actions are clear

**Pain Points:**
- No direct action path from memory to task creation
- Can't promote memory to shared-learnings from UI
- No "resolved" state to prevent re-analysis
- No bulk actions (archive multiple memories)

**Opportunities:**
- ✅ Core Feature: Create task from memory (auto-link task_id)
- 🔧 Enhancement: Promote to shared-learnings with one click
- 🔧 Enhancement: Bulk archive/select operations
- 🔧 Enhancement: "Resolved" tag to filter out fixed issues

---

### Stage 5: Retention (Loyalty)

**Trigger:** Operator returns to memory system regularly

**User Actions:**
1. Check weekly memory digest email
2. Review "Agent Coaching Board" for team-wide patterns
3. Monitor memory system performance metrics
4. Trust system to surface relevant insights automatically

**Touchpoints:**
- Weekly digest email (automated summary)
- Mission Control dashboard widget
- Agent Coaching Board (aggregated view)
- Performance metrics (storage, query latency)

**Emotional State:** Confident if system delivers value, skeptical if not

**Pain Points:**
- No automated digest (manual review required)
- Agent Coaching Board not yet implemented
- No visibility into memory system health
- Unclear ROI (time spent vs. insights gained)

**Opportunities:**
- 🔧 Enhancement: Weekly automated digest email
- 🔧 Enhancement: Agent Coaching Board dashboard
- 🔧 Enhancement: Memory system health metrics (storage, latency, hit rate)
- 🔧 Enhancement: ROI tracker (time saved, mistakes prevented)

---

## Critical User Flows

### Flow 1: Debug Agent Mistake
1. Operator notices agent made mistake (e.g., wrong branch name)
2. Opens Memory Dashboard, filters by agent + recent
3. Searches for related task or error message
4. Finds memory entry explaining agent's reasoning
5. Identifies root cause (e.g., outdated prompt, missing context)
6. **Action:** Updates agent prompt or creates corrective task
7. **Outcome:** Agent doesn't repeat mistake

**Success Metric:** Time from mistake to resolution < 10 minutes

---

### Flow 2: Review Team Learning
1. CTO agent runs weekly review cycle
2. Queries memories across all agents, last 7 days
3. Filters by type=learning, importance≥4
4. Identifies top 5 team-wide learnings
5. Promotes to shared-learnings.md
6. **Action:** Creates tasks to address systemic issues
7. **Outcome:** Team improves collective performance

**Success Metric:** 10%+ reduction in repeated mistakes month-over-month

---

### Flow 3: Onboard New Agent
1. New agent (e.g., faintech-qa) initialized
2. Loads last 30 days of memories for assigned projects
3. Reviews recent blockers and learnings
4. Identifies common pitfalls to avoid
5. **Action:** Adjusts initial approach based on team history
6. **Outcome:** Faster ramp-up, fewer early mistakes

**Success Metric:** New agent reaches baseline performance in < 3 cycles

---

## Friction Points to Address

### High Priority (P0)
1. **No semantic search** - Substring search misses related concepts
2. **No saved searches** - Repeat same filters every session
3. **No timeline view** - Can't visualize memory evolution over time
4. **No direct action path** - Can't create task from memory without context switching

### Medium Priority (P1)
5. **No cross-project search** - Must check each project separately
6. **No performance metrics** - Can't measure agent improvement
7. **No bulk operations** - Archive/delete requires individual actions
8. **No automated digest** - Manual review required every week

### Low Priority (P2)
9. **No annotations** - Can't add operator notes to memories
10. **No memory health dashboard** - Can't monitor system performance
11. **No ROI tracker** - Unclear value proposition
12. **No memory versioning** - Can't track edits to memory entries

---

## Next Steps

**Immediate (This Cycle):**
- ✅ Create this User Journey Map document
- 🔄 Create Information Architecture for memory types and hierarchy
- 🔄 Design interaction flows for memory CRUD operations

**Short-Term (Next 2 Cycles):**
- 📋 Specify visual hierarchy for list, detail, and search views
- 📋 Create component specifications (memory cards, filters, timeline)
- 📋 Design empty states and error states

**Medium-Term (Next Week):**
- 📋 Document accessibility requirements and design tokens
- 📋 Create responsive design specs for desktop/tablet/mobile
- 📋 Handoff to engineering with implementation notes

---

## Success Metrics

**Quantitative:**
- Time to find relevant memory: < 30 seconds (target)
- Memory search latency: < 100ms p99 (technical requirement)
- Weekly active users: 3+ agents + 1 human operator
- Repeated mistake reduction: 10%+ month-over-month

**Qualitative:**
- Operator can debug agent mistakes without reading logs
- Agents can onboard faster by reading team memories
- Team can identify systemic issues from memory patterns
- Memory system feels trustworthy and valuable, not overhead

---

## Appendix: Memory Entry Schema (Reference)

```typescript
interface MemoryEntry {
  timestamp: string;        // ISO 8601 (2026-03-09T13:49:00Z)
  agent_id: string;         // faintech-cpo, faintech-dev, etc.
  task_id: string;          // LAB-001, FT-ANAL-001, etc.
  project_id: string;       // faintech-os, faintrading, faintech-lab
  type: 'outcome' | 'learning' | 'preference' | 'decision' | 'blocker' | 'success';
  content: string;          // Max 1000 chars recommended
  tags: string[];           // ['security', 'testing', 'ci']
  metadata?: object;        // Optional structured data
  importance: 1-5;          // 5 = critical, 1 = trivial
}
```

**File Storage:** `~/.openclaw/memory/{project_id}/memory-{project_id}-{date}.jsonl`

---

**Document Status:** Section 2 of 10 complete  
**Next Section:** Interaction Flows - Memory CRUD Operations  
**Updated:** 2026-03-09T14:00:00Z  
**Progress:** ✅ Section 1 (User Journey), ✅ Section 2 (Information Architecture)
