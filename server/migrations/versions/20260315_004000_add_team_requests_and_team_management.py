"""Add team requests and team management support.

Revision ID: 20260315_004000
Revises: 20260315_002500
Create Date: 2026-03-15 00:40:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260315_004000"
down_revision = "20260315_002500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS team_requests (
            id SERIAL PRIMARY KEY,
            team_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(team_id, user_id)
        )
        """
    )
    op.execute(
        """
        INSERT INTO team_requests (team_id, user_id, status)
        VALUES
            (1, 4, 'pending'),
            (2, 5, 'pending')
        ON CONFLICT (team_id, user_id) DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS team_requests")
