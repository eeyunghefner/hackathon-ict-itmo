from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    firstName: str = Field(min_length=1, max_length=100)
    lastName: str = Field(min_length=1, max_length=100)
    university: str = Field(min_length=1, max_length=255)


class RegisterResponse(BaseModel):
    id: str
    email: EmailStr
    role: str
    token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)


class AuthUserResponse(BaseModel):
    id: str
    email: EmailStr
    role: str


class LoginResponse(BaseModel):
    token: str
    user: AuthUserResponse
