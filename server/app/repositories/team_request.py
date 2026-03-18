from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TeamMember, TeamRequest, User


@dataclass(slots=True)
class TeamRequestRecord:
    id: int
    team_id: int
    user_id: int
    user_name: str
    status: str


async def create_team_request(
    session: AsyncSession,
    *,
    team_id: int,
    user_id: int,
    status: str,
) -> TeamRequest:
    team_request = TeamRequest(team_id=team_id, user_id=user_id, status=status)
    session.add(team_request)
    await session.flush()
    return team_request


async def get_team_request_by_team_and_user(
    session: AsyncSession,
    *,
    team_id: int,
    user_id: int,
) -> TeamRequest | None:
    statement = select(TeamRequest).where(
        TeamRequest.team_id == team_id,
        TeamRequest.user_id == user_id,
    )
    return await session.scalar(statement)


async def get_team_request_model_by_id(
    session: AsyncSession,
    request_id: int,
) -> TeamRequest | None:
    return await session.get(TeamRequest, request_id)


async def get_team_request_by_id(
    session: AsyncSession,
    request_id: int,
) -> TeamRequestRecord | None:
    statement = (
        select(
            TeamRequest.id,
            TeamRequest.team_id,
            TeamRequest.user_id,
            User.full_name.label("user_name"),
            TeamRequest.status,
        )
        .join(User, User.id == TeamRequest.user_id)
        .where(TeamRequest.id == request_id)
    )
    row = (await session.execute(statement)).first()

    if row is None:
        return None

    return TeamRequestRecord(
        id=row.id,
        team_id=row.team_id,
        user_id=row.user_id,
        user_name=row.user_name,
        status=row.status,
    )


async def list_team_requests(
    session: AsyncSession,
    team_id: int,
) -> list[TeamRequestRecord]:
    statement = (
        select(
            TeamRequest.id,
            TeamRequest.team_id,
            TeamRequest.user_id,
            User.full_name.label("user_name"),
            TeamRequest.status,
        )
        .join(User, User.id == TeamRequest.user_id)
        .where(TeamRequest.team_id == team_id)
        .order_by(TeamRequest.created_at.asc(), TeamRequest.id.asc())
    )
    rows = (await session.execute(statement)).all()

    return [
        TeamRequestRecord(
            id=row.id,
            team_id=row.team_id,
            user_id=row.user_id,
            user_name=row.user_name,
            status=row.status,
        )
        for row in rows
    ]


async def create_team_member(
    session: AsyncSession,
    *,
    team_id: int,
    user_id: int,
) -> TeamMember:
    membership = TeamMember(team_id=team_id, user_id=user_id)
    session.add(membership)
    await session.flush()
    return membership
