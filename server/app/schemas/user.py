from pydantic import BaseModel, EmailStr, Field


class UserMeResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: EmailStr
    role: str
    university: str | None = None
    teamId: str | None = None


class UpdateUserProfileRequest(BaseModel):
    firstName: str = Field(min_length=1, max_length=100)
    lastName: str = Field(min_length=1, max_length=100)
    university: str = Field(min_length=1, max_length=255)
