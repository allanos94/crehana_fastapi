"""
Authentication-related Pydantic schemas.

This module contains schemas for authentication operations:
- User registration and login
- Token responses
- Authentication requests
"""

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    """Schema for user login requests."""

    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """Schema for user registration requests."""

    email: EmailStr
    name: str | None = None
    password: str


class Token(BaseModel):
    """Schema for token responses."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data extraction."""

    email: str | None = None


class UserResponse(BaseModel):
    """Schema for user response data."""

    id: int
    email: str
    name: str | None = None

    class Config:
        from_attributes = True
