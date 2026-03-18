from collections import defaultdict
from datetime import date, datetime, time, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    create_room_booking,
    get_room_by_id,
    get_user_profile_by_id,
    has_booking_conflict,
    has_event_room_conflict,
    list_event_slots_by_date,
    list_room_bookings_by_date,
    list_rooms,
)
from app.schemas import (
    CreateRoomBookingRequest,
    RoomAvailabilityBookingResponse,
    RoomAvailabilityResponse,
    RoomBookingResponse,
    RoomResponse,
)

ALLOWED_ROOM_BOOKER_ROLES = {"admin", "organizer"}


async def _require_room_booker(session: AsyncSession, user_id: int) -> None:
    user = await get_user_profile_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.role_name not in ALLOWED_ROOM_BOOKER_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to book rooms",
        )


def _parse_room_id(raw_room_id: str) -> int:
    if not raw_room_id.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="roomId must be numeric",
        )
    return int(raw_room_id)


def _validate_booking_window(start_time: datetime, end_time: datetime) -> None:
    if end_time <= start_time:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="endTime must be greater than startTime",
        )


def _normalize_day_bounds(target_date: date) -> tuple[datetime, datetime]:
    day_start = datetime.combine(target_date, time.min)
    return day_start, day_start + timedelta(days=1)


async def get_rooms(session: AsyncSession) -> list[RoomResponse]:
    rooms = await list_rooms(session)
    return [RoomResponse(id=str(room.id), name=room.name, capacity=room.capacity) for room in rooms]


async def get_room_availability(
    session: AsyncSession,
    target_date: date,
) -> list[RoomAvailabilityResponse]:
    rooms = await list_rooms(session)
    day_start, day_end = _normalize_day_bounds(target_date)
    bookings = await list_room_bookings_by_date(session, day_start=day_start, day_end=day_end)
    event_slots = await list_event_slots_by_date(session, day_start=day_start, day_end=day_end)

    bookings_by_room: dict[int, list[RoomAvailabilityBookingResponse]] = defaultdict(list)
    for booking in bookings:
        bookings_by_room[booking.room_id].append(
            RoomAvailabilityBookingResponse(
                startTime=booking.start_time,
                endTime=booking.end_time,
            )
        )
    for event in event_slots:
        bookings_by_room[event.room_id].append(
            RoomAvailabilityBookingResponse(
                startTime=event.start_time,
                endTime=event.end_time,
            )
        )
    for room_id, slots in bookings_by_room.items():
        bookings_by_room[room_id] = sorted(
            slots,
            key=lambda slot: (slot.startTime, slot.endTime),
        )

    return [
        RoomAvailabilityResponse(
            id=str(room.id),
            name=room.name,
            capacity=room.capacity,
            isAvailable=len(bookings_by_room[room.id]) == 0,
            bookings=bookings_by_room[room.id],
        )
        for room in rooms
    ]


async def book_room(
    session: AsyncSession,
    *,
    current_user_id: int,
    payload: CreateRoomBookingRequest,
) -> RoomBookingResponse:
    await _require_room_booker(session, current_user_id)

    room_id = _parse_room_id(payload.roomId)
    _validate_booking_window(payload.startTime, payload.endTime)

    room = await get_room_by_id(session, room_id)
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    if await has_booking_conflict(
        session,
        room_id=room_id,
        start_time=payload.startTime,
        end_time=payload.endTime,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is already booked for this time range",
        )

    if await has_event_room_conflict(
        session,
        room_id=room_id,
        start_time=payload.startTime,
        end_time=payload.endTime,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room already has an event in this time range",
        )

    booking = await create_room_booking(
        session,
        room_id=room_id,
        created_by=current_user_id,
        start_time=payload.startTime,
        end_time=payload.endTime,
    )
    await session.commit()

    return RoomBookingResponse(
        id=str(booking.id),
        roomId=str(booking.room_id),
        startTime=booking.start_time,
        endTime=booking.end_time,
    )
