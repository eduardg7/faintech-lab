# Success Metrics Template for Growth Experiments

**Purpose**: Standardized metrics for measuring growth experiment effectiveness
**Version**: 1.0
**Created**: 2026-03-17
**Owner**: faintech-growth-marketer

---

## Core Metrics Framework

All experiments should track these 4 categories:

### 1. Awareness Metrics
**Definition**: How many people saw the experiment?

| Metric | Unit | Source | Baseline | Target |
|--------|-------|---------|-----------|--------|
| **Impressions/Reach** | Count | Platform analytics (Hacker News, Twitter, Discord) | 0 | TBD per experiment |
| **Views** | Count | Page views, repo visits, profile visits | 0 | TBD per experiment |
| **Click-through Rate (CTR)** | % | Clicks / Impressions | 0% | 2-5% (varies by channel) |

### 2. Engagement Metrics
**Definition**: How many people interacted meaningfully?

| Metric | Unit | Source | Baseline | Target |
|--------|-------|---------|-----------|--------|
| **Engagement Rate** | % | (Likes + Comments + Shares) / Impressions | 0% | 3-7% |
| **Upvotes/Stars** | Count | Platform-specific (HN upvotes, GitHub stars) | 0 | TBD per experiment |
| **Comments/Discussion** | Count | Thread replies, PR comments, Discord mentions | 0 | 5+ (quality > quantity) |
| **Time on Page/README** | Seconds | Analytics (if available) | 0 | >30s |

### 3. Conversion Metrics
**Definition**: How many people took action toward beta signup?

| Metric | Unit | Source | Baseline | Target |
|--------|-------|---------|-----------|--------|
| **Signups/Interest** | Count | Beta waitlist, demo requests, direct DMs | 0 | 5-10 per experiment |
| **Repo Clones/Forks** | Count | GitHub insights | 0 | 10-20 per experiment |
| **Qualified Conversations** | Count | DMs, email threads with genuine interest | 0 | 3-5 per experiment |
| **Conversion Rate** | % | (Signups + Clones) / Impressions | 0% | 0.5-2% |

### 4. Quality/Sentiment Metrics
**Definition**: Was the response positive, relevant, and valuable?

| Metric | Unit | Source | Baseline | Target |
|--------|-------|---------|-----------|--------|
| **Sentiment Score** | 1-5 | Manual review (negative=1, neutral=3, positive=5) | 3 | >4 (positive tilt) |
| **Technical Depth** | 1-5 | Manual review (shallow=1, deep=5) | 3 | >4 (technical audience) |
| **Relevance to Target** | 1-5 | Manual review (off-topic=1, on-point=5) | 3 | >4 (target audience match) |

---

## Quick-Win Experiment Metrics

### QW-1: Hacker News Launch

**Hypothesis**: "Rigorous R&D methodology" angle resonates with HN technical audience

| Metric | Target | Measurement Period | Success Criteria |
|--------|---------|-------------------|------------------|
| **Upvotes** | 20+ | 24h post-launch | ✅ Meets target |
| **GitHub Stars** | 5+ | 48h post-launch | ✅ Meets target |
| **Repo Clones** | 10+ | 48h post-launch | ✅ Meets target |
| **Comments Quality** | 3+ technical discussions | 24h post-launch | ✅ Meets target |
| **Signups** | 3-5 beta requests | 72h post-launch | ✅ Meets target |

**Data Sources**:
- HN API or manual check (upvotes, comments)
- GitHub Insights (stars, clones, traffic)
- Beta waitlist count
- Email/DM requests

**Success Scorecard**:
- [ ] 20+ upvotes
- [ ] 5+ GitHub stars
- [ ] 10+ repo clones
- [ ] 3+ technical comment threads
- [ ] 3+ qualified beta requests

**Pass Threshold**: 4/5 criteria met
**Excellent**: 5/5 criteria met

---

### QW-2: Discord Community Soft-Launch

**Hypothesis**: Authentic help in AI agent communities leads to organic beta signups

| Metric | Target | Measurement Period | Success Criteria |
|--------|---------|-------------------|------------------|
| **Servers Joined** | 3-5 relevant AI agent communities | Day 1 | ✅ Meets target |
| **Helpful Interactions** | 10+ quality answers to memory/context questions | Week 1 | ✅ Meets target |
| **Qualified Conversations** | 5+ genuine discussions about agent challenges | Week 1 | ✅ Meets target |
| **Beta Requests** | 3-5 from Discord members | Week 2 | ✅ Meets target |
| **Community Recognition** | 2+ mentions of helpful Faintech Lab contributions | Week 2 | ✅ Meets target |

**Data Sources**:
- Discord server membership tracking
- Manual log of helpful interactions (timestamp, question, answer, community response)
- Beta signup source attribution (UTM or manual attribution)
- Discord search for mentions

**Success Scorecard**:
- [ ] 3-5 servers joined
- [ ] 10+ helpful interactions logged
- [ ] 5+ qualified conversations
- [ ] 3+ Discord-sourced beta requests
- [ ] 2+ community mentions/recognitions

**Pass Threshold**: 4/5 criteria met
**Excellent**: 5/5 criteria met

---

### QW-3: GitHub README Optimization

**Hypothesis**: Clear methodology + open-source positioning increases repo credibility

| Metric | Target | Measurement Period | Success Criteria |
|--------|---------|-------------------|------------------|
| **Star-to-Clone Ratio** | >0.5 | 7 days | ✅ Meets target |
| **Average Time on README** | >30s | 7 days | ✅ Meets target |
| **New Stars** | 10+ | 7 days | ✅ Meets target |
| **Repo Visitors** | 50+ | 7 days | ✅ Meets target |
| **Technical Depth Feedback** | >4/5 in manual review | Ongoing | ✅ Meets target |

**Data Sources**:
- GitHub Insights (stars, clones, visitors, traffic sources)
- GitHub README analytics (time on page)
- Manual sentiment review of new issues/PRs/Discussions

**Success Scorecard**:
- [ ] Star-to-clone ratio > 0.5
- [ ] >30s average time on README
- [ ] 10+ new stars
- [ ] 50+ repo visitors
- [ ] Technical depth >4/5

**Pass Threshold**: 4/5 criteria met
**Excellent**: 5/5 criteria met

---

### QW-4: Twitter Thread: Experiment Deep Dive

**Hypothesis**: Technical threads get 2-3x engagement vs single posts

| Metric | Target | Measurement Period | Success Criteria |
|--------|---------|-------------------|------------------|
| **Impressions** | 1K+ | 48h post-tweet | ✅ Meets target |
| **Engagements** | 50+ (likes + RTs + replies) | 48h post-tweet | ✅ Meets target |
| **Engagement Rate** | >3% | 48h post-tweet | ✅ Meets target |
| **Replies Quality** | 5+ technical discussions | 48h post-tweet | ✅ Meets target |
| **New Followers** | 10+ @FaintechLab followers | 72h post-tweet | ✅ Meets target |

**Data Sources**:
- Twitter Analytics (native or third-party)
- Manual engagement tracking
- Follower count tracking

**Success Scorecard**:
- [ ] 1K+ impressions
- [ ] 50+ engagements
- [ ] >3% engagement rate
- [ ] 5+ technical reply discussions
- [ ] 10+ new followers

**Pass Threshold**: 4/5 criteria met
**Excellent**: 5/5 criteria met

---

## Longer-Term Play Metrics (High-Level)

### LT-1: Discord Community Build

| Metric | Target (4-8 weeks) | Success Criteria |
|--------|---------------------|------------------|
| **Engaged Community Members** | 50+ | ✅ Meets target |
| **Weekly Active Help** | 10+ helpful interactions/week | ✅ Meets target |
| **Beta Users from Discord** | 20+ | ✅ Meets target |
| **Community Authority** | Recognized as "memory expert" (qualitative) | ✅ Meets target |

### LT-2: GitHub Open-Source Ecosystem

| Metric | Target (4-12 weeks) | Success Criteria |
|--------|----------------------|------------------|
| **GitHub Stars** | 100+ | ✅ Meets target |
| **Community Contributions** | 5+ PRs from external devs | ✅ Meets target |
| **Repo Clones** | 200+ | ✅ Meets target |
| **SEO Traffic from GitHub** | Measurable | ✅ Meets target |

### LT-3: Twitter Brand Building

| Metric | Target (8+ weeks) | Success Criteria |
|--------|-------------------|------------------|
| **Followers** | 1K+ | ✅ Meets target |
| **Weekly Impressions** | 5K+ | ✅ Meets target |
| **Technical Mentions** | 10+ @mentions from AI accounts | ✅ Meets target |
| **Content Consistency** | 3-5x/week posting maintained | ✅ Meets target |

### LT-4: Content Repurposing (Dev.to/Medium)

| Metric | Target (4-8 weeks) | Success Criteria |
|--------|----------------------|------------------|
| **Monthly Organic Visitors** | 500+ | ✅ Meets target |
| **Search Rank** | Top 20 for "agent memory" terms | ✅ Meets target |
| **Articles Published** | 2-4 | ✅ Meets target |
| **Engagement on Articles** | 10+ reactions/comments per article | ✅ Meets target |

### LT-5: Reddit Engagement Strategy

| Metric | Target (4-6 weeks) | Success Criteria |
|--------|---------------------|------------------|
| **Highly-Rated Answers** | 10+ with positive karma | ✅ Meets target |
| **Organic Mentions** | 3+ mentions of Faintech Lab | ✅ Meets target |
| **Upvote Ratio** | >80% positive on comments | ✅ Meets target |
| **Reddit-Sourced Beta Users** | 5+ | ✅ Meets target |

---

## Measurement Workflow

### Pre-Experiment
1. **Set Baseline**: Document current state (stars, followers, repo stats)
2. **Define Targets**: Use template values or adjust based on channel specifics
3. **Setup Tracking**: Ensure analytics enabled (GitHub Insights, Twitter Analytics, etc.)
4. **Create Scorecard**: Copy relevant experiment scorecard to track results

### During Experiment
1. **Daily Check**: Monitor primary metrics for early signals
2. **Log Interactions**: Manually track qualitative feedback (especially Discord, HN comments)
3. **Adjust if Needed**: If metrics are way below target by day 3, consider content/angle tweaks

### Post-Experiment (48-72h)
1. **Compile Results**: Fill in final numbers in scorecard
2. **Calculate Success Rate**: % of criteria met (Pass threshold)
3. **Document Learnings**: What worked? What didn't? Why?
4. **Update Experiments Log**: Add result to master tracking document
5. **Handoff Next Owner**: If criteria met, handoff to next owner; if failed, iterate or pivot

---

## Experiment Log Template

Add each completed experiment to this log:

| Experiment | Date | Channel | Hypothesis | Score | Outcome | Learnings | Next Action |
|------------|-------|----------|-------------|--------|----------|------------|-------------|
| QW-1 | 2026-03-XX | Hacker News | "Rigorous R&D methodology" resonates | X/5 | PASS/FAIL | ... | ... |
| QW-2 | 2026-03-XX | Discord | Authentic help → beta signups | X/5 | PASS/FAIL | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... |

---

## Success Criteria Summary

- **Pass Threshold**: 4/5 criteria met for quick wins
- **Excellent**: 5/5 criteria met
- **Failure**: <4/5 criteria met → iterate or pivot

**Key Principles**:
1. Quality > quantity (especially for engagement metrics)
2. Relevance > reach (target audience match matters more than raw numbers)
3. Learnings > vanity metrics (why it worked > that it worked)
4. Feedback loops are mandatory (update template based on real data)

---

**Next Owner**: faintech-content-creator (use QW metrics for execution)
**Review Cycle**: After each quick-win execution (weekly)
**Template Version**: 1.0
