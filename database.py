# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///password_checker.db"

# echo=True will show SQL in the console — set to False if you prefer quiet output
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()

def init_db():
    """Create all tables (imports models so they are registered)."""
    import models  # noqa: F401 - ensures models are loaded
    Base.metadata.create_all(bind=engine)
