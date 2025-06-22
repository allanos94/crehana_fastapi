"""
User domain model.

This module contains the User model representing system users.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.commons import Base

if TYPE_CHECKING:
    from app.infrastructure.db.models.task import Task


class User(Base):
    """
    User domain model representing a system user.

    Attributes:
        id: Unique identifier for the user.
        email: Unique email address of the user (max 100 characters).
        name: Optional display name of the user.
        password_hash: Hashed password for authentication.
        tasks: Collection of tasks assigned to this user.
    """

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[Optional[str]]
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")
