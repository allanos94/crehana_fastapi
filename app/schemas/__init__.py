"""
Schemas package for API request/response validation.

This package contains all Pydantic schemas for the task management API,
organized by domain entity and including common utilities.
"""

# Common schemas
from .common import (
    BaseResponse,
    ErrorResponse,
    FilterParams,
    HealthCheckResponse,
    PaginatedResponse,
    PaginationParams,
    SuccessResponse,
    ValidationErrorResponse,
)

# Task schemas
from .task import (
    TaskBase,
    TaskCreate,
    TaskResponse,
    TaskStatusUpdate,
    TaskSummaryResponse,
    TaskUpdate,
    TaskWithListResponse,
)

# Task List schemas
from .task_list import (
    TaskListBase,
    TaskListCreate,
    TaskListFilterParams,
    TaskListResponse,
    TaskListSummaryResponse,
    TaskListUpdate,
    TaskListWithTasksResponse,
)

# User schemas
from .user import (
    UserBase,
    UserCreate,
    UserFilterParams,
    UserResponse,
    UserSummaryResponse,
    UserUpdate,
)

__all__ = [
    # Task schemas
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskStatusUpdate",
    "TaskResponse",
    "TaskWithListResponse",
    "TaskSummaryResponse",
    # Task List schemas
    "TaskListBase",
    "TaskListCreate",
    "TaskListUpdate",
    "TaskListResponse",
    "TaskListWithTasksResponse",
    "TaskListSummaryResponse",
    "TaskListFilterParams",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserSummaryResponse",
    "UserFilterParams",  # Common schemas
    "BaseResponse",
    "ErrorResponse",
    "ValidationErrorResponse",
    "SuccessResponse",
    "PaginationParams",
    "PaginatedResponse",
    "FilterParams",
    "HealthCheckResponse",
]
