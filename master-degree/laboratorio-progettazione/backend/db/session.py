"""
This module sets up the database connection and session for SQLAlchemy.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if "PYTEST_CURRENT_TEST" in os.environ:
    load_dotenv(os.path.join(base_dir, ".env.test"), override=True)
else:
    load_dotenv(os.path.join(base_dir, ".env"), override=False)

def _create_engine_and_session():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URL:
        return None, None
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_timeout=60,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def get_engine_and_session():
    engine, SessionLocal = _create_engine_and_session()
    if engine is None or SessionLocal is None:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    return engine, SessionLocal


engine, SessionLocal = _create_engine_and_session()


def init_db():
    """Initialize the database by creating all tables."""
    _engine = engine
    if _engine is None:
        _engine, _ = get_engine_and_session()
    print(_engine.url)
    Base.metadata.create_all(bind=_engine)
