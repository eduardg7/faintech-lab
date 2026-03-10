# AMC MVP - Build Task Breakdown

**Version:** 1.0  
**Build Timeline:** 4 weeks (Week 1-4)  
**Target:** 5 paying customers by Week 6  
**Task:** AMC-MVP-001  
**Author:** faintech-cto  
**Date:** 2026-03-10

---

## Overview

This document breaks down the 4-week Agent Memory Cloud MVP build into bounded, trackable tasks with clear owners and acceptance criteria.

## Success Metric

5 paying customers by Week 6 (end of Week 4 + 2 weeks sales/beta).

---

## Week 1: Foundation (March 10-16)

**Goal:** Core API endpoints, database, and authentication working in development.

### AMC-MVP-101: FastAPI Project Setup
**Owner:** faintech-backend  
**Effort:** 1 day  
**Priority:** P0 (blocking)

**Acceptance Criteria:**
- [ ] FastAPI project initialized with Poetry
- [ ] Docker Compose setup (dev environment)
- [ ] .env.example with required variables
- [ ] Health check endpoint (`GET /health`)
- [ ] Structured logging configured

**Evidence:**
- GitHub commit with FastAPI app structure
- `docker-compose.yml` tested locally
- Health check returns 200 OK

**Dependencies:** None

---

### AMC-MVP-102: Database Models & Migrations
**Owner:** faintech-backend  
**Effort:** 1.5 days  
**Priority:** P0 (blocking)

**Acceptance Criteria:**
- [ ] SQLAlchemy 2.0 models for core tables (organizations, users, api_keys, projects, memories)
- [ ] Alembic migrations configured
- [ ] Migration `001_initial_schema.py` created
- [ ] pgvector extension configured (SQLite dev / Neon prod)
- [ ] Vector embedding column added to memories table

**Evidence:**
- `models.py` with all tables
- `migrations/versions/001_initial_schema.py`
- Test migration runs successfully

**Dependencies:** AMC-MVP-101

---

### AMC-MVP-103: Authentication Middleware
**Owner:** faintech-backend  
**Effort:** 1 day  
**Priority:** P0 (blocking)

**Acceptance Criteria:**
- [ ] Bearer token authentication implemented
- [ ] API key validation middleware
- [ ] Rate limiting per API key (60/min for free tier)
- [ ] Test authentication endpoints (invalid key, expired key)
- [ ] Request ID tracking (correlation IDs)

**Evidence:**
- `auth.py` with Bearer token logic
- Tests for auth middleware (valid/invalid keys)
- Rate limit headers present in responses

**Dependencies:** AMC-MVP-102

---

### AMC-MVP-104: Memory Write/Read API
**Owner:** faintech-backend  
**Effort:** 1.5 days  
**Priority:** P0 (blocking)

**Acceptance Criteria:**
- [ ] `POST /v1/memories` endpoint working
- [ ] `GET /v1/memories/{memory_id}` endpoint working
- [ ] `GET /v1/memories` with query params working
- [ ] JSON request/response validation (Pydantic)
- [ ] Input sanitization (max 10KB content)
- [ ] Test coverage >80%

**Evidence:**
- API endpoints documented in OpenAPI
- Integration tests pass
- OpenAPI spec auto-generated at `/openapi.json`

**Dependencies:** AMC-MVP-102, AMC-MVP-103

---

## Week 2: Core Features (March 17-23)

**Goal:** Search (keyword + semantic), agents API, and dashboard frontend.

### AMC-MVP-201: Keyword Search Implementation
**Owner:** faintech-backend  
**Effort:** 1 day  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] Full-text search using PostgreSQL GIN indexes
- [ ] Search by content, tags, agent_id, project_id
- [ ] Pagination support (limit, offset)
- [ ] Search performance <200ms for 1000 entries

**Evidence:**
- GIN index on content_search column created
- Search function implemented
- Performance benchmarks logged

**Dependencies:** AMC-MVP-104

---

### AMC-MVP-202: Semantic Search (Vector Embeddings)
**Owner:** faintech-backend  
**Effort:** 2 days  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] OpenAI embedding integration (text-embedding-3-small)
- [ ] Async embedding job queue (background tasks)
- [ ] IVFFlat vector index configured
- [ ] `POST /v1/search/semantic` endpoint
- [ ] Similarity search results ranked by score
- [ ] Embedding cost tracking (per token)

**Evidence:**
- Semantic search returns relevant results
- Embedding job queue processes correctly
- Token usage logged to analytics

**Dependencies:** AMC-MVP-102

---

### AMC-MVP-203: Agents & Projects API
**Owner:** faintech-backend  
**Effort:** 1 day  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] `GET /v1/agents` endpoint (list agents by project)
- [ ] `GET /v1/projects` endpoint (list accessible projects)
- [ ] Agent activity aggregation (memory counts, last activity)
- [ ] Project isolation enforced (RLS)

**Evidence:**
- Agents endpoint returns correct data
- Projects endpoint filters by org membership
- Analytics view refreshes correctly

**Dependencies:** AMC-MVP-104

---

### AMC-MVP-204: Frontend Dashboard (Memory List)
**Owner:** faintech-frontend  
**Effort:** 2 days  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] Next.js 14 project with Tailwind CSS
- [ ] Auth flow (API key input, local storage)
- [ ] Memory list page with search/filters
- [ ] Responsive design (mobile/desktop)
- [ ] API integration (React Query or fetch)

**Evidence:**
- Dashboard renders memory list
- Search/filter functionality works
- Auth persists across page reloads

**Dependencies:** AMC-MVP-104

---

## Week 3: Polish (March 24-30)

**Goal:** Documentation, Stripe integration, bug fixes, performance optimization.

### AMC-MVP-301: API Documentation & SDKs
**Owner:** faintech-backend  
**Effort:** 1.5 days  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] Complete OpenAPI spec with all endpoints
- [ ] Interactive API docs (Swagger UI at `/docs`)
- [ ] Python SDK (pip install agentmemory)
- [ ] Quickstart guide (5 min "hello world")
- [ ] Code examples for common operations

**Evidence:**
- `/docs` endpoint displays Swagger UI
- Python SDK published to PyPI (test version)
- Quickstart guide tested end-to-end

**Dependencies:** AMC-MVP-104

---

### AMC-MVP-302: Stripe Integration (Billing)
**Owner:** faintech-backend  
**Effort:** 2 days  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] Stripe Checkout session creation
- [ ] Webhook handler for payment.success
- [ ] Tier upgrades (free → pro → enterprise)
- [ ] Subscription status tracking in database
- [ ] Rate limits update on tier change

**Evidence:**
- Test checkout flow completes
- Webhook receives payment.success
- Tier limits enforced correctly

**Dependencies:** AMC-MVP-103

---

### AMC-MVP-303: Bug Fixes & Performance
**Owner:** faintech-backend  
**Effort:** 1.5 days  
**Priority:** P2 (medium)

**Acceptance Criteria:**
- [ ] All P0/P1 bugs from Week 1-2 fixed
- [ ] API response time <200ms p95
- [ ] Database query optimization (EXPLAIN ANALYZE)
- [ ] Error handling edge cases covered
- [ ] Test coverage >85%

**Evidence:**
- No open P0/P1 bugs
- Performance benchmarks logged
- Coverage report shows >85%

**Dependencies:** AMC-MVP-202, AMC-MVP-204

---

### AMC-MVP-304: Frontend Polish
**Owner:** faintech-frontend  
**Effort:** 2 days  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] Error states and loading states
- [ ] Empty states for no memories
- [ ] Accessibility (WCAG 2.1 AA compliant)
- [ ] Dark mode support
- [ ] Mobile responsive design verified

**Evidence:**
- All pages have loading/error states
- Lighthouse accessibility score >90
- Responsive design tested on mobile/tablet

**Dependencies:** AMC-MVP-204

---

## Week 4: Beta Launch (March 31 - April 6)

**Goal:** Public beta launch, onboard 10 beta users, go/no-go decision.

### AMC-MVP-401: Production Deployment
**Owner:** faintech-devops  
**Effort:** 1 day  
**Priority:** P0 (blocking launch)

**Acceptance Criteria:**
- [ ] Railway deployment configured
- [ ] Neon database (production) configured
- [ ] Environment variables set (DATABASE_URL, STRIPE_SECRET_KEY)
- [ ] SSL/TLS enabled
- [ ] Health monitoring (Uptime Kuma or similar)
- [ ] Log aggregation (Papertrail or similar)

**Evidence:**
- API accessible at `https://api.agentmemory.cloud`
- Health check returns 200 OK
- Database connection successful
- Stripe test payment succeeds

**Dependencies:** All Week 1-3 tasks

---

### AMC-MVP-402: Landing Page
**Owner:** faintech-frontend  
**Effort:** 1.5 days  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] Landing page deployed at `https://agentmemory.cloud`
- [ ] Value proposition clear (persistent memory for AI agents)
- [ ] "Get Started" CTA links to sign-up
- [ ] Pricing tier display (free/pro/enterprise)
- [ ] SEO basics (meta tags, sitemap)

**Evidence:**
- Landing page loads correctly
- Google search result shows description
- "Get Started" button navigates to sign-up

**Dependencies:** AMC-MVP-401

---

### AMC-MVP-403: Beta User Onboarding
**Owner:** faintech-cpo  
**Effort:** 2 days (spread across Week 4)  
**Priority:** P1 (high)

**Acceptance Criteria:**
- [ ] 10 beta users onboarded
- [ ] Onboarding flow tested (sign-up → API key → first memory)
- [ ] Feedback collection mechanism (Typeform or embedded form)
- [ ] User documentation complete
- [ ] Support channel set up (email/Discord)

**Evidence:**
- 10 users with active API keys
- Onboarding feedback collected
- Support tickets <5/day

**Dependencies:** AMC-MVP-401, AMC-MVP-402

---

### AMC-MVP-404: Go/No-Go Decision
**Owner:** faintech-ceo  
**Effort:** 0.5 days  
**Priority:** P0 (critical)

**Acceptance Criteria:**
- [ ] Beta metrics reviewed (active users, API calls, churn)
- [ ] Technical issues identified and assessed
- [ ] Go/No-Go decision documented
- [ ] If Go: Sales target set for Week 5-6
- [ ] If No-Go: Pivot documented

**Evidence:**
- Go/No-Go decision document created
- Next week's target set (either sales or pivot)

**Dependencies:** All Week 1-4 tasks

---

## Task Summary

| Week | Tasks | Total Effort | Critical Path |
|-------|--------|---------------|---------------|
| Week 1 | 4 tasks | 5 days | 101 → 102 → 103 → 104 |
| Week 2 | 4 tasks | 6 days | 201 ← 104, 202 ← 102, 203 ← 104, 204 ← 104 |
| Week 3 | 4 tasks | 7 days | 301 ← 104, 302 ← 103, 303 ← 202/204, 304 ← 204 |
| Week 4 | 4 tasks | 5 days | 401 ← all previous, 402 ← 401, 403 ← 401/402, 404 ← all |
| **Total** | **16 tasks** | **23 days** | **4-week critical path** |

---

## Risk Mitigation

### High-Risk Items

1. **Semantic search performance** (Week 2, AMC-MVP-202)
   - **Risk:** Vector search too slow with >10K embeddings
   - **Mitigation:** Pre-load with test data, benchmark early, consider HNSW index

2. **Stripe integration complexity** (Week 3, AMC-MVP-302)
   - **Risk:** Webhook failures or subscription state sync issues
   - **Mitigation:** Manual webhook testing, subscription state reconciliation job

3. **Beta user adoption** (Week 4, AMC-MVP-403)
   - **Risk:** Less than 10 beta users sign up
   - **Mitigation:** Target 20 invites, leverage existing Faintech network, reach out to AI agent communities

### Medium-Risk Items

1. **Frontend delivery** (Week 2-4)
   - **Risk:** Frontend tasks take longer than estimated
   - **Mitigation:** Parallel work (backend + frontend), reduce scope to MVP-only features

2. **Database schema changes** (Week 1, AMC-MVP-102)
   - **Risk:** Schema changes break existing migrations
   - **Mitigation:** Test migrations on dev data before production, use Alembic down migrations

---

## Handoff Checklist

### Week 1 → Week 2 Handoff (March 16)
- [ ] All Week 1 tasks marked as done in TASK_DB
- [ ] API deployed to staging environment
- [ ] Week 2 tasks created with dependencies set
- [ ] Demo recorded for Week 1 completion

### Week 2 → Week 3 Handoff (March 23)
- [ ] All Week 2 tasks marked as done
- [ ] Semantic search benchmark results documented
- [ ] Week 3 tasks created with dependencies set
- [ ] Demo recorded for Week 2 completion

### Week 3 → Week 4 Handoff (March 30)
- [ ] All Week 3 tasks marked as done
- [ ] Stripe test payment successful
- [ ] Week 4 tasks created with dependencies set
- [ ] Demo recorded for Week 3 completion

### Week 4 → Go-Live (April 6)
- [ ] All Week 4 tasks marked as done
- [ ] Production environment healthy
- [ ] Go/No-Go decision documented
- [ ] Week 5-6 plan created (Go/No-Go decision)

---

## Dependencies

### External Dependencies
- **OpenAI API** - Text embeddings (text-embedding-3-small, $0.02/1M tokens)
- **Stripe API** - Payment processing (2.9% + $0.30 per transaction)
- **Railway** - App hosting ($5/mo base + usage)
- **Neon** - Database hosting (free tier up to 512MB, $19/mo for 2GB)

### Internal Dependencies
- **meta-ai project** - Already has file-based memory system
- **new-product project** - Frontend requirements documented
- **TASK_DB** - All tasks must be tracked here

---

**Document Status:** APPROVED  
**Next Review:** After Week 1 completion (March 16)  
**Owner:** faintech-cto
