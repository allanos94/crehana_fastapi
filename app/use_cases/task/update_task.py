"""
Update task use case.

This module contains the business logic for updating an existing task.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.domain.models.task import Task


def update_task(
    db: Session,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Task | None:
    """
    Update an existing task's title and/or description.

    Args:
        db: Database session for persistence.
        task_id: ID of the task to update.
        title: Optional new title for the task.
        description: Optional new description for the task.

    Returns:
        Task | None: The updated task instance if found, None otherwise.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        db.commit()
        db.refresh(task)
    return task
