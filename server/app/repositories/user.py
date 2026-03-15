from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import AuthorizationDetails, TeamMember, User, UserRole


@dataclass(slots=True)
class UserProfileRecord:
    id: int
    full_name: str
    email: str
    role_names: list[str]
    university: str | None
    team_id: int | None


@dataclass(slots=True)
class AuthUserRecord:
    id: int
    email: str
    role_names: list[str]
    password_hash: str


async def get_user_profile_by_id(
    session: AsyncSession,
    user_id: int,
) -> UserProfileRecord | None:
    result = await session.execute(
        select(User)
        .options(selectinload(User.roles_association))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    team_result = await session.execute(
        select(TeamMember.team_id)
        .where(TeamMember.user_id == user_id)
        .order_by(TeamMember.joined_at.asc())
        .limit(1)
    )
    team_id = team_result.scalar_one_or_none()

    return UserProfileRecord(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role_names=[r.name for r in user.roles_association],
        university=user.university,
        team_id=team_id,
    )


async def get_user_by_isu_number(
    session: AsyncSession,
    isu_number: int,
) -> User | None:
    result = await session.execute(
        select(User)
        .options(selectinload(User.roles_association))
        .where(User.isu_number == isu_number)
    )
    return result.scalar_one_or_none()


async def get_auth_user_by_email(
    session: AsyncSession,
    email: str,
) -> AuthUserRecord | None:
    result = await session.execute(
        select(User)
        .options(selectinload(User.roles_association))
        .where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    auth_result = await session.execute(
        select(AuthorizationDetails.password_hash).where(
            AuthorizationDetails.id == user.authorization_details_id
        )
    )
    password_hash = auth_result.scalar_one_or_none()
    if password_hash is None:
        return None

    return AuthUserRecord(
        id=user.id,
        email=user.email,
        role_names=[r.name for r in user.roles_association],
        password_hash=password_hash,
    )


async def get_role_by_name(session: AsyncSession, name: str):
    from app.models import Role
    statement = select(Role).where(Role.name == name)
    return await session.scalar(statement)


async def create_user_with_password(
    session: AsyncSession,
    *,
    isu_number: int,
    email: str,
    full_name: str,
    university: str,
    role_id: int,
    password_hash: str,
) -> User:
    authorization_details = AuthorizationDetails(password_hash=password_hash)
    session.add(authorization_details)
    await session.flush()

    user = User(
        isu_number=isu_number,
        email=email,
        full_name=full_name,
        university=university,
        phone=None,
        authorization_details_id=authorization_details.id,
    )
    session.add(user)
    await session.flush()

    session.add(UserRole(user_id=user.id, role_id=role_id))
    await session.flush()

    return user


async def update_user_profile(
    session: AsyncSession,
    *,
    user_id: int,
    full_name: str,
    university: str,
) -> User | None:
    user = await session.get(User, user_id)
    if user is None:
        return None

    user.full_name = full_name
    user.university = university
    await session.flush()
    return user
