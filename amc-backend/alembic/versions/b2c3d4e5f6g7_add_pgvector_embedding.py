"""Migrate embedding column to pgvector Vector type (TD-015)

Upgrades the embedding column from float8[] (or JSON) to proper pgvector
vector(1536) type, enabling native cosine similarity search with IVFFlat index.

Only runs on PostgreSQL — skips silently on SQLite.

Revision ID: b2c3d4e5f6g7
Revises: e1f2a3b4c5d6
Create Date: 2026-03-11 12:00:00.000000

"""

import os
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b2c3d4e5f6g7"
down_revision = "e1f2a3b4c5d6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Migrate embedding column to pgvector Vector(1536) type.

    Only executes on PostgreSQL. Skips on SQLite (JSON column stays as-is).

    Steps:
    1. Install pgvector extension
    2. Drop old embedding column (float8[] from d4e5f8a7b6c or JSON from dev)
    3. Add new vector(1536) column
    4. Create IVFFlat index for cosine similarity search
    """
    bind = op.get_bind()
    dialect = bind.dialect.name

    database_type = os.getenv("DATABASE_TYPE", "sqlite").lower()

    if dialect != "postgresql" or database_type != "postgres":
        print(
            f"[TD-015] Skipping pgvector migration: "
            f"dialect={dialect}, DATABASE_TYPE={database_type}. "
            f"Set DATABASE_TYPE=postgres to run this migration."
        )
        return

    # Step 1: Install pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    print("[TD-015] pgvector extension installed (or already present)")

    # Step 2: Drop old embedding column (may be float8[] from d4e5f8a7b6c or JSON)
    # Using IF EXISTS to be safe regardless of prior migration state
    op.execute("ALTER TABLE memories DROP COLUMN IF EXISTS embedding;")
    print("[TD-015] Dropped old embedding column")

    # Step 3: Add proper vector(1536) column
    # vector(1536) = 1536-dimension float vector (text-embedding-3-small dimensions)
    op.execute("ALTER TABLE memories ADD COLUMN embedding vector(1536);")
    print("[TD-015] Added vector(1536) embedding column")

    # Step 4: Create IVFFlat index for cosine similarity search
    # lists=100 is appropriate for tables up to ~1M rows
    # For larger tables: lists = sqrt(row_count) is recommended
    # vector_cosine_ops → cosine distance (<=> operator)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_memories_embedding
        ON memories
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    """)
    print("[TD-015] Created IVFFlat cosine similarity index on embedding column")

    # Step 5: Ensure embedded_at index exists (may already exist from d4e5f8a7b6c)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_memories_embedded_at
        ON memories (embedded_at);
    """)
    print("[TD-015] Ensured embedded_at index exists")

    print("[TD-015] pgvector migration complete. Run: SELECT COUNT(*) FROM memories;")


def downgrade() -> None:
    """Revert from pgvector Vector(1536) back to JSON embedding column.

    Only executes on PostgreSQL.
    """
    bind = op.get_bind()
    dialect = bind.dialect.name

    database_type = os.getenv("DATABASE_TYPE", "sqlite").lower()

    if dialect != "postgresql" or database_type != "postgres":
        print(
            f"[TD-015] Skipping pgvector rollback: "
            f"dialect={dialect}, DATABASE_TYPE={database_type}."
        )
        return

    # Drop IVFFlat index
    op.execute("DROP INDEX IF EXISTS idx_memories_embedded_at;")
    op.execute("DROP INDEX IF EXISTS idx_memories_embedding;")
    print("[TD-015] Dropped vector indexes")

    # Drop vector column
    op.execute("ALTER TABLE memories DROP COLUMN IF EXISTS embedding;")
    print("[TD-015] Dropped vector(1536) column")

    # Restore JSON column (SQLite-compatible fallback)
    op.execute("ALTER TABLE memories ADD COLUMN embedding JSON;")
    print("[TD-015] Restored JSON embedding column (SQLite-compatible)")

    # Note: pgvector extension is NOT dropped — it may be used by other tables
    # To drop: CREATE EXTENSION IF NOT EXISTS vector is idempotent anyway
    print("[TD-015] Rollback complete. pgvector extension left in place.")
