"""
Domain value objects.

This module contains all value objects for the task management domain.
Value objects are immutable objects that are defined by their attributes
and contain domain-specific validation and business rules.
"""

import enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, enum.Enum):
    """Enumeration for task status."""

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

    def __str__(self) -> str:
        """Return the string representation of the status."""
        return self.value

    @classmethod
    def get_completed_statuses(cls) -> list["TaskStatus"]:
        """Return the statuses considered as completed."""
        return [cls.completed]

    @classmethod
    def get_active_statuses(cls) -> list["TaskStatus"]:
        """Return the statuses considered as active."""
        return [cls.pending, cls.in_progress]


class TaskPriority(str, enum.Enum):
    """Enumeration for task priority."""

    low = "low"
    medium = "medium"
    high = "high"

    def __str__(self) -> str:
        """Return the string representation of the priority."""
        return self.value

    @classmethod
    def get_order_value(cls, priority: "TaskPriority") -> int:
        """Return a numeric value for ordering priorities."""
        order = {cls.low: 1, cls.medium: 2, cls.high: 3}
        return order.get(priority, 0)


class TaskId(BaseModel):
    """Value object for task identifier."""

    value: Annotated[int, Field(gt=0)]

    def __str__(self) -> str:
        """Return the string representation of the task ID."""
        return str(self.value)

    def __int__(self) -> int:
        """Return the integer representation of the task ID."""
        return self.value


class TaskListId(BaseModel):
    """Value object for task list identifier."""

    value: Annotated[int, Field(gt=0)]

    def __str__(self) -> str:
        """Return the string representation of the task list ID."""
        return str(self.value)

    def __int__(self) -> int:
        """Return the integer representation of the task list ID."""
        return self.value


class UserId(BaseModel):
    """Value object for user identifier."""

    value: Annotated[int, Field(gt=0)]

    def __str__(self) -> str:
        """Return the string representation of the user ID."""
        return str(self.value)

    def __int__(self) -> int:
        """Return the integer representation of the user ID."""
        return self.value


class TaskListName(BaseModel):
    """Value object for task list name."""

    value: Annotated[str, Field(min_length=1, max_length=100)]

    def __str__(self) -> str:
        """Return the string representation of the task list name."""
        return self.value

    @field_validator("value")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that the name is not empty after stripping whitespace."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class TaskTitle(BaseModel):
    """Value object for task title."""

    value: Annotated[str, Field(min_length=1, max_length=200)]

    def __str__(self) -> str:
        """Return the string representation of the task title."""
        return self.value

    @field_validator("value")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate that the title is not empty after stripping whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class UserEmail(BaseModel):
    """Value object for user email."""

    value: Annotated[str, Field(max_length=100, pattern=r"^[^@]+@[^@]+\.[^@]+$")]

    def __str__(self) -> str:
        """Return the string representation of the user email."""
        return self.value

    @field_validator("value")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Normalize email by converting to lowercase and stripping spaces."""
        return v.lower().strip()


class CompletionPercentage(BaseModel):
    """Value object for completion percentage."""

    value: Annotated[float, Field(ge=0, le=100)]

    def __str__(self) -> str:
        """Return the string representation of the completion percentage."""
        return f"{self.value:.1f}%"

    @classmethod
    def calculate_from_tasks(
        cls, total_tasks: int, completed_tasks: int
    ) -> "CompletionPercentage":
        """Calculate completion percentage given total and completed tasks."""
        if total_tasks == 0:
            return cls(value=0.0)
        percentage = (completed_tasks / total_tasks) * 100
        return cls(value=percentage)
