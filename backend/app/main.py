from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import health, dashboard, transactions, ai, recovery, audit, settings as settings_router

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="RecoverAI --- Autonomous AI Payment Recovery Platform Backend"
)

# CORS Configuration for local frontend & production deployment origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(health.router)
app.include_router(dashboard.router)
app.include_router(transactions.router)
app.include_router(ai.router)
app.include_router(recovery.router)
app.include_router(audit.router)
app.include_router(settings_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
