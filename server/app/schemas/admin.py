from pydantic import BaseModel


class AdminUserResponse(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    roles: list[str]
    university: str | None = None


class UpdateAdminUserRequest(BaseModel):
    role: str
