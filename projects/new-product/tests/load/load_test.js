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

// Custom metrics
const errorRate = new Rate('errors');
const latencyTrend = new Trend('latency');
const requestCounter = new Counter('requests');

export const options = {
  stages: [
    { duration: '30s', target: 100 },
    { duration: '1m', target: 100 },
    { duration: '30s', target: 500 },
    { duration: '1m', target: 500 },
    { duration: '10s', target: 1000 },
    { duration: '30s', target: 1000 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<200'],
    errors: ['rate<0.001'],
    http_req_failed: ['rate<0.001'],
  },
};

export default function () {
  const auth = registerAndLogin(__VU);
  if (!auth.ok) {
    errorRate.add(1);
    return;
  }

  const headers = { headers: authHeaders(auth.token) };
  const agentId = `load-agent-${__VU}`;
  const projectId = `load-project-${Math.floor(__VU % 10)}`;

  testHealthEndpoint();
  testCreateMemory(agentId, projectId, headers);
  testListMemories(agentId, projectId, headers);
  testKeywordSearch(projectId, headers);

  sleep(1);
}

function testHealthEndpoint() {
  const res = http.get(`${BASE_URL}/health`);
  const success = check(res, { 'health check status is 200': (r) => r.status === 200 });
  recordMetrics(res, !success);
}

function testCreateMemory(agentId, projectId, params) {
  const payload = JSON.stringify({
    agent_id: agentId,
    project_id: projectId,
    memory_type: 'learning',
    content: `Load test memory at ${new Date().toISOString()}`,
    tags: ['load-test', 'performance'],
    metadata: { test_run: true, vu: __VU, iter: __ITER },
  });

  const res = http.post(`${API_PREFIX}/memories`, payload, params);
  const success = check(res, {
    'create memory status is 201': (r) => r.status === 201,
    'create memory has id': (r) => JSON.parse(r.body).id !== undefined,
  });
  recordMetrics(res, !success);
}

function testListMemories(agentId, projectId, params) {
  const res = http.get(`${API_PREFIX}/memories?agent_id=${agentId}&project_id=${projectId}&page_size=20`, params);
  const success = check(res, {
    'list memories status is 200': (r) => r.status === 200,
    'list memories has array': (r) => Array.isArray(JSON.parse(r.body).memories),
  });
  recordMetrics(res, !success);
}

function testKeywordSearch(projectId, params) {
  const res = http.get(`${API_PREFIX}/search/keyword?q=Load%20test&project_id=${projectId}&page_size=10`, params);
  const success = check(res, {
    'keyword search status is 200': (r) => r.status === 200,
    'keyword search has results array': (r) => Array.isArray(JSON.parse(r.body).results),
  });
  recordMetrics(res, !success);
}

function recordMetrics(res, isError = false) {
  errorRate.add(isError ? 1 : 0);
  latencyTrend.add(res.timings.duration);
  requestCounter.add(1);
}
