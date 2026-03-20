from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    create_application,
    get_application_by_id,
    get_application_by_team_and_hackathon,
    get_application_model_by_id,
    get_hackathon_by_id,
    get_team_by_id,
    get_user_profile_by_id,
    list_applications_by_hackathon,
)
from app.schemas import ApplicationResponse, CreateApplicationRequest

APPLICATION_PENDING = "pending"
APPLICATION_APPROVED = "approved"
APPLICATION_REJECTED = "rejected"
ALLOWED_ORGANIZER_ROLES = {"admin", "organizer"}


def _map_application(record) -> ApplicationResponse:
    return ApplicationResponse(
        id=str(record.id),
        teamId=str(record.team_id),
        teamName=record.team_name,
        status=record.status,
    )


async def _require_organizer(session: AsyncSession, user_id: int) -> None:
    user = await get_user_profile_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not ALLOWED_ORGANIZER_ROLES.intersection(user.role_names):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage applications",
        )


async def submit_team_application(
    session: AsyncSession,
    *,
    current_user_id: int,
    hackathon_id: int,
    payload: CreateApplicationRequest,
) -> ApplicationResponse:
    if not payload.teamId.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="teamId must be numeric",
        )

    hackathon = await get_hackathon_by_id(session, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    team = await get_team_by_id(session, int(payload.teamId))
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    if team.captain_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the team captain can submit an application",
        )

    existing_application = await get_application_by_team_and_hackathon(
        session,
        team_id=team.id,
        hackathon_id=hackathon_id,
    )
    if existing_application is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Application for this team already exists",
        )

    application = await create_application(
        session,
        hackathon_id=hackathon_id,
        team_id=team.id,
        status=APPLICATION_PENDING,
    )
    await session.commit()

    created_application = await get_application_by_id(session, application.id)
    if created_application is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Application was created but could not be loaded",
        )

    return _map_application(created_application)


async def get_hackathon_applications(
    session: AsyncSession,
    *,
    current_user_id: int,
    hackathon_id: int,
) -> list[ApplicationResponse]:
    await _require_organizer(session, current_user_id)

    hackathon = await get_hackathon_by_id(session, hackathon_id)
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found",
        )

    applications = await list_applications_by_hackathon(session, hackathon_id)
    return [_map_application(item) for item in applications]


async def update_application_status(
    session: AsyncSession,
    *,
    current_user_id: int,
    application_id: int,
    new_status: str,
) -> ApplicationResponse:
    await _require_organizer(session, current_user_id)

    application = await get_application_model_by_id(session, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    application.status = new_status
    await session.commit()

    updated_application = await get_application_by_id(session, application_id)
    if updated_application is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Application was updated but could not be loaded",
        )

    return _map_application(updated_application)


async def approve_application(
    session: AsyncSession,
    *,
    current_user_id: int,
    application_id: int,
) -> ApplicationResponse:
    return await update_application_status(
        session,
        current_user_id=current_user_id,
        application_id=application_id,
        new_status=APPLICATION_APPROVED,
    )


async def reject_application(
    session: AsyncSession,
    *,
    current_user_id: int,
    application_id: int,
) -> ApplicationResponse:
    return await update_application_status(
        session,
        current_user_id=current_user_id,
        application_id=application_id,
        new_status=APPLICATION_REJECTED,
    )
