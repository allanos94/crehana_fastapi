"""
Pytest configuration and fixtures.

This module contains shared fixtures and configuration for all tests.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.v1.endpoints import auth, task, task_list
from app.infrastructure.db.session import get_db
from tests.test_database import create_test_database, drop_test_database, get_test_db


def create_test_app() -> FastAPI:
    """Create a test FastAPI app without lifespan for testing."""
    test_app = FastAPI(
        title="Task Management API - Test",
        description="A RESTful API for managing tasks and task lists - Test Mode",
        version="1.0.0-test",
    )

    # Add basic endpoints
    @test_app.get("/")
    async def root():
        return {"message": "Task Management API - Test"}

    @test_app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    # Include routers
    test_app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
    test_app.include_router(task.router, prefix="/api/v1/tasks", tags=["tasks"])
    test_app.include_router(
        task_list.router, prefix="/api/v1/task-lists", tags=["task-lists"]
    )

    return test_app


@pytest.fixture(scope="function")
def db_session():
    """
    Create a test database session.

    This fixture creates a fresh database for each test function,
    ensuring test isolation.
    """
    create_test_database()
    db = next(get_test_db())
    try:
        yield db
    finally:
        db.close()
        drop_test_database()


@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Create a test client with database dependency override.

    This fixture provides a FastAPI test client with the database
    dependency overridden to use the test database.
    """
    test_app = create_test_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    test_app.dependency_overrides[get_db] = override_get_db

    with TestClient(test_app) as test_client:
        yield test_client

    # Clean up dependency overrides
    test_app.dependency_overrides.clear()


@pytest.fixture
def sample_task_list(db_session: Session):
    """Create a sample task list for testing."""
    from app.infrastructure.db.models import TaskList

    task_list = TaskList(name="Test Task List")
    db_session.add(task_list)
    db_session.commit()
    db_session.refresh(task_list)
    return task_list


@pytest.fixture
def sample_user(db_session: Session):
    """Create a sample user for testing."""
    from app.infrastructure.db.models import User
    from app.services.auth import AuthService

    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=AuthService.get_password_hash("testpassword123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient, db_session: Session) -> dict[str, str]:
    """Create authentication headers with JWT token for testing."""
    # Try to get existing user, create if doesn't exist
    from app.infrastructure.db.models import User
    from app.services.auth import AuthService

    email = "test@example.com"
    password = "testpassword123"

    # Check if user already exists
    existing_user = db_session.query(User).filter(User.email == email).first()

    if not existing_user:
        user = User(
            email=email,
            name="Test User",
            password_hash=AuthService.get_password_hash(password),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    # Login to get JWT token using form data (OAuth2PasswordRequestForm)
    login_data = {
        "username": email,  # OAuth2 form uses 'username' field for email
        "password": password,
    }
    response = client.post("/api/v1/auth/login", data=login_data)  # Use data= not json=
    assert (
        response.status_code == 200
    ), f"Login failed with {response.status_code}: {response.text}"
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_task(db_session: Session, sample_task_list, sample_user):
    """Create a sample task for testing."""
    from app.infrastructure.db.models import Task, TaskPriority, TaskStatus

    task = Task(
        title="Test Task",
        description="This is a test task",
        status=TaskStatus.pending,
        priority=TaskPriority.medium,
        task_list_id=sample_task_list.id,
        user_id=sample_user.id,
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task
