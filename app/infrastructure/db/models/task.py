"""
Task domain model.

This module contains the Task model and related enums for status and priority.
"""

import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.commons import Base

if TYPE_CHECKING:
    from app.infrastructure.db.models.task_list import TaskList
    from app.infrastructure.db.models.user import User


class TaskStatus(str, enum.Enum):
    """Enumeration for task status values."""

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(str, enum.Enum):
    """Enumeration for task priority levels."""

    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    """
    Task domain model representing a single task within a task list.

    Attributes:
        id: Unique identifier for the task.
        title: Title of the task (max 200 characters).
        description: Optional detailed description of the task.
        status: Current status of the task (pending, in_progress, completed).
        priority: Priority level of the task (low, medium, high).
        created_at: Timestamp when the task was created.
        updated_at: Timestamp when the task was last updated.
        task_list_id: Foreign key reference to the task list.
        user_id: Optional foreign key reference to the assigned user.
        task_list: Relationship to the parent task list.
        user: Optional relationship to the assigned user.
    """

    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]]
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.pending
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority), default=TaskPriority.medium
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    task_list_id: Mapped[int] = mapped_column(ForeignKey("task_list.id"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))

    # Relationships
    task_list: Mapped["TaskList"] = relationship(back_populates="tasks")
    user: Mapped[Optional["User"]] = relationship(back_populates="tasks")
