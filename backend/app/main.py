"""
backend/app/main.py

Entry point for HAI-SOC FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.database.connection import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):

    MongoDB.connect()

    yield

    MongoDB.close()


app = FastAPI(
    title="HAI-SOC API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)