import http from 'k6/http';
import { check } from 'k6';

// Spike test - sudden load increase
export const options = {
  stages: [
    // Start with 10 users
    { duration: '1m', target: 10 },
    // Spike to 1000 users in 5 seconds
    { duration: '5s', target: 1000 },
    // Stay at 1000 for 10 seconds
    { duration: '10s', target: 1000 },
    // Quick ramp down
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<500'], // Allow higher latency during spike
    http_req_failed: ['rate<0.1'], // Allow up to 10% failures during spike
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  const endpoints = [
    () => http.get(`${BASE_URL}/health`),
    () => http.get(`${BASE_URL}/api/v1/memories/agent/test-agent-${__VU}?limit=10`),
    () => http.post(
      `${BASE_URL}/api/v1/memories/`,
      JSON.stringify({
        agent_id: `spike-agent-${__VU}`,
        project_id: 'spike-test',
        type: 'observation',
        content: `Spike test ${Date.now()}`,
      }),
      { headers: { 'Content-Type': 'application/json' } }
    ),
  ];

  // Randomly select an endpoint to test
  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const res = endpoint();

  check(res, {
    'status is 2xx or 429': (r) => r.status >= 200 && r.status < 300 || r.status === 429,
  });
}

export function handleSummary(data) {
  return {
    'stdout': JSON.stringify(data, null, 2),
    'spike-test-results.json': JSON.stringify(data, null, 2),
  };
}
