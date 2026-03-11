"""Add task_id column to memories table (TD-013)

Revision ID: e1f2a3b4c5d6
Revises: d4e5f8a7b6c
Create Date: 2026-03-11 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e1f2a3b4c5d6"
down_revision = "d4e5f8a7b6c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add task_id column to memories table for task-scoped memory retrieval."""
    with op.batch_alter_table("memories") as batch_op:
        batch_op.add_column(
            sa.Column("task_id", sa.String(255), nullable=True, index=True)
        )


def downgrade() -> None:
    """Remove task_id column from memories table."""
    with op.batch_alter_table("memories") as batch_op:
        batch_op.drop_column("task_id")
