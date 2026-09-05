from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

if db_url.startswith("postgresql"):
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        pool_pre_ping=True,       # Check connection validity before using
        pool_size=10,             # Base number of connections in the pool
        max_overflow=20,          # Extra connections allowed during spikes
        pool_recycle=1800         # Recycle connections every 30 minutes
    )
else:
    engine = create_engine(db_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
