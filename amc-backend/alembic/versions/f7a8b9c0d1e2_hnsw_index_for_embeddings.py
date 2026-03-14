"""Replace IVFFlat with HNSW index for better vector search performance

HNSW (Hierarchical Navigable Small World) provides:
- Faster approximate nearest neighbor search
- Better recall at similar query times
- No need to rebuild index as data grows (unlike IVFFlat)

Revision ID: f7a8b9c0d1e2
Revises: b2c3d4e5f6g7
Create Date: 2026-03-13 05:00:00.000000

"""

import os
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f7a8b9c0d1e2"
down_revision = "b2c3d4e5f6g7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Replace IVFFlat index with HNSW for better performance.

    Only executes on PostgreSQL with pgvector extension.
    """
    bind = op.get_bind()
    dialect = bind.dialect.name

    database_type = os.getenv("DATABASE_TYPE", "sqlite").lower()

    if dialect != "postgresql" or database_type != "postgres":
        print(
            f"[AMC-MVP-110] Skipping HNSW migration: "
            f"dialect={dialect}, DATABASE_TYPE={database_type}. "
            f"Set DATABASE_TYPE=postgres to run this migration."
        )
        return

    # Drop old IVFFlat index
    op.execute("DROP INDEX IF EXISTS idx_memories_embedding;")
    print("[AMC-MVP-110] Dropped old IVFFlat index")

    # Create HNSW index with optimal parameters for AMC use case
    # m=16: number of bi-directional links for each node (16 is good balance)
    # ef_construction=64: size of dynamic candidate list during index build
    # These settings work well for tables with 10K-1M rows
    op.execute("""
        CREATE INDEX idx_memories_embedding_hnsw
        ON memories
        USING hnsw (embedding vector_cosine_ops)
        WITH (
            m = 16,
            ef_construction = 64
        );
    """)
    print("[AMC-MVP-110] Created HNSW index with m=16, ef_construction=64")

    print("[AMC-MVP-110] HNSW migration complete. Vector search now optimized.")


def downgrade() -> None:
    """Revert to IVFFlat index.

    Only executes on PostgreSQL.
    """
    bind = op.get_bind()
    dialect = bind.dialect.name

    database_type = os.getenv("DATABASE_TYPE", "sqlite").lower()

    if dialect != "postgresql" or database_type != "postgres":
        print(
            f"[AMC-MVP-110] Skipping HNSW rollback: "
            f"dialect={dialect}, DATABASE_TYPE={database_type}."
        )
        return

    # Drop HNSW index
    op.execute("DROP INDEX IF EXISTS idx_memories_embedding_hnsw;")
    print("[AMC-MVP-110] Dropped HNSW index")

    # Restore IVFFlat index
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_memories_embedding
        ON memories
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    """)
    print("[AMC-MVP-110] Restored IVFFlat index")
