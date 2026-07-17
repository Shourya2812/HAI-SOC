from typing import Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.database.collections import users_collection
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    """
    Extract the current authenticated user from JWT.
    """

    try:
        payload = decode_access_token(token)

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        user = users_collection.find_one({"email": email})

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        user["id"] = str(user["_id"])
        user.pop("_id")
        user.pop("hashed_password", None)

        return user

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )