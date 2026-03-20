from datetime import date, datetime, time

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    create_hackathon,
    get_hackathon_by_id,
    get_hackathon_model_by_id,
    get_hackathon_stats,
    get_hackathon_status_by_name,
    get_user_profile_by_id,
    list_hackathons,
)
from app.schemas import (
    CreateHackathonRequest,
    CreateHackathonResponse,
    HackathonDetailResponse,
    HackathonListItemResponse,
    HackathonStatsResponse,
    UpdateHackathonRequest,
)

DRAFT_STATUS = "draft"
PUBLISHED_STATUS = "published"
ARCHIVED_STATUS = "archived"
ALLOWED_HACKATHON_EDITOR_ROLES = {"admin", "organizer"}


def _as_datetime(value: date) -> datetime:
    return datetime.combine(value, time.min)


def _validate_dates(start_date: date, end_date: date) -> None:
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="endDate must be greater than or equal to startDate",
        )


async def _require_hackathon_editor(session: AsyncSession, user_id: int) -> None:
    user = await get_user_profile_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not ALLOWED_HACKATHON_EDITOR_ROLES.intersection(user.role_names):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage hackathons",
        )

def _map_hackathon_detail(record) -> HackathonDetailResponse:
    return HackathonDetailResponse(
        id=str(record.id),
        title=record.title,
        theme=record.theme,
        description=record.description,
        format=record.format,
        startDate=record.start_date.date(),
        endDate=record.end_date.date(),
        participantLimit=record.participant_limit,
        teamLimit=record.team_limit,
        rules=record.rules,
        status=record.status,
    )


async def create_hackathon_entry(
    session: AsyncSession,
    user_id: int,
    payload: CreateHackathonRequest,
) -> CreateHackathonResponse:
    await _require_hackathon_editor(session, user_id)
    _validate_dates(payload.startDate, payload.endDate)

    draft_status = await get_hackathon_status_by_name(session, DRAFT_STATUS)
    if draft_status is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Draft status is not configured",
        )

    hackathon = await create_hackathon(
        session,
        title=payload.title,
        theme=payload.theme,
        format=payload.format,
        description=payload.description,
        start_date=_as_datetime(payload.startDate),
        end_date=_as_datetime(payload.endDate),
        participant_limit=payload.participantLimit,
        team_limit=payload.teamLimit,
        rules=payload.rules,
        status_id=draft_status.id,
        created_by=user_id,
    )
    await session.commit()

    return CreateHackathonResponse(id=str(hackathon.id), status=draft_status.name)


async def list_hackathon_entries(
    session: AsyncSession,
    *,
    status_filter: str | None,
    page: int,
    limit: int,
) -> list[HackathonListItemResponse]:
    if status_filter is not None:
        status_record = await get_hackathon_status_by_name(session, status_filter)
        if status_record is None:
            return []

    items = await list_hackathons(
        session,
        status=status_filter,
        page=page,
        limit=limit,
    )
    return [
        HackathonListItemResponse(
            id=str(item.id),
            title=item.title,
            format=item.format,
            startDate=item.start_date.date(),
            status=item.status,
        )
        for item in items
    ]


async def get_hackathon_entry(
    session: AsyncSession,
    hackathon_id: int,
) -> HackathonDetailResponse:
    hackathon = await get_hackathon_by_id(session, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    return _map_hackathon_detail(hackathon)


async def update_hackathon_entry(
    session: AsyncSession,
    *,
    user_id: int,
    hackathon_id: int,
    payload: UpdateHackathonRequest,
) -> HackathonDetailResponse:
    await _require_hackathon_editor(session, user_id)

    hackathon = await get_hackathon_model_by_id(session, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    next_start_date = update_data.get("startDate", hackathon.start_date.date())
    next_end_date = update_data.get("endDate", hackathon.end_date.date())
    _validate_dates(next_start_date, next_end_date)

    if "title" in update_data:
        hackathon.title = update_data["title"]
    if "theme" in update_data:
        hackathon.theme = update_data["theme"]
    if "format" in update_data:
        hackathon.event_format = update_data["format"]
    if "description" in update_data:
        hackathon.description = update_data["description"]
    if "startDate" in update_data:
        hackathon.start_date = _as_datetime(update_data["startDate"])
        hackathon.registration_end_date = hackathon.start_date
    if "endDate" in update_data:
        hackathon.end_date = _as_datetime(update_data["endDate"])
    if "participantLimit" in update_data:
        hackathon.max_participants = update_data["participantLimit"]
    if "teamLimit" in update_data:
        hackathon.max_teams = update_data["teamLimit"]
    if "rules" in update_data:
        hackathon.rules = update_data["rules"]

    await session.commit()
    return await get_hackathon_entry(session, hackathon_id)


async def set_hackathon_status(
    session: AsyncSession,
    *,
    user_id: int,
    hackathon_id: int,
    status_name: str,
) -> HackathonDetailResponse:
    await _require_hackathon_editor(session, user_id)

    hackathon = await get_hackathon_model_by_id(session, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    target_status = await get_hackathon_status_by_name(session, status_name)
    if target_status is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status '{status_name}' is not configured",
        )

    hackathon.status_id = target_status.id
    await session.commit()
    return await get_hackathon_entry(session, hackathon_id)


async def publish_hackathon(
    session: AsyncSession,
    *,
    user_id: int,
    hackathon_id: int,
) -> HackathonDetailResponse:
    return await set_hackathon_status(
        session,
        user_id=user_id,
        hackathon_id=hackathon_id,
        status_name=PUBLISHED_STATUS,
    )


async def unpublish_hackathon(
    session: AsyncSession,
    *,
    user_id: int,
    hackathon_id: int,
) -> HackathonDetailResponse:
    return await set_hackathon_status(
        session,
        user_id=user_id,
        hackathon_id=hackathon_id,
        status_name=DRAFT_STATUS,
    )


async def archive_hackathon(
    session: AsyncSession,
    *,
    user_id: int,
    hackathon_id: int,
) -> HackathonDetailResponse:
    return await set_hackathon_status(
        session,
        user_id=user_id,
        hackathon_id=hackathon_id,
        status_name=ARCHIVED_STATUS,
    )


async def get_hackathon_stats_entry(
    session: AsyncSession,
    hackathon_id: int,
) -> HackathonStatsResponse:
    stats = await get_hackathon_stats(session, hackathon_id)
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    return HackathonStatsResponse(
        participants=stats.participants,
        teams=stats.teams,
        solutions=stats.solutions,
        durationHours=stats.duration_hours,
    )
