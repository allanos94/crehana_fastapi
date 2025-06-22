"""
Unit tests for repositories.

This module contains unit tests for repository implementations.
"""

from sqlalchemy.orm import Session

from app.infrastructure.db.models import (
    Task,
    TaskList,
    TaskPriority,
    TaskStatus,
    User,
)
from app.infrastructure.db.repositories import (
    TaskListRepository,
    TaskRepository,
    UserRepository,
)


class TestTaskRepository:
    """Test cases for TaskRepository."""

    def test_create_task(self, db_session: Session, sample_task_list):
        """Test creating a task through repository."""
        task_repo = TaskRepository(db_session)

        task = Task(
            title="Repository Test Task",
            description="Test description",
            task_list_id=sample_task_list.id,
            priority=TaskPriority.high,
        )

        created_task = task_repo.create(task)

        assert created_task.id is not None
        assert created_task.title == "Repository Test Task"
        assert created_task.priority == TaskPriority.high
        assert created_task.task_list_id == sample_task_list.id

    def test_get_task_by_id(self, db_session: Session, sample_task):
        """Test getting task by ID."""
        task_repo = TaskRepository(db_session)

        retrieved_task = task_repo.get_by_id(sample_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == sample_task.id
        assert retrieved_task.title == sample_task.title

    def test_get_task_by_id_not_found(self, db_session: Session):
        """Test getting task by ID when task doesn't exist."""
        task_repo = TaskRepository(db_session)

        retrieved_task = task_repo.get_by_id(99999)

        assert retrieved_task is None

    def test_get_tasks_by_task_list_id(self, db_session: Session, sample_task):
        """Test getting tasks by task list ID."""
        task_repo = TaskRepository(db_session)

        tasks = task_repo.get_by_task_list_id(sample_task.task_list_id)

        assert len(tasks) == 1
        assert tasks[0].id == sample_task.id

    def test_get_tasks_by_user_id(self, db_session: Session, sample_task):
        """Test getting tasks by user ID."""
        task_repo = TaskRepository(db_session)

        tasks = task_repo.get_by_user_id(sample_task.user_id)

        assert len(tasks) == 1
        assert tasks[0].id == sample_task.id

    def test_get_tasks_by_status(self, db_session: Session, sample_task):
        """Test getting tasks by status."""
        task_repo = TaskRepository(db_session)

        tasks = task_repo.get_by_status(TaskStatus.pending)

        assert len(tasks) == 1
        assert tasks[0].id == sample_task.id

    def test_get_tasks_by_priority(self, db_session: Session, sample_task):
        """Test getting tasks by priority."""
        task_repo = TaskRepository(db_session)

        tasks = task_repo.get_by_priority(TaskPriority.medium)

        assert len(tasks) == 1
        assert tasks[0].id == sample_task.id

    def test_search_tasks_by_title(self, db_session: Session, sample_task):
        """Test searching tasks by title."""
        task_repo = TaskRepository(db_session)

        tasks = task_repo.search_by_title("Test")

        assert len(tasks) == 1
        assert tasks[0].id == sample_task.id

    def test_get_tasks_with_filters(self, db_session: Session, sample_task):
        """Test getting tasks with multiple filters."""
        task_repo = TaskRepository(db_session)

        tasks = task_repo.get_tasks_with_filters(
            task_list_id=sample_task.task_list_id,
            status=TaskStatus.pending,
            priority=TaskPriority.medium,
        )

        assert len(tasks) == 1
        assert tasks[0].id == sample_task.id

    def test_update_task(self, db_session: Session, sample_task):
        """Test updating a task."""
        task_repo = TaskRepository(db_session)

        sample_task.title = "Updated Title"
        updated_task = task_repo.update(sample_task)

        assert updated_task.title == "Updated Title"

    def test_delete_task(self, db_session: Session, sample_task):
        """Test deleting a task."""
        task_repo = TaskRepository(db_session)
        task_id = sample_task.id

        deleted = task_repo.delete(task_id)

        assert deleted is True

        # Verify task is actually deleted
        retrieved_task = task_repo.get_by_id(task_id)
        assert retrieved_task is None

    def test_delete_task_not_found(self, db_session: Session):
        """Test deleting a task that doesn't exist."""
        task_repo = TaskRepository(db_session)

        deleted = task_repo.delete(99999)

        assert deleted is False


class TestTaskListRepository:
    """Test cases for TaskListRepository."""

    def test_create_task_list(self, db_session: Session):
        """Test creating a task list through repository."""
        task_list_repo = TaskListRepository(db_session)

        task_list = TaskList(name="Repository Test List")

        created_task_list = task_list_repo.create(task_list)

        assert created_task_list.id is not None
        assert created_task_list.name == "Repository Test List"

    def test_get_task_list_by_id(self, db_session: Session, sample_task_list):
        """Test getting task list by ID."""
        task_list_repo = TaskListRepository(db_session)

        retrieved_list = task_list_repo.get_by_id(sample_task_list.id)

        assert retrieved_list is not None
        assert retrieved_list.id == sample_task_list.id
        assert retrieved_list.name == sample_task_list.name

    def test_get_task_list_by_name(self, db_session: Session, sample_task_list):
        """Test getting task list by name."""
        task_list_repo = TaskListRepository(db_session)

        retrieved_list = task_list_repo.get_by_name(sample_task_list.name)

        assert retrieved_list is not None
        assert retrieved_list.id == sample_task_list.id

    def test_search_task_lists_by_name(self, db_session: Session, sample_task_list):
        """Test searching task lists by name."""
        task_list_repo = TaskListRepository(db_session)

        task_lists = task_list_repo.search_by_name("Test")

        assert len(task_lists) == 1
        assert task_lists[0].id == sample_task_list.id

    def test_get_all_task_lists(self, db_session: Session, sample_task_list):
        """Test getting all task lists."""
        task_list_repo = TaskListRepository(db_session)

        task_lists = task_list_repo.get_all()

        assert len(task_lists) == 1
        assert task_lists[0].id == sample_task_list.id


class TestUserRepository:
    """Test cases for UserRepository."""

    def test_create_user(self, db_session: Session):
        """Test creating a user through repository."""
        user_repo = UserRepository(db_session)

        from app.services.auth import AuthService

        user = User(
            email="repo@test.com",
            name="Repository User",
            password_hash=AuthService.get_password_hash("testpassword"),
        )

        created_user = user_repo.create(user)

        assert created_user.id is not None
        assert created_user.email == "repo@test.com"
        assert created_user.name == "Repository User"

    def test_get_user_by_id(self, db_session: Session, sample_user):
        """Test getting user by ID."""
        user_repo = UserRepository(db_session)

        retrieved_user = user_repo.get_by_id(sample_user.id)

        assert retrieved_user is not None
        assert retrieved_user.id == sample_user.id
        assert retrieved_user.email == sample_user.email

    def test_get_user_by_email(self, db_session: Session, sample_user):
        """Test getting user by email."""
        user_repo = UserRepository(db_session)

        retrieved_user = user_repo.get_by_email(sample_user.email)

        assert retrieved_user is not None
        assert retrieved_user.id == sample_user.id

    def test_search_users_by_name(self, db_session: Session, sample_user):
        """Test searching users by name."""
        user_repo = UserRepository(db_session)

        users = user_repo.search_by_name("Test")

        assert len(users) == 1
        assert users[0].id == sample_user.id
