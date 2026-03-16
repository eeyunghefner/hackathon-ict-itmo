"""Add archived hackathon status.

Revision ID: 20260315_001000
Revises: 20260314_235500
Create Date: 2026-03-15 00:10:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260315_001000"
down_revision = "20260314_235500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO hackathon_status (name)
        SELECT 'archived'
        WHERE NOT EXISTS (
            SELECT 1
            FROM hackathon_status
            WHERE name = 'archived'
        )
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM hackathon_status
        WHERE name = 'archived'
        """
    )
