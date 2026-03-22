from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import EventResponse, UpdateEventRequest
from app.services import delete_event_entry, update_event_entry

router = APIRouter(prefix="/events", tags=["events"])


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event_route(
    event_id: int,
    payload: UpdateEventRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> EventResponse:
    return await update_event_entry(
        session,
        current_user_id=current_user_id,
        event_id=event_id,
        payload=payload,
    )


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_route(
    event_id: int,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    await delete_event_entry(
        session,
        current_user_id=current_user_id,
        event_id=event_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
