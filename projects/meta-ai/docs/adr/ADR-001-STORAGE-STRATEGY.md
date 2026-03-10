# ADR-001: Storage Strategy (SQLite Dev / PostgreSQL Prod)

**Status:** Accepted  
**Date:** 2026-03-10  
**Decision:** faintech-cto  
**Context:** AMC MVP Technical Planning  
**Related:** AMC-MVP-001

---

## Context

We need to choose storage strategies for Agent Memory Cloud MVP across development and production environments.

### Options Considered

**Option A: PostgreSQL Everywhere**
- Pros: Single codebase, feature parity, no migration pain
- Cons: Slower dev setup, requires Docker, higher local resource usage

**Option B: SQLite Dev / PostgreSQL Prod**
- Pros: Fast local dev (no Docker), cheap/simple setup, production-ready database for prod
- Cons: Feature differences (no pgvector in SQLite), migration test gap

**Option C: File-based Dev / PostgreSQL Prod**
- Pros: Leverages existing meta-ai file-based system
- Cons: Different APIs, higher integration gap, rewrites required for cloud

---

## Decision

**Selected: Option B - SQLite for Development / PostgreSQL with pgvector for Production**

### Rationale

1. **Developer Experience** - SQLite is zero-setup, works everywhere, fast for local testing
2. **Feature Gap Mitigation** - pgvector-specific features mocked in SQLite for dev, tested in staging
3. **Production Readiness** - PostgreSQL is battle-tested, supports concurrent writes, ACID compliance
4. **Cost** - Neon PostgreSQL free tier covers MVP; Railway hosting <$5/mo
5. **Migration Path** - Alembic handles schema differences automatically

### Implementation

#### Development (SQLite)
```python
# models.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if os.getenv("ENV") == "production":
    DATABASE_URL = os.getenv("DATABASE_URL")  # Neon PostgreSQL
else:
    DATABASE_URL = "sqlite:///./agent_memory.db"  # Local SQLite

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

#### Production (PostgreSQL + pgvector)
```sql
-- Enable pgvector in production only
CREATE EXTENSION IF NOT EXISTS vector;

-- Vector embedding column
ALTER TABLE memories ADD COLUMN embedding vector(1536);
```

#### Feature Gap Handling
```python
# Mock semantic search in SQLite
def search_semantic(query: str, org_id: str):
    if ENV == "production":
        return vector_search(query, org_id)  # pgvector
    else:
        return keyword_search(query, org_id)  # SQLite fallback
```

---

## Consequences

### Positive
- Faster local development (no Docker required)
- Lower resource usage on dev machines
- Production-ready PostgreSQL with vector search
- Easy migration between environments via Alembic

### Negative
- Semantic search must be tested on staging (not dev)
- Two databases to maintain in test suite
- Potential bugs from SQLite/PostgreSQL differences

### Mitigation
- Integration tests run on PostgreSQL staging before deploy
- Feature flags for pgvector-specific features
- Automated tests cover both databases

---

## Alternatives Considered

### PostgreSQL Everywhere (Rejected)
- Dev experience too slow (Docker required)
- Overkill for local development

### File-based in Prod (Rejected)
- Not production-ready (no ACID, no concurrent writes)
- No scaling path for multi-tenant SaaS

---

## Status

**Accepted** - Decision to use SQLite (dev) / PostgreSQL (prod) is final for MVP.

---

**Review Date:** Week 4 (April 6, 2026)  
**Owner:** faintech-cto
