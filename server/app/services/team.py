from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import (
    create_team,
    create_team_member,
    create_team_request,
    delete_team_member,
    get_next_team_member_after_leave,
    get_team_by_id,
    get_team_by_name,
    get_team_detail,
    get_team_member,
    get_team_request_by_id,
    get_team_request_by_team_and_user,
    get_team_request_model_by_id,
    list_teams,
    list_team_requests,
)
from app.schemas import (
    CreateTeamRequest,
    TeamJoinRequestResponse,
    TeamMemberResponse,
    TeamResponse,
    UpdateTeamCaptainRequest,
)

TEAM_REQUEST_PENDING = "pending"
TEAM_REQUEST_APPROVED = "approved"
TEAM_REQUEST_REJECTED = "rejected"


def _map_team(record) -> TeamResponse:
    return TeamResponse(
        id=str(record.id),
        name=record.name,
        description=record.description,
        captainId=str(record.captain_id) if record.captain_id is not None else None,
        members=[
            TeamMemberResponse(
                id=str(member.id),
                name=member.name,
            )
            for member in record.members
        ],
    )


def _map_team_request(record) -> TeamJoinRequestResponse:
    return TeamJoinRequestResponse(
        id=str(record.id),
        userId=str(record.user_id),
        userName=record.user_name,
        status=record.status,
    )


async def _require_team_captain(
    session: AsyncSession,
    *,
    team_id: int,
    current_user_id: int,
):
    team = await get_team_by_id(session, team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    if team.captain_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the team captain can perform this action",
        )

    return team


async def create_team_entry(
    session: AsyncSession,
    *,
    current_user_id: int,
    payload: CreateTeamRequest,
) -> TeamResponse:
    existing_team = await get_team_by_name(session, payload.name)
    if existing_team is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team with this name already exists",
        )

    try:
        team = await create_team(
            session,
            name=payload.name,
            description=payload.description,
            captain_id=current_user_id,
        )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team with this name already exists",
        ) from exc

    team_detail = await get_team_detail(session, team.id)
    if team_detail is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team was created but could not be loaded",
        )

    return _map_team(team_detail)


async def list_team_entries(
    session: AsyncSession,
    *,
    hackathon_id: int | None,
) -> list[TeamResponse]:
    teams = await list_teams(session, hackathon_id)
    result: list[TeamResponse] = []
    for team in teams:
        detail = await get_team_detail(session, team.id)
        if detail is not None:
            result.append(_map_team(detail))
    return result


async def get_team_entry(
    session: AsyncSession,
    team_id: int,
) -> TeamResponse:
    team = await get_team_detail(session, team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    return _map_team(team)


async def leave_team(
    session: AsyncSession,
    *,
    current_user_id: int,
    team_id: int,
) -> TeamResponse | None:
    team = await get_team_by_id(session, team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    membership = await get_team_member(session, team_id=team_id, user_id=current_user_id)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this team",
        )

    await delete_team_member(session, membership)

    next_member = await get_next_team_member_after_leave(session, team_id)
    if next_member is None:
        await session.delete(team)
        await session.commit()
        return None

    if team.captain_id == current_user_id:
        team.captain_id = next_member.user_id

    await session.commit()
    return await get_team_entry(session, team_id)


async def create_join_request(
    session: AsyncSession,
    *,
    current_user_id: int,
    team_id: int,
) -> TeamJoinRequestResponse:
    team = await get_team_by_id(session, team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    if team.captain_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Captain is already in the team",
        )

    membership = await get_team_member(session, team_id=team_id, user_id=current_user_id)
    if membership is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a team member",
        )

    existing_request = await get_team_request_by_team_and_user(
        session,
        team_id=team_id,
        user_id=current_user_id,
    )
    if existing_request is not None:
        if existing_request.status in {TEAM_REQUEST_PENDING, TEAM_REQUEST_APPROVED}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Join request already exists",
            )

        existing_request.status = TEAM_REQUEST_PENDING
        await session.commit()

        updated_request = await get_team_request_by_id(session, existing_request.id)
        if updated_request is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Join request was updated but could not be loaded",
            )

        return _map_team_request(updated_request)

    team_request = await create_team_request(
        session,
        team_id=team_id,
        user_id=current_user_id,
        status=TEAM_REQUEST_PENDING,
    )
    await session.commit()

    created_request = await get_team_request_by_id(session, team_request.id)
    if created_request is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Join request was created but could not be loaded",
        )

    return _map_team_request(created_request)


async def get_join_requests(
    session: AsyncSession,
    *,
    current_user_id: int,
    team_id: int,
) -> list[TeamJoinRequestResponse]:
    await _require_team_captain(session, team_id=team_id, current_user_id=current_user_id)
    requests = await list_team_requests(session, team_id)
    return [_map_team_request(item) for item in requests]


async def _update_join_request_status(
    session: AsyncSession,
    *,
    current_user_id: int,
    request_id: int,
    new_status: str,
) -> TeamJoinRequestResponse:
    team_request = await get_team_request_model_by_id(session, request_id)
    if team_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team request not found",
        )

    if team_request.status != TEAM_REQUEST_PENDING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only pending requests can be updated",
        )

    await _require_team_captain(
        session,
        team_id=team_request.team_id,
        current_user_id=current_user_id,
    )

    if new_status == TEAM_REQUEST_APPROVED:
        membership = await get_team_member(
            session,
            team_id=team_request.team_id,
            user_id=team_request.user_id,
        )
        if membership is None:
            await create_team_member(
                session,
                team_id=team_request.team_id,
                user_id=team_request.user_id,
            )

    team_request.status = new_status
    await session.commit()

    updated_request = await get_team_request_by_id(session, request_id)
    if updated_request is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team request was updated but could not be loaded",
        )

    return _map_team_request(updated_request)


async def approve_join_request(
    session: AsyncSession,
    *,
    current_user_id: int,
    request_id: int,
) -> TeamJoinRequestResponse:
    return await _update_join_request_status(
        session,
        current_user_id=current_user_id,
        request_id=request_id,
        new_status=TEAM_REQUEST_APPROVED,
    )


async def reject_join_request(
    session: AsyncSession,
    *,
    current_user_id: int,
    request_id: int,
) -> TeamJoinRequestResponse:
    return await _update_join_request_status(
        session,
        current_user_id=current_user_id,
        request_id=request_id,
        new_status=TEAM_REQUEST_REJECTED,
    )


async def remove_team_member(
    session: AsyncSession,
    *,
    current_user_id: int,
    team_id: int,
    user_id: int,
) -> TeamResponse:
    team = await _require_team_captain(
        session,
        team_id=team_id,
        current_user_id=current_user_id,
    )

    if user_id == team.captain_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Captain cannot be removed with this endpoint",
        )

    membership = await get_team_member(session, team_id=team_id, user_id=user_id)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team member not found",
        )

    await delete_team_member(session, membership)
    await session.commit()
    return await get_team_entry(session, team_id)


async def assign_team_captain(
    session: AsyncSession,
    *,
    current_user_id: int,
    team_id: int,
    payload: UpdateTeamCaptainRequest,
) -> TeamResponse:
    team = await _require_team_captain(
        session,
        team_id=team_id,
        current_user_id=current_user_id,
    )

    if not payload.userId.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="userId must be numeric",
        )

    membership = await get_team_member(
        session,
        team_id=team_id,
        user_id=int(payload.userId),
    )
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not a member of this team",
        )

    team.captain_id = membership.user_id
    await session.commit()
    return await get_team_entry(session, team_id)
