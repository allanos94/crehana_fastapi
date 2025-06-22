"""
User schemas for API request/response validation.

This module contains Pydantic schemas for user-related API operations,
including request validation and response serialization.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base schema for user with common fields."""

    email: EmailStr = Field(..., description="User email address")
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="User display name"
    )


class UserCreate(UserBase):
    """Schema for creating a new user."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    email: Optional[EmailStr] = Field(None, description="User email address")
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="User display name"
    )


class UserResponse(UserBase):
    """Schema for user response."""

    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class UserSummaryResponse(UserResponse):
    """Schema for user summary with task statistics."""

    total_tasks: int = Field(..., ge=0, description="Total number of tasks")
    completed_tasks: int = Field(..., ge=0, description="Number of completed tasks")


class UserFilterParams(BaseModel):
    """Schema for user filtering parameters."""

    email: Optional[str] = Field(None, description="Filter by email (partial match)")
    name: Optional[str] = Field(None, description="Filter by name (partial match)")
    limit: int = Field(10, ge=1, le=100, description="Number of results to return")
    offset: int = Field(0, ge=0, description="Number of results to skip")

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True
