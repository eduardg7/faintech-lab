# AMC MVP - Infrastructure Cost Estimate

**Version:** 1.0  
**Target:** <$100/month for MVP  
**Break-even:** 1 paying customer  
**Task:** AMC-MVP-001  
**Author:** faintech-cto  
**Date:** 2026-03-10

---

## Overview

This document estimates monthly infrastructure costs for Agent Memory Cloud MVP across development, staging, and production environments.

**Assumptions:**
- 5 paying customers by Week 6 (end of April)
- 100K total memories stored
- 10K new embeddings generated per month
- Uptime target: 99.9% (acceptable downtime: 43 min/month)

---

## Production Infrastructure (Live at Week 4)

### Hosting (Railway)

| Resource | Specification | Cost/month | Notes |
|-----------|----------------|---------------|---------|
| App container | 512MB RAM, 0.5 vCPU | $5.00 | Base tier, scales vertically |
| Build minutes | 500 included, $0.001/extra | ~$1.00 | 1 deployment/day @ 10min |
| Custom domain | Free | $0.00 | `agentmemory.cloud` |
| **Railway Subtotal** | | **$6.00** | |

### Database (Neon PostgreSQL)

| Resource | Specification | Cost/month | Notes |
|-----------|----------------|---------------|---------|
| Database | 2GB RAM, 32GB storage | $19.00 | Supports 10K+ memories |
| Storage | 8GB (included) | $0.00 | pgvector indexes ~2GB |
| Reads/Writes | 32M included | $0.00 | Ample for MVP |
| Backups | Daily (7 days) | $0.00 | Included |
| **Neon Subtotal** | | **$19.00** | |

### OpenAI API (Embeddings)

| Usage | Rate | Cost/month |
|--------|-------|------------|
| 10,000 embeddings | $0.02/1M tokens | $0.27 |
| 133K avg words/memory × 10K | ~1.3M tokens/month | |
| **OpenAI Subtotal** | | **$0.27** | |

### Monitoring & Logging

| Service | Specification | Cost/month |
|---------|----------------|------------|
| Uptime Kuma (1 instance) | Self-hosted on app | $0.00 |
| Papertrail (free tier) | 100MB logs/day | $0.00 |
| **Monitoring Subtotal** | | **$0.00** | |

### Production Total

| Component | Cost/month |
|-----------|------------|
| Railway hosting | $6.00 |
| Neon database | $19.00 |
| OpenAI embeddings | $0.27 |
| Monitoring | $0.00 |
| **Production Total** | **$25.27** |

---

## Staging Infrastructure

### Purpose
- Pre-production testing
- Integration tests on PostgreSQL
- Load testing for API performance

### Cost Estimate

| Resource | Cost/month |
|-----------|------------|
| Railway (dev tier) | $0.00 (free) |
| Neon (free tier) | $0.00 |
| **Staging Total** | **$0.00** |

---

## Development Infrastructure

### Purpose
- Local development
- Docker Compose (if needed)
- SQLite database (local)

### Cost Estimate

| Resource | Cost/month |
|-----------|------------|
| Local dev (self-hosted) | $0.00 |
| **Dev Total** | **$0.00** |

---

## Total Infrastructure Cost (All Environments)

| Environment | Cost/month |
|-------------|------------|
| Production | $25.27 |
| Staging | $0.00 |
| Development | $0.00 |
| **Grand Total** | **$25.27** |

---

## Cost per Customer

### Breakeven Analysis

| Metric | Value |
|---------|--------|
| Total monthly cost | $25.27 |
| Breakeven customers | 1 |
| Target customers (Week 6) | 5 |
| Margin per customer (5 customers) | $5.05 |

### Pricing Tiers (Target)

| Tier | Price/month | Profit/customer | Total Profit (5 customers) |
|------|-------------|-----------------|--------------------------|
| Free | $0.00 | -$5.05 | -$25.25 |
| Pro | $19.00 | +$13.95 | +$69.75 |
| Enterprise | $99.00 | +$93.95 | +$469.75 |

### Assumptions

- 5 customers: 3 Pro, 2 Enterprise (optimistic)
- 2 Free tier users (marketing funnel)
- Infrastructure cost scales linearly with storage/embeddings

---

## Cost Scaling Analysis

### Scenario 1: 10 Customers (Week 8)
- Infrastructure cost: $30.00 (scales with storage)
- Revenue: 6 Pro × $19 + 4 Enterprise × $99 = $510.00
- Profit: $480.00/month

### Scenario 2: 50 Customers (Week 12)
- Infrastructure cost: $50.00 (next tier Railway)
- Revenue: 30 Pro × $19 + 20 Enterprise × $99 = $2,550.00
- Profit: $2,500.00/month

### Scenario 3: 500 Customers (Month 6)
- Infrastructure cost: $200.00 (multi-instance)
- Revenue: 300 Pro × $19 + 200 Enterprise × $99 = $25,500.00
- Profit: $25,300.00/month

---

## Cost Optimization Opportunities

### Phase 1 (Week 1-6)
- Use free tiers where possible (Railway dev, Neon free)
- Optimize embedding batch size (reduce API calls)
- Cache frequently-accessed memories (Redis, Phase 2)

### Phase 2 (Week 7-12)
- Switch to self-hosted embeddings at 50K+ memories (ADR-002 review)
- Implement read replicas (Neon read pool)
- CDN for static assets (Vercel, Netlify)

### Phase 3 (Week 13+)
- Sharding by customer (multi-database)
- Cold storage for old memories (S3)
- Reserved instances for consistent load

---

## Cost Risks

### High-Risk Items

1. **Embedding cost explosion**
   - **Risk:** Customers generate 100K+ embeddings/month
   - **Impact:** Cost could reach $10+/month
   - **Mitigation:** Embedding limits per tier, caching

2. **Database storage growth**
   - **Risk:** pgvector indexes grow faster than expected
   - **Impact:** Neon tier upgrade required sooner
   - **Mitigation:** Compaction policies, tiered pricing

3. **Railway overage**
   - **Risk:** App CPU/RAM usage spikes on load
   - **Impact:** Hourly billing adds up quickly
   - **Mitigation:** Horizontal scaling, load testing

### Medium-Risk Items

1. **Unexpected OpenAI rate limits**
   - **Risk:** API throttling during peak usage
   - **Impact:** Degraded search quality
   - **Mitigation:** Retry logic, fallback to keyword search

2. **Database connection pool exhaustion**
   - **Risk:** Too many concurrent connections
   - **Impact:** API errors, degraded performance
   - **Mitigation:** PgBouncer, connection limits

---

## Cost Monitoring

### Dashboard Metrics

Track these metrics in customer dashboard:

1. **Total memories stored** (per customer)
2. **Embeddings generated this month** (per customer)
3. **API calls this month** (per customer)
4. **Estimated cost** (per customer)

### Alerts

- Cost anomaly detection (>2× normal usage)
- Tier limit warnings (approaching free tier limits)
- Unusual embedding volume (potential abuse)

---

## Comparison: Self-Hosted Alternative

### Fully Self-Hosted (Option B)

| Component | Cost/month | Notes |
|-----------|------------|---------|
| VPS (4 vCPU, 8GB RAM) | $40.00 | Hetzner, DigitalOcean |
| Database (self-hosted PostgreSQL) | $0.00 | Included in VPS |
| Embeddings (SentenceTransformers) | $0.00 | Self-hosted model |
| Monitoring (Grafana, Prometheus) | $0.00 | Self-hosted |
| **Self-Hosted Total** | **$40.00** | No vendor lock-in |

### Comparison with Managed ($25.27)

| Factor | Managed | Self-Hosted | Winner |
|---------|----------|--------------|---------|
| Monthly cost | $25.27 | $40.00 | Managed |
| Dev time | Low (managed) | High (maintenance) | Managed |
| Reliability | High (SLA) | Medium (self-maintain) | Managed |
| Scalability | Auto | Manual | Managed |
| Vendor lock-in | Yes | No | Self-Hosted |

**Decision:** Managed (Railway + Neon) for MVP. Switch to self-hosted if cost >$100/month.

---

## Summary

### Key Takeaways

1. **Target achieved:** $25.27/month is <<$100/month target
2. **Breakeven:** 1 paying customer covers infrastructure
3. **Profit potential:** $480/month with 5 customers (Week 6)
4. **Scalability:** Cost scales linearly, profit scales exponentially

### Recommendation

✅ **Proceed with managed infrastructure (Railway + Neon)**
- Faster time-to-market (Week 4 vs Week 6)
- Lower dev overhead (no self-hosting)
- Competitive pricing (vs self-hosted)

⚠️ **Review at 50 customers:** Consider self-hosted for cost control

---

**Document Status:** APPROVED  
**Next Review:** Week 8 (April 20, 2026) - Re-evaluate at 10 customers  
**Owner:** faintech-cto
