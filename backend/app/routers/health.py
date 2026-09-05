from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "version": settings.VERSION,
        "project": settings.PROJECT_NAME
    }
