from pydantic import BaseModel


class TeamJoinRequestResponse(BaseModel):
    id: str
    userId: str
    userName: str
    status: str


class UpdateTeamCaptainRequest(BaseModel):
    userId: str
