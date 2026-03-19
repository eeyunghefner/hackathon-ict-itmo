"""Migrate roles to many-to-many via user_role table, add isu_number to users.

Revision ID: 20260315_020000
Revises: 20260315_013500
Create Date: 2026-03-15 02:00:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260315_020000"
down_revision = "20260315_013500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add isu_number as nullable first so existing rows are not rejected
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS isu_number INTEGER
        """
    )

    # 2. Populate isu_number for existing seed users
    op.execute(
        """
        UPDATE users SET isu_number = CASE id
            WHEN 1 THEN 100001
            WHEN 2 THEN 100002
            WHEN 3 THEN 100003
            WHEN 4 THEN 100004
            WHEN 5 THEN 100005
            WHEN 6 THEN 100006
            ELSE 1000000 + id
        END
        WHERE isu_number IS NULL
        """
    )

    # 3. Apply NOT NULL + UNIQUE constraint
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN isu_number SET NOT NULL
        """
    )
    op.execute(
        """
        ALTER TABLE users
        ADD CONSTRAINT users_isu_number_unique UNIQUE (isu_number)
        """
    )

    # 4. Create user_role association table
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS user_role (
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_id INT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
            PRIMARY KEY (user_id, role_id)
        )
        """
    )

    # 5. Migrate existing role assignments from users.role_id into user_role
    op.execute(
        """
        INSERT INTO user_role (user_id, role_id)
        SELECT id, role_id FROM users
        ON CONFLICT DO NOTHING
        """
    )

    # 6. Drop the role_id FK and column from users
    op.execute(
        """
        ALTER TABLE users
        DROP CONSTRAINT IF EXISTS users_role_id_fkey
        """
    )
    op.execute(
        """
        ALTER TABLE users
        DROP COLUMN IF EXISTS role_id
        """
    )


def downgrade() -> None:
    # 1. Re-add role_id column (nullable initially)
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS role_id INT
        """
    )

    # 2. Restore role_id from user_role (pick the lowest role_id per user)
    op.execute(
        """
        UPDATE users u
        SET role_id = (
            SELECT role_id FROM user_role ur
            WHERE ur.user_id = u.id
            ORDER BY role_id ASC
            LIMIT 1
        )
        """
    )

    # 3. Set NOT NULL and FK constraint on role_id
    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN role_id SET NOT NULL
        """
    )
    op.execute(
        """
        ALTER TABLE users
        ADD CONSTRAINT users_role_id_fkey
        FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE RESTRICT
        """
    )

    # 4. Drop user_role table
    op.execute("DROP TABLE IF EXISTS user_role")

    # 5. Drop isu_number column
    op.execute(
        """
        ALTER TABLE users
        DROP CONSTRAINT IF EXISTS users_isu_number_unique
        """
    )
    op.execute(
        """
        ALTER TABLE users
        DROP COLUMN IF EXISTS isu_number
        """
    )
