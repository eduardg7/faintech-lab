# Customer Health Monitoring Dashboard Template

> Task: OS-20260318085922-8EFE - CSM AC4/4

## Overview

This template provides the structure and specifications for building a customer health monitoring dashboard. The dashboard visualizes health scores for beta users based on the Health Score Calculator implementation.

## API Endpoint

**GET** `/v1/health-score/dashboard`

Returns aggregated metrics for the dashboard.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `users` | JSON array | No | Array of `UserActivityData` objects. If omitted, returns example data. |

### Response Structure

```typescript
interface DashboardMetrics {
  overview: {
    totalUsers: number;
    averageHealthScore: number;
    healthScoreTrend: 'up' | 'down' | 'stable';
  };
  riskDistribution: {
    low: number;
    medium: number;
    high: number;
    critical: number;
  };
  engagementMetrics: {
    averageFeatureAdoptionRate: number;
    averageLoginFrequency: number;
    activeUsersLast7Days: number;
    activeUsersLast30Days: number;
  };
  retentionMetrics: {
    averageTenure: number;
    churnRiskUsers: number;
  };
  feedbackMetrics: {
    averageNps: number | null;
    sentimentDistribution: {
      positive: number;
      neutral: number;
      negative: number;
      noFeedback: number;
    };
  };
}
```

## Dashboard Layout

### Header Section

```
┌─────────────────────────────────────────────────────────────────┐
│  Customer Health Dashboard                    Last updated: X   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Total    │  │ Avg      │  │ Trend    │  │ At Risk  │        │
│  │ Users    │  │ Score    │  │ ↗ ↘ →    │  │ Users    │        │
│  │   25     │  │   72     │  │   ↗      │  │    5     │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### Risk Distribution Panel

```
┌─────────────────────────────────────────────────────────────────┐
│  Risk Level Distribution                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🟢 Low Risk      ████████████████████████  12 (48%)           │
│  🟡 Medium Risk   ████████████████          8 (32%)            │
│  🟠 High Risk     ██████                    3 (12%)            │
│  🔴 Critical      ████                      2 (8%)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Engagement Metrics Panel

```
┌─────────────────────────────────────────────────────────────────┐
│  Engagement Metrics                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Feature Adoption Rate                                          │
│  ████████████████████████████████████████████████░░░░░░░ 58%    │
│                                                                 │
│  Avg Login Frequency: 4.2 per week                             │
│                                                                 │
│  Active Users (7 days):  18 / 25  (72%)                        │
│  Active Users (30 days): 22 / 25  (88%)                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Retention Metrics Panel

```
┌─────────────────────────────────────────────────────────────────┐
│  Retention Metrics                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Average Tenure: 45 days                                       │
│                                                                 │
│  Churn Risk Users: 5                                           │
│  ┌────────────────────────────────────────────┐                │
│  │ ⚠️ Users requiring immediate attention:    │                │
│  │    - 2 critical risk                       │                │
│  │    - 3 high risk                           │                │
│  └────────────────────────────────────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Feedback Metrics Panel

```
┌─────────────────────────────────────────────────────────────────┐
│  Feedback Metrics                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Average NPS: 7 / 10                                           │
│                                                                 │
│  Sentiment Distribution:                                        │
│  😊 Positive: 15 (60%)                                         │
│  😐 Neutral:  6 (24%)                                          │
│  😞 Negative: 2 (8%)                                           │
│  ❓ No Data:  2 (8%)                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation Notes

### Health Score Formula

```
healthScore = engagement * 0.30 +
              activity * 0.25 +
              retention * 0.25 +
              feedback * 0.20
```

### Risk Level Thresholds

| Score Range | Risk Level | Color  | Action                              |
|-------------|------------|--------|-------------------------------------|
| 80-100      | Low        | 🟢      | Monitor normally                    |
| 50-79       | Medium     | 🟡      | Check engagement patterns           |
| 30-49       | High       | 🟠      | Proactive outreach recommended      |
| 0-29        | Critical   | 🔴      | Immediate intervention required     |

### Component Scoring

#### Engagement Score (30% weight)
- Feature adoption rate (0-70 points)
- Task completion bonus (0-30 points)

#### Activity Score (25% weight)
- Login frequency (0-50 points)
- Recency bonus (0-50 points based on last active)

#### Retention Score (25% weight)
- Base score: 50
- Time bonus: +5 to +30 based on tenure
- Inactivity penalty: -20 to -40

#### Feedback Score (20% weight)
- Normalized NPS (0-100 scale from -10 to +10)
- Sentiment adjustment: +10 positive, -15 negative

## Alert Thresholds

### Automated Alerts

| Metric                    | Warning | Critical | Action                          |
|---------------------------|---------|----------|---------------------------------|
| Health Score Drop         | >10 pts | >20 pts  | Trigger outreach workflow       |
| Inactivity Period         | >14 days| >30 days | Send re-engagement email        |
| NPS Score                 | <5      | <3       | Schedule feedback call          |
| Feature Adoption          | <30%    | <20%     | Product training recommendation |

## Data Refresh Recommendations

- **Real-time**: Individual user health scores (on-demand)
- **Hourly**: Dashboard aggregates
- **Daily**: Trend calculations and historical comparisons

## Related Endpoints

- `POST /v1/health-score/calculate` - Single user calculation
- `POST /v1/health-score/batch` - Multiple user calculation
- `GET /v1/health-score/dashboard` - Aggregated metrics (this endpoint)
