from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import (
    CreateHackathonRequest,
    CreateHackathonResponse,
    HackathonDetailResponse,
    HackathonListItemResponse,
    UpdateHackathonRequest,
)
from app.services import (
    create_hackathon_entry,
    get_hackathon_entry,
    list_hackathon_entries,
    update_hackathon_entry,
)

router = APIRouter(prefix="/hackathons", tags=["hackathons"])


@router.post("", response_model=CreateHackathonResponse, status_code=status.HTTP_201_CREATED)
async def create_hackathon(
    payload: CreateHackathonRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> CreateHackathonResponse:
    return await create_hackathon_entry(session, current_user_id, payload)


@router.get("", response_model=list[HackathonListItemResponse])
async def read_hackathons(
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> list[HackathonListItemResponse]:
    return await list_hackathon_entries(
        session,
        status_filter=status,
        page=page,
        limit=limit,
    )


@router.get("/{hackathon_id}", response_model=HackathonDetailResponse)
async def read_hackathon(
    hackathon_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> HackathonDetailResponse:
    return await get_hackathon_entry(session, hackathon_id)


@router.patch("/{hackathon_id}", response_model=HackathonDetailResponse)
async def update_hackathon(
    hackathon_id: int,
    payload: UpdateHackathonRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> HackathonDetailResponse:
    return await update_hackathon_entry(
        session,
        user_id=current_user_id,
        hackathon_id=hackathon_id,
        payload=payload,
    )
