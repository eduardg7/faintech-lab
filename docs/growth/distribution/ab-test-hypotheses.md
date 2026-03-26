# A/B Test Hypotheses - Post-Launch Distribution

**Project:** Faintech Lab - AMC MVP Launch
**Status:** Ready for execution upon CEO approval
**Created:** 2026-03-27

---

## Test Philosophy

We will test 2-3 key hypotheses per channel to identify messaging that resonates with our target audience (developers, technical founders, enterprise buyers).

**Success Criteria:**
- Statistical significance not required (small sample size)
- Directional signal > perfection
- Iterate rapidly based on feedback
- Focus on quality of engagement, not just vanity metrics

---

## Hypothesis 1: HN Title Variant Impact

**Question:** Which title structure drives higher upvotes and substantive comments?

### Variants

#### A. Technical Depth
*"Show HN: We built an AI memory system that remembers across conversations so agents don't forget context"*

**Hypothesis:** Technical specificity attracts higher quality developers who provide useful feedback.

#### B. Founder Story
*"Show HN: After 687 posts about agents forgetting context, we built Faintech Lab to fix it"*

**Hypothesis:** Narrative approach creates emotional connection, higher engagement.

#### C. Direct Value
*"Show HN: Faintech Lab - AI agents that remember across conversations (beta, open source)"*

**Hypothesis:** Clear value proposition converts better, shorter decision time.

### Success Metrics
| Variant | Upvotes (Target: 30+) | Comments (Target: 15+) | Substantive Comments | Signups |
|---------|------------------------|--------------------------|----------------------|----------|
| A (Technical) | | | | |
| B (Story) | | | | |
| C (Direct) | | | | |

### Duration
- **Test Window:** 24h (09:00-09:00 PST)
- **Decision:** Double down on best-performing variant for Day 2-3

---

## Hypothesis 2: Twitter Thread Length Impact

**Question:** Does 7-tweet thread perform better than 5-tweet thread?

### Variants

#### A. 7-Tweet Thread (Full Story)
- Structure: Hook → Problem → Solution → GIF → Architecture → Pricing → CTA
- **Hypothesis:** More content = higher engagement, but lower completion rate

#### B. 5-Tweet Thread (Technical Depth)
- Structure: Hook → GIF → Architecture → Pricing → CTA
- **Hypothesis:** Concise = higher completion rate, more focused engagement

### Success Metrics
| Variant | Impressions | Engagement Rate | Completion Rate | Signups |
|---------|-------------|------------------|------------------|----------|
| A (7 tweets) | | | | |
| B (5 tweets) | | | | |

### Duration
- **Test Window:** 24h (launch to next day same time)
- **Decision:** Use winning structure for Day 3-5 content

---

## Hypothesis 3: Twitter Content Focus Impact

**Question:** Does technical architecture thread attract higher quality users than founder journey?

### Variants

#### A. Technical Architecture Focus
- Content: Byte-rover implementation, graph vs vector, stack decisions
- **Hypothesis:** Attracts engineers who evaluate code, more likely to pay

#### B. Founder Journey Focus
- Content: Discovery → Prototype failure → Pivot → Launch → Vulnerability
- **Hypothesis:** Builds trust, emotional connection, broader audience

#### C. Use Case Showcase Focus
- Content: Real beta user story, before/after, concrete metrics
- **Hypothesis:** Practical application signals value to enterprise buyers

### Success Metrics
| Variant | Impressions | GitHub Stars | High-Quality Comments | Signups |
|---------|-------------|---------------|----------------------|----------|
| A (Technical) | | | | |
| B (Journey) | | | | |
| C (Use Case) | | | | |

### Duration
- **Test Window:** Day 3 (24h)
- **Decision:** Use top performer for Day 4-6

---

## Hypothesis 4: LinkedIn Headline Order Impact

**Question:** Does starting with problem or technical details drive more views?

### Variants

#### A. Problem First
*"After 687 HackerNews posts about AI agents forgetting context, we built a persistent memory system to fix it"*

**Hypothesis:** Problem statement captures attention faster, broader audience.

#### B. Technical First
*"Technical breakdown: How we built Faintech Lab's persistent memory graph and why it matters for enterprise AI"*

**Hypothesis:** Technical credibility attracts B2B decision-makers faster.

### Success Metrics
| Variant | Views | Scroll Depth | Connection Requests | Signups |
|---------|--------|--------------|-------------------|----------|
| A (Problem) | | | | |
| B (Technical) | | | | |

### Duration
- **Test Window:** 48h (Day 1-3)
- **Decision:** Use winning structure for LinkedIn follow-up posts

---

## Hypothesis 5: CTA Placement Impact

**Question:** Does explicit CTA at end of content increase conversion vs embedded CTAs?

### Variants

#### A. End CTA
- All CTAs at final paragraph
- **Hypothesis:** Readers consume full content before deciding, more informed signup

#### B. Embedded CTAs
- CTAs in 3 locations (intro, middle, end)
- **Hypothesis:** Multiple touchpoints capture fence-sitters, higher conversion

### Success Metrics
| Variant | Signups | Conversion Rate | Feedback on CTA Placement |
|---------|----------|-----------------|--------------------------|
| A (End) | | | |
| B (Embedded) | | | |

### Duration
- **Test Window:** Day 2-4 (72h)
- **Decision:** Use winning CTA strategy for all subsequent content

---

## Hypothesis 6: Pricing Transparency Impact

**Question:** Does transparent pricing explanation increase trust vs hiding pricing?

### Variants

#### A. Transparent Pricing
*"Beta: $49/mo for early adopters, $97/mo standard. Why? Real compute costs + small team bootstrapping."*

**Hypothesis:** Honesty builds trust, higher signups, less churn.

#### B. Pricing Hidden
*"Pricing: Start free, upgrade for advanced features. Contact for enterprise."*

**Hypothesis:** Curiosity drives more trial signups, but lower conversion to paid.

### Success Metrics
| Variant | Signups | Activation Rate | Conversion to Paid | Churn (Day 7) |
|---------|----------|----------------|-------------------|-------------------|
| A (Transparent) | | | | |
| B (Hidden) | | | | |

### Duration
- **Test Window:** Week 1 (7 days)
- **Decision:** Transparent pricing is our philosophy, likely stick with A unless data shows B wins dramatically

---

## Test Protocol

### How to Run Tests
1. **Pre-test:** All content variants prepared, reviewed, approved
2. **Launch:** Deploy all variants simultaneously (same time window)
3. **Track:** Manual logging for platform metrics, automated for signups
4. **Analyze:** Compare against success criteria at test window end
5. **Decide:** Pick winner, document reasoning, double down

### Sample Size Consideration
- We don't have volume for statistical significance
- Directional signal is acceptable (e.g., A gets 2x signups of B = A wins)
- Qualitative feedback matters (comment quality, user questions)

### Iteration Speed
- **24h test windows:** HN (news cycle), Twitter (feed velocity)
- **48h test windows:** LinkedIn (evergreen content, slower velocity)
- **Decision made immediately:** No analysis paralysis, move to next test

---

## Documentation & Learnings

### After Each Test
```markdown
## [Test Name] Results

### Winner
- **Variant:** [A/B/C]
- **Metrics:** [key performance data]
- **Reasoning:** [why this variant won]

### Loser
- **Variant:** [A/B/C]
- **Metrics:** [key performance data]
- **Reasoning:** [why this variant lost]

### Learnings
1. [Specific insight about audience preference]
2. [Surprise or counterintuitive finding]
3. [Actionable insight for next content]

### Next Action
- [Apply winning variant to all subsequent content]
- [Design next hypothesis to test]
- [Update content calendar if needed]
```

### Weekly Synthesis
At end of Week 1, synthesize all test learnings:
- Which messaging themes work across channels?
- Which platform performs best for our audience?
- What's the optimal title/structure pattern?
- Document in shared-learnings.md for long-term memory

---

## Escalation Triggers

### If No Clear Winner
- **Condition:** Variants perform within 20% of each other
- **Action:** Test more variants or combine elements
- **Escalation:** Not needed - continue testing

### If All Variants Underperform
- **Condition:** 0 signups across all variants at test window end
- **Action:** Escalate to CEO immediately
- **Decision Required:** Is this execution issue or PMF issue?

### If One Channel Dominates
- **Condition:** One platform gets 3x+ signups vs others
- **Action:** Double down on that channel, deprioritize others
- **Strategy:** Focus resources where conversion happens

---

*Last updated: 2026-03-27*
