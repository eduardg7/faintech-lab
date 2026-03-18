# Customer Health Monitoring Dashboard Template

## Overview

This template provides a reusable dashboard component for monitoring customer/user health scores in beta programs. It visualizes user engagement, feature adoption, feedback sentiment, and consistency metrics.

## Components

### HealthScoreDashboard

**Location:** `../HealthScoreDashboard.tsx`

**Purpose:** Display user health scores with tier-based classification and component breakdown.

### Usage

```tsx
import HealthScoreDashboard from '@/components/dashboard/HealthScoreDashboard';
import { healthScoreApi } from '@/lib/stats-api';

// In your page component
const [healthData, setHealthData] = useState<HealthScoreBatchResponse | null>(null);
const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
  async function fetchHealthScores() {
    try {
      const response = await healthScoreApi.calculateBatchHealthScores(userData);
      setHealthData(response);
    } finally {
      setIsLoading(false);
    }
  }
  fetchHealthScores();
}, []);

return (
  <HealthScoreDashboard data={healthData} isLoading={isLoading} />
);
```

### Data Structure

```typescript
interface HealthScoreBatchResponse {
  results: HealthScoreUser[];
  total_users: number;
  average_health_score: number;
  tier_distribution: {
    Champion: number;
    Healthy: number;
    'At-Risk': number;
    Critical: number;
  };
}

interface HealthScoreUser {
  user_id: string;
  health_score: number;
  components: {
    engagement: number;
    feature_adoption: number;
    feedback_sentiment: number;
    consistency: number;
  };
  health_tier: 'Champion' | 'Healthy' | 'At-Risk' | 'Critical';
}
```

## Scoring Formula

The health score is calculated using weighted components:

- **Engagement (40%)**: Sessions per week, session duration, messages per week
- **Feature Adoption (30%)**: Agents created, active agents, memories stored, projects created
- **Feedback Sentiment (20%)**: NPS score, in-app rating, text feedback sentiment
- **Consistency (10%)**: Daily streak, weekly frequency, device consistency

## Tier Classification

| Score Range | Tier      | Color  |
|-------------|-----------|--------|
| 8.0+        | Champion  | Green  |
| 6.0-7.9     | Healthy   | Blue   |
| 4.0-5.9     | At-Risk   | Yellow |
| <4.0        | Critical  | Red    |

## Backend API

### Endpoints

- `POST /v1/health-score/calculate` - Calculate health score for single user
- `POST /v1/health-score/batch` - Calculate health scores for multiple users

### Python Implementation

**Location:** `amc-backend/app/core/health_score.py`

The HealthScoreCalculator class implements the weighted scoring algorithm.

## Customization

### Adding New Components

1. Extend the `HealthScoreCalculator` in Python
2. Update TypeScript interfaces
3. Add new progress bar in the component

### Changing Weights

Modify the weight constants in `health_score.py`:

```python
ENGAGEMENT_WEIGHT = 0.40
FEATURE_ADOPTION_WEIGHT = 0.30
FEEDBACK_SENTIMENT_WEIGHT = 0.20
CONSISTENCY_WEIGHT = 0.10
```

### Custom Tier Thresholds

Update the `scoreColor` function in the component:

```typescript
const scoreColor = (score: number): string => {
  if (score >= 8) return 'text-green-600';  // Champion
  if (score >= 6) return 'text-blue-600';    // Healthy
  if (score >= 4) return 'text-yellow-600';  // At-Risk
  return 'text-red-600';                     // Critical
};
```

## Related Files

- `amc-frontend/src/app/dashboard/health/page.tsx` - Health dashboard page
- `amc-frontend/src/lib/stats-api.ts` - API client for health scores
- `amc-backend/app/core/health_score.py` - Python calculator
- `amc-backend/app/routers/health_score.py` - FastAPI endpoints
- `tests/api/health-score.test.ts` - Test suite (141 tests passing)

## Version

- Created: 2026-03-18
- Last Updated: 2026-03-18
- Status: Production Ready
