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

export const options = {
  stages: [
    { duration: '1m', target: 10 },
    { duration: '5s', target: 1000 },
    { duration: '10s', target: 1000 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<500'],
    http_req_failed: ['rate<0.1'],
  },
};

export default function () {
  const auth = registerAndLogin(__VU);
  if (!auth.ok) return;

  const headers = { headers: authHeaders(auth.token) };
  const agentId = `spike-agent-${__VU}`;
  const projectId = `spike-project-${Math.floor(__VU % 20)}`;

  const endpoints = [
    () => http.get(`${BASE_URL}/health`),
    () => http.get(`${API_PREFIX}/memories?agent_id=${agentId}&project_id=${projectId}&page_size=10`, headers),
    () => http.post(
      `${API_PREFIX}/memories`,
      JSON.stringify({
        agent_id: agentId,
        project_id: projectId,
        memory_type: 'observation',
        content: `Spike test ${Date.now()}`,
        tags: ['spike-test'],
        metadata: { vu: __VU, iter: __ITER },
      }),
      headers,
    ),
  ];

  const endpoint = endpoints[Math.floor(Math.random() * endpoints.length)];
  const res = endpoint();
  check(res, {
    'status is 2xx or 429': (r) => (r.status >= 200 && r.status < 300) || r.status === 429,
  });
}
