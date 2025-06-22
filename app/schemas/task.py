"""
Task schemas for API request/response validation.

This module contains Pydantic schemas for task-related API operations,
including request validation and response serialization.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.domain.value_objects import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    """Base schema for task with common fields."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=1000, description="Task description")
    priority: TaskPriority = Field(TaskPriority.medium, description="Task priority level")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    task_list_id: int = Field(..., gt=0, description="ID of the task list")
    user_id: int | None = Field(None, gt=0, description="ID of assigned user")


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: str | None = Field(
        None, min_length=1, max_length=200, description="Task title"
    )
    description: str | None = Field(None, max_length=1000, description="Task description")
    priority: TaskPriority | None = Field(None, description="Task priority level")
    user_id: int | None = Field(None, gt=0, description="ID of assigned user")


class TaskStatusUpdate(BaseModel):
    """Schema for updating task status."""

    status: TaskStatus = Field(..., description="New task status")


class TaskResponse(TaskBase):
    """Schema for task response."""

    id: int = Field(..., description="Task ID")
    status: TaskStatus = Field(..., description="Current task status")
    task_list_id: int = Field(..., description="ID of the task list")
    user_id: int | None = Field(None, description="ID of assigned user")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class TaskWithListResponse(TaskResponse):
    """Schema for task response with task list information."""

    task_list: Any = Field(..., description="Task list information")


class TaskSummaryResponse(BaseModel):
    """Schema for task summary with completion percentage."""

    task: TaskResponse = Field(..., description="Task information")
    completion_percentage: float = Field(
        ..., ge=0, le=100, description="Completion percentage"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True
