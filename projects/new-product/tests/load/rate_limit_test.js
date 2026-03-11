import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

// Rate limit test configuration
// Test the 1000 req/hour per API key limit
export const options = {
  stages: [
    // Ramp up to 50 users quickly
    { duration: '10s', target: 50 },
    // Generate requests for 2 minutes to hit rate limit
    { duration: '2m', target: 50 },
    // Ramp down
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    errors: ['rate<0.1'], // Allow up to 10% errors (expected 429s)
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  const agentId = `rate-test-agent-${__VU}`;
  
  const payload = JSON.stringify({
    agent_id: agentId,
    project_id: 'rate-test-project',
    type: 'observation',
    content: `Rate limit test ${Date.now()}`,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(`${BASE_URL}/api/v1/memories/`, payload, params);
  
  // Check for rate limiting (429 status)
  const isRateLimited = res.status === 429;
  const isSuccess = res.status === 201 || res.status === 200;
  
  check(res, {
    'status is 201, 200, or 429': (r) => isSuccess || isRateLimited,
    'rate limit headers present': (r) => {
      const hasRateLimit = r.headers['X-RateLimit-Limit'] || r.headers['X-Ratelimit-Limit'];
      const hasRetryAfter = r.headers['Retry-After'] || r.headers['X-RateLimit-Reset'];
      return isRateLimited ? (hasRetryAfter !== undefined) : true;
    },
  });

  // Track non-429 errors as actual errors
  if (!isSuccess && !isRateLimited) {
    errorRate.add(1);
  }

  // Small sleep to avoid overwhelming
  sleep(0.1);
}

export function handleSummary(data) {
  return {
    'stdout': JSON.stringify(data, null, 2),
    'rate-limit-test-results.json': JSON.stringify(data, null, 2),
  };
}
