from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import (
    ApplicationResponse,
    CreateHackathonRequest,
    CreateApplicationRequest,
    CreateEventRequest,
    CreateHackathonResponse,
    EventResponse,
    HackathonDetailResponse,
    HackathonListItemResponse,
    HackathonStatsResponse,
    UpdateHackathonRequest,
)
from app.services import (
    archive_hackathon,
    create_hackathon_entry,
    create_event_entry,
    get_hackathon_entry,
    get_hackathon_applications,
    get_hackathon_events,
    get_hackathon_stats_entry,
    list_hackathon_entries,
    publish_hackathon,
    submit_team_application,
    unpublish_hackathon,
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


@router.post("/{hackathon_id}/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event_for_hackathon(
    hackathon_id: int,
    payload: CreateEventRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> EventResponse:
    return await create_event_entry(
        session,
        current_user_id=current_user_id,
        hackathon_id=hackathon_id,
        payload=payload,
    )


@router.post("/{hackathon_id}/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application_for_hackathon(
    hackathon_id: int,
    payload: CreateApplicationRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> ApplicationResponse:
    return await submit_team_application(
        session,
        current_user_id=current_user_id,
        hackathon_id=hackathon_id,
        payload=payload,
    )


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


@router.get("/{hackathon_id}/applications", response_model=list[ApplicationResponse])
async def read_hackathon_applications(
    hackathon_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> list[ApplicationResponse]:
    return await get_hackathon_applications(
        session,
        current_user_id=current_user_id,
        hackathon_id=hackathon_id,
    )


@router.get("/{hackathon_id}/events", response_model=list[EventResponse])
async def read_hackathon_events(
    hackathon_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> list[EventResponse]:
    return await get_hackathon_events(session, hackathon_id)


@router.get("/{hackathon_id}/stats", response_model=HackathonStatsResponse)
async def read_hackathon_stats(
    hackathon_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> HackathonStatsResponse:
    return await get_hackathon_stats_entry(session, hackathon_id)


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


@router.patch("/{hackathon_id}/publish", response_model=HackathonDetailResponse)
async def publish_hackathon_route(
    hackathon_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> HackathonDetailResponse:
    return await publish_hackathon(
        session,
        user_id=current_user_id,
        hackathon_id=hackathon_id,
    )


@router.patch("/{hackathon_id}/unpublish", response_model=HackathonDetailResponse)
async def unpublish_hackathon_route(
    hackathon_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> HackathonDetailResponse:
    return await unpublish_hackathon(
        session,
        user_id=current_user_id,
        hackathon_id=hackathon_id,
    )


@router.patch("/{hackathon_id}/archive", response_model=HackathonDetailResponse)
async def archive_hackathon_route(
    hackathon_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> HackathonDetailResponse:
    return await archive_hackathon(
        session,
        user_id=current_user_id,
        hackathon_id=hackathon_id,
    )
