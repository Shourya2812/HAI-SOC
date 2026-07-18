from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    message: str


class CurrentUserResponse(BaseModel):
    id: str
    email: EmailStr
    role: str
    created_at: datetime
    last_login: datetime | None = None