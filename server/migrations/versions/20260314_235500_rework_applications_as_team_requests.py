"""Rework applications as team requests.

Revision ID: 20260314_235500
Revises: 20260314_232000
Create Date: 2026-03-14 23:55:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260314_235500"
down_revision = "20260314_232000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS applications")
    op.execute(
        """
        CREATE TABLE applications (
            id SERIAL PRIMARY KEY,
            team_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
            hackathon_id INT NOT NULL REFERENCES hackathons(id) ON DELETE CASCADE,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(team_id, hackathon_id)
        )
        """
    )
    op.execute(
        """
        INSERT INTO applications (team_id, hackathon_id, status)
        VALUES
            (1, 1, 'pending'),
            (2, 1, 'approved'),
            (3, 2, 'pending')
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS applications")
    op.execute(
        """
        CREATE TABLE applications (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            hackathon_id INT NOT NULL REFERENCES hackathons(id) ON DELETE CASCADE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, hackathon_id)
        )
        """
    )
    op.execute(
        """
        INSERT INTO applications (user_id, hackathon_id)
        VALUES
            (3, 1),
            (4, 1),
            (5, 1),
            (6, 1),
            (3, 2),
            (4, 2)
        """
    )
