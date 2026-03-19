"""Add university to users and seed password hashes.

Revision ID: 20260314_225500
Revises:
Create Date: 2026-03-14 22:55:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260314_225500"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS university VARCHAR(255)
        """
    )
    op.execute(
        """
        UPDATE authorization_details
        SET password_hash = CASE id
            WHEN 1 THEN 'pbkdf2_sha256$100000$ABEiM0RVZneImaq7zN3u_w$umGCViBGdu25Ilh0rwtLMy3LgeunGkO1M5rvYAVVhEY'
            WHEN 2 THEN 'pbkdf2_sha256$100000$EREiIjMzRERVVWZmd3eIiA$GAQFeX3ZtUwf0xmkTn-7gzUCzbnxAUaXzHExpAO_F4I'
            WHEN 3 THEN 'pbkdf2_sha256$100000$IiIzM0REVVVmZnd3iIiZmQ$_kz-2FGgvwqdUazrY_eAO7JZsaz4tENLmahR00OBPUU'
            WHEN 4 THEN 'pbkdf2_sha256$100000$MzNERFVVZmZ3d4iImZmqqg$MYNd07TzrZ5oE58SK_Cjm9zAu2D6DH4tIyWUrJiC5bQ'
            WHEN 5 THEN 'pbkdf2_sha256$100000$RERVVWZmd3eIiJmZqqq7uw$MCe5qyD1PrEqkTWRiq1cmdGZuxXXvp477MAEOjU9gB0'
            WHEN 6 THEN 'pbkdf2_sha256$100000$VVVmZnd3iIiZmaqqu7vMzA$x7pX9p4QdepOYim6zUdwQ_poUT_4l1Vf6_9f8YFEwFM'
            ELSE password_hash
        END
        """
    )
    op.execute(
        """
        UPDATE users
        SET university = CASE id
            WHEN 1 THEN 'ITMO University'
            WHEN 2 THEN 'ITMO University'
            WHEN 3 THEN 'ITMO University'
            WHEN 4 THEN 'MSU'
            WHEN 5 THEN 'SPbSU'
            WHEN 6 THEN 'HSE'
            ELSE university
        END
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE authorization_details
        SET password_hash = CASE id
            WHEN 1 THEN 'hash_admin'
            WHEN 2 THEN 'hash_org'
            WHEN 3 THEN 'hash_user1'
            WHEN 4 THEN 'hash_user2'
            WHEN 5 THEN 'hash_user3'
            WHEN 6 THEN 'hash_user4'
            ELSE password_hash
        END
        """
    )
    op.execute(
        """
        ALTER TABLE users
        DROP COLUMN IF EXISTS university
        """
    )
