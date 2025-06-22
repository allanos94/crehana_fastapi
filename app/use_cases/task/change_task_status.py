"""
Change task status use case.

This module contains the business logic for changing a task's status.
"""

from sqlalchemy.orm import Session

from app.domain.models.task import Task, TaskStatus


def change_task_status(db: Session, task_id: int, status: TaskStatus) -> Task | None:
    """
    Change the status of a task.

    Args:
        db: Database session for persistence.
        task_id: ID of the task to update.
        status: New status to set for the task.

    Returns:
        Task | None: The updated task instance if found, None otherwise.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task
