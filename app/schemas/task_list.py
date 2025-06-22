"""
TaskList schemas for API request/response validation.

This module contains Pydantic schemas for task list-related API operations,
including request validation and response serialization.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import BaseResponse


class TaskListBase(BaseModel):
    """Base schema for task list with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Task list name")


class TaskListCreate(TaskListBase):
    """Schema for creating a new task list."""

    pass


class TaskListUpdate(BaseModel):
    """Schema for updating an existing task list."""

    name: str | None = Field(
        None, min_length=1, max_length=100, description="Task list name"
    )


class TaskListResponse(TaskListBase, BaseResponse):
    """Schema for task list response."""

    pass


class TaskListWithTasksResponse(TaskListResponse):
    """Schema for task list response with tasks included."""

    tasks: list[Any] = Field(default_factory=list, description="List of tasks")


class TaskListSummaryResponse(TaskListResponse):
    """Schema for task list summary with completion statistics."""

    total_tasks: int = Field(..., ge=0, description="Total number of tasks")
    completed_tasks: int = Field(..., ge=0, description="Number of completed tasks")
    completion_percentage: float = Field(
        ..., ge=0, le=100, description="Completion percentage"
    )


class TaskListFilterParams(BaseModel):
    """Schema for task list filtering parameters."""

    name: str | None = Field(None, description="Filter by task list name (partial match)")
    limit: int = Field(10, ge=1, le=100, description="Number of results to return")
    offset: int = Field(0, ge=0, description="Number of results to skip")

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
