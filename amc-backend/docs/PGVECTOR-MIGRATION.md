# PGVector Migration Plan (TD-015)

## Current State (TD-014)

**Status:** SQLite with JSON-stored embeddings
**Performance:** Python-based cosine similarity calculation
**Limitations:**
- All embeddings loaded into memory for similarity search
- Slower performance at scale (O(n) per query)
- No index support for vector operations

## Migration Target

**Database:** PostgreSQL with pgvector extension
**Column Type:** `Vector(1536)` for text-embedding-3-small
**Performance:** Indexed vector similarity search
**Benefits:**
- Sub-linear query performance with IVFFlat or HNSW indexes
- Native SQL operators (`<=>`, `<->`, `<#>`)
- Production-ready for millions of vectors

## Migration Steps

### 1. Setup PostgreSQL with pgvector

```bash
# Install PostgreSQL
brew install postgresql@15

# Install pgvector extension
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
make install  # may require sudo
```

### 2. Create Migration Script

```python
# alembic/versions/xxx_migrate_to_pgvector.py

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

def upgrade():
    # Add pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Add new vector column
    op.add_column('memories', sa.Column('embedding_vec', Vector(1536)))

    # Migrate data from JSON to Vector
    op.execute('''
        UPDATE memories
        SET embedding_vec = embedding::jsonb::text::vector
        WHERE embedding IS NOT NULL
    ''')

    # Drop old JSON column
    op.drop_column('memories', 'embedding')

    # Rename new column
    op.alter_column('memories', 'embedding_vec', new_column_name='embedding')

    # Create vector index (IVFFlat for ~1000-1M vectors)
    op.execute('''
        CREATE INDEX idx_memories_embedding ON memories
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    ''')
```

### 3. Update SQLAlchemy Model

```python
# app/models/memory.py
from pgvector.sqlalchemy import Vector

class Memory(Base):
    embedding = Column(Vector(1536), nullable=True)
```

### 4. Update Semantic Search Query

```python
# app/routers/semantic.py
from sqlalchemy import text

query = text("""
    SELECT
        id, workspace_id, agent_id, project_id, type, content,
        tags, importance, created_at, updated_at,
        1 - (embedding <=> :query_vector) as similarity
    FROM memories
    WHERE deleted_at IS NULL
    AND embedding IS NOT NULL
    ORDER BY similarity DESC
    LIMIT :limit
""")
```

### 5. Testing Checklist

- [ ] PostgreSQL container running locally
- [ ] pgvector extension installed
- [ ] Migration script tested on copy of production data
- [ ] Semantic search returns same results as Python implementation
- [ ] Performance benchmarks (query time, memory usage)
- [ ] Index creation successful
- [ ] All existing tests pass

## Performance Expectations

| Metric | SQLite (JSON) | PostgreSQL (pgvector) |
|--------|---------------|----------------------|
| Query time (1K vectors) | ~50ms | ~5ms |
| Query time (10K vectors) | ~500ms | ~10ms |
| Query time (100K vectors) | ~5s | ~20ms |
| Memory usage | High (loads all) | Low (indexed) |
| Index support | No | Yes (IVFFlat/HNSW) |

## Rollback Plan

If migration fails:
1. Restore from backup
2. Revert to TD-014 code (JSON embeddings)
3. Investigate failure in staging environment

## Timeline

- **Week 1:** Setup PostgreSQL locally, test migration script
- **Week 2:** Performance benchmarks, index tuning
- **Week 3:** Staging deployment, validation
- **Week 4:** Production deployment with monitoring

## Dependencies

- PostgreSQL 15+
- pgvector extension 0.5.0+
- SQLAlchemy 2.0+
- Alembic migration tool

## Related Tasks

- TD-014: Fix SQLite ARRAY Type Incompatibility (current)
- TD-015: Migrate to pgvector (this task)
- AMC-MVP-110: Memory Search Optimization (blocked by this)

## References

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [PostgreSQL Vector Search](https://supabase.com/blog/pg-embed)
- [Migration Guide](https://github.com/pgvector/pgvector#migrating-data)
