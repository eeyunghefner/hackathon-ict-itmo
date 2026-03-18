from datetime import date

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import (
    AdminHackathonHistoryItemResponse,
    AdminUserResponse,
    UpdateAdminUserRequest,
)
from app.services import (
    delete_admin_user,
    get_admin_hackathon_history,
    get_admin_users,
    update_admin_user,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[AdminUserResponse])
async def read_admin_users(
    role: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> list[AdminUserResponse]:
    return await get_admin_users(
        session,
        current_user_id=current_user_id,
        role=role,
        page=page,
    )


@router.get("/hackathons/history", response_model=list[AdminHackathonHistoryItemResponse])
async def read_admin_hackathon_history(
    startDate: date | None = Query(default=None),
    endDate: date | None = Query(default=None),
    participantsMin: int | None = Query(default=None, ge=0),
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> list[AdminHackathonHistoryItemResponse]:
    return await get_admin_hackathon_history(
        session,
        current_user_id=current_user_id,
        start_date=startDate,
        end_date=endDate,
        participants_min=participantsMin,
    )


@router.patch("/users/{user_id}", response_model=AdminUserResponse)
async def patch_admin_user(
    user_id: int,
    payload: UpdateAdminUserRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> AdminUserResponse:
    return await update_admin_user(
        session,
        current_user_id=current_user_id,
        user_id=user_id,
        payload=payload,
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_admin_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    await delete_admin_user(
        session,
        current_user_id=current_user_id,
        user_id=user_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
