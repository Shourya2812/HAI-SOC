"""
backend/app/api/router.py

Central router for HAI-SOC.
"""

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.logs import router as logs_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes import auth

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(logs_router)
api_router.include_router(incidents_router)
api_router.include_router(auth.router)