"""Add full-text GIN index for memory content search

Revision ID: c8f3a1d2e5b4
Revises: b542b4effa56
Create Date: 2026-03-10 20:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8f3a1d2e5b4'
down_revision = 'b542b4effa56'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add GIN index for full-text search on memories.content.
    
    Note: This migration is PostgreSQL-specific. For SQLite development,
    the search router falls back to LIKE-based search.
    """
    # Check if we're on PostgreSQL
    bind = op.get_bind()
    dialect = bind.dialect.name
    
    if dialect == 'postgresql':
        # Create a generated column for tsvector (PostgreSQL specific)
        # This allows efficient full-text search with GIN index
        op.execute("""
            -- Add tsvector generated column for content
            ALTER TABLE memories 
            ADD COLUMN IF NOT EXISTS content_tsvector tsvector 
            GENERATED ALWAYS AS (to_tsvector('english', coalesce(content, ''))) STORED;
        """)
        
        # Create GIN index on the tsvector column
        op.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_content_gin 
            ON memories USING GIN (content_tsvector);
        """)
        
        # Also add GIN index on tags for efficient tag search
        op.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_tags_gin 
            ON memories USING GIN (tags jsonb_path_ops);
        """)
    else:
        # For SQLite, create a simple FTS5 virtual table if available
        # Otherwise, rely on the search router's fallback to LIKE
        print(f"Skipping PostgreSQL-specific full-text index creation for {dialect}")


def downgrade() -> None:
    """Remove full-text search indexes."""
    bind = op.get_bind()
    dialect = bind.dialect.name
    
    if dialect == 'postgresql':
        op.execute("""
            DROP INDEX IF EXISTS idx_memories_tags_gin;
        """)
        
        op.execute("""
            DROP INDEX IF EXISTS idx_memories_content_gin;
        """)
        
        op.execute("""
            ALTER TABLE memories DROP COLUMN IF EXISTS content_tsvector;
        """)
