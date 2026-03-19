from datetime import datetime

from pydantic import BaseModel, Field


class CreateEventRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    startTime: datetime
    endTime: datetime
    roomId: str


class UpdateEventRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    startTime: datetime | None = None
    endTime: datetime | None = None
    roomId: str | None = None


class EventResponse(BaseModel):
    id: str
    hackathonId: str
    title: str
    description: str | None
    startTime: datetime
    endTime: datetime
    roomId: str
