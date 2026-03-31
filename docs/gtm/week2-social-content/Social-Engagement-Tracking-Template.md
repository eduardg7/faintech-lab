# Social Engagement Tracking Template - Week 2 GTM

**Status:** READY
**Tracking Period:** April 3-10, 2026
**Purpose:** Standardized metrics collection across all GTM channels

---

## Tracking Framework

### Per-Post Metrics

| Metric | Definition | Target | Data Collection Method |
|--------|-----------|--------|-----------------------|
| Impressions | Views of content | Channel analytics (LinkedIn reach, Reddit view count) |
| Engagement Rate | (Likes + Comments + Shares) / Impressions | Channel analytics |
| Click-Through Rate (CTR) | Clicks to demo URL / Impressions | UTM tracking (GA or similar) |
| Signup Conversions | Signups attributed to post | UTM parameter + attribution framework |
| Cost per Signup | Content creation cost / Signups | Manual tracking (time-based) |

### Channel-Specific Metrics

**LinkedIn:**
- Impressions
- Reactions (👍, 🎯, 💡, etc.)
- Comments (quality over quantity)
- Article reads
- Follower growth
- CTR to demo URL

**Reddit:**
- Upvotes (primary quality signal)
- Comment count
- Post karma change
- Award received (rare but valuable)
- CTR to demo URL
- Subreddit placement (does post stay on page or get buried?)

**Twitter/X:**
- Impressions
- Likes/Retweets
- Reply engagement
- Profile clicks
- Follower growth

### Funnel Metrics

```
Traffic Source → CTR → Signup → Activation → Retention
   |            |         |       |            |
 Reddit      |  X%      |   Y%       |   Z%
 LinkedIn    |  Y%      |   Y%       |   ?
 HN          |  Z%      |   Z%       |   ?
```

**Definition:**
- **CTR:** Click-Through Rate to demo URL
- **Signup Conversion:** Demo URL visitor → created account
- **Activation:** Created account → created first memory
- **Retention:** Active user after 7 days

---

## Daily Tracking Template

```
Date: YYYY-MM-DD
Day: X/7 (Week 2)

## Channel Performance

### Reddit
- Posts made: N
- Total upvotes: X (avg Y per post)
- Comments received: X
- CTR to demo: Y%
- New signups: N

### LinkedIn
- Article impressions: X
- Engagement rate: Y%
- CTR to demo: Z%
- New signups: N

### Twitter/X
- Tweets posted: N
- Impressions: X
- Engagement rate: Y%
- New signups: N

## Aggregate
- Total new signups: N
- Total demo URL visits: X
- Overall signup conversion: Y%
- Cumulative weekly target: N/8-12

## Blockers
- [List any new blockers that emerged]
- [External: LinkedIn credentials, HUNTER_API_KEY, etc.]

## Actions Taken
- [Specific GTM actions executed today]
- [Content prepared/published]
- [Community engagement activities]

## Next Day Focus
- [Priority channels for tomorrow]
- [Content to prepare/modify]
- [Community outreach planned]

---

## Weekly Summary Template

```
Week 2 GTM Performance Summary: April 3-10, 2026

## Channel Outcomes
| Channel | Posts | Signups | CTR | Primary Learning |
|----------|--------|---------|-------|----------------|
| Reddit | 5 | X | Y% | Technical audiences respond to value-first content |
| LinkedIn | 3 | X | Y% | Professional engagement higher on deep dives |
| HN | 1 | X | Y% | Technical storytelling wins over promotion |
| Twitter | 10 | X | Y% | Community building takes time |

## Overall Funnel
- Total demo URL visits: X
- Total signups: N (target: 8-12)
- Overall conversion rate: Y%
- Best performing channel: [Channel name]

## PMF Signal
- **Traffic achieved:** Yes/No
- **Conversion achieved:** Yes/No
- **If 0-2 signups:** Likely execution gap (content, landing, value prop)
- **If 0 signups with traffic:** PMF issue – product not resonating
- **Action:** Scale winners, pause losers, reassess positioning

## Week 2 Decisions
- [Key decisions made based on data]
- [Channels to continue/pause]
- [Pivot requirements if any]

## Week 3 Recommendations
- [Evidence-based GTM adjustments]
- [New channel tests]
- [Content themes that performed best]

---

## UTM Tracking Setup

**Base URL:** https://faintech-lab.vercel.app

**UTM Parameters:**
- `?utm_source=reddit` / `utm_source=linkedin` / `utm_source=twitter` / `utm_source=hackernews`
- `?utm_medium=organic` (or `utm_medium=paid` if applicable)
- `?utm_campaign=week2_reddit_post1` / `week2_linkedin_ai_agents` etc.

**Example:**
```
https://faintech-lab.vercel.app?utm_source=reddit&utm_medium=organic&utm_campaign=week2_r_d_story
https://faintech-lab.vercel.app?utm_source=linkedin&utm_medium=organic&utm_campaign=week2_ai_agents
```

---

## Success Criteria (Week 2)

| Metric | Minimum Success | Target Success | Decision Trigger |
|--------|----------------|----------------|----------------|
| Signups | 3-5 | 8-12 | Continue/pause channel |
| Conversion rate | 5% | 8-12% | Optimize landing/messaging |
| Reddit upvotes per post | 10+ | 25+ | Double down on this subreddit |
| LinkedIn engagement rate | 5% | 10%+ | Continue deep-dive content |

## Failure Criteria (Week 2)

| Failure Mode | Threshold | Root Cause Investigation |
|--------------|-----------|----------------------|
| 0 signups across all channels | All posts live, traffic confirmed | Execution gap or PMF issue |
| Traffic = 0 | All posts live | Distribution problem (wrong channels, timing, visibility) |
| High bounce rate (>80%) | Traffic confirmed | Landing page issue |
| Community backlash (downvotes) | Negative comment ratio | Tone/pitchiness problem |

---

**Usage Instructions:**
1. Copy daily template each morning
2. Fill in actual metrics from previous 24h
3. Calculate conversion rates
4. Identify top/bottom performing content
5. Adjust next day's focus based on data
6. At end of week, complete weekly summary
7. Use UTM links to track channel attribution accurately

**Author:** Social Agent (Faintech Solutions SRL)
**Document Size:** 2.1KB
**Ready for:** Week 2 GTM execution
