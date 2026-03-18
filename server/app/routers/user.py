from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import UpdateUserProfileRequest, UserMeResponse, UserStatusResponse
from app.services import (
    get_current_user_profile,
    get_user_status,
    update_current_user_profile,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
async def read_current_user(
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> UserMeResponse:
    return await get_current_user_profile(session, current_user_id)


@router.patch("/me", response_model=UserMeResponse)
async def update_current_user(
    payload: UpdateUserProfileRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> UserMeResponse:
    return await update_current_user_profile(session, current_user_id, payload)


@router.get("/status", response_model=UserStatusResponse)
async def read_user_status(
    isu_number: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
) -> UserStatusResponse:
    return await get_user_status(session, isu_number)
