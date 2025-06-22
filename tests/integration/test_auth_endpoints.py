"""
Integration tests for authentication endpoints.

This module tests:
- User registration endpoint
- User login endpoint
- Protected routes with JWT tokens
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.main import app
from app.infrastructure.db.models import Base
from app.infrastructure.db.session import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    """Create test client with test database."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


class TestAuthEndpoints:
    """Test cases for authentication endpoints."""

    def test_register_user_success(self, client):
        """Test successful user registration."""
        user_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "password": "testpassword123",
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned

    def test_register_user_duplicate_email(self, client):
        """Test registration with duplicate email."""
        # First registration
        user_data = {
            "email": "duplicate@example.com",
            "name": "Test User",
            "password": "testpassword123",
        }
        client.post("/api/v1/auth/register", json=user_data)

        # Second registration with same email
        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 400
        data = response.json()
        assert "already registered" in data["detail"]

    def test_register_user_invalid_email(self, client):
        """Test registration with invalid email."""
        user_data = {
            "email": "invalid-email",
            "name": "Test User",
            "password": "testpassword123",
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 422  # Validation error

    def test_login_user_success(self, client):
        """Test successful user login."""
        # Register user first
        user_data = {
            "email": "logintest@example.com",
            "name": "Login Test",
            "password": "testpassword123",
        }
        client.post("/api/v1/auth/register", json=user_data)

        # Login
        login_data = {
            "username": user_data["email"],  # OAuth2 uses 'username'
            "password": user_data["password"],
        }

        response = client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_user_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        login_data = {"username": "nonexistent@example.com", "password": "wrongpassword"}

        response = client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == 401
        data = response.json()
        assert "Incorrect email or password" in data["detail"]

    def test_get_current_user_success(self, client):
        """Test getting current user with valid token."""
        # Register and login user
        user_data = {
            "email": "currentuser@example.com",
            "name": "Current User",
            "password": "testpassword123",
        }
        client.post("/api/v1/auth/register", json=user_data)

        login_data = {"username": user_data["email"], "password": user_data["password"]}
        login_response = client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]

        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 401
        data = response.json()
        assert "Could not validate credentials" in data["detail"]

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401
