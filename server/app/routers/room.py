from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.routers.dependencies import get_current_user_id
from app.schemas import (
    CreateRoomBookingRequest,
    RoomAvailabilityResponse,
    RoomBookingResponse,
    RoomResponse,
)
from app.services import book_room, get_room_availability, get_rooms

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomResponse])
async def read_rooms(
    session: AsyncSession = Depends(get_async_session),
) -> list[RoomResponse]:
    return await get_rooms(session)


@router.get("/availability", response_model=list[RoomAvailabilityResponse])
async def read_room_availability(
    date_value: date = Query(alias="date"),
    session: AsyncSession = Depends(get_async_session),
) -> list[RoomAvailabilityResponse]:
    return await get_room_availability(session, date_value)


@router.post("/book", response_model=RoomBookingResponse, status_code=status.HTTP_201_CREATED)
async def create_room_booking_route(
    payload: CreateRoomBookingRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
) -> RoomBookingResponse:
    return await book_room(
        session,
        current_user_id=current_user_id,
        payload=payload,
    )
