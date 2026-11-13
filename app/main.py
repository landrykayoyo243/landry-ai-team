from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="API REST sécurisée de LANDRY AI TEAM. Les agents ne sont pas encore connectés à des modèles IA.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["system"])
def health() -> dict[str, str | bool]:
    return {"status": "ok", "service": settings.app_name, "healthy": True}


@app.get("/", tags=["system"])
def landing() -> dict[str, str]:
    return {"message": "LANDRY AI TEAM API", "docs": "/docs", "status": "initialized"}
