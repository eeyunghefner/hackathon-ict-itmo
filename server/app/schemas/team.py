from pydantic import BaseModel, Field


class CreateTeamRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)


class TeamMemberResponse(BaseModel):
    id: str
    name: str


class TeamResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    captainId: str | None = None
    members: list[TeamMemberResponse]
