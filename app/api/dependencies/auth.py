"""
Authentication dependencies for FastAPI.

This module provides dependencies for:
- Token validation
- Current user extraction
- Protected routes
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infrastructure.db.models.user import User
from app.infrastructure.db.session import get_db
from app.services.auth import AuthService
from app.services.user import UserService

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Get current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract email from token
    email = AuthService.get_user_from_token(token)
    if email is None:
        raise credentials_exception

    # Get user from database
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception

    return user


# Type alias for current user dependency
CurrentUser = Annotated[User, Depends(get_current_user)]
