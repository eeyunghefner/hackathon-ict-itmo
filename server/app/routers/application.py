from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import ApplicationResponse
from app.services import approve_application, reject_application

router = APIRouter(prefix="/applications", tags=["applications"])


@router.patch("/{application_id}/approve", response_model=ApplicationResponse)
async def approve_hackathon_application(
    application_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> ApplicationResponse:
    return await approve_application(
        session,
        current_user_id=current_user_id,
        application_id=application_id,
    )


@router.patch("/{application_id}/reject", response_model=ApplicationResponse)
async def reject_hackathon_application(
    application_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> ApplicationResponse:
    return await reject_application(
        session,
        current_user_id=current_user_id,
        application_id=application_id,
    )
