"""
backend/app/api/routes/auth.py

Authentication routes for HAI-SOC.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.api.dependencies import get_current_user
from app.schemas.user_schema import CreateUserRequest
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schema import (
    RegisterResponse,
    TokenResponse,
    CurrentUserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
)
def register(
    request: CreateUserRequest,
):
    """
    Register a new user.
    """
    try:
        return AuthService.register_user(request)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Authenticate a user and return a JWT.
    """
    try:
        return AuthService.login(
            email=form_data.username,
            password=form_data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_me(
    current_user=Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """
    return current_user