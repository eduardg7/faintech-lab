"""Add embedding column for semantic search

Revision ID: d4e5f8a7b6c
Revises: c8f3a1d2e5b4
Create Date: 2026-03-10 20:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e5f8a7b6c'
down_revision = 'c8f3a1d2e5b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add embedding column and index for semantic search."""
    
    # Check if we're on PostgreSQL
    bind = op.get_bind()
    dialect = bind.dialect.name
    
    if dialect == 'postgresql':
        # Add embedding column (array of floats for 1536 dimensions)
        op.execute("""
            ALTER TABLE memories
            ADD COLUMN IF NOT EXISTS embedding float8[];
        """)
        
        # Add embedding timestamp
        op.execute("""
            ALTER TABLE memories
            ADD COLUMN IF NOT EXISTS embedded_at TIMESTAMP;
        """)
        
        # Create vector index using pgvector (requires extension)
        # Note: pgvector extension must be installed first
        op.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_embedding
            ON memories USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        """)
        
        # Create index for embedding timestamp
        op.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_embedded_at
            ON memories (embedded_at);
        """)
    else:
        # For SQLite, embedding is not supported (no vector operations)
        # Store a marker that embedding is not available
        print(f"Skipping vector embedding column creation for {dialect} (not supported)")


def downgrade() -> None:
    """Remove embedding column and index."""
    
    bind = op.get_bind()
    dialect = bind.dialect.name
    
    if dialect == 'postgresql':
        op.execute("""
            DROP INDEX IF EXISTS idx_memories_embedded_at;
        """)
        
        op.execute("""
            DROP INDEX IF EXISTS idx_memories_embedding;
        """)
        
        op.execute("""
            ALTER TABLE memories DROP COLUMN IF EXISTS embedding;
        """)
        
        op.execute("""
            ALTER TABLE memories DROP COLUMN IF EXISTS embedded_at;
        """)
