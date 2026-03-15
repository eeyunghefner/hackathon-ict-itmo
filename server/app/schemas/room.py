from datetime import datetime

from pydantic import BaseModel


class RoomResponse(BaseModel):
    id: str
    name: str
    capacity: int


class RoomAvailabilityBookingResponse(BaseModel):
    startTime: datetime
    endTime: datetime


class RoomAvailabilityResponse(BaseModel):
    id: str
    name: str
    capacity: int
    isAvailable: bool
    bookings: list[RoomAvailabilityBookingResponse]


class CreateRoomBookingRequest(BaseModel):
    roomId: str
    startTime: datetime
    endTime: datetime


class RoomBookingResponse(BaseModel):
    id: str
    roomId: str
    startTime: datetime
    endTime: datetime
