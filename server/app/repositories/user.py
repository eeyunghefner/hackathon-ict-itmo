from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuthorizationDetails, Role, TeamMember, User


@dataclass(slots=True)
class UserProfileRecord:
    id: int
    full_name: str
    email: str
    role_name: str
    university: str | None
    team_id: int | None


@dataclass(slots=True)
class AuthUserRecord:
    id: int
    email: str
    role_name: str
    password_hash: str


async def get_user_profile_by_id(
    session: AsyncSession,
    user_id: int,
) -> UserProfileRecord | None:
    statement = (
        select(
            User.id,
            User.full_name,
            User.email,
            Role.name.label("role_name"),
            User.university,
            TeamMember.team_id,
        )
        .join(Role, User.role_id == Role.id)
        .outerjoin(TeamMember, TeamMember.user_id == User.id)
        .where(User.id == user_id)
        .order_by(TeamMember.joined_at.asc())
        .limit(1)
    )
    row = (await session.execute(statement)).first()

    if row is None:
        return None

    return UserProfileRecord(
        id=row.id,
        full_name=row.full_name,
        email=row.email,
        role_name=row.role_name,
        university=row.university,
        team_id=row.team_id,
    )


async def get_auth_user_by_email(
    session: AsyncSession,
    email: str,
) -> AuthUserRecord | None:
    statement = (
        select(
            User.id,
            User.email,
            Role.name.label("role_name"),
            AuthorizationDetails.password_hash,
        )
        .join(Role, User.role_id == Role.id)
        .join(
            AuthorizationDetails,
            User.authorization_details_id == AuthorizationDetails.id,
        )
        .where(User.email == email)
    )
    row = (await session.execute(statement)).first()

    if row is None:
        return None

    return AuthUserRecord(
        id=row.id,
        email=row.email,
        role_name=row.role_name,
        password_hash=row.password_hash,
    )


async def get_role_by_name(session: AsyncSession, name: str) -> Role | None:
    statement = select(Role).where(Role.name == name)
    return await session.scalar(statement)


async def create_user_with_password(
    session: AsyncSession,
    *,
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
        email=email,
        full_name=full_name,
        university=university,
        phone=None,
        role_id=role_id,
        authorization_details_id=authorization_details.id,
    )
    session.add(user)
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
