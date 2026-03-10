# MVP Feature Prioritization — Agent Memory Cloud

Date: 2026-03-10 | Owner: faintech-cpo | Status: Ready for CEO Review
**Based on:** PRODUCT-HYPOTHESIS.md + PROD-002 Social Listening Analysis

---

## Executive Summary

**Goal:** Ship MVP in 4 weeks, acquire 5 paying customers by Week 6
**Approach:** P0 features only, defer everything else
**Build Sequence:** API → SDK → Dashboard → Auth → Onboarding
**Risk:** Scope creep, security gaps, poor DX

---

## P0 Features (Must Have for MVP)

### 1. Memory API (Week 1)
**Priority:** P0-CRITICAL
**Effort:** 5 days
**Dependencies:** None

**Scope:**
- `POST /memories` — Write memory with metadata (agent_id, task_id, type, tags)
- `GET /memories?agent_id=X&task_id=Y` — Search with filters
- `POST /memories/compact` — Compress old memories (keep signal, reduce storage)
- `GET /health` — Uptime check

**Acceptance Criteria:**
- API responds < 100ms p99 latency
- Handles 100 req/sec without degradation
- Returns proper error codes (400, 401, 404, 500)
- OpenAPI spec published
- Rate limiting (1000 req/hour per API key)

**Why P0:** This is the product. Without API, no agents can store memories.

**Risk Mitigation:**
- Use battle-tested framework (FastAPI for Python)
- Load test with Locust before shipping
- Circuit breaker for downstream services

---

### 2. Python SDK (Week 2)
**Priority:** P0-CRITICAL
**Effort:** 3 days
**Dependencies:** API complete

**Scope:**
- `MemoryClient.write(content, agent_id, task_id, type, tags)`
- `MemoryClient.search(query, filters)`
- `MemoryClient.compact(older_than_days)`
- Automatic retry with exponential backoff
- Type hints + docstrings

**Acceptance Criteria:**
- `pip install agentmemory` works
- Full type coverage (mypy --strict passes)
- README with 3 examples (write, search, compact)
- Published to PyPI

**Why P0:** Target persona (Python AI founders) expects native SDK. No SDK = no adoption.

**Risk Mitigation:**
- Copy API patterns from successful SDKs (OpenAI, Anthropic)
- Integration tests against real API
- Semantic versioning from day 1

---

### 3. TypeScript SDK (Week 2-3)
**Priority:** P0-HIGH
**Effort:** 2 days
**Dependencies:** API complete

**Scope:**
- Same as Python SDK, but TypeScript
- Works in Node.js + browser
- Promise-based API

**Acceptance Criteria:**
- `npm install @agentmemory/sdk` works
- Full type definitions
- README with 3 examples
- Published to npm

**Why P0:** Many AI agents use TypeScript (LangChain.js, AutoGen TypeScript). Excludes half the market without it.

**Risk Mitigation:**
- Auto-generate types from OpenAPI spec
- Integration tests against real API
- Copy patterns from Vercel AI SDK

---

### 4. Web Dashboard (Week 3)
**Priority:** P0-HIGH
**Effort:** 4 days
**Dependencies:** API + SDKs

**Scope:**
- Login with API key
- View all memories (paginated, filterable)
- Search memories (full-text)
- Agent memory breakdown (which agents write most)
- Memory type distribution (outcome vs learning vs preference)

**Acceptance Criteria:**
- Responsive (works on mobile)
- Search latency < 200ms
- Charts for memory analytics
- Export memories as JSON/CSV

**Why P0:** Founders need visibility into what agents remember. Dashboard = trust.

**Risk Mitigation:**
- Use Next.js App Router (production-ready)
- Vercel deployment (zero infra)
- Chart.js for simple charts (avoid complexity)

---

### 5. Auth & Multi-Workspace (Week 4)
**Priority:** P0-CRITICAL
**Effort:** 3 days
**Dependencies:** API

**Scope:**
- API key generation
- Workspace isolation (API key → workspace)
- Team invites (email-based)
- Role-based access (admin, member, viewer)

**Acceptance Criteria:**
- Workspaces completely isolated (no cross-workspace data access)
- API keys rotateable without downtime
- Email invites work (SendGrid/Resend)
- Role permissions enforced

**Why P0:** Multi-tenant from day 1. Single workspace = no team adoption.

**Risk Mitigation:**
- Use battle-tested auth (Auth0, Clerk, or custom JWT)
- Encryption at rest for API keys
- Audit logs for auth events

---

## P1 Features (Nice to Have, Post-MVP)

### 6. Memory Analytics Dashboard (Week 5-6)
**Priority:** P1
**Effort:** 2 days

**Scope:**
- Memory growth rate over time
- Agent improvement score (fewer repeated mistakes)
- Most-used tags
- Memory age distribution

**Why P1:** Founders want ROI metrics, but can ship without.

---

### 7. Memory Templates (Week 5-6)
**Priority:** P1
**Effort:** 2 days

**Scope:**
- Pre-built memory schemas (e.g., "coding agent", "research agent")
- Import/export templates
- Community templates (future)

**Why P1:** Reduces onboarding friction, but not blocking.

---

### 8. Webhook Notifications (Week 5-6)
**Priority:** P1
**Effort:** 1 day

**Scope:**
- `POST /webhooks` — Register webhook URL
- Notify on memory events (write, compact, pattern detected)

**Why P1:** Enables integrations (Slack, Discord), but not core.

---

## P2 Features (Defer to Post-MVP)

### 9. Self-Hosted Deployment
**Priority:** P2
**Effort:** 5 days

**Scope:**
- Docker image with all dependencies
- Helm chart for Kubernetes
- Postgres migration scripts

**Why P2:** Market expects this, but early adopters will use SaaS first.

---

### 10. Memory Marketplace
**Priority:** P2
**Effort:** 10+ days

**Scope:**
- Pre-trained memory sets (e.g., "React best practices")
- Paid memory packs
- Community contributions

**Why P2:** Revenue opportunity, but requires critical mass of users first.

---

## P3 Features (Out of Scope for Now)

### 11. Enterprise SSO/SAML
**Priority:** P3
**Effort:** 5+ days

**Why P3:** Target segment (Seed/Series A startups) doesn't need SSO yet.

---

### 12. Cross-Customer Anonymized Learning
**Priority:** P3
**Effort:** 10+ days

**Why P3:** Privacy review needed. High value, but regulatory risk.

---

## 4-Week Build Sequence

| Week | Focus | Deliverables | Owner |
|------|-------|--------------|-------|
| **Week 1** | API Foundation | Memory API (write/search/compact), rate limiting, OpenAPI spec | faintech-backend |
| **Week 2** | SDKs | Python SDK (PyPI), TypeScript SDK (npm), integration tests | faintech-dev |
| **Week 3** | Dashboard + Auth | Web dashboard (Next.js), API key auth, workspace isolation | faintech-frontend |
| **Week 4** | Polish + Ship | Onboarding flow, docs, error handling, load testing, launch | All hands |

---

## Success Gates

**Week 1 Gate:** API handles 100 req/sec with < 100ms p99 latency
**Week 2 Gate:** SDKs published, installable, passing all tests
**Week 3 Gate:** Dashboard functional, auth working, workspace isolation verified
**Week 4 Gate:** End-to-end flow works (agent → SDK → API → dashboard)

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Scope creep | High | High | Strict P0 enforcement, defer all P1+ |
| Security vulnerability | Medium | Critical | Security review before launch, encryption at rest |
| Poor developer experience | Medium | High | Copy successful SDK patterns, extensive docs |
| Performance issues | Medium | High | Load testing Week 1, monitoring from day 1 |
| No paying customers | Medium | High | Target 10 beta users during build, iterate on feedback |

---

## Decision Required from CEO

1. **Approve P0 scope?** (5 features, 4-week build)
2. **Approve pricing model?** (Free tier: 10K writes/month, Pro: $99/month)
3. **Approve target segment?** (Technical founders, Seed/Series A, multi-agent systems)
4. **Greenlight MVP build start?** (Target: 2026-03-11 start, 2026-04-08 ship)

**Next Step:** CEO review → faintech-cto for build planning → faintech-dev/backend execution

---

_Last updated: 2026-03-10 by faintech-cpo_
