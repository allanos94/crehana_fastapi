"""
Repository implementations for data access.

This module contains concrete implementations of repository interfaces
for database operations using SQLAlchemy.
"""

from abc import ABC
from typing import Generic, Optional, TypeVar

from sqlalchemy.orm import Session

from app.infrastructure.db.models import Task, TaskList, TaskPriority, TaskStatus, User

# Generic type for repository entities
T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    """
    Abstract base repository with common CRUD operations.

    This class provides a generic interface for repository implementations
    following the Repository pattern.
    """

    def __init__(self, db: Session, model_class: type[T]):
        self.db = db
        self.model_class = model_class

    def create(self, entity: T) -> T:
        """Create a new entity in the database."""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get an entity by its ID."""
        return (
            self.db.query(self.model_class)
            .filter(self.model_class.id == entity_id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """Get all entities with pagination."""
        return self.db.query(self.model_class).offset(skip).limit(limit).all()

    def update(self, entity: T) -> T:
        """Update an existing entity."""
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        """Delete an entity by ID."""
        entity = self.get_by_id(entity_id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False


class TaskRepository(BaseRepository[Task]):
    """Repository for Task entity operations."""

    def __init__(self, db: Session):
        super().__init__(db, Task)

    def get_by_task_list_id(
        self, task_list_id: int, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get all tasks for a specific task list."""
        return (
            self.db.query(Task)
            .filter(Task.task_list_id == task_list_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Task]:
        """Get all tasks assigned to a specific user."""
        return (
            self.db.query(Task)
            .filter(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get all tasks with a specific status."""
        return (
            self.db.query(Task)
            .filter(Task.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_priority(
        self, priority: TaskPriority, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Get all tasks with a specific priority."""
        return (
            self.db.query(Task)
            .filter(Task.priority == priority)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_title(
        self, search_term: str, skip: int = 0, limit: int = 100
    ) -> list[Task]:
        """Search tasks by title (case-insensitive partial match)."""
        return (
            self.db.query(Task)
            .filter(Task.title.ilike(f"%{search_term}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tasks_with_filters(
        self,
        task_list_id: Optional[int] = None,
        user_id: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        """Get tasks with multiple optional filters."""
        query = self.db.query(Task)

        if task_list_id is not None:
            query = query.filter(Task.task_list_id == task_list_id)
        if user_id is not None:
            query = query.filter(Task.user_id == user_id)
        if status is not None:
            query = query.filter(Task.status == status)
        if priority is not None:
            query = query.filter(Task.priority == priority)

        return query.offset(skip).limit(limit).all()


class TaskListRepository(BaseRepository[TaskList]):
    """Repository for TaskList entity operations."""

    def __init__(self, db: Session):
        super().__init__(db, TaskList)

    def get_by_name(self, name: str) -> Optional[TaskList]:
        """Get a task list by its name."""
        return self.db.query(TaskList).filter(TaskList.name == name).first()

    def search_by_name(
        self, search_term: str, skip: int = 0, limit: int = 100
    ) -> list[TaskList]:
        """Search task lists by name (case-insensitive partial match)."""
        return (
            self.db.query(TaskList)
            .filter(TaskList.name.ilike(f"%{search_term}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_tasks(self, task_list_id: int) -> Optional[TaskList]:
        """Get a task list with its tasks loaded."""
        return self.db.query(TaskList).filter(TaskList.id == task_list_id).first()


class UserRepository(BaseRepository[User]):
    """Repository for User entity operations."""

    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address."""
        return self.db.query(User).filter(User.email == email).first()

    def search_by_name(
        self, search_term: str, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Search users by name (case-insensitive partial match)."""
        return (
            self.db.query(User)
            .filter(User.name.ilike(f"%{search_term}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_tasks(self, user_id: int) -> Optional[User]:
        """Get a user with their assigned tasks loaded."""
        return self.db.query(User).filter(User.id == user_id).first()
