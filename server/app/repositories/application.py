from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Application, Team


@dataclass(slots=True)
class ApplicationRecord:
    id: int
    team_id: int
    team_name: str
    status: str
    hackathon_id: int


async def get_team_by_id(
    session: AsyncSession,
    team_id: int,
) -> Team | None:
    return await session.get(Team, team_id)


async def create_application(
    session: AsyncSession,
    *,
    hackathon_id: int,
    team_id: int,
    status: str,
) -> Application:
    application = Application(
        hackathon_id=hackathon_id,
        team_id=team_id,
        status=status,
    )
    session.add(application)
    await session.flush()
    return application


async def get_application_by_team_and_hackathon(
    session: AsyncSession,
    *,
    team_id: int,
    hackathon_id: int,
) -> Application | None:
    statement = select(Application).where(
        Application.team_id == team_id,
        Application.hackathon_id == hackathon_id,
    )
    return await session.scalar(statement)


async def list_applications_by_hackathon(
    session: AsyncSession,
    hackathon_id: int,
) -> list[ApplicationRecord]:
    statement = (
        select(
            Application.id,
            Application.team_id,
            Team.name.label("team_name"),
            Application.status,
            Application.hackathon_id,
        )
        .join(Team, Team.id == Application.team_id)
        .where(Application.hackathon_id == hackathon_id)
        .order_by(Application.applied_at.asc(), Application.id.asc())
    )
    rows = (await session.execute(statement)).all()

    return [
        ApplicationRecord(
            id=row.id,
            team_id=row.team_id,
            team_name=row.team_name,
            status=row.status,
            hackathon_id=row.hackathon_id,
        )
        for row in rows
    ]


async def get_application_by_id(
    session: AsyncSession,
    application_id: int,
) -> ApplicationRecord | None:
    statement = (
        select(
            Application.id,
            Application.team_id,
            Team.name.label("team_name"),
            Application.status,
            Application.hackathon_id,
        )
        .join(Team, Team.id == Application.team_id)
        .where(Application.id == application_id)
    )
    row = (await session.execute(statement)).first()

    if row is None:
        return None

    return ApplicationRecord(
        id=row.id,
        team_id=row.team_id,
        team_name=row.team_name,
        status=row.status,
        hackathon_id=row.hackathon_id,
    )


async def get_application_model_by_id(
    session: AsyncSession,
    application_id: int,
) -> Application | None:
    return await session.get(Application, application_id)
