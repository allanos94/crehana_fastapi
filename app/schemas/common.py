"""
Common schemas for API request/response validation.

This module contains reusable Pydantic schemas for common API patterns
like error responses, pagination, and filtering.
"""

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

# Generic type for paginated responses
T = TypeVar("T")


class BaseResponse(BaseModel):
    """Base schema for API responses with common fields."""

    id: int = Field(..., description="Resource ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    error: str = Field(..., description="Error type or code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict[str, Any]] = Field(
        None, description="Additional error details"
    )


class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses."""

    error: str = Field(default="validation_error", description="Error type")
    message: str = Field(default="Validation failed", description="Error message")
    details: list[dict[str, Any]] = Field(..., description="List of validation errors")


class SuccessResponse(BaseModel):
    """Schema for success responses without data."""

    success: bool = Field(True, description="Success indicator")
    message: str = Field(..., description="Success message")


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""

    limit: int = Field(10, ge=1, le=100, description="Number of results to return")
    offset: int = Field(0, ge=0, description="Number of results to skip")


class PaginatedResponse(BaseModel, Generic[T]):
    """Schema for paginated responses."""

    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., ge=0, description="Total number of items")
    limit: int = Field(..., ge=1, description="Number of items per page")
    offset: int = Field(..., ge=0, description="Number of items skipped")
    has_next: bool = Field(..., description="Whether there are more items")
    has_previous: bool = Field(..., description="Whether there are previous items")

    @classmethod
    def create(
        cls, items: list[T], total: int, limit: int, offset: int
    ) -> "PaginatedResponse[T]":
        """
        Create a paginated response.

        Args:
            items: List of items for current page.
            total: Total number of items.
            limit: Number of items per page.
            offset: Number of items skipped.

        Returns:
            PaginatedResponse: The paginated response object.
        """
        return cls(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
            has_next=offset + limit < total,
            has_previous=offset > 0,
        )


class FilterParams(BaseModel):
    """Base schema for filtering parameters."""

    search: Optional[str] = Field(None, description="Search term for text fields")
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: Optional[str] = Field(
        "asc", pattern="^(asc|desc)$", description="Sort order: asc or desc"
    )

    class Config:
        """Pydantic configuration."""

        str_strip_whitespace = True


class HealthCheckResponse(BaseModel):
    """Schema for health check responses."""

    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: Optional[str] = Field(None, description="API version")
    database: Optional[str] = Field(None, description="Database status")
