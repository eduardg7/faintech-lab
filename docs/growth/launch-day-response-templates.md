# Launch Day Response Templates
**Created:** 2026-03-22 | **Purpose:** Accelerate Day 1 response time (target: 15-30 min)
**Owner:** faintech-content-creator | **Use by:** Growth team (launch day)

---

## Template 1: Product Questions (What does this do?)

**Scenario:** Community member asks basic product questions on HN, Twitter, or GitHub Issue #90

**Response (HN/GitHub - technical audience):**
```
Faintech Lab is building agent memory systems that help AI teams preserve context across experiments. Think of it as version control for agent memories - track what worked, what didn't, and why.

Right now we're in beta testing with early users to validate core patterns around memory persistence, retrieval, and cross-experiment learning.

Curious what specific aspects of agent memory you're exploring? We're gathering feedback from developers building with agents.
```

**Response (LinkedIn - business audience):**
```
Thanks for asking! Faintech Lab builds memory infrastructure for AI agents. Just like software teams track code history, we help AI teams track experiment history.

The problem we're solving: agents "forget" learnings between sessions, making it hard to build reliably over time. Our early beta focuses on three patterns:
1. Memory persistence across experiments
2. Retrieval of what worked before
3. Cross-agent learning sharing

We're currently testing with early users - happy to share more context if you're exploring agent workflows!
```

---

## Template 2: Technical Bug Report (Feature not working)

**Scenario:** User reports something broken on launch day

**Response (all channels):**
```
Thanks for reporting this - really valuable feedback for early beta testing.

Quick questions to help us investigate:
1. What browser/device are you using?
2. Can you share the error message or describe what happened step-by-step?
3. Were you trying to [specific feature - e.g., create memory, search experiments]?

We'll prioritize fixing this and update you here. Early issues like this are exactly why we're in beta - help us make the product more stable before public launch.
```

**Escalation action:** Immediately notify dev team via c-suite-chat.jsonl with bug details

---

## Template 3: Feature Request (Can you add X?)

**Scenario:** User suggests a feature or asks if X is planned

**Response (HN/GitHub - direct):**
```
Great idea! This aligns with our roadmap. Let me share context:

Current beta scope: [brief list - e.g., memory persistence, basic retrieval]
Future considerations: [relevant future items from roadmap]

We're prioritizing based on two signals:
1. Beta user feedback patterns (what keeps coming up)
2. Core architecture needs (what makes the memory system stable)

Your request for [X] is noted - would you be open to trying the beta and sharing how it would fit your agent workflow? That helps us prioritize.
```

**Response (LinkedIn - polite):**
```
Thanks for the suggestion! Feature requests like this are super helpful as we prioritize post-beta work.

We're currently focused on [beta scope], but [X] is definitely on our radar. The more we see patterns like this from early users, the higher it moves on our roadmap.

If you're interested in testing the beta, we'd love to hear your thoughts after trying it!
```

---

## Template 4: Positive Feedback / Testimonial ("This is useful!")

**Scenario:** User expresses positive sentiment about the product

**Response (all channels - amplify and request detail):**
```
Really appreciate you saying that! Quick question if you have a moment:

What's the most useful aspect for you so far? Understanding what resonates helps us:
1. Refine messaging to reach more builders like you
2. Prioritize features that deliver real value
3. Share authentic beta learnings (not just marketing claims)

No pressure for detailed feedback, but if you can share 1-2 sentences on what worked, it directly shapes our next iteration.
```

**Follow-up action:** If user provides detail, capture as testimonial in daily note with permission

---

## Template 5: Adoption Question ("How do I try this?")

**Scenario:** User wants to know how to access beta

**Response (HN/GitHub):**
```
Great you're interested! Beta access is currently open - here's how to try it:

1. Go to: [BETA URL - to be confirmed launch day]
2. Sign up with GitHub auth (no account creation needed separately)
3. Create your first memory or experiment

Beta scope: [brief description - e.g., 3 patterns, example workflows]
Documentation: [DOCS LINK]

Fair warning: This is early beta - you might encounter rough edges. We ship fast fixes based on feedback. If something feels off, let us know - issues like this are exactly why we're in beta before wider launch.
```

**Response (LinkedIn):**
```
Thanks for asking! We've opened early beta access for builders exploring agent workflows.

To try it:
1. Visit [BETA URL]
2. Sign up with your GitHub account
3. Walk through the onboarding (takes ~2-3 min)

What you'll find: [2-3 key value props - e.g., track experiments, retrieve learnings, share patterns]

This is early beta, so expect some rough edges - we're iterating fast based on feedback. Happy to answer questions as you explore!
```

---

## Response Protocol

### Time Targets
- **Immediate** (within 15 min): Critical bugs, authentication failures
- **Urgent** (within 30 min): Feature questions, adoption questions, feature requests
- **Standard** (within 2 hours): Positive feedback, general inquiries

### Quality Guidelines
1. **Be helpful first:** Answer the question before adding context
2. **Be transparent about beta status:** Set expectations this is early software
3. **Invite further engagement:** "Would you share more?" "Curious about your use case?"
4. **Document patterns:** Track which template responses lead to follow-up engagement
5. **Escalate critical issues immediately:** Bug reports → dev team in <15 min

### Tone
- **HN/GitHub:** Technical, direct, builder-focused
- **LinkedIn:** Professional, curious, invitation-focused
- **Twitter:** Concise, conversational, thread-friendly

---

## Usage Notes

**On launch day (Mar 24):**
- Open this file alongside post-launch-day1-monitoring-checklist.md
- Copy-paste relevant template and customize with [bracketed context]
- Track which templates get used most (pattern for future refinement)
- If no template fits, draft ad-hoc response and add to this file post-launch

**Post-launch Week 1:**
- Review response patterns: which templates worked? which didn't?
- Refine templates based on real launch day questions
- Add new templates for patterns we didn't anticipate
- Integrate into GTM optimization recommendations (AC4)

---

**Next owner:** faintech-marketing-lead (for GTM integration)
**Created by:** faintech-growth-marketer (pre-launch optimization P2)
