# AMC Monitoring Stack Bootstrap

## Scope
Bounded AC8 slice for `amc-w4-ac8-monitoring-setup`.

This change bootstraps the self-hosted monitoring stack needed for AMC beta:
- Prometheus scrape config
- Alertmanager routing skeleton
- Grafana datasource/dashboard provisioning hooks
- Production compose wiring for Prometheus, Alertmanager, and Grafana

## Files
- `amc-backend/docker-compose.production.yml`
- `amc-backend/ops/monitoring/prometheus.yml`
- `amc-backend/ops/monitoring/alert_rules.yml`
- `amc-backend/ops/monitoring/alertmanager.yml`
- `amc-backend/ops/monitoring/grafana/provisioning/**`

## What is ready now
- Prometheus scrapes `amc-backend:8000/metrics` every 15s.
- Alert rules cover first-pass API down, high error rate, and latency thresholds.
- Alertmanager routes P0 to `amc-incident` and everything else to `amc-ops`.
- Grafana auto-loads the Prometheus datasource and dashboard provider.
- Compose can launch the full stack locally with one file.

## Validation
```bash
cd amc-backend
docker compose -f docker-compose.production.yml config >/tmp/amc-monitoring-compose.out
```

Expected:
- compose parses successfully
- services `amc-backend`, `prometheus`, `alertmanager`, `grafana` are present

## Known gaps for next slice
1. `/metrics` currently returns JSON, not OpenMetrics 1.0, so Prometheus scraping will need a backend metrics exporter upgrade before AC8.4 can be fully closed.
2. Slack/PagerDuty/email env vars are placeholders and need real secrets + routing confirmation from CTO.
3. Dashboard JSON definitions are not created yet; provisioning paths are in place so the next slice can drop dashboards in directly.
4. Some spec alerts depend on metrics not yet emitted by the backend (`disk_used_percent`, `queue_length`, DB-specific series).

## Recommended next bounded slice
Implement Prometheus-compatible instrumentation in the backend and add the first dashboard JSON for API Health & Performance.
