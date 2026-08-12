"""
backend/app/main.py

Entry point for HAI-SOC FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import api_router
from backend.app.database.connection import MongoDB


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

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)