from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Event


@dataclass(slots=True)
class EventRecord:
    id: int
    hackathon_id: int
    room_id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime


async def create_event(
    session: AsyncSession,
    *,
    hackathon_id: int,
    room_id: int,
    title: str,
    description: str,
    start_time: datetime,
    end_time: datetime,
) -> Event:
    event = Event(
        hackathon_id=hackathon_id,
        room_id=room_id,
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
    )
    session.add(event)
    await session.flush()
    return event


async def list_events_by_hackathon(
    session: AsyncSession,
    hackathon_id: int,
) -> list[EventRecord]:
    rows = (
        await session.execute(
            select(Event)
            .where(Event.hackathon_id == hackathon_id)
            .order_by(Event.start_time.asc(), Event.id.asc())
        )
    ).scalars().all()
    return [
        EventRecord(
            id=row.id,
            hackathon_id=row.hackathon_id,
            room_id=row.room_id,
            title=row.title,
            description=row.description,
            start_time=row.start_time,
            end_time=row.end_time,
        )
        for row in rows
    ]


async def get_event_model_by_id(session: AsyncSession, event_id: int) -> Event | None:
    return await session.get(Event, event_id)


async def get_event_by_id(session: AsyncSession, event_id: int) -> EventRecord | None:
    row = await get_event_model_by_id(session, event_id)
    if row is None:
        return None
    return EventRecord(
        id=row.id,
        hackathon_id=row.hackathon_id,
        room_id=row.room_id,
        title=row.title,
        description=row.description,
        start_time=row.start_time,
        end_time=row.end_time,
    )


async def has_event_room_conflict(
    session: AsyncSession,
    *,
    room_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_event_id: int | None = None,
) -> bool:
    statement = select(Event.id).where(
        Event.room_id == room_id,
        Event.start_time < end_time,
        Event.end_time > start_time,
    )
    if exclude_event_id is not None:
        statement = statement.where(Event.id != exclude_event_id)

    return (await session.execute(statement)).first() is not None


async def list_event_slots_by_date(
    session: AsyncSession,
    *,
    day_start: datetime,
    day_end: datetime,
) -> list[EventRecord]:
    rows = (
        await session.execute(
            select(Event)
            .where(
                Event.start_time < day_end,
                Event.end_time > day_start,
            )
            .order_by(Event.start_time.asc(), Event.id.asc())
        )
    ).scalars().all()
    return [
        EventRecord(
            id=row.id,
            hackathon_id=row.hackathon_id,
            room_id=row.room_id,
            title=row.title,
            description=row.description,
            start_time=row.start_time,
            end_time=row.end_time,
        )
        for row in rows
    ]
