# Beta User Health Metrics Template

**Version:** 1.0
**Launch Period:** March 24 - March 31, 2026

---

## Overview

This template defines the health metrics to track for beta users to assess engagement, product fit, and beta success. Metrics are tracked at user-level and cohort-level.

---

## Metric Categories

### 1. Engagement Metrics

**Definition:** How actively users are using the product

| Metric | Formula | Target | Data Source |
|--------|----------|--------|-------------|
| Daily Active Users (DAU) | Users with ≥1 session in last 24h | 80% of cohort | Session logs |
| Weekly Active Users (WAU) | Users with ≥1 session in last 7 days | 100% of cohort | Session logs |
| Session Duration | Avg. time per session | 5+ minutes | Session logs |
| Sessions per User | Total sessions / unique users | 3+ / user | Session logs |

---

### 2. Usage Frequency Metrics

**Definition:** How often users return and create value

| Metric | Formula | Target | Data Source |
|--------|----------|--------|-------------|
| Memories Created | Total memories / unique users | 10+ / user | Database |
| Days Active | Days with ≥1 session | 5+ days | Session logs |
| Retention Rate (D7) | Users active on Day 7 / Users started | 70% | Session logs |
| Retention Rate (D30) | Users active on Day 30 / Users started | 50% | Session logs |

---

### 3. Feature Adoption Metrics

**Definition:** Which features users are adopting

| Metric | Formula | Target | Data Source |
|--------|----------|--------|-------------|
| Search Usage | Users who performed ≥1 search | 60% | Analytics logs |
| Tag Usage | Users who created ≥1 tag | 50% | Database |
| Linking Usage | Users who linked ≥2 memories | 40% | Database |
| Bulk Operations | Users who used bulk import/export | 30% | Analytics logs |

---

### 4. Satisfaction Metrics

**Definition:** How satisfied users are with the product

| Metric | Formula | Target | Data Source |
|--------|----------|--------|-------------|
| NPS Score | (% Promoters - % Detractors) | +20 | Survey |
| CSAT Score | Avg. rating (1-5) | 4.0+ | Survey |
| Feedback Completion | Users who completed survey | 80% | Survey platform |
| Support Tickets | Tickets / unique users | <0.5 / user | Support system |

---

## Health Score Calculation

**Formula:**
```
Health Score = (Engagement × 0.3) + (Usage × 0.3) + (Adoption × 0.2) + (Satisfaction × 0.2)
```

**Score Interpretation:**
- 90-100: HEALTHY (green) - Users thriving, product fit strong
- 70-89: STABLE (yellow) - Good engagement, some improvement areas
- <70: AT-RISK (red) - Low engagement, intervention needed

---

## Cohort-Level Metrics

**Daily Dashboard Metrics:**
1. Total beta users invited
2. Total beta users onboarded (completed onboarding)
3. DAU / WAU ratio
4. Avg. health score across cohort
5. Users with health score <70 (flagged for intervention)

**Weekly Dashboard Metrics:**
1. Retention curves (D1, D7, D14, D21, D30)
2. Feature adoption trends
3. NPS trend
4. Support ticket volume by category

---

## Automated Alerts

Trigger manual review when:
- ⚠️ DAU drops below 50% of cohort size for 2+ consecutive days
- ⚠️ Avg. health score drops below 70
- ⚠️ 3+ users churn (no activity for 7+ days)
- ⚠️ NPS score drops below 0

---

## Data Collection Method

| Source | Collection Frequency | Automation Level |
|---------|---------------------|-------------------|
| Session logs | Real-time | Automated (DB) |
| Memory database | Daily cron | Automated (script) |
| Analytics events | Real-time | Automated (Posthog/amplitude if available) |
| Surveys | Day 7, Day 30 | Manual (CSM triggers) |
| Support tickets | Real-time | Manual (CSM tracks) |

---

*Last Updated: March 21, 2026*
