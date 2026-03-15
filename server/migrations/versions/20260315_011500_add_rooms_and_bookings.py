"""Add rooms and room bookings.

Revision ID: 20260315_011500
Revises: 20260315_004000
Create Date: 2026-03-15 01:15:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260315_011500"
down_revision = "20260315_004000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            capacity INT NOT NULL
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS room_bookings (
            id SERIAL PRIMARY KEY,
            room_id INT NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
            created_by INT NULL REFERENCES users(id) ON DELETE SET NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    op.execute(
        """
        INSERT INTO rooms (name, capacity)
        VALUES
            ('Auditorium A', 200),
            ('Lecture Hall B', 120),
            ('Conference Room C', 40)
        ON CONFLICT (name) DO NOTHING
        """
    )
    op.execute(
        """
        INSERT INTO room_bookings (room_id, created_by, start_time, end_time)
        VALUES
            (1, 2, '2026-05-10 10:00:00', '2026-05-10 14:00:00'),
            (2, 2, '2026-05-10 12:00:00', '2026-05-10 15:30:00')
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS room_bookings")
    op.execute("DROP TABLE IF EXISTS rooms")
