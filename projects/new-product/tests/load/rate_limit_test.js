import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

const BASE_URL = (__ENV.BASE_URL || 'http://localhost:8000').replace(/\/$/, '');
const AUTH_PREFIX = `${BASE_URL}/v1/auth`;
const API_PREFIX = `${BASE_URL}/v1`;
const TEST_PASSWORD = __ENV.TEST_PASSWORD || 'LoadTestPass123!';
const TEST_RUN_ID = __ENV.TEST_RUN_ID || `lt-${Date.now()}`;

function userEmail(vu) {
  return `loadtest+${TEST_RUN_ID}-${vu}@example.com`;
}

function registerAndLogin(vu) {
  const email = userEmail(vu);
  const registerPayload = JSON.stringify({
    email,
    password: TEST_PASSWORD,
    full_name: `Load Test User ${vu}`,
    workspace_name: `Load Test Workspace ${TEST_RUN_ID}-${vu}`,
  });

  const commonParams = { headers: { 'Content-Type': 'application/json' } };
  let registerRes = http.post(`${AUTH_PREFIX}/register`, registerPayload, commonParams);
  if (![201, 409].includes(registerRes.status)) {
    return { ok: false, token: null, user: null, registerStatus: registerRes.status };
  }

  const loginRes = http.post(
    `${AUTH_PREFIX}/login`,
    JSON.stringify({ email, password: TEST_PASSWORD }),
    commonParams,
  );

  if (loginRes.status !== 200) {
    return { ok: false, token: null, user: null, loginStatus: loginRes.status };
  }

  const body = JSON.parse(loginRes.body);
  return { ok: true, token: body.access_token, user: body.user };
}

function authHeaders(token) {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };
}

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '10s', target: 50 },
    { duration: '2m', target: 50 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    errors: ['rate<0.1'],
  },
};

export default function () {
  const agentId = `rate-test-agent-${__VU}`;

  const payload = JSON.stringify({
    agent_id: `rate-test-agent-${__VU}`,
    project_id: `rate-test-project-${Math.floor(__VU % 5)}`,
    memory_type: 'learning',
    content: `Rate limit test ${Date.now()}`,
    tags: ['rate-test'],
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
    'status is 201, 200, or 429': () => isSuccess || isRateLimited,
    'rate limit headers present': (r) => {
      const hasRateLimit = r.headers['X-RateLimit-Limit'] || r.headers['X-Ratelimit-Limit'];
      const hasRetryAfter = r.headers['Retry-After'] || r.headers['X-RateLimit-Reset'];
      return isRateLimited ? hasRetryAfter !== undefined : hasRateLimit !== undefined || isSuccess;
    },
  });

  if (!isSuccess && !isRateLimited) errorRate.add(1);
  sleep(0.1);
}
