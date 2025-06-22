"""
Create task list use case.

This module contains the business logic for creating a new task list.
"""

from sqlalchemy.orm import Session

from app.exceptions import ConflictException
from app.infrastructure.db.models import TaskList
from app.infrastructure.db.repositories import TaskListRepository


def create_task_list(db: Session, name: str) -> TaskList:
    """
    Create a new task list.

    Args:
        db: Database session for persistence.
        name: Name for the new task list.

    Returns:
        TaskList: The created task list instance.

    Raises:
        ConflictException: If a task list with the same name already exists.
    """
    task_list_repo = TaskListRepository(db)

    # Check if a task list with the same name already exists
    existing = task_list_repo.get_by_name(name)
    if existing:
        raise ConflictException(f"Task list with name '{name}' already exists")

    # Create the task list
    task_list = TaskList(name=name)
    return task_list_repo.create(task_list)
