from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    create_event,
    get_event_by_id,
    get_event_model_by_id,
    get_hackathon_by_id,
    get_room_by_id,
    get_user_profile_by_id,
    has_booking_conflict,
    has_event_room_conflict,
    list_events_by_hackathon,
)
from app.schemas import CreateEventRequest, EventResponse, UpdateEventRequest

ALLOWED_EVENT_EDITOR_ROLES = {"admin", "organizer"}


def _map_event(record) -> EventResponse:
    return EventResponse(
        id=str(record.id),
        hackathonId=str(record.hackathon_id),
        title=record.title,
        description=record.description,
        startTime=record.start_time,
        endTime=record.end_time,
        roomId=str(record.room_id),
    )


async def _require_event_editor(session: AsyncSession, user_id: int) -> None:
    user = await get_user_profile_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.role_name not in ALLOWED_EVENT_EDITOR_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage events",
        )


def _parse_room_id(raw_room_id: str) -> int:
    if not raw_room_id.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="roomId must be numeric",
        )
    return int(raw_room_id)


def _validate_time_range(start_time, end_time) -> None:
    if end_time <= start_time:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="endTime must be greater than startTime",
        )


def _validate_hackathon_bounds(hackathon, start_time, end_time) -> None:
    if start_time < hackathon.start_date or end_time > hackathon.end_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Event time must fit within hackathon dates",
        )


async def _ensure_room_free(
    session: AsyncSession,
    *,
    room_id: int,
    start_time,
    end_time,
    exclude_event_id: int | None = None,
) -> None:
    if await has_booking_conflict(
        session,
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is already booked for this time range",
        )

    if await has_event_room_conflict(
        session,
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
        exclude_event_id=exclude_event_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room already has an event in this time range",
        )


async def create_event_entry(
    session: AsyncSession,
    *,
    current_user_id: int,
    hackathon_id: int,
    payload: CreateEventRequest,
) -> EventResponse:
    await _require_event_editor(session, current_user_id)
    _validate_time_range(payload.startTime, payload.endTime)

    hackathon = await get_hackathon_by_id(session, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    room_id = _parse_room_id(payload.roomId)
    room = await get_room_by_id(session, room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    _validate_hackathon_bounds(hackathon, payload.startTime, payload.endTime)

    await _ensure_room_free(
        session,
        room_id=room_id,
        start_time=payload.startTime,
        end_time=payload.endTime,
    )

    event = await create_event(
        session,
        hackathon_id=hackathon_id,
        room_id=room_id,
        title=payload.title,
        description=payload.description,
        start_time=payload.startTime,
        end_time=payload.endTime,
    )
    await session.commit()

    created_event = await get_event_by_id(session, event.id)
    if created_event is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Event was created but could not be loaded",
        )

    return _map_event(created_event)


async def get_hackathon_events(
    session: AsyncSession,
    hackathon_id: int,
) -> list[EventResponse]:
    hackathon = await get_hackathon_by_id(session, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    return [_map_event(item) for item in await list_events_by_hackathon(session, hackathon_id)]


async def update_event_entry(
    session: AsyncSession,
    *,
    current_user_id: int,
    event_id: int,
    payload: UpdateEventRequest,
) -> EventResponse:
    await _require_event_editor(session, current_user_id)

    event = await get_event_model_by_id(session, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    next_start = update_data.get("startTime", event.start_time)
    next_end = update_data.get("endTime", event.end_time)
    next_room_id = _parse_room_id(update_data["roomId"]) if "roomId" in update_data else event.room_id

    _validate_time_range(next_start, next_end)

    hackathon = await get_hackathon_by_id(session, event.hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )
    _validate_hackathon_bounds(hackathon, next_start, next_end)

    room = await get_room_by_id(session, next_room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    await _ensure_room_free(
        session,
        room_id=next_room_id,
        start_time=next_start,
        end_time=next_end,
        exclude_event_id=event.id,
    )

    if "title" in update_data:
        event.title = update_data["title"]
    if "description" in update_data:
        event.description = update_data["description"]
    if "startTime" in update_data:
        event.start_time = update_data["startTime"]
    if "endTime" in update_data:
        event.end_time = update_data["endTime"]
    if "roomId" in update_data:
        event.room_id = next_room_id

    await session.commit()
    updated_event = await get_event_by_id(session, event.id)
    if updated_event is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Event was updated but could not be loaded",
        )

    return _map_event(updated_event)


async def delete_event_entry(
    session: AsyncSession,
    *,
    current_user_id: int,
    event_id: int,
) -> None:
    await _require_event_editor(session, current_user_id)

    event = await get_event_model_by_id(session, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    await session.delete(event)
    await session.commit()
