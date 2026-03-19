from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Room, RoomBooking


@dataclass(slots=True)
class RoomRecord:
    id: int
    name: str
    capacity: int


@dataclass(slots=True)
class RoomBookingRecord:
    id: int
    room_id: int
    start_time: datetime
    end_time: datetime


async def list_rooms(session: AsyncSession) -> list[RoomRecord]:
    rows = (await session.execute(select(Room).order_by(Room.name.asc(), Room.id.asc()))).scalars().all()
    return [RoomRecord(id=row.id, name=row.name, capacity=row.capacity) for row in rows]


async def get_room_by_id(session: AsyncSession, room_id: int) -> Room | None:
    return await session.get(Room, room_id)


async def list_room_bookings_by_date(
    session: AsyncSession,
    *,
    day_start: datetime,
    day_end: datetime,
) -> list[RoomBookingRecord]:
    rows = (
        await session.execute(
            select(RoomBooking)
            .where(
                RoomBooking.start_time < day_end,
                RoomBooking.end_time > day_start,
            )
            .order_by(RoomBooking.start_time.asc(), RoomBooking.id.asc())
        )
    ).scalars().all()
    return [
        RoomBookingRecord(
            id=row.id,
            room_id=row.room_id,
            start_time=row.start_time,
            end_time=row.end_time,
        )
        for row in rows
    ]


async def has_booking_conflict(
    session: AsyncSession,
    *,
    room_id: int,
    start_time: datetime,
    end_time: datetime,
) -> bool:
    statement = select(RoomBooking.id).where(
        RoomBooking.room_id == room_id,
        RoomBooking.start_time < end_time,
        RoomBooking.end_time > start_time,
    )
    return (await session.execute(statement)).first() is not None


async def create_room_booking(
    session: AsyncSession,
    *,
    room_id: int,
    created_by: int,
    start_time: datetime,
    end_time: datetime,
) -> RoomBooking:
    booking = RoomBooking(
        room_id=room_id,
        created_by=created_by,
        start_time=start_time,
        end_time=end_time,
    )
    session.add(booking)
    await session.flush()
    return booking
