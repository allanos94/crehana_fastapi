"""
Authentication endpoints for user registration and login.

This module provides:
- User registration
- User login with JWT token generation
- Protected user profile endpoint
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies.auth import CurrentUser
from app.domain.schemas.auth import Token, UserRegister, UserResponse
from app.infrastructure.db.session import get_db
from app.services.auth import ACCESS_TOKEN_EXPIRE_MINUTES, AuthService
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user_data: UserRegister, db: Annotated[Session, Depends(get_db)]):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        UserResponse: Created user data

    Raises:
        HTTPException: If email already exists
    """
    user_service = UserService(db)

    # Check if user already exists
    existing_user = user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    user = user_service.create_user(user_data)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=Token)
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Login user and return JWT token.

    Args:
        form_data: OAuth2 password form with username (email) and password
        db: Database session

    Returns:
        Token: JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    user_service = UserService(db)

    # Authenticate user
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: CurrentUser):
    """
    Get current user profile.

    Args:
        current_user: Current authenticated user

    Returns:
        UserResponse: User profile data
    """
    return UserResponse.model_validate(current_user)
