# AMC Production Deployment & Monitoring Runbook

## Scope
Bounded DevOps slice for `amc-w3-20260311-f2a8`.

This runbook provides the minimum production deployment contract for the AMC backend:
- Dockerized production runtime
- Manual deployment trigger
- Health verification
- Monitoring/alert checks
- Rollback notes

## Required files
- `amc-backend/.env.production.example`
- `amc-backend/docker-compose.production.yml`
- `amc-backend/scripts/deploy-production.sh`

## Prerequisites
1. Docker Engine + Docker Compose plugin installed on target host
2. Postgres database provisioned with `pgvector` enabled
3. `.env.production` created from `.env.production.example`
4. Port `8000` reachable from the uptime checker

## Production environment checklist
- `DATABASE_TYPE=postgres`
- `DATABASE_URL=postgresql+asyncpg://...`
- `DEBUG=false`
- `APP_VERSION` matches release being deployed

## Manual deployment trigger
```bash
cd amc-backend
cp .env.production.example .env.production
# edit .env.production with real values
chmod +x scripts/deploy-production.sh
./scripts/deploy-production.sh
```

## Verification
### Health endpoint
```bash
curl http://127.0.0.1:8000/health
```
Expected:
- `status` is `healthy` or explicitly investigated if `degraded`
- `database.status` is `ok`
- `version` matches expected release

### Metrics endpoint
```bash
curl http://127.0.0.1:8000/metrics
```
Check:
- endpoint responds with JSON
- `requests_total` increments after test traffic
- `latency_ms` keys exist

## Monitoring setup
### Uptime monitoring
Configure an uptime checker against:
- `GET /health`
- interval: 1 minute
- alert threshold: 2 consecutive failures

### Error monitoring
Watch container logs for:
- `level=ERROR`
- repeated 5xx responses
- database connection failures

Suggested command:
```bash
docker logs amc-backend --since=10m | grep '"level": "ERROR"'
```

### Rollup operational checks
Run after each deploy:
```bash
docker ps --filter name=amc-backend
curl -f http://127.0.0.1:8000/health
curl -f http://127.0.0.1:8000/metrics >/dev/null
```

## Rollback
If the deploy is unhealthy:
1. Inspect logs: `docker logs amc-backend --tail=200`
2. Stop stack: `docker compose -f docker-compose.production.yml down`
3. Re-deploy last known good image/tag
4. Re-run health verification

## Known gap after this slice
This bounded cycle creates the deploy contract and operator runbook, but does **not** provision cloud infra or external alerting accounts. Those are the next execution slice once the target host/provider is chosen.
