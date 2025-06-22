"""
Create task use case.

This module contains the business logic for creating a new task.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.infrastructure.db.models import Task, TaskPriority, TaskStatus
from app.infrastructure.db.repositories import TaskListRepository, TaskRepository


def create_task(
    db: Session,
    task_list_id: int,
    title: str,
    description: Optional[str] = None,
    priority: TaskPriority = TaskPriority.medium,
    user_id: Optional[int] = None,
) -> Task:
    """
    Create a new task within a task list.

    Args:
        db: Database session for persistence.
        task_list_id: ID of the task list to add the task to.
        title: Title of the new task.
        description: Optional detailed description of the task.
        priority: Priority level of the task.
        user_id: Optional ID of the user to assign the task to.

    Returns:
        Task: The created task instance.

    Raises:
        NotFoundException: If the task list doesn't exist.
    """
    # Verify that the task list exists
    task_list_repo = TaskListRepository(db)
    task_list = task_list_repo.get_by_id(task_list_id)
    if not task_list:
        raise NotFoundException(f"Task list with id {task_list_id} not found")

    # Create the task
    task = Task(
        title=title,
        description=description,
        task_list_id=task_list_id,
        priority=priority,
        user_id=user_id,
        status=TaskStatus.pending,
    )

    # Use repository to persist
    task_repo = TaskRepository(db)
    return task_repo.create(task)
