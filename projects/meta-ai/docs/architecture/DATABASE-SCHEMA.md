# Agent Memory Cloud - Database Schema

**Version:** 1.0 (MVP)  
**Database:** PostgreSQL 15+ with pgvector extension  
**Task:** AMC-MVP-001  
**Author:** faintech-cto  
**Date:** 2026-03-10

---

## Overview

This document defines the PostgreSQL schema for the Agent Memory Cloud MVP. The design supports:
- Fast keyword and semantic search
- Efficient filtering by agent/project/task
- Automatic embedding generation for semantic search
- Data isolation between customers

---

## Extensions

```sql
-- Enable pgvector for semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable full-text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

---

## Schema

### Organizations

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    tier VARCHAR(50) NOT NULL DEFAULT 'free', -- free, pro, enterprise
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 60,
    max_memories INTEGER NOT NULL DEFAULT 10000,
    max_projects INTEGER NOT NULL DEFAULT 3,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_tier CHECK (tier IN ('free', 'pro', 'enterprise'))
);

CREATE INDEX idx_organizations_slug ON organizations(slug);
```

---

### Users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'member', -- admin, member, viewer
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_role CHECK (role IN ('admin', 'member', 'viewer'))
);

CREATE INDEX idx_users_org ON users(org_id);
CREATE INDEX idx_users_email ON users(email);
```

---

### API Keys

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    key_hash VARCHAR(255) NOT NULL, -- SHA-256 hash
    name VARCHAR(255), -- "Production", "Dev", etc.
    scopes TEXT[] NOT NULL DEFAULT ARRAY['read', 'write'],
    project_scope UUID[], -- NULL = all projects, or array of project IDs
    last_used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    revoked_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT valid_scopes CHECK (scopes <@ ARRAY['read', 'write', 'admin'])
);

CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_api_keys_org ON api_keys(org_id);
```

---

### Projects

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(org_id, slug)
);

CREATE INDEX idx_projects_org ON projects(org_id);
CREATE INDEX idx_projects_slug ON projects(slug);
```

---

### Memories (Core Table)

```sql
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    agent_id VARCHAR(255) NOT NULL,
    task_id VARCHAR(255),
    type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    content_search TEXT GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    metadata JSONB DEFAULT '{}'::JSONB,
    embedding vector(1536), -- OpenAI text-embedding-3-small
    embedding_version INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_type CHECK (type IN ('learning', 'error', 'decision', 'pattern', 'fact')),
    CONSTRAINT content_size CHECK (length(content) <= 10240) -- 10KB max
);

-- Indexes for fast filtering
CREATE INDEX idx_memories_org ON memories(org_id);
CREATE INDEX idx_memories_project ON memories(project_id);
CREATE INDEX idx_memories_agent ON memories(agent_id);
CREATE INDEX idx_memories_task ON memories(task_id) WHERE task_id IS NOT NULL;
CREATE INDEX idx_memories_type ON memories(type);
CREATE INDEX idx_memories_created ON memories(created_at DESC);
CREATE INDEX idx_memories_tags ON memories USING GIN(tags);

-- Full-text search index
CREATE INDEX idx_memories_content_search ON memories USING GIN(content_search);

-- Vector similarity search index (IVFFlat for >1M rows, else use simple)
CREATE INDEX idx_memories_embedding ON memories 
    USING ivfflat (embedding vector_cosine_ops) 
    WITH (lists = 100);
```

---

### Memory Analytics (Materialized View)

```sql
CREATE MATERIALIZED VIEW memory_analytics AS
SELECT 
    org_id,
    project_id,
    agent_id,
    COUNT(*) as total_memories,
    COUNT(*) FILTER (WHERE type = 'learning') as learnings,
    COUNT(*) FILTER (WHERE type = 'error') as errors,
    COUNT(*) FILTER (WHERE type = 'decision') as decisions,
    COUNT(*) FILTER (WHERE type = 'pattern') as patterns,
    COUNT(*) FILTER (WHERE type = 'fact') as facts,
    MAX(created_at) as last_activity,
    MIN(created_at) as first_activity
FROM memories
GROUP BY org_id, project_id, agent_id;

CREATE UNIQUE INDEX idx_memory_analytics_key ON memory_analytics(org_id, project_id, agent_id);

-- Refresh strategy: Every 5 minutes via cron
-- REFRESH MATERIALIZED VIEW CONCURRENTLY memory_analytics;
```

---

### Embedding Jobs (Async Processing)

```sql
CREATE TABLE embedding_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memory_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, processing, completed, failed
    attempts INTEGER DEFAULT 0,
    last_error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT valid_status CHECK (status IN ('pending', 'processing', 'completed', 'failed'))
);

CREATE INDEX idx_embedding_jobs_status ON embedding_jobs(status) WHERE status IN ('pending', 'processing');
CREATE INDEX idx_embedding_jobs_memory ON embedding_jobs(memory_id);
```

---

### Audit Log

```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL,
    user_id UUID REFERENCES users(id),
    api_key_id UUID REFERENCES api_keys(id),
    action VARCHAR(100) NOT NULL, -- memory.create, memory.delete, project.create, etc.
    resource_type VARCHAR(50) NOT NULL, -- memory, project, api_key
    resource_id UUID,
    ip_address INET,
    user_agent TEXT,
    request_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_log_org ON audit_log(org_id, created_at DESC);
CREATE INDEX idx_audit_log_user ON audit_log(user_id, created_at DESC);
CREATE INDEX idx_audit_log_resource ON audit_log(resource_type, resource_id);

-- Partitioning for scale (Phase 2)
-- CREATE TABLE audit_log_2026_03 PARTITION OF audit_log
--     FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
```

---

## Functions

### Update Timestamp Trigger

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_organizations_updated_at
    BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_projects_updated_at
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_memories_updated_at
    BEFORE UPDATE ON memories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

---

### Semantic Search Function

```sql
CREATE OR REPLACE FUNCTION search_memories_semantic(
    query_embedding vector(1536),
    p_org_id UUID,
    p_project_id UUID DEFAULT NULL,
    p_agent_id VARCHAR DEFAULT NULL,
    p_limit INTEGER DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    agent_id VARCHAR,
    content TEXT,
    type VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.agent_id,
        m.content,
        m.type,
        m.created_at,
        1 - (m.embedding <=> query_embedding) as similarity
    FROM memories m
    WHERE m.org_id = p_org_id
      AND (p_project_id IS NULL OR m.project_id = p_project_id)
      AND (p_agent_id IS NULL OR m.agent_id = p_agent_id)
      AND m.embedding IS NOT NULL
    ORDER BY m.embedding <=> query_embedding
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;
```

---

### Keyword Search Function

```sql
CREATE OR REPLACE FUNCTION search_memories_keyword(
    p_query TEXT,
    p_org_id UUID,
    p_project_id UUID DEFAULT NULL,
    p_agent_id VARCHAR DEFAULT NULL,
    p_type VARCHAR DEFAULT NULL,
    p_tags TEXT[] DEFAULT NULL,
    p_limit INTEGER DEFAULT 10,
    p_offset INTEGER DEFAULT 0
)
RETURNS TABLE (
    id UUID,
    agent_id VARCHAR,
    content TEXT,
    type VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE,
    rank FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.agent_id,
        m.content,
        m.type,
        m.created_at,
        ts_rank(m.content_search, plainto_tsquery('english', p_query)) as rank
    FROM memories m
    WHERE m.org_id = p_org_id
      AND (p_project_id IS NULL OR m.project_id = p_project_id)
      AND (p_agent_id IS NULL OR m.agent_id = p_agent_id)
      AND (p_type IS NULL OR m.type = p_type)
      AND (p_tags IS NULL OR m.tags @> p_tags)
      AND m.content_search @@ plainto_tsquery('english', p_query)
    ORDER BY rank DESC, m.created_at DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
```

---

## Migrations

Migration files will be managed via Alembic:

```
alembic/
├── versions/
│   ├── 001_initial_schema.py
│   ├── 002_add_embedding_jobs.py
│   ├── 003_add_audit_log.py
│   └── ...
├── env.py
└── alembic.ini
```

**Migration strategy:**
1. All schema changes via Alembic migrations
2. Test on staging before production
3. Backwards-compatible migrations where possible
4. Backup before destructive migrations

---

## Performance Considerations

### Index Strategy

1. **Primary indexes** - All foreign keys and frequently filtered columns
2. **Composite indexes** - (org_id, project_id, created_at) for common queries
3. **Partial indexes** - WHERE clauses for filtered queries (e.g., active projects only)
4. **GIN indexes** - For arrays (tags) and JSONB (metadata)

### Query Optimization

1. **Use materialized views** - For analytics queries
2. **Limit result sets** - Enforce max limits (100)
3. **Connection pooling** - PgBouncer in transaction mode
4. **Prepared statements** - For repeated queries

### Vector Search Optimization

1. **IVFFlat index** - Good balance of speed/accuracy for >1M vectors
2. **Lists parameter** - Start with sqrt(rows), adjust based on performance
3. **Batch embedding generation** - Queue-based async processing
4. **Embedding cache** - Cache recent embeddings (Phase 2)

---

## Data Retention

### Free Tier
- 90 days retention
- Max 10,000 memories per org
- Auto-delete old memories

### Pro Tier
- 365 days retention
- Max 100,000 memories per org
- Manual deletion only

### Enterprise Tier
- Unlimited retention
- Custom limits
- Archive to cold storage (Phase 2)

---

## Backup Strategy

1. **Daily full backups** - Automated via managed PostgreSQL
2. **Point-in-time recovery** - 7 days for all tiers
3. **Cross-region replication** - Enterprise tier only
4. **Backup testing** - Monthly restore tests

---

## Security

1. **Row-level security (RLS)** - Ensure org isolation
2. **Encrypted at rest** - PostgreSQL TDE
3. **Encrypted in transit** - TLS 1.3
4. **Secrets scanning** - Pre-insert hooks to detect API keys
5. **Audit logging** - All write operations logged

---

## Schema Diagram

```
organizations (1) ---> (N) users
organizations (1) ---> (N) api_keys
organizations (1) ---> (N) projects
organizations (1) ---> (N) memories

projects (1) ---> (N) memories

users (1) ---> (N) api_keys

memories (1) ---> (1) embedding_jobs
```

---

**Document Status:** APPROVED  
**Next Review:** After MVP launch (Week 5)  
**Owner:** faintech-cto
