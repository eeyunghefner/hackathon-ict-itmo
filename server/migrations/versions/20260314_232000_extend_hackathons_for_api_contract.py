"""Extend hackathons for API contract.

Revision ID: 20260314_232000
Revises: 20260314_225500
Create Date: 2026-03-14 23:20:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260314_232000"
down_revision = "20260314_225500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE hackathons
        ADD COLUMN IF NOT EXISTS theme VARCHAR(255)
        """
    )
    op.execute(
        """
        ALTER TABLE hackathons
        ADD COLUMN IF NOT EXISTS format VARCHAR(50)
        """
    )
    op.execute(
        """
        ALTER TABLE hackathons
        ADD COLUMN IF NOT EXISTS rules TEXT
        """
    )
    op.execute(
        """
        UPDATE hackathon_status
        SET name = 'published'
        WHERE name = 'registration_open'
        """
    )
    op.execute(
        """
        UPDATE hackathons
        SET
            theme = COALESCE(theme, title),
            format = COALESCE(format, 'online'),
            rules = COALESCE(rules, 'Follow the event rules published by organizers.')
        """
    )
    op.execute(
        """
        ALTER TABLE hackathons
        ALTER COLUMN theme SET NOT NULL
        """
    )
    op.execute(
        """
        ALTER TABLE hackathons
        ALTER COLUMN format SET NOT NULL
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE hackathon_status
        SET name = 'registration_open'
        WHERE name = 'published'
        """
    )
    op.execute(
        """
        ALTER TABLE hackathons
        DROP COLUMN IF EXISTS rules
        """
    )
    op.execute(
        """
        ALTER TABLE hackathons
        DROP COLUMN IF EXISTS format
        """
    )
    op.execute(
        """
        ALTER TABLE hackathons
        DROP COLUMN IF EXISTS theme
        """
    )
