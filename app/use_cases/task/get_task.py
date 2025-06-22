"""
Get task use case.

This module contains the business logic for retrieving a single task.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.infrastructure.db.models import Task
from app.infrastructure.db.repositories import TaskRepository


def get_task(db: Session, task_id: int) -> Task:
    """
    Retrieve a single task by its ID.

    Args:
        db: Database session for data access.
        task_id: ID of the task to retrieve.

    Returns:
        Task: The task instance.

    Raises:
        NotFoundException: If the task doesn't exist.
    """
    task_repo = TaskRepository(db)
    task = task_repo.get_by_id(task_id)

    if not task:
        raise NotFoundException(f"Task with id {task_id} not found")

    return task


def get_task_optional(db: Session, task_id: int) -> Optional[Task]:
    """
    Retrieve a single task by its ID, returning None if not found.

    Args:
        db: Database session for data access.
        task_id: ID of the task to retrieve.

    Returns:
        Optional[Task]: The task instance if found, None otherwise.
    """
    task_repo = TaskRepository(db)
    return task_repo.get_by_id(task_id)
