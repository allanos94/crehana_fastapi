"""
Common domain model components.

This module contains shared base classes and common components
used across all domain models.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    This class serves as the declarative base for all domain models,
    providing common functionality and metadata handling.
    """

    pass
