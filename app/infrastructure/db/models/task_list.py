"""
TaskList domain model.

This module contains the TaskList model representing a collection of tasks.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.commons import Base

if TYPE_CHECKING:
    from app.infrastructure.db.models.task import Task


class TaskList(Base):
    """
    TaskList domain model representing a collection of related tasks.

    Attributes:
        id: Unique identifier for the task list.
        name: Name of the task list (max 100 characters).
        tasks: Collection of tasks belonging to this list.
    """

    __tablename__ = "task_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="task_list", cascade="all, delete-orphan"
    )
