"""Tests for observability endpoints and structured logging utilities."""

import json
import logging
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from app.core.database import Base, get_db
from app.models.workspace import Workspace
from app.core.logging import JSONFormatter, setup_logging, get_logger
from app.core.metrics import MetricsStore


# ---------------------------------------------------------------------------
# Test database helpers
# ---------------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
async def db_session():
    """Ephemeral in-memory DB for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        workspace = Workspace(
            id="default-workspace",
            name="Default Workspace",
            slug="default-workspace",
        )
        session.add(workspace)
        await session.commit()
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session):
    """HTTP test client wired to the in-memory DB."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# /health endpoint
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_health_returns_200(client):
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_includes_required_fields(client):
    data = (await client.get("/health")).json()
    assert "status" in data
    assert "version" in data
    assert "uptime_seconds" in data
    assert "database" in data


@pytest.mark.asyncio
async def test_health_database_ok(client):
    data = (await client.get("/health")).json()
    assert data["database"]["status"] == "ok"
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_uptime_positive(client):
    data = (await client.get("/health")).json()
    assert data["uptime_seconds"] >= 0


# ---------------------------------------------------------------------------
# /metrics endpoint
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_metrics_returns_200(client):
    response = await client.get("/metrics")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_metrics_includes_required_fields(client):
    data = (await client.get("/metrics")).json()
    assert "uptime_seconds" in data
    assert "requests_total" in data
    assert "errors_total" in data
    assert "latency_ms" in data
    assert "endpoints" in data


@pytest.mark.asyncio
async def test_metrics_requests_count_increases(client):
    # Make a couple of requests then verify counter went up
    await client.get("/health")
    await client.get("/health")
    data = (await client.get("/metrics")).json()
    assert data["requests_total"] >= 2


@pytest.mark.asyncio
async def test_metrics_latency_structure(client):
    await client.get("/health")
    data = (await client.get("/metrics")).json()
    lat = data["latency_ms"]
    assert "p50" in lat
    assert "p95" in lat
    assert "p99" in lat


# ---------------------------------------------------------------------------
# JSONFormatter unit tests
# ---------------------------------------------------------------------------


def test_json_formatter_produces_valid_json():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="hello world",
        args=(),
        exc_info=None,
    )
    output = formatter.format(record)
    parsed = json.loads(output)  # must not raise
    assert parsed["message"] == "hello world"
    assert parsed["level"] == "INFO"


def test_json_formatter_includes_timestamp():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname="",
        lineno=0,
        msg="warn",
        args=(),
        exc_info=None,
    )
    parsed = json.loads(formatter.format(record))
    assert "timestamp" in parsed


def test_json_formatter_merges_extra():
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="event",
        args=(),
        exc_info=None,
    )
    record.extra = {"request_id": "abc-123", "duration_ms": 42.5}
    parsed = json.loads(formatter.format(record))
    assert parsed["request_id"] == "abc-123"
    assert parsed["duration_ms"] == 42.5


def test_json_formatter_includes_exception_info():
    formatter = JSONFormatter()
    try:
        raise ValueError("boom")
    except ValueError:
        import sys

        exc_info = sys.exc_info()

    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname="",
        lineno=0,
        msg="error occurred",
        args=(),
        exc_info=exc_info,
    )
    parsed = json.loads(formatter.format(record))
    assert "exception" in parsed
    assert parsed["exception"]["type"] == "ValueError"


# ---------------------------------------------------------------------------
# MetricsStore unit tests
# ---------------------------------------------------------------------------


def test_metrics_store_initial_state():
    store = MetricsStore()
    snap = store.snapshot()
    assert snap["requests_total"] == 0
    assert snap["errors_total"] == 0
    assert snap["uptime_seconds"] >= 0


def test_metrics_store_records_request():
    store = MetricsStore()
    store.record("/v1/memories", "GET", 200, 50.0)
    snap = store.snapshot()
    assert snap["requests_total"] == 1
    assert snap["errors_total"] == 0


def test_metrics_store_counts_errors():
    store = MetricsStore()
    store.record("/v1/memories", "POST", 422, 30.0)
    snap = store.snapshot()
    assert snap["errors_total"] == 1


def test_metrics_store_latency_percentiles():
    store = MetricsStore()
    for i in range(1, 101):
        store.record("/v1/memories", "GET", 200, float(i))
    snap = store.snapshot()
    # With 100 samples 1..100 ms, p50 should be around 50
    assert snap["latency_ms"]["p50"] is not None
    assert snap["latency_ms"]["p95"] is not None
    assert snap["latency_ms"]["p99"] is not None


def test_metrics_store_endpoint_breakdown():
    store = MetricsStore()
    store.record("/v1/memories", "GET", 200, 10.0)
    store.record("/v1/search", "POST", 200, 20.0)
    snap = store.snapshot()
    paths = {e["path"] for e in snap["endpoints"]}
    assert "/v1/memories" in paths
    assert "/v1/search" in paths


def test_get_logger_returns_logger():
    logger = get_logger("test.obs")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.obs"
