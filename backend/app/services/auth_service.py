"""
backend/app/services/auth_service.py

Authentication service for HAI-SOC.
"""

from datetime import datetime, UTC

from app.database.collections import users_collection
from app.models.user import User
from app.schemas.user_schema import CreateUserRequest
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    def register_user(request: CreateUserRequest):

        existing_user = users_collection.find_one(
            {
                "email": request.email
            }
        )

        if existing_user:
            raise ValueError("Email already registered.")

        user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
            role=request.role,
            created_at=datetime.now(UTC),
        )

        users_collection.insert_one(
            user.model_dump()
        )

        return {
            "message": "User registered successfully."
        }

    @staticmethod
    def login(
        email: str,
        password: str,
    ) -> TokenResponse:
        user = users_collection.find_one(
            {
                "email": email
            }
        )

        if user is None:
            raise ValueError("Invalid credentials.")

        if not verify_password(
            password,
            user["hashed_password"],
        ):
            raise ValueError("Invalid credentials.")

        token = create_access_token(
            subject=user["email"]
        )

        return TokenResponse(
            access_token=token
        )