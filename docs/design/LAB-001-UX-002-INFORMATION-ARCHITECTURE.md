# Information Architecture - Agent Memory System

**Task:** LAB-001-UX-002
**Designer:** faintech-product-designer
**Date:** 2026-03-09
**Status:** DRAFT
**Related:** LAB-001-UX-001 (User Journey Map)

---

## Overview

This Information Architecture defines the hierarchical structure, categorization scheme, and navigation model for the Agent Memory System. It ensures operators can find, organize, and understand agent memories efficiently.

---

## Core Design Principles

1. **Mental Model Match** - Align with how operators think about agent work (projects → agents → tasks → outcomes)
2. **Scalability** - Support 1000+ memory entries without performance degradation
3. **Multi-Path Access** - Allow navigation via time, agent, task, type, or tags
4. **Semantic Clarity** - Category names should be self-explanatory without training
5. **Progressive Disclosure** - Show overview first, drill down on demand

---

## Primary Navigation Hierarchy

```
Mission Control (Root)
├── Projects (Namespace Filter)
│   ├── faintech-os (15 agents, 342 memories)
│   ├── faintrading (12 agents, 128 memories)
│   └── faintech-lab (4 agents, 67 memories)
├── Agents (List View)
│   ├── faintech-ceo
│   ├── faintech-cto
│   ├── faintech-cpo
│   └── ... (20+ agents)
├── Memories (Content View)
│   ├── Recent (last 24 hours)
│   ├── Search Results
│   └── Saved Filters
└── Analytics (Insights)
    ├── Performance Dashboard
    ├── Coaching Board
    └── System Health
```

---

## Memory Type Taxonomy

### Hierarchy Level 1: Primary Categories

| Category | Description | Icon | Color Badge |
|----------|-------------|-------|-------------|
| **Outcome** | Results, deliverables, completion evidence | ✅ | Green |
| **Learning** | Knowledge gained, patterns recognized | 🧠 | Blue |
| **Blocker** | Obstacles, failures, issues encountered | 🚧 | Red |
| **Success** | Wins, validated approaches, best practices | ⭐ | Gold |
| **Decision** | Choices made, tradeoffs considered | ⚖️ | Purple |
| **Preference** | Agent settings, operator preferences, configuration | ⚙️ | Gray |

### Hierarchy Level 2: Sub-Types

**Outcome Sub-Types:**
- `completed-task` - Task finished successfully
- `merged-pr` - Pull request merged to master
- `released-feature` - Feature deployed to production
- `delivered-milestone` - Milestone completed

**Learning Sub-Types:**
- `pattern-recognition` - Repeated issue identified
- `process-improvement` - Better way of working found
- `correction-applied` - Mistake fixed and learned from
- `knowledge-gap` - New information acquired

**Blocker Sub-Types:**
- `dependency-missing` - Waiting on another task
- `resource-unavailable` - Tool, API, or system down
- `permission-denied` - Access or auth issue
- `technical-failure` - Code, build, or deployment error

**Success Sub-Types:**
- `validated-approach` - Method proven to work
- `cost-optimization` - Resources or tokens saved
- `quality-improvement` - Bugs prevented, tests passed
- `velocity-increase` - Work completed faster

**Decision Sub-Types:**
- `architecture-choice` - Technical direction selected
- `priority-tradeoff` - Tasks ordered by importance
- `ownership-change` - Task reassigned to different agent
- `acceptance-refinement` - Criteria clarified or adjusted

**Preference Sub-Types:**
- `agent-config` - Model, temperature, tools enabled
- `human-preference` - Operator communication style, cadence
- `workflow-pattern` - Preferred way of working
- `notification-setting` - Alert frequency, channels

---

## Project Namespace Model

### Namespace Isolation
- Each project maintains separate memory namespace
- Cross-project search available via unified index
- Project badge visible on all memory entries

### Namespace Metadata

```typescript
interface ProjectNamespace {
  project_id: string;           // 'faintech-os', 'faintrading', 'faintech-lab'
  project_name: string;          // Display name
  agent_count: number;           // Active agents in project
  memory_count: number;          // Total memories in namespace
  last_activity: string;         // ISO 8601 timestamp
  owner: string;                // Project owner (faintech-pm)
  sla_profile: string;          // 'critical', 'hardening', 'standard'
}
```

### Multi-Project Search

**Unified Index:** All memories indexed across projects with project_id field

**Search Behavior:**
- Default: Search within selected project namespace
- Option: "All Projects" toggle for cross-namespace search
- Results: Grouped by project, sorted by relevance
- Badges: Show project icon/color for each result

**Use Case:** CTO agent reviewing team-wide patterns to identify systemic issues

---

## Tagging System

### Tag Categories (Controlled Vocabulary)

**Area Tags:**
- `security`, `finance`, `ops`, `dev`, `qa`, `devops`, `product`, `growth`
- Enforce: Only one area tag per memory

**Technology Tags:**
- `typescript`, `nextjs`, `fastapi`, `python`, `docker`, `k8s`, `github`
- Multi-select allowed

**Task-Type Tags:**
- `planning`, `execution`, `review`, `deployment`, `monitoring`, `research`
- Multi-select allowed

**Outcome Tags:**
- `merged`, `rejected`, `reopened`, `approved`, `escalated`
- Single-select, mutually exclusive

**Custom Tags:**
- Free-form for project-specific needs
- Maximum: 5 custom tags per memory
- Suggested: System auto-recommends based on content analysis

### Tag Hierarchy

```
Area (1 required)
├── Technology (0-3 optional)
├── Task-Type (0-2 optional)
├── Outcome (0-1 optional)
└── Custom (0-5 optional)
```

### Tag Suggestion Algorithm

**Auto-Suggest on Memory Write:**
1. Extract keywords from memory content
2. Match against controlled vocabulary
3. Suggest top 3 candidates per category
4. Human accepts/edits before save

**Example:**
```
Memory: "Fixed JWT auth bug in cost tracking API"
Suggested Tags:
  - Area: security
  - Technology: typescript, fastapi
  - Task-Type: execution, review
  - Outcome: merged
```

---

## Memory Schema Definition

### Core Fields (Required)

```typescript
interface MemoryEntry {
  // Identification
  id: string;                  // UUID v4
  timestamp: string;            // ISO 8601 (2026-03-09T14:00:00Z)

  // Namespace
  project_id: string;           // 'faintech-os', 'faintrading', 'faintech-lab'
  agent_id: string;             // 'faintech-cto', 'faintech-dev', etc.

  // Classification
  type: 'outcome' | 'learning' | 'blocker' | 'success' | 'decision' | 'preference';
  subtype?: string;             // From controlled vocabulary (e.g., 'completed-task')
  importance: 1-5;           // 5 = critical, 1 = trivial

  // Content
  content: string;              // Markdown, max 2000 chars recommended
  tags: string[];               // Tag hierarchy enforced

  // Metadata
  task_id?: string;            // Optional: Related task identifier
  session_id?: string;         // Optional: Session that generated memory
  related_memories?: string[]; // IDs of linked memories

  // Lifecycle
  resolved?: boolean;           // True if blocker/issue is fixed
  archived?: boolean;           // True if compressed to long-term storage
  created_at: string;          // ISO 8601
  updated_at: string;          // ISO 8601
}
```

### Indexing Strategy

**Primary Indexes:**
- `by_timestamp` - Recent-first view
- `by_agent` - Filter by specific agent
- `by_project` - Namespace isolation
- `by_type` - Outcome/learning/blocker filtering
- `by_importance` - High-importance prioritization

**Secondary Indexes:**
- `by_tag` - Tag-based search
- `by_task` - Task-related memories
- `by_importance_and_timestamp` - Sorted by (importance DESC, timestamp DESC)

**Full-Text Search:**
- Content indexed with BM25 ranking
- Supports substring, phrase, and proximity queries
- Highlights matches in result preview

---

## View States and Information Layout

### View 1: Recent Memories (Default)

**Layout:**
- Left sidebar: Filters (Project, Agent, Type, Tags, Importance)
- Main content: Memory cards (reverse-chronological)
- Top bar: Search, saved filters toggle, "All Projects" toggle

**Card Structure:**
```
┌─────────────────────────────────────────────┐
│ [Badge: outcome] [Badge: faintech-os] │
│ ✅ Completed task FT-SEC-001            │
│ [Icon: faintech-ciso] 2h ago        │
│ Tags: security, review, merged          │
│ Importance: ⭐⭐⭐⭐⭐ (4/5)        │
│                                       │
│ Click to expand full content →           │
└─────────────────────────────────────────────┘
```

### View 2: Search Results

**Layout:**
- Same as Recent, but sorted by relevance
- Search query visible in top bar
- Result count: "42 memories found"
- Empty state: "No memories match 'JWT auth bug'"

**Sorting Options:**
- Relevance (default)
- Most recent
- Highest importance
- Most related (by tags)

### View 3: Memory Detail (Drill-Down)

**Layout:**
- Left: Memory content with full formatting
- Right: Related memories, timeline view, action menu

**Content Sections:**
```markdown
## ✅ Completed task FT-SEC-001

**Agent:** faintech-ciso
**Time:** 2026-03-09T14:00:00Z
**Importance:** ⭐⭐⭐⭐⭐

### Details
[Full content in Markdown...]

### Tags
security, review, merged, typescript, fastapi

### Related Memories
- [LRN-20250215-003] Pattern: JWT auth requires role check
- [BLK-20250210-001] Blocker: JWT middleware not applied

### Actions
[Create Task] [Promote to Shared] [Archive] [Edit Tags]
```

### View 4: Timeline Visualization

**Layout:**
- X-axis: Time (last 7 days, 30 days, custom)
- Y-axis: Activity (memory count)
- Clickable bubbles: Show memory summary on hover

**Visual Encoding:**
- Bubble color: Memory type (green=outcome, blue=learning, red=blocker)
- Bubble size: Importance (larger = higher importance)
- Opacity: Recency (more opaque = recent)

**Interaction:**
- Click bubble: Open memory detail
- Drag on timeline: Zoom in/out
- Legend toggle: Show/hide specific memory types

---

## Saved Filters and Search Presets

### Pre-Built Presets

| Preset Name | Filters | Use Case |
|--------------|----------|-----------|
| **Critical Issues** | Type=blocker, Importance=5 | Debug urgent problems |
| **My Mistakes** | Agent=[current], Type=blocker | Self-correction review |
| **Team Learnings** | Type=learning, Importance≥4 | Weekly team sync |
| **Recent Activity** | Time=last 24h, All Types | Morning catch-up |
| **Cross-Project Issues** | Type=blocker, All Projects | Systemic problem scan |

### User-Defined Saved Filters

**Creation:**
1. Apply filters in sidebar
2. Click "Save Filter" button
3. Name the filter (e.g., "Security blockers this week")
4. Option: Set as default view

**Management:**
- "Saved Filters" dropdown in top bar
- Edit/delete filters
- Reorder by drag-and-drop
- Share with team (future feature)

---

## Empty States

### Empty State 1: No Memories in Project

**Message:** "No memories yet in [Project Name]. Start by enabling automatic memory capture for agents."

**Actions:**
- [Enable Memory Capture] [View Documentation]

**Visual:** Illustration of empty memory timeline with plus button

---

### Empty State 2: No Search Results

**Message:** "No memories match '[search query]'"

**Suggestions:**
- Try different keywords
- Check spelling
- Clear filters
- Search across all projects

**Actions:**
- [Clear Filters] [Search All Projects]

---

### Empty State 3: No Agent Activity

**Message:** "[Agent Name] hasn't written any memories yet"

**Context:** Agent initialized but no task completed

**Actions:**
- [View Agent Profile] [Check Task Status]

---

## Accessibility Considerations

### Keyboard Navigation

- `Cmd/Ctrl + K`: Focus search bar
- `Cmd/Ctrl + F`: Filter by agent name
- `Cmd/Ctrl + L`: Filter by memory type
- `Cmd/Ctrl + T`: Focus tag selector
- `Arrow keys`: Navigate memory list
- `Enter`: Open selected memory detail
- `Escape`: Close modal/dialog

### Screen Reader Support

- Semantic HTML: `<main>`, `<nav>`, `<aside>` landmarks
- ARIA labels: All filters, buttons, interactive elements
- Live regions: Search results, filter updates announced
- Focus management: Modal open/close traps focus

### Color Contrast

- WCAG AA: 4.5:1 contrast ratio minimum
- Badges: Use icons + color (don't rely on color alone)
- High-contrast mode: Support dark/light theme with toggle

---

## Performance Requirements

### Load Time Targets

- Initial view render: < 500ms p95
- Search results: < 300ms p95 (for 1000 memories)
- Memory detail view: < 200ms p95
- Timeline visualization: < 400ms p95 (for 7 days)

### Indexing Strategy

- In-memory cache: Last 100 memories for instant access
- Lazy loading: Infinite scroll, load 50 memories per batch
- Debounced search: 300ms delay after keystroke before query

---

## Success Metrics

**Quantitative:**
- Memory search success rate: >95% (user finds relevant memory)
- Average search time: < 30 seconds end-to-end
- Saved filter adoption: 3+ filters created by active users
- Cross-project search usage: 20% of searches span multiple projects

**Qualitative:**
- Operators can debug agent mistakes without reading logs
- New agents onboard faster by reviewing team memories
- Team can identify systemic issues from memory patterns
- Memory system feels like an enabler, not overhead

---

## Future Enhancements (Phase 2)

1. **Semantic Search with Embeddings**
   - Vector similarity search beyond substring matching
   - "Find memories about authentication security" returns JWT-related entries

2. **Memory Clustering**
   - Auto-group related memories by topic
   - "5 memories about CI/CD failures" cluster

3. **Performance Analytics**
   - Agent improvement metrics over time
   - "faintech-dev reduced errors by 15% this month"

4. **Memory Recommendations**
   - "Based on this blocker, see these 3 related learnings"
   - Proactive surfacing during task execution

---

**Document Status:** DRAFT
**Related:** LAB-001-UX-001 (User Journey Map)
**Next:** LAB-001-UX-003 (Interaction Flows - Memory CRUD Operations)
**Updated:** 2026-03-09T13:58:00Z
