from dataclasses import dataclass
from datetime import date, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Application, Hackathon, HackathonStatus, TeamMember

APPROVED_APPLICATION_STATUS = "approved"


@dataclass(slots=True)
class HackathonStatsRecord:
    participants: int
    teams: int
    solutions: int
    duration_hours: int


@dataclass(slots=True)
class AdminHackathonHistoryRecord:
    id: int
    title: str
    start_date: datetime
    end_date: datetime
    status: str
    participants: int
    teams: int


async def get_hackathon_stats(
    session: AsyncSession,
    hackathon_id: int,
) -> HackathonStatsRecord | None:
    hackathon = await session.get(Hackathon, hackathon_id)
    if hackathon is None:
        return None

    aggregate_statement = (
        select(
            func.count(func.distinct(TeamMember.user_id)).label("participants"),
            func.count(func.distinct(Application.team_id)).label("teams"),
        )
        .select_from(Application)
        .outerjoin(TeamMember, TeamMember.team_id == Application.team_id)
        .where(
            Application.hackathon_id == hackathon_id,
            Application.status == APPROVED_APPLICATION_STATUS,
        )
    )
    aggregate_row = (await session.execute(aggregate_statement)).first()

    participants = int(aggregate_row.participants or 0)
    teams = int(aggregate_row.teams or 0)
    duration_hours = int((hackathon.end_date - hackathon.start_date).total_seconds() // 3600)

    return HackathonStatsRecord(
        participants=participants,
        teams=teams,
        solutions=0,
        duration_hours=duration_hours,
    )


async def list_hackathon_history(
    session: AsyncSession,
    *,
    start_date: date | None,
    end_date: date | None,
    participants_min: int | None,
) -> list[AdminHackathonHistoryRecord]:
    participants_subquery = (
        select(
            Application.hackathon_id.label("hackathon_id"),
            func.count(func.distinct(TeamMember.user_id)).label("participants"),
            func.count(func.distinct(Application.team_id)).label("teams"),
        )
        .select_from(Application)
        .outerjoin(TeamMember, TeamMember.team_id == Application.team_id)
        .where(Application.status == APPROVED_APPLICATION_STATUS)
        .group_by(Application.hackathon_id)
        .subquery()
    )

    statement = (
        select(
            Hackathon.id,
            Hackathon.title,
            Hackathon.start_date,
            Hackathon.end_date,
            HackathonStatus.name.label("status"),
            func.coalesce(participants_subquery.c.participants, 0).label("participants"),
            func.coalesce(participants_subquery.c.teams, 0).label("teams"),
        )
        .join(HackathonStatus, Hackathon.status_id == HackathonStatus.id)
        .outerjoin(participants_subquery, participants_subquery.c.hackathon_id == Hackathon.id)
        .order_by(Hackathon.start_date.desc(), Hackathon.id.desc())
    )

    if start_date is not None:
        statement = statement.where(Hackathon.start_date >= start_date)
    if end_date is not None:
        statement = statement.where(Hackathon.end_date <= end_date)
    if participants_min is not None:
        statement = statement.where(func.coalesce(participants_subquery.c.participants, 0) >= participants_min)

    rows = (await session.execute(statement)).all()
    return [
        AdminHackathonHistoryRecord(
            id=row.id,
            title=row.title,
            start_date=row.start_date,
            end_date=row.end_date,
            status=row.status,
            participants=int(row.participants or 0),
            teams=int(row.teams or 0),
        )
        for row in rows
    ]
