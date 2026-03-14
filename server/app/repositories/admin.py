from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuthorizationDetails, Role, User


@dataclass(slots=True)
class AdminUserRecord:
    id: int
    email: str
    full_name: str
    role_name: str
    university: str | None


async def list_users_for_admin(
    session: AsyncSession,
    *,
    role: str | None,
    page: int,
    limit: int,
) -> list[AdminUserRecord]:
    statement = (
        select(
            User.id,
            User.email,
            User.full_name,
            Role.name.label("role_name"),
            User.university,
        )
        .join(Role, User.role_id == Role.id)
        .order_by(User.id.asc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    if role is not None:
        statement = statement.where(Role.name == role)

    rows = (await session.execute(statement)).all()
    return [
        AdminUserRecord(
            id=row.id,
            email=row.email,
            full_name=row.full_name,
            role_name=row.role_name,
            university=row.university,
        )
        for row in rows
    ]


async def get_user_with_role_for_admin(
    session: AsyncSession,
    user_id: int,
) -> AdminUserRecord | None:
    statement = (
        select(
            User.id,
            User.email,
            User.full_name,
            Role.name.label("role_name"),
            User.university,
        )
        .join(Role, User.role_id == Role.id)
        .where(User.id == user_id)
    )
    row = (await session.execute(statement)).first()
    if row is None:
        return None

    return AdminUserRecord(
        id=row.id,
        email=row.email,
        full_name=row.full_name,
        role_name=row.role_name,
        university=row.university,
    )


async def get_user_model_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_authorization_details_by_id(
    session: AsyncSession,
    authorization_details_id: int,
) -> AuthorizationDetails | None:
    return await session.get(AuthorizationDetails, authorization_details_id)
