"""
Pydantic schemas used by the User API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.enums import UserRole


class CreateUserRequest(BaseModel):
    """
    Request schema for creating a new user.
    """

    email: EmailStr

    password: str

    role: UserRole

    model_config = ConfigDict(extra="forbid")


class UpdateUserRequest(BaseModel):
    """
    Request schema for updating user information.
    """

    role: Optional[UserRole] = None

    password: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
    """
    Response returned to clients.
    """

    id: str

    email: EmailStr

    role: UserRole

    created_at: datetime

    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)