from dataclasses import dataclass

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import AuthorizationDetails, User, UserRole


@dataclass(slots=True)
class AdminUserRecord:
    id: int
    email: str
    full_name: str
    role_names: list[str]
    university: str | None


async def list_users_for_admin(
    session: AsyncSession,
    *,
    role: str | None,
    page: int,
    limit: int,
) -> list[AdminUserRecord]:
    statement = (
        select(User)
        .options(selectinload(User.roles_association))
        .order_by(User.id.asc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    if role is not None:
        from app.models import Role
        statement = (
            statement
            .join(UserRole, UserRole.user_id == User.id)
            .join(Role, Role.id == UserRole.role_id)
            .where(Role.name == role)
        )

    rows = (await session.scalars(statement)).all()
    return [
        AdminUserRecord(
            id=u.id,
            email=u.email,
            full_name=u.full_name,
            role_names=[r.name for r in u.roles_association],
            university=u.university,
        )
        for u in rows
    ]


async def get_user_with_role_for_admin(
    session: AsyncSession,
    user_id: int,
) -> AdminUserRecord | None:
    result = await session.execute(
        select(User)
        .options(selectinload(User.roles_association))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    return AdminUserRecord(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role_names=[r.name for r in user.roles_association],
        university=user.university,
    )


async def get_user_model_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_authorization_details_by_id(
    session: AsyncSession,
    authorization_details_id: int,
) -> AuthorizationDetails | None:
    return await session.get(AuthorizationDetails, authorization_details_id)


async def set_user_roles(
    session: AsyncSession,
    *,
    user_id: int,
    role_id: int,
) -> None:
    """Replace all user roles with a single new role."""
    await session.execute(delete(UserRole).where(UserRole.user_id == user_id))
    session.add(UserRole(user_id=user_id, role_id=role_id))
    await session.flush()
