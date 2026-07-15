"""
backend/app/main.py

Entry point for the HAI-SOC backend.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.database.connection import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    # Startup
    MongoDB.connect()
    print("🚀 HAI-SOC Backend Started")

    yield

    # Shutdown
    MongoDB.close()
    print("🛑 HAI-SOC Backend Stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    """

    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Healthcare AI Security Operations Center Backend",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """

    try:
        MongoDB.get_database()

        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.APP_VERSION,
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }