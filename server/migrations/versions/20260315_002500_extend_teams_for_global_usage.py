"""Extend teams for global usage.

Revision ID: 20260315_002500
Revises: 20260315_001000
Create Date: 2026-03-15 00:25:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260315_002500"
down_revision = "20260315_001000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE teams
        ADD COLUMN IF NOT EXISTS description TEXT
        """
    )
    op.execute(
        """
        ALTER TABLE teams
        ALTER COLUMN hackathon_id DROP NOT NULL
        """
    )
    op.execute(
        """
        UPDATE teams
        SET description = COALESCE(description, 'Team description is not set')
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE teams
        SET hackathon_id = 1
        WHERE hackathon_id IS NULL
        """
    )
    op.execute(
        """
        ALTER TABLE teams
        ALTER COLUMN hackathon_id SET NOT NULL
        """
    )
    op.execute(
        """
        ALTER TABLE teams
        DROP COLUMN IF EXISTS description
        """
    )
