# GTM Metrics Tracking Templates

**Purpose:** Structured data collection for Week 1 GTM performance analysis
**Created:** 2026-03-29
**Owner:** faintech-marketing-lead
**Status:** Ready for Week 1 execution (Mar 27 - Apr 2)

---

## Overview

Week 1 GTM execution requires structured metrics collection across all distribution channels to enable data-driven Week 2 strategy decisions. This document provides templates and schemas for tracking signups, engagement, and conversion metrics.

**Channels Tracked:**
- Hacker News (Show HN launch - Apr 1)
- LinkedIn (Organic article post)
- Twitter/X (Daily posting cadence)
- GitHub (Issue #90 + stars/forks)
- Direct (Beta signup form)

---

## Daily Metrics Snapshot Template

### Date: [YYYY-MM-DD]
**Time:** [HH:MM] EET

### Signups by Source
```json
{
  "date": "2026-MM-DD",
  "total_signups": 0,
  "by_source": {
    "hacker_news": 0,
    "linkedin": 0,
    "twitter": 0,
    "github_issue_90": 0,
    "direct": 0
  },
  "cumulative_signups": 0
}
```

### Engagement Metrics
```json
{
  "date": "2026-MM-DD",
  "hacker_news": {
    "upvotes": 0,
    "comments": 0,
    "rank": 0,
    "submission_url": ""
  },
  "linkedin": {
    "impressions": 0,
    "reactions": 0,
    "comments": 0,
    "article_url": ""
  },
  "twitter": {
    "impressions": 0,
    "likes": 0,
    "retweets": 0,
    "replies": 0,
    "tweets_posted": 0
  },
  "github": {
    "issue_90_comments": 0,
    "issue_90_reactions": 0,
    "stars": 0,
    "forks": 0
  }
}
```

### Quality Signals
```json
{
  "date": "2026-MM-DD",
  "user_feedback_threads": 0,
  "technical_questions": 0,
  "integration_requests": 0,
  "negative_sentiment": 0,
  "spam_reports": 0
}
```

---

## Channel-Specific Success Criteria

### Hacker News (Launch: Apr 1, 17:00 EET)
**Success Thresholds:**
- Minimum viable: 30+ upvotes, 5+ comments, 50+ signups
- Strong success: 100+ upvotes, 20+ comments, 100+ signups
- Exceptional: 500+ upvotes, 50+ comments, 500+ signups

**Key Metrics to Track:**
- Peak rank position (front page rank)
- Comment velocity (comments per hour in first 24h)
- Upvote velocity (upvotes per hour in first 24h)
- Time to first signup
- Signup conversion rate (signups / upvotes)

**Data Collection Points:**
- 17:05 EET (5 min post-launch)
- 17:15 EET (15 min)
- 17:30 EET (30 min)
- 18:00 EET (1 hour)
- 19:00 EET (2 hours)
- 22:00 EET (5 hours)
- Apr 2, 17:00 EET (24 hours)
- Apr 3, 17:00 EET (48 hours)

---

### LinkedIn Organic Article
**Success Thresholds:**
- Minimum viable: 500+ impressions, 15+ reactions, 10+ comments
- Strong success: 2000+ impressions, 50+ reactions, 30+ comments
- Exceptional: 10000+ impressions, 200+ reactions, 100+ comments

**Key Metrics to Track:**
- Impressions velocity (impressions per hour in first 24h)
- Engagement rate (reactions + comments / impressions)
- Comment sentiment (positive/neutral/negative)
- Time to first engagement
- Article shares (0 or count if available)

**Data Collection Points:**
- Immediately after publication (capture initial metrics)
- 2 hours post-publication
- 6 hours post-publication
- 24 hours post-publication
- 48 hours post-publication (if article still active)

---

### Twitter/X Daily Cadence
**Success Thresholds (per tweet):**
- Minimum viable: 200+ impressions, 10+ likes, 5+ replies
- Strong success: 1000+ impressions, 50+ likes, 20+ replies
- Exceptional: 5000+ impressions, 200+ likes, 100+ replies

**Daily Aggregate Targets (2 tweets per day):**
- Minimum viable: 400+ impressions, 20+ likes, 10+ replies
- Strong success: 2000+ impressions, 100+ likes, 40+ replies

**Key Metrics to Track:**
- Tweet performance distribution (best/worst/median tweet)
- Hashtag effectiveness ( impressions per hashtag)
- Time-of-day performance (which posting windows work best)
- Mention/quote tweet volume

**Data Collection Points:**
- 2 hours after each tweet
- 6 hours after each tweet
- End of day (23:59 EET)

---

### GitHub Organic (Issue #90)
**Success Thresholds:**
- Minimum viable: 10+ comments, 5+ reactions
- Strong success: 30+ comments, 20+ reactions
- Exceptional: 100+ comments, 50+ reactions

**Key Metrics to Track:**
- Comment velocity (comments per day)
- Issue star/fork impact (correlation with signups)
- Technical discussion depth (code comments vs. "cool" comments)
- Bug report mentions

**Data Collection Points:**
- Daily at 10:00 EET
- Weekly on Sundays

---

## Week 1 Analysis Framework (Apr 2 Review)

### Question 1: Channel Performance Ranking
**Metric:** Signups by channel / Channel effort investment
**Output:**
```markdown
| Channel | Signups | Effort (hrs) | Signups/hr | Rank |
|---------|----------|----------------|-------------|-------|
| Hacker News | [X] | [0.5] | [Y] | [#] |
| LinkedIn | [X] | [1.0] | [Y] | [#] |
| Twitter | [X] | [0.5] | [Y] | [#] |
| GitHub | [X] | [0] | [Y] | [#] |
| Direct | [X] | [0] | [Y] | [#] |
```

---

### Question 2: Conversion Funnel Analysis
**Metric:** Traffic to signup conversion rate
**Output:**
```json
{
  "channel": "hacker_news",
  "impressions": [X],
  "clicks": [Y],
  "signups": [Z],
  "impressions_to_signup_rate": [Z/X],
  "click_to_signup_rate": [Z/Y],
  "top_acquisition_source": "[channel_name]"
}
```

---

### Question 3: User Segmentation Analysis
**Metric:** Signups by user type
**Output:**
```json
{
  "total_signups": [X],
  "by_segment": {
    "technical_founder": [X],
    "product_manager": [Y],
    "developer": [Z],
    "researcher": [W],
    "enterprise_cto": [V],
    "other": [U]
  },
  "highest_value_segment": "[segment_name]",
  "segment_recommendation": "[focus Tier 2 expansion on this segment]"
}
```

---

### Question 4: Messaging Effectiveness Analysis
**Metric:** Which messages resonated?
**Output:**
```markdown
### Top Performing Messages

1. **[Message Title]** - [Channel]
   - Impressions: [X]
   - Engagement Rate: [Y%]
   - Signups: [Z]
   - Why it worked: [hypothesis]

2. **[Message Title]** - [Channel]
   - Impressions: [X]
   - Engagement Rate: [Y%]
   - Signups: [Z]
   - Why it worked: [hypothesis]

### Underperforming Messages

1. **[Message Title]** - [Channel]
   - Impressions: [X]
   - Engagement Rate: [Y%]
   - Signups: [Z]
   - What to change: [iteration idea]
```

---

## Week 2 Strategy Decision Matrix

Based on Week 1 data, answer these questions to shape Week 2:

| Question | Data Source | Decision Threshold | Week 2 Action |
|----------|--------------|-------------------|-----------------|
| Which channel drives highest ROI? | Signups/hr by channel | 2x higher than #2 | Double down on top channel |
| Which messaging angle converts best? | Top messages by signup rate | >10% signup/engagement | Scale message angle to all channels |
| Which user segment converts best? | Signup by segment analysis | >40% of total | Tailor Tier 2 expansion to segment |
| Is minimum viable traction achieved? | Total signups Week 1 | 5-10 signups | Continue current GTM |
| Should we activate partnerships? | Total signups + engagement quality | >20 signups + positive sentiment | Begin partnership outreach |
| Should we pivot messaging? | Negative sentiment ratio | >30% negative sentiment | Reframe value proposition |
| Should we expand to new channels? | Top channel saturation point | <50% signup growth day 3-4 vs 1-2 | Add Reddit, IndieHackers, etc. |

---

## Tier 2 Expansion Readiness Checklist

**Trigger:** Week 1 review (Apr 2) confirms minimum viable traction (5-10 signups)

### Data Collection Requirements
- [ ] Signups by source (complete Week 1)
- [ ] Engagement metrics (all channels)
- [ ] User segmentation (signup surveys complete)
- [ ] Top messaging analysis (best/worst performers)
- [ ] Technical questions cataloged (for content roadmap)

### Tier 2 Channel Candidates
| Channel | Relevance Score | Activation Effort | Estimated Cost | Priority |
|----------|-----------------|-------------------|----------------|----------|
| Product Hunt | High | Medium (prep assets) | $0 | P1 |
| Reddit (self-promo phase) | Medium | Low (karma ready) | $0 | P2 |
| IndieHackers | Medium | Low (submit post) | $0 | P2 |
| Dev.to | Medium | Low (write article) | $0 | P3 |
| HackerNoon | Low | Low (submit post) | $0 | P3 |
| BetaList | Medium | Medium (apply + maintain) | $0 | P3 |
| AI-specific communities (r/LocalLLaMA promo) | High | Low (track 2A progress) | $0 | P1 |

---

## Evidence Format for Week 1 Review

**File:** `/Users/eduardgridan/faintech-lab/docs/gtm/week1-performance-analysis.md`

**Required Sections:**
```markdown
# Week 1 GTM Performance Analysis - [Date: 2026-04-02]

## Executive Summary
- Total signups: [X]
- Target: 5-10
- Status: [ON TRACK / BEHIND / AHEAD]
- Top channel: [channel_name]
- Key finding: [1-2 sentence insight]

## Channel Performance
[Channel performance ranking table]

## User Segmentation
[User segment analysis with pie chart description]

## Messaging Effectiveness
[Top/underperforming messages analysis]

## Week 2 Recommendations
1. [Specific recommendation 1]
2. [Specific recommendation 2]
3. [Specific recommendation 3]

## Evidence
- Daily metrics snapshots: [path to daily logs]
- Raw data: [path to JSON files]
- Screenshots/exports: [list if available]
```

---

**Created:** 2026-03-29T08:12:00+02:00
**Owner:** faintech-marketing-lead
**Next Owner:** cmo (for Week 1 GTM execution support)
**Status:** ✅ COMPLETE - Ready for Week 1 execution
