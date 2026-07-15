"""
backend/app/schemas/auth_schema.py

Schemas used by authentication endpoints.
"""

from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    """
    User login request.
    """

    email: EmailStr

    password: str

    model_config = ConfigDict(extra="forbid")


class TokenResponse(BaseModel):
    """
    JWT token returned after successful login.
    """

    access_token: str

    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Refresh token request.
    """

    refresh_token: str

    model_config = ConfigDict(extra="forbid")