from datetime import date

from pydantic import BaseModel, Field


class CreateHackathonRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    theme: str = Field(min_length=1, max_length=255)
    format: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1)
    startDate: date
    endDate: date
    participantLimit: int = Field(gt=0)
    teamLimit: int = Field(gt=0)
    rules: str = Field(min_length=1)


class CreateHackathonResponse(BaseModel):
    id: str
    status: str


class HackathonListItemResponse(BaseModel):
    id: str
    title: str
    format: str
    startDate: date
    status: str


class HackathonDetailResponse(BaseModel):
    id: str
    title: str
    theme: str
    description: str | None
    format: str
    startDate: date
    endDate: date
    participantLimit: int | None
    teamLimit: int | None
    rules: str | None
    status: str


class UpdateHackathonRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    theme: str | None = Field(default=None, min_length=1, max_length=255)
    format: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, min_length=1)
    startDate: date | None = None
    endDate: date | None = None
    participantLimit: int | None = Field(default=None, gt=0)
    teamLimit: int | None = Field(default=None, gt=0)
    rules: str | None = Field(default=None, min_length=1)


class HackathonStatsResponse(BaseModel):
    participants: int
    teams: int
    solutions: int
    durationHours: int
