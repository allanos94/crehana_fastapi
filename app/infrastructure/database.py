"""
Database configuration and connection management.

This module sets up the SQLAlchemy engine, session factory, and provides
database initialization functionality.
"""

import os
import subprocess

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.models import Base

# Load environment variables from .env file (for local development)
# This is optional - Docker Compose can override these values
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL variable is not set. Please set it in your .env file."
    )

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize the database using Alembic migrations.

    This function runs pending migrations to set up the database schema.
    If you need to create tables manually (for testing), use Base.metadata.create_all().
    """
    try:
        # Run Alembic migrations
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Database migrations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Migration failed: {e}")
        # Fallback to create_all for development/testing
        print("Falling back to create_all() for table creation...")
        Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency function to provide database sessions.

    Yields:
        SessionLocal: Database session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
