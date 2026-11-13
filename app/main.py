from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="LANDRY AI TEAM — plateforme multi-agents IA sans Docker",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
        "healthy": True,
    }


@app.get("/api/system")
def system() -> dict[str, str]:
    return {
        "app_name": settings.app_name,
        "api_prefix": settings.api_v1_prefix,
        "database_url": settings.database_url,
    }


@app.get("/")
def landing() -> dict[str, str]:
    return {
        "message": "LANDRY AI TEAM est prêt.",
        "role": "manager",
        "status": "initialized",
    }
