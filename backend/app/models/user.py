from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr

    hashed_password: str

    role: str

    created_at: datetime

    last_login: datetime | None = None