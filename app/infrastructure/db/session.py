"""
Database session management.

This module provides database session dependency injection for FastAPI
and handles session lifecycle management.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.infrastructure.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.

    This function creates a database session and ensures it's properly
    closed after use. It's designed to be used as a FastAPI dependency.

    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
