"""
Test database configuration.

This module provides database configuration for testing,
using SQLite in-memory database for faster tests.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.db.models import Base

# SQLite in-memory database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine with specific configurations for SQLite
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

# Create test session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def create_test_database():
    """Create all tables in the test database."""
    Base.metadata.create_all(bind=test_engine)


def drop_test_database():
    """Drop all tables in the test database."""
    Base.metadata.drop_all(bind=test_engine)


def get_test_db():
    """
    Get test database session.

    This function creates a test database session and ensures it's properly
    closed after use. It's designed to be used as a FastAPI dependency override.

    Yields:
        Session: SQLAlchemy test database session.
    """
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
