import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const latencyTrend = new Trend('latency');
const requestCounter = new Counter('requests');

// Test configuration
export const options = {
  stages: [
    // Ramp up to 100 users over 30 seconds
    { duration: '30s', target: 100 },
    // Stay at 100 users for 1 minute
    { duration: '1m', target: 100 },
    // Ramp up to 500 users over 30 seconds
    { duration: '30s', target: 500 },
    // Stay at 500 users for 1 minute
    { duration: '1m', target: 500 },
    // Spike to 1000 users over 10 seconds
    { duration: '10s', target: 1000 },
    // Stay at 1000 users for 30 seconds
    { duration: '30s', target: 1000 },
    // Ramp down to 0 users
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<100'], // 99% of requests must complete < 100ms
    errors: ['rate<0.05'], // Error rate must be < 5%
    http_req_failed: ['rate<0.05'], // Failed request rate < 5%
  },
};

// Base URL - adjust if needed
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

// Test data
const testAgents = ['agent-1', 'agent-2', 'agent-3', 'agent-4', 'agent-5'];
const testProjects = ['project-alpha', 'project-beta', 'project-gamma'];
const testTasks = ['task-001', 'task-002', 'task-003'];

export default function () {
  // Randomly select test data
  const agentId = testAgents[Math.floor(Math.random() * testAgents.length)];
  const projectId = testProjects[Math.floor(Math.random() * testProjects.length)];
  const taskId = testTasks[Math.floor(Math.random() * testTasks.length)];

  // Test 1: Health check
  testHealthEndpoint();

  // Test 2: Create memory
  const memoryId = testCreateMemory(agentId, projectId, taskId);

  // Test 3: Search memories
  testSearchMemories(agentId);

  // Test 4: Get agent memories
  testGetAgentMemories(agentId);

  // Test 5: Get task memories
  testGetTaskMemories(projectId, taskId);

  // Think time
  sleep(1);
}

function testHealthEndpoint() {
  const res = http.get(`${BASE_URL}/health`);

  check(res, {
    'health check status is 200': (r) => r.status === 200,
  });

  recordMetrics(res);
}

function testCreateMemory(agentId, projectId, taskId) {
  const payload = JSON.stringify({
    agent_id: agentId,
    project_id: projectId,
    task_id: taskId,
    type: 'observation',
    content: `Load test memory at ${new Date().toISOString()}`,
    tags: ['load-test', 'performance'],
    metadata: {
      test_run: true,
      timestamp: Date.now(),
    },
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(`${BASE_URL}/api/v1/memories/`, payload, params);

  const success = check(res, {
    'create memory status is 201': (r) => r.status === 201,
    'create memory has id': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.id !== undefined;
      } catch {
        return false;
      }
    },
  });

  recordMetrics(res, !success);

  if (success) {
    try {
      const body = JSON.parse(res.body);
      return body.id;
    } catch {
      return null;
    }
  }
  return null;
}

function testSearchMemories(agentId) {
  const payload = JSON.stringify({
    query: 'load test',
    agent_id: agentId,
    limit: 10,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(`${BASE_URL}/api/v1/memories/search`, payload, params);

  const success = check(res, {
    'search memories status is 200': (r) => r.status === 200,
    'search memories has results': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.memories !== undefined && Array.isArray(body.memories);
      } catch {
        return false;
      }
    },
  });

  recordMetrics(res, !success);
}

function testGetAgentMemories(agentId) {
  const res = http.get(`${BASE_URL}/api/v1/memories/agent/${agentId}?limit=20`);

  const success = check(res, {
    'get agent memories status is 200': (r) => r.status === 200,
    'get agent memories has results': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.memories !== undefined;
      } catch {
        return false;
      }
    },
  });

  recordMetrics(res, !success);
}

function testGetTaskMemories(projectId, taskId) {
  const res = http.get(`${BASE_URL}/api/v1/memories/task/${projectId}/${taskId}?limit=50`);

  const success = check(res, {
    'get task memories status is 200': (r) => r.status === 200,
    'get task memories has results': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.memories !== undefined;
      } catch {
        return false;
      }
    },
  });

  recordMetrics(res, !success);
}

function recordMetrics(res, isError = false) {
  errorRate.add(isError ? 1 : 0);
  latencyTrend.add(res.timings.duration);
  requestCounter.add(1);
}

export function handleSummary(data) {
  return {
    'stdout': textSummary(data, { indent: ' ', enableColors: true }),
    'load-test-results.json': JSON.stringify(data, null, 2),
  };
}

function textSummary(data, options = {}) {
  const indent = options.indent || '  ';
  const colors = options.enableColors || false;

  let summary = '\n' + '='.repeat(60) + '\n';
  summary += 'LOAD TEST SUMMARY\n';
  summary += '='.repeat(60) + '\n\n';

  // Overall metrics
  summary += `${indent}Total Requests: ${data.metrics.requests?.values?.count || 0}\n`;
  summary += `${indent}Request Rate: ${data.metrics.http_reqs?.values?.rate?.toFixed(2) || 0} req/s\n`;
  summary += `${indent}Error Rate: ${(data.metrics.errors?.values?.rate * 100 || 0).toFixed(2)}%\n`;
  summary += '\n';

  // Latency metrics
  summary += `${indent}Latency (ms):\n`;
  summary += `${indent}${indent}Avg: ${data.metrics.http_req_duration?.values?.avg?.toFixed(2) || 0}\n`;
  summary += `${indent}${indent}Min: ${data.metrics.http_req_duration?.values?.min?.toFixed(2) || 0}\n`;
  summary += `${indent}${indent}Max: ${data.metrics.http_req_duration?.values?.max?.toFixed(2) || 0}\n`;
  summary += `${indent}${indent}P90: ${data.metrics.http_req_duration?.values?.['p(90)']?.toFixed(2) || 0}\n`;
  summary += `${indent}${indent}P95: ${data.metrics.http_req_duration?.values?.['p(95)']?.toFixed(2) || 0}\n`;
  summary += `${indent}${indent}P99: ${data.metrics.http_req_duration?.values?.['p(99)']?.toFixed(2) || 0}\n`;
  summary += '\n';

  // Threshold checks
  summary += `${indent}Threshold Checks:\n`;
  if (data.root_group?.checks) {
    const checks = data.root_group.checks;
    const passed = checks.filter(c => c.passes > 0 && c.fails === 0).length;
    const total = checks.length;
    summary += `${indent}${indent}Passed: ${passed}/${total}\n`;
  }

  summary += '\n' + '='.repeat(60) + '\n';

  return summary;
}
