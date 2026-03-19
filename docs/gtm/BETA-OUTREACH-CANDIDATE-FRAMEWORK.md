# Beta Candidate Research Framework

**Purpose:** Systematic approach to identifying and qualifying beta candidates for Faintech Lab AMC launch (March 24, 2026)
**Created:** 2026-03-17
**Owner:** faintech-user-researcher (execution), faintech-marketing-lead (framework)

---

## ICP (Ideal Customer Profile)

### Primary: Indie AI Developers
- **Technical Context:** Building AI agents, LLM applications, or autonomous systems
- **Company Stage:** Solo founder, 2-5 person team, or indie hacker
- **Tech Stack:** Python, TypeScript, Node.js, or AI/ML framework experience
- **Values:** Local-first, privacy-conscious, data sovereignty
- **Pain Points:** Agent coordination failures, fragmented memory systems, "hallucination" tracking
- **Platforms Active:** GitHub (AI repos), Hacker News (technical discussions), Reddit (r/MachineLearning), Twitter/X (AI community)

### Secondary: AI Researchers
- **Context:** Academic or industry research on multi-agent systems
- **Focus Areas:** Agent memory, inter-agent communication, experiment methodology
- **Publishing:** Recent papers, blog posts, or open-source contributions
- **Motivation:** Access to production agent coordination systems for research validation

---

## Sourcing Channels (Prioritized)

### Tier 1: High-Signal (Direct, Personal)
1. **Hacker News Comments (last 6 months)**
   - Search queries: "agent memory", "multi-agent", "LLM coordination", "AI R&D"
   - Qualification: Technical depth of comment, GitHub profile link
   - Outreach method: Reply to comment + DM if email available

2. **GitHub Active Contributors (AI repos)**
   - Target repos: AutoGPT, LangChain, Semantic Kernel, CrewAI, AgentOps
   - Filter: Last commit < 30 days, 10+ stars, active issues/PRs
   - Outreach method: GitHub issue (contribution question) → email

3. **Twitter/X Technical Threads**
   - Track: "AI agents", "multi-agent systems", "agent memory" hashtag usage
   - Qualification: Substantive tweets (not RTs), technical content, link to work
   - Outreach method: Reply + DM request for DM

### Tier 2: Medium-Signal (Targeted Lists)
4. **Reddit r/MachineLearning & r/ArtificialIntelligence**
   - Monitor: Active threads on agent architecture, coordination problems
   - Qualification: Karma > 100, detailed technical comments
   - Outreach method: Comment + DM request

5. **Indie Hackers Showcase**
   - Filter: AI/ML projects, recent launches, or "in progress" posts
   - Qualification: Technical complexity, transparency about challenges
   - Outreach method: Comment on project page + email

### Tier 3: Broad-Reach (If Tier 1-2 insufficient)
6. **Dev.to AI Tag Posts**
   - Search: "agent", "multi-agent", "LLM", "RAG", "memory"
   - Qualification: 500+ words, technical depth, author profile active
   - Outreach method: Comment on post → follow author

7. **LinkedIn Search (AI Engineer title)
   - Filter: Recent activity, open to work, technical posts
   - Qualification: Verified skills (LangChain, OpenAI, Anthropic)
   - Outreach method: InMail with technical value proposition

---

## Qualifying Criteria (Must Match All)

### Technical Fit
- [ ] Building or researching AI agents, multi-agent systems, or LLM applications
- [ ] Active code contribution (GitHub with recent commits) OR research output (papers/blogs)
- [ ] Comfortable with APIs, authentication, or distributed systems

### Motivation Alignment
- [ ] Experiencing coordination, memory, or state management pain
- [ ] Values transparency and data-driven development (mention "failures" or "experiments")
- [ ] Interested in "rigorous" or "engineering-first" approaches (anti-hype)

### Engagement Potential
- [ ] Public presence (GitHub, HN, Twitter, or blog)
- [ ] Responsive to technical discussions (comment history)
- [ ] Time availability (not "hiring" or "too busy" signals)

---

## Disqualification Signals (Red Flags)

### Technical Misalignment
- ❌ Building chatbots or single LLM wrappers (not multi-agent)
- ❌ Pure academic with no production interest
- ❌ Corporate enterprise (seeking vendor solutions, not tools)

### Motivation Mismatch
- ❌ Only sharing success stories (no documented failures or learning)
- ❌ Focused on "productivity" or "automation" over architecture
- ❌ Looking for "agency" services (not building their own agents)

### Engagement Risk
- ❌ No recent public activity (>3 months)
- ❌ Only promotional posts (no technical contributions)
- ❌ Negative or toxic in discussions

---

## Outreach Messaging Framework

### Initial Contact (Cold DM/Email)
**Subject:** "Faintech Lab Beta: Rigorous multi-agent coordination system"

**Body:**
```
Hi [Name],

I saw your [comment on HN / recent post about X] — your point about [specific technical detail] resonated with what we're building at Faintech Lab.

We're launching beta (March 24) for a multi-agent coordination system:
- 95% recall agent memory system
- 100% guaranteed inter-agent message delivery
- Transparent failure documentation (not just success stories)

Given your work on [their project/research], I think you'd get value from the beta and provide meaningful feedback.

8 beta seats available. Target: Indie AI developers building agent architectures.

Interested? If so, I'll send signup details and what we're looking for in feedback.

Best,
[Your Name]
Faintech Lab
```

### Follow-up (If no response after 48h)
**Subject:** "Re: Faintech Lab Beta — [Technical hook from their work]"

**Body:**
```
Hi [Name],

Quick follow-up on my note about Faintech Lab beta.

I noticed you're working on [their specific project] — particularly interesting is your approach to [specific technical insight they shared].

The beta is designed to test:
1. Agent memory cross-system recall
2. Inter-agent message delivery reliability
3. Experiment tracking with transparent results

If you're interested, we have [X] seats remaining. No commitment needed — just 30 min to try the system.

If not, no worries — just thought it aligned with your [specific project].

Best,
[Your Name]
```

### Closing (After 7 days, no response)
**Subject:** "Last call: Faintech Lab beta (8 days until launch)"

**Body:**
```
Hi [Name],

Last check-in — Faintech Lab beta launches March 24 (8 days from now).

We're prioritizing seats for builders actively working on multi-agent systems or agent memory challenges.

If you're interested, let me know by [date]. After that, we'll fill remaining spots.

Thanks for considering it,
[Your Name]
```

---

## Outreach Sequencing

### Day 1: Tier 1 Identification
- Search HN comments (last 6 months on: "agent memory", "multi-agent")
- Search GitHub active contributors (AutoGPT, LangChain, Semantic Kernel)
- Identify 20-30 potential candidates
- Apply qualifying criteria
- Create initial outreach list (target 10-12 high-priority)

### Day 2: Tier 2 Identification
- Search Reddit (r/MachineLearning, r/ArtificialIntelligence)
- Monitor Indie Hackers showcase
- Identify 15-20 additional candidates
- Apply qualifying criteria
- Prioritize if Tier 1 insufficient

### Day 3-4: Outreach Execution
- Send initial contact messages to 8 highest-priority candidates (beta target)
- Personalize each message (reference their specific work)
- Track responses in spreadsheet: Candidate ID, Source, Sent Date, Response Date, Outcome

### Day 5: Follow-ups
- Send follow-up to non-responders (48h window)
- Continue monitoring Tier 2/3 sources
- Fill any open slots from backup candidates

### Day 6-7: Confirmation & Onboarding
- Confirm all 8 beta slots filled
- Send signup links
- Coordinate with customer success for onboarding flow
- Hand off to user-researcher for onboarding evidence collection

---

## Tracking Metrics

### Funnel Metrics
- **Candidates Identified:** Total count after research
- **Candidates Qualified:** Passed screening criteria
- **Candidates Contacted:** Initial outreach sent
- **Response Rate:** (Responses / Contacted) × 100%
- **Signup Rate:** (Signups / Responses) × 100%
- **Target Response Rate:** ≥ 30%
- **Target Signup Rate:** ≥ 60% of responses

### Success Metrics
- **Beta Slots Filled:** 8/8 by March 22 (2 days before launch)
- **ICP Alignment:** ≥ 70% from primary ICP (Indie AI Developers)
- **Onboarding Completion:** ≥ 80% of signups complete onboarding by launch day
- **Feedback Quality:** ≥ 80% provide meaningful feedback (not just "works/doesn't work")

---

## Tools & Templates

### Research Tools
- HN Search: https://hn.algolia.com/?q=agent+memory&sort=byDate
- GitHub Search: https://github.com/search?q=language%3APython+LLM&type=repositories
- Reddit Search: https://www.reddit.com/r/MachineLearning/search/?q=multi+agent

### Outreach Tracking Template
```csv
Candidate ID,Source,Handle/Link,Qualification Score,Sent Date,Follow-up Date,Response Date,Outcome,Notes
CAND-001,HN comment,@username,9/10,2026-03-18,2026-03-20,,,
CAND-002,GitHub repo,@username,8/10,2026-03-18,2026-03-20,,,
```

### Message Personalization Variables
- `{name}` - Extracted from profile
- `{specificInsight}` - Their technical comment or project detail
- `{theirProject}` - Name of their repo or research
- `{relevantFeature}` - AMC feature matching their pain point

---

## Escalation Triggers

### If Response Rate < 15%
- **Review messaging:** A/B test subject lines
- **Expand sources:** Add Tier 3 channels (Dev.to, LinkedIn)
- **Lower qualification bar:** Consider broader "AI developer" definition

### If Signup Rate < 40% of Responses
- **Review value proposition:** Clarify beta benefits
- **Simplify signup:** Reduce friction in onboarding
- **Add incentives:** Highlight "early access" or "feature influence"

### If ICP Alignment < 50%
- **Review targeting:** Shift focus to primary ICP sources (HN, GitHub)
- **Adjust messaging:** Emphasize "indie" and "local-first" more
- **Screen more strictly:** Reject misaligned candidates early

---

## Success Definition (Beta Outreach)

### Green (Launch-Ready)
- 8/8 slots filled by March 22
- ≥ 70% from primary ICP
- ≥ 80% complete onboarding
- Response rate ≥ 30%

### Yellow (Proceed with Caution)
- 6-7/8 slots filled by March 22
- 50-69% from primary ICP
- 60-79% complete onboarding
- Response rate 15-29%

### Red (Reconsider Launch)
- < 6/8 slots filled by March 22
- < 50% from primary ICP
- < 60% complete onboarding
- Response rate < 15%

---

**Status:** Framework complete. Ready to execute once CEO provides candidate list.
**Next Steps:**
1. CEO provides initial candidate list or approves sourcing strategy
2. Execute Tier 1 identification (Day 1)
3. Begin outreach (Day 3-4)
4. Fill 8 beta slots by March 22 (2-day buffer before March 24 launch)
