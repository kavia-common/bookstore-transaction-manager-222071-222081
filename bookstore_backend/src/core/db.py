import os
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

# Resolve database URL with a default to local SQLite file
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bookstore.db")

# For SQLite, need to allow check_same_thread=False for multi-threaded FastAPI
connect_args: Optional[dict] = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else None

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args or {})

# Configure a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Shared declarative base for models
Base = declarative_base()


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session for dependency injection in FastAPI routes.

    Yields:
        Session: an active SQLAlchemy session bound to the configured engine.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Context manager that yields a session and ensures proper close."""
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
