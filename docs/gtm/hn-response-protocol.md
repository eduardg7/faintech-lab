# HN Launch Response Protocol
**Created:** March 27, 2026
**Owner:** social (monitoring and engagement)
**Context:** Hacker News launch scheduled April 1, 17:00 EET

---

## Response SLAs

### Critical Priority (0-30 minutes)
- **First Comment:** Founder posts immediately after submission appears on HN
- **Clarification Questions:** Technical questions that block understanding (e.g., "What does persistent memory mean?")
- **Moderation Issues:** Post doesn't appear, is flagged, or removed

### High Priority (2 hours)
- **Architecture Questions:** System design, scalability, technical implementation details
- **Privacy/Compliance Questions:** GDPR, data residency, EU hosting details
- **Open Source Inquiries:** GitHub repo links, contribution guidelines
- **Bug Reports:** If someone reports a technical issue with the demo

### Standard Priority (4 hours)
- **Feature Requests:** New capabilities, integrations, improvements
- **Pricing Questions:** Cost breakdown, competitor comparisons
- **Use Case Inquiries:** How to use for specific scenarios
- **Competitive Comparisons**: vs Mem0, vs LangChain, vs custom solutions

### Low Priority (24 hours)
- **General Feedback:** UX impressions, general thoughts
- **Future Roadmap:** Feature suggestions for future iterations
- **Non-Technical**: Compliments, encouragement (thank them, no need to respond immediately)

---

## Question Categories & Response Templates

### Category A: Architecture & Technical Design

**Common Questions:**
- "How does the memory layer work technically?"
- "What's the vector search implementation?"
- "How do agents coordinate across memory?"
- "What database/tech stack are you using?"

**Response Template:**
```
Great question. The architecture is:

[Technical details - 2-3 sentences]

Key design decisions:
1. [Decision 1]: [Brief explanation]
2. [Decision 2]: [Brief explanation]
3. [Decision 3]: [Brief explanation]

Trade-offs we considered:
- [Alternative 1]: Rejected because [reason]
- [Alternative 2]: Considered but not implemented due to [reason]

Happy to dive deeper into specific aspects you're interested in.
```

### Category B: Privacy & GDPR

**Common Questions:**
- "How is user data protected?"
- "Is this GDPR compliant?"
- "Where is data hosted?"
- "Can I export/delete my data?"

**Response Template:**
```
Privacy is a core design principle. Here's our approach:

Data Residency:
- All data hosted in Frankfurt, Germany (EU)
- Compliant with GDPR Article 35 DPIA
- Verified EU hosting across 7 components (database, storage, logs, backups, cache, CDN, compute)

Data Controls:
- Automatic retention: 90 days for memories, 30 days for logs
- User can export all data via API
- User can delete all data with single API call
- No data sold to third parties

Legal Context:
- Full DPIA pre-consultation submitted to ANSPDCP (Romanian DPA)
- Production launch blocked until DPIA complete
- Beta proceeds with consent-based approach

Transparency:
- Open source memory API available on GitHub
- Public documentation of data flows
- No dark patterns or hidden data collection

Questions about specific aspects of privacy or GDPR compliance?
```

### Category C: Open Source & Contribution

**Common Questions:**
- "Is the code open source?"
- "How can I contribute?"
- "License?"
- "What parts are open source vs paid?"

**Response Template:**
```
We believe in open collaboration. Here's the open source breakdown:

Open Source (MIT License):
- Core memory API: https://github.com/eduardg7/faintech-lab/memory-api
- Agent coordination protocols: Public documentation
- Experiment schemas: Example configs in repo

Paid Service:
- Hosted platform (EU infrastructure, maintenance)
- Team collaboration features
- Advanced analytics and dashboards

Contribution:
- All contributions welcome via GitHub PRs
- Roadground prioritizes community-requested features
- We ship community-driven features weekly

Want to contribute? Check out [specific repo/issue] for good first issues.
```

### Category D: Pricing & Competition

**Common Questions:**
- "Why $49 vs Mem0's $249?"
- "What's included in pricing?"
- "Is there a free tier?"
- "How do costs compare to building it yourself?"

**Response Template:**
```
Transparent pricing breakdown is important. Here's ours:

Pricing ($49/mo for 1M tokens, 100K memories):
- EU hosting (Frankfurt): ~30% of cost
- Engineering team maintenance: ~50% of cost
- Platform operations & support: ~15% of cost
- Platform margin: ~5% of cost

Why cheaper than Mem0 ($249/mo):
- No VC funding: We're bootstrapped, not running on investor capital
- EU operations: Lower costs than US infrastructure
- Smaller team: Lean team vs larger funded companies
- Self-hostable: We offer open source if you want to run it yourself

Free Tier:
- Beta is currently free (testing & feedback phase)
- Production pricing applies after beta ends
- Academic/research discounts available

Competitive position:
- We win on: EU data residency, self-hosting option, transparent pricing
- Mem0 wins on: Larger team, more funding, feature breadth

Fair comparison?
```

### Category E: Use Cases & Applications

**Common Questions:**
- "What can I use this for?"
- "Can it replace LangChain?"
- "Good for [specific use case]?"
- "Does it work with [specific model/API]?"

**Response Template:**
```
Great question about use cases. Here's what we've tested and validated:

Primary Use Cases:
1. State persistence for long-running agent tasks
   - Example: Multi-step research agents maintaining context
   - Benefit: No state loss between API calls/LLM turns

2. Cross-agent knowledge sharing
   - Example: Research team agents collaborating on findings
   - Benefit: Shared memory space prevents redundant work

3. User interaction history
   - Example: Customer service agent remembering past conversations
   - Benefit: Contextual responses without full re-prompting

4. Agent workflow state management
   - Example: Multi-step process automation (e.g., research → draft → review)
   - Benefit: Each step can access previous step's outputs

Integration:
- Works with any LLM (OpenAI, Anthropic, local models)
- API-first: REST endpoints for any programming language
- Not replacing LangChain: Can be used as a memory backend FOR LangChain agents

For [specific use case mentioned]: Yes/no + specific guidance or alternative.
```

### Category F: Bug Reports & Technical Issues

**Common Questions:**
- "Demo is down / not working"
- "Getting error X"
- "Slow performance"

**Response Template:**
```
Thanks for reporting this - we'll investigate immediately.

If you can share:
- Error message or screenshot
- Browser/device you're using
- What you were trying to do

We're checking our logs now. For transparency, here's our status:
- [Current status: investigating / confirming / fixing / fixed]

Update timeline: We'll respond within 2 hours with resolution or workaround.

In the meantime:
- GitHub repo is working: https://github.com/eduardg7/faintech-lab
- API docs available at [link]

Apologies for the issue - help us make it better by reporting any other problems.
```

---

## Red Lines (What to Avoid)

### NEVER Do:
- Say "Check us out" or "we're live" (marketing, not technical substance)
- Get defensive about pricing, features, or technical choices
- Claim metrics we don't have ("thousands of users", "50% faster", etc.)
- Over-promise capabilities we don't have
- Dismiss technical questions as "not relevant"

### ALWAYS Do:
- Be transparent about beta status and limitations
- Provide code examples or links for technical questions
- Acknowledge trade-offs and design decisions honestly
- Invite collaboration and feedback
- Admit when we don't know something (then commit to finding out)
- Respond with technical depth, not brevity

---

## Escalation Protocol

### When to Escalate
- **Technical questions we can't answer:** Escalate to CTO/backend team
- **Security/compliance issues:** Escalate to CISO immediately
- **Bug reports requiring code changes:** Escalate to backend/dev team
- **PR/legal concerns:** Escalate to legal/CP immediately
- **Founder availability needed:** Page Eduard via preferred channel

### Escalation Format
```
[AGENT NAME] ESCALATION - [CATEGORY]

Question from HN:
[Question text]

Context:
[What we know, what we tried, what we don't know]

Request:
[What we need from team]

Timeline:
[Why this needs immediate attention]
```

### Escalation SLAs
- **CISO (Security):** Respond within 1 hour, resolve within 4 hours
- **CTO (Technical Architecture):** Respond within 2 hours, resolve within 8 hours
- **Backend/Dev (Bugs):** Respond within 2 hours, fix within 12 hours
- **Eduard (Founder):** Respond within 30 minutes for PR/legal

---

## Launch Day Monitoring Timeline

### T+0h to T+2h (Critical Phase)
- **Monitor:** HN post for new comments every 5 minutes
- **Respond:** All questions within 15 minutes
- **Focus:** Technical substance, not marketing
- **Document:** Track questions, responses, sentiment

### T+2h to T+24h (Engagement Phase)
- **Monitor:** HN post every 30 minutes
- **Respond:** All new comments within 2 hours
- **Analyze:** Comment themes, common questions, sentiment
- **Prepare:** Follow-up content for recurring topics

### T+24h to T+72h (Follow-up Phase)
- **Monitor:** HN post every 2 hours
- **Respond:** Remaining questions within 4 hours
- **Summarize:** Key insights, feedback, feature requests
- **Plan:** Next actions based on community response

---

## Metrics Tracking

### Real-Time Metrics (T+0h to T+24h)
- Upvotes count (track hourly)
- Comment count and themes
- Ranking position (top 30, top 10, front page)
- Site traffic (check Plausible every 15 min)
- Signups (check Mixpanel every 30 min)

### Post-Launch Analysis (T+72h)
- **Total Upvotes:** Target > 30 for success, > 100 for excellent
- **Total Comments:** Target > 10 for success, > 30 for excellent
- **Unique Visitors:** Target > 200 for success, > 500 for excellent
- **Signups:** Target > 5 for success, > 12 for excellent
- **Average Session Duration:** Target > 3 minutes (genuine interest)
- **Bounce Rate:** Target < 60% (staying to explore)
- **Top Questions:** Document recurring themes
- **Sentiment Analysis:** Positive/neutral/negative ratios

---

## Contingency Responses

### If Downvoted to 0 or Negative
```
Thanks for the feedback. We're beta-stage and learning fast.

What we got wrong:
- [Specific issues mentioned in comments]

What we'll fix:
- [Specific improvements based on feedback]

We're building for developers running agent systems - your input helps us get it right. Open to more feedback via GitHub issues or direct DM.
```

### If Post is Removed/Flagged
```
Our HN post seems to have been removed. We're reviewing:

- Community guidelines (no self-promotion, technical substance only)
- Title formatting (avoiding "Show HN" if problematic)
- Content substance (ensuring technical depth, not marketing)

If this was an error or we misunderstood guidelines, we'd appreciate guidance. Otherwise, we'll wait 7-10 days before reposting with revised content.

[Optional: Link to GitHub repo for those interested]
```

### If Traffic Overwhelms Site
```
We're seeing high traffic - thanks HN!

If site is slow/unavailable:
- GitHub repo is still accessible: https://github.com/eduardg7/faintech-lab
- API docs available at: [link]
- We're scaling infrastructure now - check back in 15-30 min

Thanks for your patience - we didn't expect this level of interest (good problem to have!).
```

### If Technical Questions Are Beyond Our Knowledge
```
That's a great question, and honestly, we don't have enough data/experience to answer it definitively.

Here's what we DO know:
- [What we know about the topic]

Here's what we DON'T know:
- [What we're uncertain about]

We'd love to hear from others who've tackled this: [invite community input]

In the meantime, we're researching this and will share what we learn. If you have insights or references, please share - we're all learning together here.
```

---

## Success Criteria

### Minimum Viable Launch
- 50+ upvotes (top 30 ranking)
- 10+ substantive comments
- 100+ visitors to site
- 1-2 signups

### Good Outcome
- 100+ upvotes (front page placement)
- 20+ substantive comments
- 300+ visitors to site
- 3-5 signups

### Excellent Outcome
- 200+ upvotes (sustained top 20 for 24h)
- 30+ substantive comments
- 500+ visitors to site
- 8-12 signups

---

## Owner Notes

- **Document created:** March 27, 2026
- **Purpose:** Ensure consistent, high-quality responses to HN community
- **Success metric:** Technical substance > brevity, transparency > defensiveness, speed matters
- **Next update:** After HN launch, incorporate learnings and refine protocols
