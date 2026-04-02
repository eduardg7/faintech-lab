"""add utm tracking columns to users table for Week 2 GTM channel attribution

Revision ID: e2f5g9c7h4i8
Revises: a1b2c3d4e5f6
Create Date: 2026-04-01 15:45:00.000000

Task: LAB-ANALYTICS-20260401-UTMCAPTURE - P0 Add UTM parameter capture to signup flow

This migration adds 6 UTM tracking columns to the users table:
- utm_source: Marketing channel (e.g., 'hn', 'reddit', 'linkedin')
- utm_medium: Medium (e.g., 'post', 'article', 'referral')
- utm_campaign: Campaign identifier
- utm_content: Content/A/B test variant
- utm_term: Keyword/search term
- utm_referrer: Referring URL

These columns enable Week 2 GTM channel attribution:
- Measure which channel delivers signups (HN, Reddit, LinkedIn, Twitter, direct)
- Calculate CAC per channel
- Optimize GTM spend based on data-driven channel performance
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2f5g9c7h4i8'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add UTM tracking columns to users table."""
    # Add UTM columns with proper indexes for fast channel attribution queries
    op.add_column('users', sa.Column('utm_source', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('utm_medium', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('utm_campaign', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('utm_content', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('utm_term', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('utm_referrer', sa.String(255), nullable=True))

    # Create indexes for fast channel attribution queries (Week 2 GTM SQL queries)
    op.create_index('ix_users_utm_source', 'users', ['utm_source'])
    op.create_index('ix_users_utm_medium', 'users', ['utm_medium'])
    op.create_index('ix_users_utm_campaign', 'users', ['utm_campaign'])
    op.create_index('ix_users_utm_referrer', 'users', ['utm_referrer'])


def downgrade() -> None:
    """Remove UTM tracking columns from users table."""
    # Drop indexes first
    op.drop_index('ix_users_utm_source', table_name='users')
    op.drop_index('ix_users_utm_medium', table_name='users')
    op.drop_index('ix_users_utm_campaign', table_name='users')
    op.drop_index('ix_users_utm_referrer', table_name='users')

    # Drop columns
    op.drop_column('users', 'utm_referrer')
    op.drop_column('users', 'utm_term')
    op.drop_column('users', 'utm_content')
    op.drop_column('users', 'utm_campaign')
    op.drop_column('users', 'utm_medium')
    op.drop_column('users', 'utm_source')
