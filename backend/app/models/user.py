from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.enums import UserRole


class User(BaseModel):
    """
    User model for authentication and authorization.
    """

    email: EmailStr

    hashed_password: str

    role: UserRole

    created_at: datetime

    last_login: datetime | None = None

    model_config = ConfigDict(
        extra="forbid"
    )