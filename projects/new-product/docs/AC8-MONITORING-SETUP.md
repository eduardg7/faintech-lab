# AC8: Monitoring Setup & Alerting Configuration

**Task ID:** AMC-MVP-117-AC8
**Parent Task:** AMC-MVP-117 (Launch Prep Beta Mar 24)
**Owner:** faintech-devops
**Deadline:** 2026-03-20 (4 days before launch)
**Source:** MONITORING-SPEC.md
**Status:** Ready for Implementation

---

## Objective

Configure production-grade monitoring and alerting for AMC MVP beta launch. Ensure full observability and rapid incident response capability on launch day (March 24, 2026).

---

## Acceptance Criteria

### AC8.1: P0 Critical Alerts Implemented
- [ ] API Down alert: `up{job="amc-backend"} = 0` → Slack #amc-ops + PagerDuty → Escalate to CTO+CEO (5 min)
- [ ] High Error Rate alert: error rate > 1% → Slack #amc-ops + email devops → Escalate to CTO (10 min)
- [ ] Database Down alert: `pg_up{cluster="amc"} = 0` → Slack #amc-ops + PagerDuty → Escalate to CTO+CEO (5 min)
- [ ] Rate Limit Exhaustion alert: > 10/min → Slack #amc-ops → Escalate to CTO (15 min)
- [ ] Storage Exhausted alert: disk > 90% → Slack #amc-ops + email devops → Escalate to CTO (1 hour)

### AC8.2: P1 Warning Alerts Implemented
- [ ] High Latency P99 alert: latency > 200ms → Slack #amc-ops → Notify PM (1 hour)
- [ ] High Latency P95 alert: latency > 100ms → Slack #amc-ops → Notify PM (2 hours)
- [ ] Elevated Error Rate alert: error rate > 0.5% → Slack #amc-ops → Notify PM (2 hours)
- [ ] Queue Backlog alert: queue length > 100 → Slack #amc-ops → Notify DevOps (1 hour)
- [ ] Memory High alert: memory > 2GB → Slack #amc-ops → Notify DevOps (2 hours)

### AC8.3: Grafana Dashboards Created
Create 4 dashboards with all panels specified in MONITORING-SPEC.md:
- [ ] Dashboard 1: API Health & Performance (6 panels: Request Rate, Error Rate, Latency P50/P95/P99, Request Volume, Status Codes, Uptime)
- [ ] Dashboard 2: Business Metrics (7 panels: Total Beta Users, Active Users (7d), API Keys Created, Memories Written, Searches Performed, Payment Methods Added, Conversion Rate)
- [ ] Dashboard 3: Database Health (6 panels: Connection Pool Usage, Query Duration P99, Slow Queries, Cache Hit Ratio, Database Size, Replication Lag)
- [ ] Dashboard 4: Infrastructure Health (5 panels: CPU Usage, Memory Usage, Disk Usage, Network I/O, Open File Descriptors)
- [ ] All dashboards shared with team (CTO, DevOps, PM)

### AC8.4: Prometheus Scraping Configured
- [ ] AMC backend added to `prometheus.yml`
- [ ] `/metrics` endpoint accessible and returning valid OpenMetrics 1.0 format
- [ ] All required metrics exposed: http_requests_total, http_request_duration_seconds, beta_signup_total, memories_written_total, searches_performed_total, pg_stat_activity_count, process_resident_memory_bytes, disk_used_percent
- [ ] Scraping interval set to 15s
- [ ] Prometheus successfully collecting data (verify in Prometheus UI)

### AC8.5: Alert Routing Configured
- [ ] Slack webhook integration: P0 alerts to #amc-incident, all alerts to #amc-ops
- [ ] PagerDuty service created: `amc-mvp-beta`
- [ ] PagerDuty escalation policy configured: DevOps → CTO → CEO (5/15+ min)
- [ ] Email notifications: P0 to devops+cto, P1 to pm
- [ ] Test alert sent to all channels and verified received

### AC8.6: Incident Response Playbook Documented
- [ ] P0: API Down playbook (symptoms, immediate actions, escalation)
- [ ] P1: High Error Rate playbook (investigation steps, actions)
- [ ] P2: High Latency playbook (investigation steps, actions)
- [ ] Runbook accessible to all team members (Notion/docs link)
- [ ] Escalation contacts documented (CTO, CEO phone/Slack)

### AC8.7: Launch Day Checklist Executed
Complete 24h pre-launch checklist:
- [ ] Verify all dashboards are rendering correctly
- [ ] Test alert notifications (send test alert to all channels)
- [ ] Confirm PagerDuty on-call rotation is set
- [ ] Baseline metrics captured (document "normal" traffic patterns)
- [ ] Validate Prometheus scraping is working
- [ ] Test Grafana login for all team members (CTO, DevOps, PM)

---

## Success Metrics

- All P0 and P1 alerts firing correctly with correct routing
- All 4 Grafana dashboards visible and updating
- Prometheus collecting metrics from AMC backend
- Alert notifications arriving in < 10 seconds
- Team can access and read all dashboards and runbook
- Launch day checklist fully completed by Mar 23

---

## Dependencies

- AMC backend deployed and exposing `/metrics` endpoint
- PostgreSQL database accessible for pg_stat queries
- Slack webhook URL available
- PagerDuty account configured (if not, escalate to CTO)

---

## Questions for CTO Review (from MONITORING-SPEC.md)

1. Do we have Prometheus and Grafana infrastructure in place for this project?
2. What is our PagerDuty account status? Need setup?
3. Should we use separate alerting for staging vs production?
4. Do we need Datadog or New Relic in addition to Prometheus?
5. What is our budget for monitoring infrastructure?

---

**Created:** 2026-03-11T12:00:00Z
**Owner:** faintech-devops
**Reviewer:** faintech-cto (technical review), faintech-ciso (security review)
**Source Document:** projects/new-product/docs/MONITORING-SPEC.md
