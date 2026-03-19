from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Team
from app.repositories import get_user_by_isu_number, get_user_profile_by_id, update_user_profile
from app.schemas import UpdateUserProfileRequest, UserMeResponse, UserStatusResponse


def split_full_name(full_name: str) -> tuple[str, str]:
    parts = full_name.strip().split(maxsplit=1)
    first_name = parts[0] if parts else ""
    last_name = parts[1] if len(parts) > 1 else ""
    return first_name, last_name


def build_full_name(first_name: str, last_name: str) -> str:
    return f"{first_name.strip()} {last_name.strip()}".strip()


async def get_current_user_profile(
    session: AsyncSession,
    user_id: int,
) -> UserMeResponse:
    user = await get_user_profile_by_id(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    first_name, last_name = split_full_name(user.full_name)

    return UserMeResponse(
        id=str(user.id),
        firstName=first_name,
        lastName=last_name,
        email=user.email,
        roles=user.role_names,
        university=user.university,
        teamId=str(user.team_id) if user.team_id is not None else None,
    )


async def update_current_user_profile(
    session: AsyncSession,
    user_id: int,
    payload: UpdateUserProfileRequest,
) -> UserMeResponse:
    user = await update_user_profile(
        session,
        user_id=user_id,
        full_name=build_full_name(payload.firstName, payload.lastName),
        university=payload.university,
    )

    if user is None:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await session.commit()
    return await get_current_user_profile(session, user_id)


async def get_user_status(
    session: AsyncSession,
    isu_number: int,
) -> UserStatusResponse:
    user = await get_user_by_isu_number(session, isu_number)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role_names = {r.name for r in user.roles_association}

    captain_result = await session.execute(
        select(Team.id).where(Team.captain_id == user.id).limit(1)
    )
    is_captain = captain_result.scalar_one_or_none() is not None

    return UserStatusResponse(
        is_admin="admin" in role_names,
        is_organizer="organizer" in role_names,
        is_captain=is_captain,
        is_attendee="participant" in role_names,
    )
