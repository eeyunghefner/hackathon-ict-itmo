"""Add events.

Revision ID: 20260315_013500
Revises: 20260315_011500
Create Date: 2026-03-15 01:35:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260315_013500"
down_revision = "20260315_011500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            hackathon_id INT NOT NULL REFERENCES hackathons(id) ON DELETE CASCADE,
            room_id INT NOT NULL REFERENCES rooms(id) ON DELETE RESTRICT,
            title TEXT NOT NULL,
            description TEXT,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    op.execute(
        """
        INSERT INTO events (hackathon_id, room_id, title, description, start_time, end_time)
        VALUES
            (1, 3, 'Opening Ceremony', 'Opening speech and kickoff', '2026-05-10 10:00:00', '2026-05-10 11:00:00'),
            (1, 3, 'Team Introductions', 'Short presentations by teams', '2026-05-10 11:30:00', '2026-05-10 12:30:00')
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS events")
