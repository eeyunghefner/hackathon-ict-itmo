from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Hackathon, HackathonStatus


@dataclass(slots=True)
class HackathonSummaryRecord:
    id: int
    title: str
    format: str
    start_date: datetime
    status: str


@dataclass(slots=True)
class HackathonDetailRecord:
    id: int
    title: str
    theme: str
    description: str | None
    format: str
    start_date: datetime
    end_date: datetime
    participant_limit: int | None
    team_limit: int | None
    rules: str | None
    status: str


def _base_hackathon_query() -> Select[tuple[Hackathon, str]]:
    return select(Hackathon, HackathonStatus.name.label("status")).join(
        HackathonStatus,
        Hackathon.status_id == HackathonStatus.id,
    )


async def get_hackathon_status_by_name(
    session: AsyncSession,
    name: str,
) -> HackathonStatus | None:
    statement = select(HackathonStatus).where(HackathonStatus.name == name)
    return await session.scalar(statement)


async def create_hackathon(
    session: AsyncSession,
    *,
    title: str,
    theme: str,
    format: str,
    description: str,
    start_date: datetime,
    end_date: datetime,
    participant_limit: int,
    team_limit: int,
    rules: str,
    status_id: int,
    created_by: int,
) -> Hackathon:
    hackathon = Hackathon(
        title=title,
        theme=theme,
        event_format=format,
        description=description,
        rules=rules,
        status_id=status_id,
        registration_start_date=datetime.utcnow(),
        registration_end_date=start_date,
        start_date=start_date,
        end_date=end_date,
        max_participants=participant_limit,
        max_teams=team_limit,
        created_by=created_by,
    )
    session.add(hackathon)
    await session.flush()
    return hackathon


async def list_hackathons(
    session: AsyncSession,
    *,
    status: str | None,
    page: int,
    limit: int,
) -> list[HackathonSummaryRecord]:
    statement = _base_hackathon_query().order_by(Hackathon.start_date.asc(), Hackathon.id.asc())

    if status is not None:
        statement = statement.where(HackathonStatus.name == status)

    statement = statement.offset((page - 1) * limit).limit(limit)
    rows = (await session.execute(statement)).all()

    return [
        HackathonSummaryRecord(
            id=hackathon.id,
            title=hackathon.title,
            format=hackathon.event_format,
            start_date=hackathon.start_date,
            status=row_status,
        )
        for hackathon, row_status in rows
    ]


async def get_hackathon_by_id(
    session: AsyncSession,
    hackathon_id: int,
) -> HackathonDetailRecord | None:
    statement = _base_hackathon_query().where(Hackathon.id == hackathon_id)
    row = (await session.execute(statement)).first()

    if row is None:
        return None

    hackathon, status = row
    return HackathonDetailRecord(
        id=hackathon.id,
        title=hackathon.title,
        theme=hackathon.theme,
        description=hackathon.description,
        format=hackathon.event_format,
        start_date=hackathon.start_date,
        end_date=hackathon.end_date,
        participant_limit=hackathon.max_participants,
        team_limit=hackathon.max_teams,
        rules=hackathon.rules,
        status=status,
    )


async def get_hackathon_model_by_id(
    session: AsyncSession,
    hackathon_id: int,
) -> Hackathon | None:
    return await session.get(Hackathon, hackathon_id)
