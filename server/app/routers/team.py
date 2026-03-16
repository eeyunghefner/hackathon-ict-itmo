from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import (
    CreateTeamRequest,
    TeamJoinRequestResponse,
    TeamResponse,
    UpdateTeamCaptainRequest,
)
from app.services import (
    assign_team_captain,
    create_join_request,
    create_team_entry,
    get_join_requests,
    get_team_entry,
    leave_team,
    list_team_entries,
    remove_team_member,
)

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    payload: CreateTeamRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse:
    return await create_team_entry(
        session,
        current_user_id=current_user_id,
        payload=payload,
    )


@router.get("", response_model=list[TeamResponse])
async def read_teams(
    hackathonId: int | None = Query(default=None),
    session: AsyncSession = Depends(get_async_session),
) -> list[TeamResponse]:
    return await list_team_entries(session, hackathon_id=hackathonId)


@router.get("/{team_id}", response_model=TeamResponse)
async def read_team(
    team_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse:
    return await get_team_entry(session, team_id)


@router.post("/{team_id}/leave", response_model=TeamResponse | None, status_code=status.HTTP_200_OK)
async def leave_current_team(
    team_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse | None:
    result = await leave_team(
        session,
        current_user_id=current_user_id,
        team_id=team_id,
    )
    return result


@router.post("/{team_id}/join-request", response_model=TeamJoinRequestResponse, status_code=status.HTTP_201_CREATED)
async def request_team_join(
    team_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> TeamJoinRequestResponse:
    return await create_join_request(
        session,
        current_user_id=current_user_id,
        team_id=team_id,
    )


@router.get("/{team_id}/join-requests", response_model=list[TeamJoinRequestResponse])
async def read_team_join_requests(
    team_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> list[TeamJoinRequestResponse]:
    return await get_join_requests(
        session,
        current_user_id=current_user_id,
        team_id=team_id,
    )


@router.delete("/{team_id}/members/{user_id}", response_model=TeamResponse)
async def delete_team_member_route(
    team_id: int,
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse:
    return await remove_team_member(
        session,
        current_user_id=current_user_id,
        team_id=team_id,
        user_id=user_id,
    )


@router.patch("/{team_id}/captain", response_model=TeamResponse)
async def update_team_captain(
    team_id: int,
    payload: UpdateTeamCaptainRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> TeamResponse:
    return await assign_team_captain(
        session,
        current_user_id=current_user_id,
        team_id=team_id,
        payload=payload,
    )
