"""
backend/app/api/routes/health.py

Health check endpoints.
"""

from fastapi import APIRouter

router = APIRouter(
    tags=["Health"]
)


@router.get("/")
def root():
    """
    Root endpoint.
    """

    return {
        "message": "Welcome to HAI-SOC API 🚀"
    }


@router.get("/health")
def health():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy"
    }