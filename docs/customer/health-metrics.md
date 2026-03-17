# Beta Customer Health Metrics

**Project:** Faintech Lab Beta
**Owner:** Customer Success Manager
**Last Updated:** 2026-03-17
**Purpose:** Quantify beta user engagement, identify at-risk users, measure success

---

## Health Score Overview

The health score is a composite metric (0-10) that predicts beta user success. A score of 7+ indicates a healthy, engaged user. A score below 6 indicates risk of churn.

**Health Score Formula:**

```
Health Score = (Engagement × 0.4) + (FeatureAdoption × 0.3) + (FeedbackSentiment × 0.2) + (Consistency × 0.1)
```

Where:
- **Engagement (0-10):** Frequency of usage, session duration, daily/weekly activity
- **FeatureAdoption (0-10):** % of core features used (agents, memories, projects, search)
- **FeedbackSentiment (0-10):** Qualitative feedback rating (0-5 stars mapped to 0-10)
- **Consistency (0-10):** Predictability of usage (e.g., daily streak, weekly patterns)

---

## Engagement Metrics

### Core Metrics

| Metric | Definition | Data Source | Weight |
|--------|------------|-------------|--------|
| **Daily Active Users (DAU)** | Users with ≥1 session in last 24h | User activity log | - |
| **Weekly Active Users (WAU)** | Users with ≥1 session in last 7 days | User activity log | - |
| **Session Duration** | Average time between login and logout | Session timestamps | High |
| **Sessions Per Week** | Average number of sessions per active user | Activity count | High |
| **Messages to Agents** | Number of console messages sent per week | Console logs | High |

### Engagement Score Calculation (0-10)

```
Engagement = min(10, (
  (Sessions per week / 5) × 3 +
  (Avg session duration / 15min) × 3 +
  (Messages per week / 20) × 4
))
```

**Thresholds:**
- 9-10: Power user (daily, multiple sessions)
- 7-8: Regular user (2-3x/week, moderate usage)
- 5-6: Casual user (1x/week, light usage)
- 0-4: At-risk (rare or no usage)

---

## Feature Adoption Metrics

### Core Features

| Feature | Metric | Definition | Target for Beta |
|---------|--------|------------|-----------------|
| **Agents** | Agents created | Number of agents created per user | ≥2 |
| **Agents** | Agents active | Agents with ≥1 execution in last 7d | ≥1 |
| **Memories** | Memories stored | Number of memories added | ≥5 |
| **Projects** | Projects created | Number of projects created | ≥1 |
| **Search** | Search queries | Number of search queries per week | ≥3 |

### Feature Adoption Score (0-10)

```
FeatureAdoption = min(10, (
  (Agents created / 2) × 3 +
  (Memories stored / 5) × 2 +
  (Projects created / 1) × 3 +
  (Search queries / 3) × 2
))
```

**Thresholds:**
- 9-10: Feature explorer (uses all features regularly)
- 7-8: Productive user (uses key features well)
- 5-6: Feature explorer (uses 1-2 features)
- 0-4: Feature unaware (minimal feature usage)

---

## Feedback Sentiment Metrics

### Feedback Collection

| Feedback Type | Method | Frequency | Sentiment Scale |
|---------------|--------|-----------|-----------------|
| **In-app rating** | One-click emoji picker | Daily (after key actions) | 😐=0, 😊=5, 😄=10 |
| **NPS** | "How likely to recommend?" | Weekly (Day 7) | 0-10 |
| **Text feedback** | Open text field | On-demand | Manual sentiment analysis |
| **Support tickets** | Email/in-app messaging | Event-driven | Keyword-based sentiment |

### Feedback Sentiment Score (0-10)

```
FeedbackSentiment = (
  (Avg in-app rating × 0.4) +
  (NPS score / 10 × 0.3) +
  (Text feedback sentiment × 0.2) +
  (Support ticket sentiment × 0.1)
)
```

**Sentiment Classification (text feedback):**
- Positive: "great", "love", "helpful", "easy", "fast"
- Negative: "confusing", "slow", "bug", "error", "broken"
- Neutral: "okay", "works", "fine"

**Thresholds:**
- 8-10: Promoter (high satisfaction)
- 6-7: Passive (satisfied but not excited)
- 0-5: Detractor (at risk of churn)

---

## Consistency Metrics

### Usage Patterns

| Metric | Definition | Data Source |
|--------|------------|-------------|
| **Daily Streak** | Consecutive days with ≥1 session | Activity log |
| **Weekly Frequency** | % of weeks with ≥1 session | Activity log |
| **Time of Day** | Consistency of usage time (standard deviation) | Session timestamps |
| **Device Consistency** | % of sessions from same device/browser | User agent logs |

### Consistency Score (0-10)

```
Consistency = min(10, (
  (Daily streak days / 7) × 5 +
  (Weekly frequency / 1.0) × 3 +
  (Device consistency / 0.8) × 2
))
```

**Thresholds:**
- 9-10: Highly consistent (daily, same device)
- 7-8: Consistent (regular pattern)
- 5-6: Semi-consistent (occasional)
- 0-4: Inconsistent (no pattern)

---

## Health Score Tiers

| Tier | Score Range | Definition | Action |
|------|------------|------------|--------|
| **Champion** | 9-10 | Power user, highly engaged, loves product | Ask for testimonials, invite to exclusive programs |
| **Healthy** | 7-8 | Regular user, good adoption, positive feedback | Maintain, check in monthly |
| **At-Risk** | 5-6 | Casual usage, minimal adoption, neutral feedback | Proactive outreach, offer onboarding help |
| **Critical** | 0-4 | No usage, negative feedback, technical issues | Immediate intervention, 1:1 support |

---

## Automated Alerts

### Trigger Rules

| Alert | Trigger Condition | Notification Destination |
|-------|-------------------|---------------------------|
| **New User Drop-off** | No activity within 24h of signup | CSM (email) |
| **Health Drop** | Health score drops by ≥2 in 7 days | CSM (email) |
| **Critical Risk** | Health score ≤3 | CSM (immediate), CEO (if >3 users) |
| **Negative Feedback** | Sentiment score ≤3 with text feedback | CSM (email) |
| **Feature Adoption Gap** | Active 7 days, 0 memories created | CSM (email) |

### Alert Escalation

| Time Since Alert | Action |
|------------------|--------|
| 0h | Alert sent to CSM |
| 24h | If no action taken, escalate to COO |
| 48h | If still unresolved, escalate to CEO |

---

## Success KPIs for Beta

### Overall Beta Health

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Healthy Users** | 70% of beta users have health score ≥7 | Weekly health score report |
| **Retention Rate** | 60% of users active at Day 7 | WAU / Day 7 signups |
| **Feature Adoption** | 50% of users create ≥2 agents | Agent creation metrics |
| **NPS Score** | ≥7 | Net Promoter Score |

### Weekly Report Format

```
Week of: YYYY-MM-DD
Total beta users: X
Healthy users (score ≥7): Y (Z%)
At-risk users (score 5-6): A (B%)
Critical users (score 0-4): C (D%)

Top features used:
- Agents: M users (N%)
- Memories: O users (P%)
- Projects: Q users (R%)
- Search: S users (T%)

Feedback sentiment: U (0-10)
NPS score: V
Retention rate: W%

Actions taken:
- New user drop-offs: X users reached out
- Health drops: Y users reached out
- Critical risks: Z users in 1:1 support
```

---

## Data Collection & Privacy

### Data Stored
- User activity logs (timestamps, session duration)
- Feature usage metrics (agents created, memories stored)
- Feedback (in-app ratings, NPS, text feedback)
- Technical signals (errors, timeouts, API failures)

### Data NOT Stored
- Console message content (privacy)
- Memory content (privacy)
- Agent task details (privacy)

### Retention Policy
- Beta period (March 24 - April 30): All data retained
- Post-beta: Anonymized aggregated metrics only
- User deletion request: All data deleted within 7 days

---

## Dependencies

- Onboarding checklist: `onboarding-checklist.md`
- Feedback collection mechanism: `feedback-collection.md`
- Welcome email template: `welcome-email.md`
- TASK_DB: Health score calculation and alert triggers

---

## Implementation Roadmap

### Phase 1 (Pre-Launch)
- [ ] Health score calculation logic implemented in backend
- [ ] Metrics collection agents configured
- [ ] Alert triggers set up (email notifications to CSM)

### Phase 2 (Launch Week)
- [ ] Daily health score monitoring
- [ ] Automated alert execution
- [ ] Weekly health reports generated

### Phase 3 (Post-Launch)
- [ ] Refine health score formula based on actual usage data
- [ ] Add predictive churn models
- [ ] Integrate with customer success CRM

---

**Owner:** csm
**Status:** Ready for implementation
**Priority:** P1 (Beta launch: March 24)
