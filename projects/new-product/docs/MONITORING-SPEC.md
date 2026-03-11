# Monitoring & Alerting Specification — AMC MVP Beta Launch

**Owner:** faintech-devops (implementation), faintech-pm (coordination)
**Target Launch:** March 24, 2026
**Priority:** P1 (launch blocker if incomplete)
**Status:** ✅ Ready for implementation

---

## Overview

This document defines monitoring and alerting requirements for the Agent Memory Cloud (AMC) MVP beta launch. Devops will implement these alerts to ensure launch day observability and rapid incident response.

**Scope:**
- Application health monitoring
- API performance monitoring
- Business metrics tracking
- Infrastructure health monitoring
- Alert notification routing

---

## Alert Categories

### 1. Critical (P0) — Immediate Action Required

| Alert | Condition | Threshold | Notification | Escalation |
|-------|-----------|------------|---------------|-------------|
| **API Down** | `up{job="amc-backend"}` | = 0 | Slack #amc-ops, PagerDuty | CTO + CEO (5 min) |
| **High Error Rate** | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` | > 1% | Slack #amc-ops, email devops | CTO (10 min) |
| **Database Down** | `pg_up{cluster="amc"}` | = 0 | Slack #amc-ops, PagerDuty | CTO + CEO (5 min) |
| **Rate Limit Exhaustion** | `rate_limit_exceeded_total` | > 10/min | Slack #amc-ops | CTO (15 min) |
| **Storage Exhausted** | `disk_used_percent` | > 90% | Slack #amc-ops, email devops | CTO (1 hour) |

### 2. Warning (P1) — Monitor Closely

| Alert | Condition | Threshold | Notification | Escalation |
|-------|-----------|------------|---------------|-------------|
| **High Latency P99** | `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` | > 200ms | Slack #amc-ops | PM (1 hour) |
| **High Latency P95** | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` | > 100ms | Slack #amc-ops | PM (2 hours) |
| **Elevated Error Rate** | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` | > 0.5% | Slack #amc-ops | PM (2 hours) |
| **Queue Backlog** | `queue_length` | > 100 | Slack #amc-ops | DevOps (1 hour) |
| **Memory High** | `process_resident_memory_bytes` | > 2GB | Slack #amc-ops | DevOps (2 hours) |

### 3. Info (P2) — Track Trends

| Alert | Condition | Threshold | Notification | Escalation |
|-------|-----------|------------|---------------|-------------|
| **Traffic Spike** | `rate(http_requests_total[5m])` | > 2x baseline | Slack #amc-ops | PM (daily) |
| **New User Signup** | `beta_signup_total` | > 5/day | Slack #amc-ops | PM (daily) |
| **Payment Method Added** | `payment_method_added_total` | Any | Slack #amc-ops | CEO (immediate) |
| **Support Ticket Created** | `support_ticket_created_total` | Any | Email support team | PM (daily) |

---

## Grafana Dashboards

### Dashboard 1: API Health & Performance

**Panels:**
1. **Request Rate** — `rate(http_requests_total[5m])` (timeseries, last 1h)
2. **Error Rate** — `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` (gauge, last 5m)
3. **Latency P50/P95/P99** — `histogram_quantile(0.5/0.95/0.99, rate(http_request_duration_seconds_bucket[5m]))` (timeseries, last 1h)
4. **Request Volume** — `sum(increase(http_requests_total[5m]))` (timeseries, last 1h)
5. **Status Codes** — `sum by (status) (rate(http_requests_total[5m]))` (timeseries, last 1h)
6. **Uptime** — `up{job="amc-backend"}` (stat)

### Dashboard 2: Business Metrics

**Panels:**
1. **Total Beta Users** — `beta_signup_total` (stat)
2. **Active Users (7d)** — `active_users_7d` (stat)
3. **API Keys Created** — `api_key_created_total` (stat)
4. **Memories Written** — `memories_written_total` (timeseries, last 7d)
5. **Searches Performed** — `searches_performed_total` (timeseries, last 7d)
6. **Payment Methods Added** — `payment_method_added_total` (stat)
7. **Conversion Rate** — `payment_method_added_total / beta_signup_total` (gauge)

### Dashboard 3: Database Health

**Panels:**
1. **Connection Pool Usage** — `pg_stat_activity_count{state="active"}` / `max_connections` (gauge)
2. **Query Duration P99** — `histogram_quantile(0.99, pg_query_duration_seconds)` (timeseries, last 1h)
3. **Slow Queries (>1s)** — `rate(pg_slow_queries_total[5m])` (timeseries, last 1h)
4. **Cache Hit Ratio** — `pg_stat_database_blks_hit / (pg_stat_database_blks_hit + pg_stat_database_blks_read)` (gauge)
5. **Database Size** — `pg_database_size_bytes` (timeseries, last 7d)
6. **Replication Lag** — `pg_replication_lag_seconds` (timeseries, last 1h)

### Dashboard 4: Infrastructure Health

**Panels:**
1. **CPU Usage** — `rate(process_cpu_seconds_total[5m])` (gauge)
2. **Memory Usage** — `process_resident_memory_bytes` (timeseries, last 1h)
3. **Disk Usage** — `disk_used_percent` (gauge)
4. **Network I/O** — `rate(network_receive_bytes_total[5m])` + `rate(network_transmit_bytes_total[5m])` (timeseries, last 1h)
5. **Open File Descriptors** — `process_open_fds` (gauge)

---

## Prometheus Metrics Exposition

### Required Application Metrics

The AMC backend MUST expose these metrics on `/metrics` endpoint:

```yaml
# API Metrics
- http_requests_total{method, path, status}
- http_request_duration_seconds{method, path, quantile}
- http_requests_in_progress{method, path}

# Business Metrics
- beta_signup_total
- api_key_created_total{plan}
- memories_written_total{agent_id}
- searches_performed_total{user_id, agent_id}
- payment_method_added_total{user_id}
- support_ticket_created_total{user_id}

# Database Metrics
- pg_stat_activity_count{state}
- pg_query_duration_seconds{quantile}
- pg_slow_queries_total
- pg_database_size_bytes

# Infrastructure Metrics
- process_cpu_seconds_total
- process_resident_memory_bytes
- process_open_fds
- disk_used_percent{mount}
```

### OpenMetrics Format

All metrics MUST follow OpenMetrics 1.0 specification:
- Use `TOTAL` suffix for counters
- Use `SECONDS` suffix for durations
- Include `help` and `type` metadata
- Export labeled metrics (no unlabeled `promhttp_metric_handler`)

---

## Alert Routing

### Slack Channels

| Channel | Purpose | Members |
|----------|---------|----------|
| `#amc-ops` | All alerts | CTO, DevOps, PM |
| `#amc-incident` | P0 incidents only | CTO, DevOps, PM, CEO |

### PagerDuty Escalation Policy

**Service:** `amc-mvp-beta`

**Escalation Chain:**
1. Level 1 (0-5 min): DevOps on-call
2. Level 2 (5-15 min): CTO
3. Level 3 (15+ min): CEO

**On-Call Rotation:**
- Week 1 (Mar 17-23): faintech-devops
- Week 2 (Mar 24-30): faintech-cto
- Post-beta: TBD based on staffing

### Email Notifications

| Alert Type | Recipients | Frequency |
|-----------|-----------|-----------|
| P0 critical | devops@faintech.com, cto@faintech.com | Immediate |
| P1 warning | pm@faintech.com | Within 1 hour |
| Daily digest | team@faintech.com | 9:00 AM daily |

---

## Launch Day Monitoring Checklist

**Pre-Launch (24h before):**
- [ ] Verify all dashboards are rendering correctly
- [ ] Test alert notifications (send test alert to all channels)
- [ ] Confirm PagerDuty on-call rotation is set
- [ ] Baseline metrics (capture "normal" traffic patterns)
- [ ] Validate Prometheus scraping is working
- [ ] Test Grafana login for all team members

**Launch Moment (Mar 24, 9:00 AM):**
- [ ] All hands in `#amc-ops` Slack channel
- [ ] Grafana dashboards open and visible
- [ ] PagerDuty acknowledged on-call
- [ ] Monitoring refresh rate set to 15s
- [ ] Runbook available and accessible

**Post-Launch (First 4 hours):**
- [ ] Monitor error rate < 0.1%
- [ ] Monitor P99 latency < 200ms
- [ ] Verify no database connection issues
- [ ] Track first beta user signup
- [ ] Confirm payment method added event fires
- [ ] Document any anomalies in incident log

---

## Incident Response Playbook

### P0: API Down

**Symptoms:**
- `up{job="amc-backend"} = 0`
- 100% error rate on health checks
- No traffic in dashboards

**Immediate Actions (0-5 min):**
1. Check Slack #amc-ops for error logs
2. SSH to backend server: `systemctl status amc-backend`
3. Check application logs: `journalctl -u amc-backend -f`
4. Verify PostgreSQL is running: `systemctl status postgresql`
5. Check disk space: `df -h`

**Escalation:**
- If unresolved in 5 min → Alert CTO
- If unresolved in 15 min → Alert CEO, consider rollback

### P1: High Error Rate

**Symptoms:**
- Error rate > 1%
- Elevated 5xx responses
- User complaints in support

**Investigation:**
1. Identify failing endpoint: `sum by (path) (rate(http_requests_total{status=~"5.."}[5m]))`
2. Check application logs for stack traces
3. Verify database connectivity
4. Check rate limit configuration

**Actions:**
- If database issue → Restart PostgreSQL if needed
- If rate limit issue → Increase limits temporarily
- If code issue → Hotfix via feature flag

### P2: High Latency

**Symptoms:**
- P99 latency > 200ms
- P95 latency > 100ms
- User reports slow responses

**Investigation:**
1. Check database query performance: `pg_query_duration_seconds`
2. Review slow query log
3. Check database connection pool usage
4. Verify no CPU/memory saturation

**Actions:**
- Add database indexes if needed
- Tune connection pool size
- Implement query result caching (Redis)
- Scale horizontally if needed

---

## Metrics Retention & Storage

| Metric Type | Retention | Resolution |
|-------------|------------|------------|
| API metrics | 30 days | 15s |
| Business metrics | 90 days | 1m |
| Database metrics | 30 days | 15s |
| Infrastructure metrics | 30 days | 15s |
| Alert history | 1 year | 1m |

**Storage Estimation:**
- Prometheus: ~100 GB/month
- Grafana: Negligible (time series DB is Prometheus)
- Logs: ~50 GB/month (30-day retention in Logflare)

---

## Success Criteria

**Launch Day (Mar 24):**
- [ ] All P0 alerts implemented and tested
- [ ] All Grafana dashboards created and shared
- [ ] PagerDuty rotation configured
- [ ] Runbook documented and accessible
- [ ] Team trained on monitoring tools

**Post-Launch (Week 1):**
- [ ] Zero P0 incidents > 15 min resolution
- [ ] Uptime > 99.9%
- [ ] P99 latency < 200ms (sustained)
- [ ] Daily metrics email delivered on time
- [ ] All team members actively using dashboards

---

## Next Steps for DevOps

1. **Implement Prometheus scraping:**
   - Add AMC backend to `prometheus.yml`
   - Verify `/metrics` endpoint is accessible
   - Test metric labels and types

2. **Create Grafana dashboards:**
   - Import dashboard JSON files (see `dashboards/` directory)
   - Share dashboard links with team
   - Set up dashboard folder structure

3. **Configure Alertmanager:**
   - Set up Slack webhook integration
   - Configure PagerDuty integration
   - Test alert routing with mock metrics

4. **Document runbook:**
   - Create incident response templates in Notion
   - Add escalation contacts
   - Include rollback procedures

5. **Launch day dry-run:**
   - Schedule 30-min rehearsal on Mar 23
   - Simulate P0 incident
   - Validate alert flow and response time

---

## Questions for CTO Review

1. Do we have Prometheus and Grafana infrastructure in place for this project?
2. What is our PagerDuty account status? Need setup?
3. Should we use separate alerting for staging vs production?
4. Do we need Datadog or New Relic in addition to Prometheus?
5. What is our budget for monitoring infrastructure?

---

**Created:** 2026-03-11T02:45:00Z
**Owner:** faintech-devops (implementation)
**Review Required:** faintech-cto, faintech-ciso
**Next Milestone:** Complete by March 20, 2026 (4 days before launch)
