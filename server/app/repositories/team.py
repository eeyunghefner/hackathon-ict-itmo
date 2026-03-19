from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Application, Team, TeamMember, User


@dataclass(slots=True)
class TeamMemberRecord:
    id: int
    name: str
    joined_at: datetime


@dataclass(slots=True)
class TeamRecord:
    id: int
    name: str
    description: str | None
    captain_id: int | None
    members: list[TeamMemberRecord]


async def create_team(
    session: AsyncSession,
    *,
    name: str,
    description: str,
    captain_id: int,
) -> Team:
    team = Team(
        name=name,
        description=description,
        hackathon_id=None,
        captain_id=captain_id,
        max_members=None,
    )
    session.add(team)
    await session.flush()

    membership = TeamMember(team_id=team.id, user_id=captain_id)
    session.add(membership)
    await session.flush()
    return team


async def get_team_by_name(
    session: AsyncSession,
    name: str,
) -> Team | None:
    statement = select(Team).where(Team.name == name)
    return await session.scalar(statement)


async def get_team_by_id(
    session: AsyncSession,
    team_id: int,
) -> Team | None:
    return await session.get(Team, team_id)


async def list_teams(
    session: AsyncSession,
    hackathon_id: int | None = None,
) -> list[Team]:
    statement = select(Team).order_by(Team.created_at.asc(), Team.id.asc())

    if hackathon_id is not None:
        statement = (
            statement.join(Application, Application.team_id == Team.id)
            .where(Application.hackathon_id == hackathon_id)
            .distinct()
        )

    result = await session.scalars(statement)
    return list(result)


async def list_team_members(
    session: AsyncSession,
    team_id: int,
) -> list[TeamMemberRecord]:
    statement = (
        select(
            User.id,
            User.full_name,
            TeamMember.joined_at,
        )
        .join(TeamMember, TeamMember.user_id == User.id)
        .where(TeamMember.team_id == team_id)
        .order_by(TeamMember.joined_at.asc(), User.id.asc())
    )
    rows = (await session.execute(statement)).all()

    return [
        TeamMemberRecord(
            id=row.id,
            name=row.full_name,
            joined_at=row.joined_at,
        )
        for row in rows
    ]


async def get_team_detail(
    session: AsyncSession,
    team_id: int,
) -> TeamRecord | None:
    team = await get_team_by_id(session, team_id)
    if team is None:
        return None

    members = await list_team_members(session, team_id)
    return TeamRecord(
        id=team.id,
        name=team.name,
        description=team.description,
        captain_id=team.captain_id,
        members=members,
    )


async def get_team_member(
    session: AsyncSession,
    *,
    team_id: int,
    user_id: int,
) -> TeamMember | None:
    statement = select(TeamMember).where(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id,
    )
    return await session.scalar(statement)


async def delete_team_member(session: AsyncSession, membership: TeamMember) -> None:
    await session.delete(membership)
    await session.flush()


async def get_next_team_member_after_leave(
    session: AsyncSession,
    team_id: int,
) -> TeamMember | None:
    statement = (
        select(TeamMember)
        .where(TeamMember.team_id == team_id)
        .order_by(TeamMember.joined_at.asc(), TeamMember.user_id.asc())
        .limit(1)
    )
    return await session.scalar(statement)
