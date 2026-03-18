from datetime import date

from pydantic import BaseModel


class AdminHackathonHistoryItemResponse(BaseModel):
    id: str
    title: str
    startDate: date
    endDate: date
    status: str
    participants: int
    teams: int
