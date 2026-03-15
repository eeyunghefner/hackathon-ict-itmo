from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    get_authorization_details_by_id,
    get_hackathon_stats,
    get_role_by_name,
    get_user_model_by_id,
    get_user_profile_by_id,
    get_user_with_role_for_admin,
    list_hackathon_history,
    list_users_for_admin,
    set_user_roles,
)
from app.schemas import (
    AdminHackathonHistoryItemResponse,
    AdminUserResponse,
    UpdateAdminUserRequest,
)
from app.services.user import split_full_name

ADMIN_ROLE = "admin"
DEFAULT_ADMIN_USERS_LIMIT = 10


def _map_admin_user(record) -> AdminUserResponse:
    first_name, last_name = split_full_name(record.full_name)
    return AdminUserResponse(
        id=str(record.id),
        firstName=first_name,
        lastName=last_name,
        email=record.email,
        roles=record.role_names,
        university=record.university,
    )


async def _require_admin(session: AsyncSession, user_id: int) -> None:
    user = await get_user_profile_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if ADMIN_ROLE not in user.role_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access is required",
        )


async def get_admin_users(
    session: AsyncSession,
    *,
    current_user_id: int,
    role: str | None,
    page: int,
) -> list[AdminUserResponse]:
    await _require_admin(session, current_user_id)
    users = await list_users_for_admin(
        session,
        role=role,
        page=page,
        limit=DEFAULT_ADMIN_USERS_LIMIT,
    )
    return [_map_admin_user(user) for user in users]


async def get_admin_hackathon_history(
    session: AsyncSession,
    *,
    current_user_id: int,
    start_date,
    end_date,
    participants_min: int | None,
) -> list[AdminHackathonHistoryItemResponse]:
    await _require_admin(session, current_user_id)
    records = await list_hackathon_history(
        session,
        start_date=start_date,
        end_date=end_date,
        participants_min=participants_min,
    )
    return [
        AdminHackathonHistoryItemResponse(
            id=str(record.id),
            title=record.title,
            startDate=record.start_date.date(),
            endDate=record.end_date.date(),
            status=record.status,
            participants=record.participants,
            teams=record.teams,
        )
        for record in records
    ]


async def update_admin_user(
    session: AsyncSession,
    *,
    current_user_id: int,
    user_id: int,
    payload: UpdateAdminUserRequest,
) -> AdminUserResponse:
    await _require_admin(session, current_user_id)

    user = await get_user_model_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = await get_role_by_name(session, payload.role)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    await set_user_roles(session, user_id=user.id, role_id=role.id)
    await session.commit()

    updated_user = await get_user_with_role_for_admin(session, user_id)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User was updated but could not be loaded",
        )

    return _map_admin_user(updated_user)


async def delete_admin_user(
    session: AsyncSession,
    *,
    current_user_id: int,
    user_id: int,
) -> None:
    await _require_admin(session, current_user_id)

    user = await get_user_model_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    authorization_details = await get_authorization_details_by_id(
        session,
        user.authorization_details_id,
    )

    await session.delete(user)
    await session.flush()

    if authorization_details is not None:
        await session.delete(authorization_details)

    await session.commit()
