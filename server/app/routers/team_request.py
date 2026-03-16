from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import TeamJoinRequestResponse
from app.services import approve_join_request, reject_join_request

router = APIRouter(prefix="/team-requests", tags=["team-requests"])


@router.patch("/{request_id}/approve", response_model=TeamJoinRequestResponse)
async def approve_team_request_route(
    request_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> TeamJoinRequestResponse:
    return await approve_join_request(
        session,
        current_user_id=current_user_id,
        request_id=request_id,
    )


@router.patch("/{request_id}/reject", response_model=TeamJoinRequestResponse)
async def reject_team_request_route(
    request_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> TeamJoinRequestResponse:
    return await reject_join_request(
        session,
        current_user_id=current_user_id,
        request_id=request_id,
    )
