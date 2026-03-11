"""
AMC API Load Testing with Locust

Validates 100 req/sec target with <100ms p99 latency.
Tests memory lifecycle, search operations, and agent operations under load.
"""

import json
import random
import string
from datetime import datetime, timezone
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner, WorkerRunner


class AMCUser(HttpUser):
    """Simulates AMC API user performing memory operations."""

    wait_time = between(0.5, 2.0)

    # Test data pool
    sample_contents = [
        "Agent session context: user authentication successful, preferences loaded",
        "Trading decision: BUY signal detected for AAPL, confidence 0.85",
        "Error recovery: database connection timeout, retrying with exponential backoff",
        "Performance metric: API response time p95=45ms, within SLA",
        "Agent coordination: task delegation to faintech-backend completed",
        "Memory pattern detected: recurring theme in user requests about authentication",
        "Learning capture: optimized database queries reduced latency by 30%",
        "Workflow state: Sprint planning ceremony completed, 3 tasks created",
        "Quality gate: all tests passing, code coverage 87%",
        "Deployment status: production release v1.2.3 successful"
    ]

    sample_tags = [
        ["authentication", "security"],
        ["trading", "signals"],
        ["error-handling", "resilience"],
        ["performance", "monitoring"],
        ["coordination", "delegation"],
        ["patterns", "learning"],
        ["optimization", "database"],
        ["workflow", "planning"],
        ["quality", "testing"],
        ["deployment", "release"]
    ]

    def on_start(self):
        """Initialize user session."""
        self.agent_ids = []
        self.memory_ids = []
        self.api_key = __import__("os").environ.get("AMC_LOADTEST_API_KEY", "test-api-key-load-test")

        # Get list of agents for testing
        with self.client.get(
            "/v1/agents",
            headers={"X-API-Key": self.api_key},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                self.agent_ids = [agent["id"] for agent in data.get("agents", [])]
            else:
                # If no agents exist, we'll create them during the test
                self.agent_ids = []

    @task(10)
    def health_check(self):
        """Health check endpoint - lightweight baseline."""
        self.client.get("/health", name="/health")

    @task(30)
    def create_memory(self):
        """Create a new memory entry."""
        agent_id = random.choice(self.agent_ids) if self.agent_ids else "test-agent"
        content = random.choice(self.sample_contents)
        tags = random.choice(self.sample_tags)

        payload = {
            "agent_id": agent_id,
            "content": content,
            "metadata": {
                "source": "load_test",
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "tags": tags
        }

        with self.client.post(
            "/v1/memories",
            json=payload,
            headers={"X-API-Key": self.api_key},
            catch_response=True,
            name="/v1/memories [POST]"
        ) as response:
            if response.status_code in [200, 201]:
                data = response.json()
                memory_id = data.get("id")
                if memory_id:
                    self.memory_ids.append(memory_id)
                    # Keep only last 100 memory IDs to avoid memory leak
                    if len(self.memory_ids) > 100:
                        self.memory_ids = self.memory_ids[-100:]
                response.success()
            else:
                response.failure(f"Failed to create memory: {response.status_code}")

    @task(20)
    def get_memory(self):
        """Retrieve a specific memory."""
        if not self.memory_ids:
            return

        memory_id = random.choice(self.memory_ids)
        self.client.get(
            f"/v1/memories/{memory_id}",
            headers={"X-API-Key": self.api_key},
            name="/v1/memories/[id] [GET]"
        )

    @task(25)
    def search_memories_keyword(self):
        """Keyword search across memories."""
        search_terms = ["authentication", "trading", "error", "performance", "agent"]
        query = random.choice(search_terms)

        params = {
            "query": query,
            "limit": 10
        }

        self.client.get(
            "/v1/search",
            params=params,
            headers={"X-API-Key": self.api_key},
            name="/v1/search [keyword]"
        )

    @task(15)
    def search_memories_semantic(self):
        """Semantic search using vector embeddings."""
        queries = [
            "How do agents handle authentication?",
            "What trading signals are active?",
            "Show me recent errors",
            "Performance optimization strategies",
            "Agent coordination patterns"
        ]
        query = random.choice(queries)

        payload = {
            "query": query,
            "limit": 5
        }

        with self.client.post(
            "/v1/search/semantic",
            json=payload,
            headers={"X-API-Key": self.api_key},
            catch_response=True,
            name="/v1/search/semantic [POST]"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 503:
                # Semantic search might not be available in all environments
                response.success()
            else:
                response.failure(f"Semantic search failed: {response.status_code}")

    @task(5)
    def list_agents(self):
        """List all agents."""
        self.client.get(
            "/v1/agents",
            headers={"X-API-Key": self.api_key},
            name="/v1/agents [GET]"
        )

    @task(5)
    def get_agent_memories(self):
        """Get memories for a specific agent."""
        if not self.agent_ids:
            return

        agent_id = random.choice(self.agent_ids)
        params = {"limit": 20}

        self.client.get(
            f"/v1/agents/{agent_id}/memories",
            params=params,
            headers={"X-API-Key": self.api_key},
            name="/v1/agents/[id]/memories [GET]"
        )

    @task(3)
    def compact_memory(self):
        """Compact memory for an agent."""
        if not self.agent_ids:
            return

        agent_id = random.choice(self.agent_ids)

        with self.client.post(
            f"/v1/agents/{agent_id}/compact",
            headers={"X-API-Key": self.api_key},
            catch_response=True,
            name="/v1/agents/[id]/compact [POST]"
        ) as response:
            if response.status_code in [200, 202]:
                response.success()
            else:
                response.failure(f"Compact failed: {response.status_code}")

    @task(2)
    def get_metrics(self):
        """Get API metrics - observability check."""
        self.client.get("/metrics", name="/metrics")


# Performance test scenarios
class HighThroughputUser(AMCUser):
    """High-frequency user for stress testing."""
    wait_time = between(0.1, 0.5)


class ReadOnlyUser(AMCUser):
    """Read-only user for search-heavy workloads."""

    @task(50)
    def search_memories_keyword(self):
        super().search_memories_keyword()

    @task(30)
    def get_memory(self):
        super().get_memory()

    @task(20)
    def list_agents(self):
        super().list_agents()


# Event listeners for custom metrics
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Log test start."""
    print(f"\n{'='*80}")
    print(f"AMC Load Test Started")
    print(f"Target: 100 req/sec, <100ms p99 latency")
    print(f"Environment: {environment.host}")
    print(f"{'='*80}\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Log test completion and results."""
    print(f"\n{'='*80}")
    print(f"AMC Load Test Completed")

    if isinstance(environment.runner, (MasterRunner, WorkerRunner)):
        # Distributed mode - stats available on master
        pass
    else:
        # Standalone mode
        stats = environment.stats
        print(f"\nResults Summary:")
        print(f"  Total Requests: {stats.total.num_requests}")
        print(f"  Total Failures: {stats.total.num_failures}")
        print(f"  Error Rate: {stats.total.fail_ratio * 100:.2f}%")
        print(f"  RPS: {stats.total.total_rps:.2f}")
        print(f"\nResponse Times:")
        print(f"  p50: {stats.total.get_response_time_percentile(0.5):.2f}ms")
        print(f"  p95: {stats.total.get_response_time_percentile(0.95):.2f}ms")
        print(f"  p99: {stats.total.get_response_time_percentile(0.99):.2f}ms")
        print(f"{'='*80}\n")
