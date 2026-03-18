from pydantic import BaseModel


class CreateApplicationRequest(BaseModel):
    teamId: str


class ApplicationResponse(BaseModel):
    id: str
    teamId: str
    teamName: str
    status: str
