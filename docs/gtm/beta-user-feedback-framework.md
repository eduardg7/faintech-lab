# Beta User Feedback Collection Framework

**Created:** 2026-03-20 05:10 EET
**Owner:** faintech-user-researcher
**Purpose:** Structured user evidence collection during AMC beta period (Mar 24 - Apr 14)
**Target:** 5-12 Tier 1 + 20-50 Tier 2 beta users

---

## 1. Feedback Collection Methods

### 1.1 Onboarding Survey (Day 0)
**Trigger:** User accepts beta invitation
**Channel:** Email (Typeform link or in-app)
**Questions:**
1. What type of multi-agent system are you building? (open text)
2. What's your current memory solution? (options: None, Vector DB, Custom, LangChain Memory, Other)
3. What's your biggest pain point with agent memory today? (open text)
4. How many agents in your system? (options: 1-5, 6-20, 21-50, 50+)
5. What's your technical stack? (options: Python, TypeScript, Node.js, Go, Other)

**Evidence target:** 80%+ completion rate, user segmentation data

### 1.2 First-Week Check-in (Day 3-5)
**Trigger:** User completes onboarding
**Channel:** Email + in-app prompt
**Questions:**
1. Did you successfully create your first memory? (yes/no)
2. How long did it take to get value from AMC? (options: <1 hour, 1-4 hours, 1 day, >1 day, haven't yet)
3. What was confusing about the onboarding? (open text)
4. What feature do you wish existed? (open text)
5. On a scale of 1-10, how likely are you to recommend AMC to a colleague? (NPS)

**Evidence target:** 70%+ response rate, friction points identified

### 1.3 Weekly Pulse Survey (Day 7, 14, 21)
**Trigger:** Weekly automated
**Channel:** Email (brief 3-question survey)
**Questions:**
1. How many memories has your system stored this week? (auto-collect if possible)
2. What's working well? (open text)
3. What's blocking you from using AMC more? (open text)

**Evidence target:** 50%+ response rate, usage patterns, blockers

### 1.4 Exit Interview (Day 21-28 or churn)
**Trigger:** User stops using AMC for 7+ days OR end of beta
**Channel:** 1:1 call (15-20 min) or async survey
**Questions:**
1. What made you decide to try AMC?
2. What did you expect vs. what you experienced?
3. Would you pay for this? If yes, how much? If no, why not?
4. What would make you a daily user?
5. Would you recommend AMC to a friend building agents?

**Evidence target:** 100% of churned users, 50%+ of active users

---

## 2. User Segmentation Framework

### 2.1 Segment by System Type
- **Single-agent developers:** Building one AI assistant
- **Multi-agent orchestrators:** 2-10 coordinated agents
- **Enterprise fleets:** 10+ agents in production
- **Researchers:** Experimenting with agent architectures

**Action:** Tag each user by segment in onboarding survey

### 2.2 Segment by Pain Point
- **Context drift sufferers:** Agents losing context mid-conversation
- **Memory searchers:** Need to find past decisions/actions
- **Compliance seekers:** Audit trails and memory governance
- **Performance optimizers:** Latency/cost issues with current memory

**Action:** Track pain points to prioritize feature roadmap

### 2.3 Segment by Engagement
- **Power users:** 10+ memories/day
- **Regular users:** 1-10 memories/day
- **Light users:** <1 memory/day
- **Churned:** No activity 7+ days

**Action:** Weekly cohort analysis by engagement level

---

## 3. Evidence Collection Targets

### Quantitative Evidence
| Metric | Week 1 Target | Week 4 Target | Collection Method |
|--------|---------------|---------------|-------------------|
| Memories created | 50+ | 500+ | Auto-collect |
| Users active daily | 50%+ | 40%+ | Auto-collect |
| NPS score | 8+ | 8+ | Survey |
| Onboarding completion | 80%+ | 85%+ | Funnel tracking |
| Feature requests | 10+ | 30+ | Survey + in-app |

### Qualitative Evidence
| Evidence Type | Target | Collection Method |
|---------------|--------|-------------------|
| User quotes | 20+ | Survey + interviews |
| Friction points | 10+ | Onboarding + weekly pulse |
| Feature requests | 30+ | All channels |
| Success stories | 5+ | Exit interviews |
| Churn reasons | 100% of churn | Exit interviews |

---

## 4. Interview Question Bank

### 4.1 Technical Deep-Dive Questions
- "Walk me through how your agents use memory today"
- "What happens when an agent forgets context?"
- "How do you search across past conversations?"
- "What's your current vector DB setup?"
- "How do you handle memory governance/compliance?"

### 4.2 Value Perception Questions
- "If AMC disappeared tomorrow, what would you miss most?"
- "What would you pay for this if it saved you 2 hours/week?"
- "How does AMC compare to LangChain Memory?"
- "What's the #1 thing that would make you recommend AMC?"

### 4.3 Roadmap Prioritization Questions
- "If you could have ONE feature next month, what would it be?"
- "What's missing from AMC that your current solution has?"
- "Would you use a team collaboration feature for shared memories?"
- "How important is self-hosting vs. cloud?"

---

## 5. Feedback Loop Integration

### 5.1 Weekly Synthesis
**Owner:** faintech-user-researcher
**Cadence:** Every Monday during beta
**Output:** User Evidence Digest (1-page summary)
**Distribution:** cpo, pm, cto

**Digest Structure:**
- Top 3 user quotes
- Top 3 friction points
- Top 3 feature requests
- Engagement metrics snapshot
- Segment insights

### 5.2 Sprint Planning Input
**Trigger:** Before each sprint planning session
**Output:** Prioritized user evidence packet
**Format:**
- Feature requests sorted by user demand
- Friction points sorted by impact
- Segment-specific needs

### 5.3 Beta Retrospective
**Trigger:** End of beta (Apr 14)
**Output:** Comprehensive User Research Report
**Sections:**
- User segmentation analysis
- Feature adoption patterns
- NPS trends
- Churn analysis
- Roadmap recommendations
- Pricing insights

---

## 6. Tools & Infrastructure

### Recommended Tools
- **Surveys:** Typeform or Google Forms
- **Interviews:** Cal.com for scheduling, Zoom for recording
- **Analysis:** Notion or Coda for evidence repository
- **Tracking:** AMC's own analytics + custom events

### Data Storage
- **Location:** `/Users/eduardgridan/faintech-lab/research/beta-user-evidence/`
- **Structure:**
  - `surveys/` - Raw survey responses
  - `interviews/` - Interview notes and transcripts
  - `analysis/` - Weekly digests and synthesis
  - `final-report/` - Beta retrospective

---

## 7. Success Criteria

### Evidence Quality Gates
- ✅ 80%+ onboarding survey completion
- ✅ 70%+ weekly pulse response rate
- ✅ 50%+ exit interview completion
- ✅ 20+ user quotes collected
- ✅ 30+ feature requests documented
- ✅ NPS ≥ 8

### Actionable Outcomes
- ✅ Top 3 friction points identified and addressed
- ✅ Roadmap priorities validated by user demand
- ✅ Pricing insights gathered for commercialization
- ✅ Segment-specific needs documented

---

## 8. Escalation Triggers

### P0 Escalation (Immediate)
- NPS drops below 6
- >30% churn in first week
- Critical bug reported by 3+ users

### P1 Escalation (Within 24h)
- <50% onboarding completion
- Major feature gap identified by 5+ users
- Security/privacy concern raised

### P2 Escalation (Weekly digest)
- Feature request pattern emerging
- Segment-specific needs identified
- Competitive insights gathered

---

**Next Action:** Activate framework upon Tier 1 list receipt (due Mar 21)
**Owner:** faintech-user-researcher
**Status:** READY FOR ACTIVATION
